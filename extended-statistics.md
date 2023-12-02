---
title: Introduction to Extended Statistics
summary: Learn how to use extended statistics to guide the optimizer.
---

# 拡張統計の概要 {#introduction-to-extended-statistics}

TiDB は、次の 2 種類の統計を収集できます。

-   基本統計: ヒストグラムや Count-Min Sketch などの統計。詳細については[統計入門](/statistics.md)を参照してください。
-   拡張統計: テーブルと列によってフィルターされた統計。

> **ヒント：**
>
> このドキュメントを読む前に、まず[統計入門](/statistics.md)を読むことをお勧めします。

`ANALYZE`ステートメントが手動または自動で実行される場合、TiDB はデフォルトで基本統計のみを収集し、拡張統計は収集しません。これは、拡張統計は特定のシナリオでのオプティマイザの推定にのみ使用され、それらの収集には追加のオーバーヘッドが必要になるためです。

拡張統計はデフォルトでは無効になっています。拡張統計を収集するには、まず拡張統計を有効にしてから、個々の拡張統計オブジェクトを登録する必要があります。

登録後、次回`ANALYZE`ステートメントが実行されると、TiDB は基本統計と登録された拡張統計の両方を収集します。

## 制限事項 {#limitations}

拡張統計は、次のシナリオでは収集されません。

-   インデックスのみの統計収集
-   `ANALYZE INCREMENTAL`コマンドを使用した統計収集
-   システム変数`tidb_enable_fast_analyze`の値が`true`に設定されている場合の統計収集

## 共通操作 {#common-operations}

### 拡張統計を有効にする {#enable-extended-statistics}

拡張統計を有効にするには、システム変数`tidb_enable_extended_stats`から`ON`を設定します。

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

この変数のデフォルト値は`OFF`です。このシステム変数の設定は、すべての拡張統計オブジェクトに適用されます。

### 拡張統計の登録 {#register-extended-statistics}

拡張統計の登録は 1 回限りのタスクではないため、拡張統計オブジェクトごとに登録を繰り返す必要があります。

拡張統計を登録するには、SQL ステートメント`ALTER TABLE ADD STATS_EXTENDED`を使用します。構文は次のとおりです。

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

構文では、収集する拡張統計のテーブル名、統計名、統計タイプ、および列名を指定できます。

-   `table_name`拡張統計が収集されるテーブルの名前を指定します。
-   `stats_name`統計オブジェクトの名前を指定します。この名前はテーブルごとに一意である必要があります。
-   `stats_type`統計のタイプを指定します。現在、相関タイプのみがサポートされています。
-   `column_name`列グループを指定します。列グループには複数の列が含まれる場合があります。現在、指定できる列名は 2 つだけです。

<details><summary>使い方</summary>

アクセス パフォーマンスを向上させるために、各 TiDB ノードは拡張統計用にシステム テーブル`mysql.stats_extended`にキャッシュを維持します。拡張統計を登録した後、次回`ANALYZE`ステートメントが実行されると、システム テーブル`mysql.stats_extended`に対応するオブジェクトがある場合、TiDB は拡張統計を収集します。

`mysql.stats_extended`テーブルの各行には`version`列があります。行が更新されると、 `version`の値が増加します。このように、TiDB はテーブルを完全ではなく段階的にメモリにロードします。

TiDB は、キャッシュがテーブル内のデータと同じに保たれるように、定期的に`mysql.stats_extended`をロードします。

> **警告：**
>
> `mysql.stats_extended`システム テーブルを直接操作することは**推奨されません**。そうしないと、異なる TiDB ノードでキャッシュの不整合が発生します。
>
> テーブルを誤って操作した場合は、各 TiDB ノードで次のステートメントを実行できます。次に、現在のキャッシュがクリアされ、 `mysql.stats_extended`テーブルが完全に再ロードされます。
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 拡張統計の削除 {#delete-extended-statistics}

拡張統計オブジェクトを削除するには、次のステートメントを使用します。

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

<details><summary>使い方</summary>

ステートメントを実行すると、TiDB はオブジェクトを直接削除するのではなく、 `mysql.stats_extended`の列`status` ～ `2`に対応するオブジェクトの値をマークします。

他の TiDB ノードはこの変更を読み取り、メモリキャッシュ内のオブジェクトを削除します。バックグラウンドのガベージコレクション、最終的にオブジェクトは削除されます。

> **警告：**
>
> `mysql.stats_extended`システム テーブルを直接操作することは**推奨されません**。そうしないと、異なる TiDB ノードでキャッシュの不整合が発生します。
>
> テーブルを誤って操作した場合は、各 TiDB ノードで次のステートメントを使用できます。次に、現在のキャッシュがクリアされ、 `mysql.stats_extended`テーブルが完全に再ロードされます。
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 拡張統計のエクスポートとインポート {#export-and-import-extended-statistics}

拡張統計をエクスポートまたはインポートする方法は、基本統計をエクスポートまたはインポートする方法と同じです。詳細については[統計の概要 - 統計のインポートとエクスポート](/statistics.md#import-and-export-statistics)を参照してください。

## 相関型拡張統計の使用例 {#usage-examples-for-correlation-type-extended-statistics}

現在、TiDB は相関タイプの拡張統計のみをサポートしています。このタイプは、範囲クエリ内の行数を推定し、インデックス選択を改善するために使用されます。次の例は、相関タイプの拡張統計を使用して範囲クエリの行数を推定する方法を示しています。

### ステップ 1. テーブルを定義する {#step-1-define-the-table}

テーブル`t`次のように定義します。

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

テーブル`t`の`col1`と`col2`両方とも、行の順序で単調増加する制約に従うと仮定します。これは、 `col1`と`col2`の値が順番に厳密に相関しており、相関係数が`1`であることを意味します。

### ステップ 2. 拡張統計を使用せずにクエリ例を実行する {#step-2-execute-an-example-query-without-extended-statistics}

拡張統計を使用せずに次のクエリを実行します。

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

前述のクエリを実行する場合、TiDB オプティマイザーにはテーブル`t`にアクセスするための次のオプションがあります。

-   `col1`のインデックスを使用してテーブル`t`にアクセスし、結果を`col2`でソートして`Top-1`を計算します。
-   `col2`のインデックスを使用して、 `col1 > 1`を満たす最初の行を検索します。このアクセス方法のコストは主に、TiDB が`col2`の順序でテーブルをスキャンするときにフィルターで除外される行の数によって決まります。

拡張統計がないと、TiDB オプティマイザーは`col1`と`col2`が独立していると想定するだけであり、これが**重大な推定誤差につながります**。

### ステップ 3. 拡張統計を有効にする {#step-3-enable-extended-statistics}

`tidb_enable_extended_stats`を`ON`に設定し、 `col1`と`col2`に拡張統計オブジェクトを登録します。

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

登録後に`ANALYZE`を実行すると、TiDB はテーブル`t`の`col`と`col2`の[ピアソン相関係数](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)計算し、オブジェクトを`mysql.stats_extended`テーブルに書き込みます。

### ステップ 4. 拡張統計がどのような違いを生むかを確認する {#step-4-see-how-extended-statistics-make-a-difference}

TiDB が相関に関する拡張統計を取得すると、オプティマイザーはスキャンする行数をより正確に推定できるようになります。

このとき、 [ステージ 2. 拡張統計を使用せずにクエリ例を実行する](#step-2-execute-an-example-query-without-extended-statistics)のクエリでは、 `col1` 、 `col2`順に厳密に対応付けられます。 TiDB が`col2`のインデックスを使用してテーブル`t`にアクセスし、 `col1 > 1`を満たす最初の行を検索すると、TiDB オプティマイザーは行数の推定を次のクエリに変換します。

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

前述のクエリ結果に 1 を加えたものが、行数の最終推定値となります。この方法では、独立した仮定を使用する必要がなくなり、**重大な推定誤差が回避されます**。

相関係数 (この例では`1` ) がシステム変数`tidb_opt_correlation_threshold`の値より小さい場合、オプティマイザーは独立した仮定を使用しますが、推定値もヒューリスティックに増加します。 `tidb_opt_correlation_exp_factor`の値が大きいほど、推定結果は大きくなります。相関係数の絶対値が大きいほど、推定結果は大きくなります。
