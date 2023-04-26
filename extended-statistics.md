---
title: Introduction to Extended Statistics
summary: Learn how to use extended statistics to guide the optimizer.
---

# 拡張統計の概要 {#introduction-to-extended-statistics}

TiDB は、次の 2 種類の統計を収集できます。

-   基本統計: ヒストグラムや Count-Min Sketch などの統計。詳細は[統計入門](/statistics.md)を参照してください。
-   拡張統計: テーブルと列でフィルタリングされた統計。

> **ヒント：**
>
> このドキュメントを読む前に、まず[統計入門](/statistics.md)を読むことをお勧めします。

`ANALYZE`ステートメントが手動または自動で実行されると、TiDB はデフォルトで基本統計のみを収集し、拡張統計は収集しません。これは、拡張統計が特定のシナリオでオプティマイザの推定にのみ使用され、それらを収集するには追加のオーバーヘッドが必要になるためです。

拡張統計はデフォルトで無効になっています。拡張統計を収集するには、まず拡張統計を有効にしてから、個々の拡張統計オブジェクトを登録する必要があります。

登録後、次に`ANALYZE`ステートメントが実行されると、TiDB は基本統計と登録された拡張統計の両方を収集します。

## 制限事項 {#limitations}

次のシナリオでは、拡張統計は収集されません。

-   インデックスのみの統計収集
-   `ANALYZE INCREMENTAL`コマンドによる統計収集
-   システム変数`tidb_enable_fast_analyze`の値を`true`に設定した場合の統計収集

## 共通操作 {#common-operations}

### 拡張統計を有効にする {#enable-extended-statistics}

拡張統計を有効にするには、システム変数`tidb_enable_extended_stats` `ON`に設定します。

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

この変数のデフォルト値は`OFF`です。このシステム変数の設定は、すべての拡張統計オブジェクトに適用されます。

### 拡張統計の登録 {#register-extended-statistics}

拡張統計の登録は 1 回限りのタスクではなく、拡張統計オブジェクトごとに登録を繰り返す必要があります。

拡張統計を登録するには、SQL 文`ALTER TABLE ADD STATS_EXTENDED`を使用します。構文は次のとおりです。

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

構文では、収集する拡張統計の表名、統計名、統計タイプ、および列名を指定できます。

-   `table_name`拡張統計が収集されるテーブルの名前を指定します。
-   `stats_name`統計オブジェクトの名前を指定します。これは、テーブルごとに一意である必要があります。
-   `stats_type`統計のタイプを指定します。現在、相関タイプのみがサポートされています。
-   `column_name`列グループを指定します。これには複数の列が含まれる場合があります。現在、指定できる列名は 2 つだけです。

<details><summary>使い方</summary>

アクセス パフォーマンスを向上させるために、各 TiDB ノードは拡張統計用にシステム テーブル`mysql.stats_extended`にキャッシュを保持します。拡張統計を登録した後、次に`ANALYZE`ステートメントが実行されたときに、システム テーブル`mysql.stats_extended`に対応するオブジェクトがある場合、TiDB は拡張統計を収集します。

`mysql.stats_extended`テーブルの各行には`version`列があります。行が更新されると、値`version`が増加します。このようにして、TiDB はテーブルを完全にではなく段階的にメモリにロードします。

TiDB は定期的に`mysql.stats_extended`をロードして、キャッシュがテーブル内のデータと同じに保たれるようにします。

> **警告：**
>
> `mysql.stats_extended`システム テーブルを直接操作することは**お勧めしません**。そうしないと、異なる TiDB ノードで一貫性のないキャッシュが発生します。
>
> テーブルを誤って操作してしまった場合は、各 TiDB ノードで次のステートメントを実行できます。次に、現在のキャッシュがクリアされ、 `mysql.stats_extended`テーブルが完全にリロードされます。
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

ステートメントを実行した後、TiDB はオブジェクトを直接削除するのではなく、対応するオブジェクトの値を`mysql.stats_extended`の列`status`から`2`にマークします。

他の TiDB ノードはこの変更を読み取り、メモリキャッシュ内のオブジェクトを削除します。バックグラウンドガベージコレクションは、最終的にオブジェクトを削除します。

> **警告：**
>
> `mysql.stats_extended`システム テーブルを直接操作することは**お勧めしません**。そうしないと、異なる TiDB ノードで一貫性のないキャッシュが発生します。
>
> テーブルを誤って操作した場合は、各 TiDB ノードで次のステートメントを使用できます。次に、現在のキャッシュがクリアされ、 `mysql.stats_extended`テーブルが完全にリロードされます。
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 拡張統計のエクスポートとインポート {#export-and-import-extended-statistics}

拡張統計をエクスポートまたはインポートする方法は、基本統計をエクスポートまたはインポートする方法と同じです。詳細は[統計の概要 - 統計のインポートとエクスポート](/statistics.md#import-and-export-statistics)を参照してください。

## 相関型拡張統計の使用例 {#usage-examples-for-correlation-type-extended-statistics}

現在、TiDB は相関タイプの拡張統計のみをサポートしています。このタイプは、範囲クエリの行数を見積もり、インデックスの選択を改善するために使用されます。次の例は、相関タイプの拡張統計を使用して、範囲クエリの行数を見積もる方法を示しています。

### ステップ 1. テーブルを定義する {#step-1-define-the-table}

テーブル`t`次のように定義します。

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

表`t`の`col1`と`col2`両方が、行順の単調増加制約に従うとします。これは、値`col1`と`col2`が順番に厳密に相関しており、相関係数が`1`であることを意味します。

### 手順 2. 拡張統計なしでサンプル クエリを実行する {#step-2-execute-an-example-query-without-extended-statistics}

拡張統計を使用せずに次のクエリを実行します。

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

上記のクエリを実行するために、TiDB オプティマイザーには、テーブル`t`にアクセスするための次のオプションがあります。

-   `col1`のインデックスを使用してテーブル`t`にアクセスし、結果を`col2`で並べ替えて`Top-1`を計算します。
-   `col2`のインデックスを使用して、 `col1 > 1`を満たす最初の行を見つけます。このアクセス方法のコストは主に、TiDB が`col2`の順序でテーブルをスキャンするときに除外される行の数によって異なります。

拡張統計がない場合、TiDB オプティマイザーは`col1`と`col2`が独立していると仮定するだけであり、これが**重大な推定エラーにつながります**。

### ステップ 3. 拡張統計を有効にする {#step-3-enable-extended-statistics}

`tidb_enable_extended_stats`から`ON`を設定し、 `col1`と`col2`の拡張統計オブジェクトを登録します。

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

登録後に`ANALYZE`を実行すると、TiDB は表`t`の`col`と`col2`の[ピアソン相関係数](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)計算し、オブジェクトを`mysql.stats_extended`の表に書き込みます。

### ステップ 4. 拡張統計がどのように違いを生むかを確認する {#step-4-see-how-extended-statistics-make-a-difference}

TiDB が相関のための拡張統計を取得した後、オプティマイザはスキャンする行数をより正確に見積もることができます。

このとき、 [ステージ 2. 拡張統計なしでサンプル クエリを実行する](#step-2-execute-an-example-query-without-extended-statistics)のクエリに対して、 `col1`と`col2`順序が厳密に関連付けられます。 TiDB が`col2`のインデックスを使用して`col1 > 1`を満たす最初の行に一致するようにテーブル`t`にアクセスする場合、TiDB オプティマイザーは行数の見積もりを次のクエリに同等に変換します。

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

前のクエリ結果に 1 を加えた値が、行数の最終的な見積もりになります。この方法では、独立した仮定を使用する必要がなく、**重大な推定エラーが回避されます**。

相関係数 (この例では`1` ) がシステム変数`tidb_opt_correlation_threshold`の値より小さい場合、オプティマイザーは独立した仮定を使用しますが、ヒューリスティックに推定値を増やします。 `tidb_opt_correlation_exp_factor`の値が大きいほど、推定結果が大きくなります。相関係数の絶対値が大きいほど、推定結果が大きくなります。
