---
title: Introduction to Extended Statistics
summary: 拡張統計を使用してオプティマイザーをガイドする方法を学習します。
---

# 拡張統計入門 {#introduction-to-extended-statistics}

TiDB は次の 2 種類の統計を収集できます。

-   基本統計: ヒストグラムやCount-Min Sketchなどの統計。詳細については[統計入門](/statistics.md)を参照してください。
-   拡張統計: テーブルと列でフィルタリングされた統計。

> **ヒント：**
>
> この文書を読む前に、まず[統計入門](/statistics.md)読むことをお勧めします。

`ANALYZE`文が手動または自動で実行されると、TiDB はデフォルトで基本統計のみを収集し、拡張統計は収集しません。これは、拡張統計は特定のシナリオでのオプティマイザーの推定にのみ使用され、収集には追加のオーバーヘッドが必要になるためです。

拡張統計はデフォルトでは無効になっています。拡張統計を収集するには、まず拡張統計を有効にし、次に個々の拡張統計オブジェクトを登録する必要があります。

登録後、次に`ANALYZE`ステートメントが実行されると、TiDB は基本統計と登録された拡張統計の両方を収集します。

## 制限事項 {#limitations}

次のシナリオでは拡張統計は収集されません。

-   インデックスのみの統計収集
-   `ANALYZE INCREMENTAL`コマンドを使用した統計収集
-   システム変数`tidb_enable_fast_analyze`の値が`true`に設定されている場合の統計収集

## 一般的な操作 {#common-operations}

### 拡張統計を有効にする {#enable-extended-statistics}

拡張統計を有効にするには、システム変数`tidb_enable_extended_stats`を`ON`に設定します。

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

この変数のデフォルト値は`OFF`です。このシステム変数の設定は、すべての拡張統計オブジェクトに適用されます。

### 拡張統計を登録する {#register-extended-statistics}

拡張統計の登録は 1 回限りのタスクではなく、拡張統計オブジェクトごとに登録を繰り返す必要があります。

拡張統計を登録するには、SQL 文`ALTER TABLE ADD STATS_EXTENDED`を使用します。構文は次のとおりです。

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

構文では、収集する拡張統計のテーブル名、統計名、統計タイプ、列名を指定できます。

-   `table_name` 、拡張統計が収集されるテーブルの名前を指定します。
-   `stats_name`統計オブジェクトの名前を指定します。この名前はテーブルごとに一意である必要があります。
-   `stats_type`統計のタイプを指定します。現在は相関タイプのみがサポートされています。
-   `column_name` 、複数の列を持つ可能性がある列グループを指定します。現在、指定できる列名は 2 つだけです。

<details><summary>使い方</summary>

アクセス パフォーマンスを向上させるために、各 TiDB ノードはシステム テーブル`mysql.stats_extended`に拡張統計のキャッシュを保持します。拡張統計を登録すると、次に`ANALYZE`ステートメントが実行されたときに、システム テーブル`mysql.stats_extended`に対応するオブジェクトがある場合、TiDB は拡張統計を収集します。

`mysql.stats_extended`テーブルの各行には`version`列があります。行が更新されると、 `version`の値が増加します。このようにして、TiDB はテーブルを完全にではなく、増分的にメモリにロードします。

TiDB は、キャッシュがテーブル内のデータと同じ状態に保たれるように、定期的に`mysql.stats_extended`ロードします。

> **警告：**
>
> `mysql.stats_extended`システム テーブルを直接操作することは**推奨されません**。そうしないと、異なる TiDB ノードでキャッシュの不整合が発生します。
>
> テーブルを誤って操作した場合は、各 TiDB ノードで次のステートメントを実行できます。これにより、現在のキャッシュがクリアされ、 `mysql.stats_extended`テーブルが完全に再ロードされます。
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 拡張統計を削除する {#delete-extended-statistics}

拡張統計オブジェクトを削除するには、次のステートメントを使用します。

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

<details><summary>使い方</summary>

ステートメントを実行すると、TiDB はオブジェクトを直接削除するのではなく、 `mysql.stats_extended`の列`status` ～ `2`の対応するオブジェクトの値をマークします。

他の TiDB ノードはこの変更を読み取り、メモリキャッシュ内のオブジェクトを削除します。バックグラウンドガベージコレクション、最終的にオブジェクトが削除されます。

> **警告：**
>
> `mysql.stats_extended`システム テーブルを直接操作することは**推奨されません**。そうしないと、異なる TiDB ノードでキャッシュの不整合が発生します。
>
> テーブルを誤って操作した場合は、各 TiDB ノードで次のステートメントを使用できます。これにより、現在のキャッシュがクリアされ、 `mysql.stats_extended`テーブルが完全に再ロードされます。
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 拡張統計のエクスポートとインポート {#export-and-import-extended-statistics}

拡張統計のエクスポートまたはインポートの方法は、基本統計のエクスポートまたはインポートと同じです。詳細については[統計入門 - 輸入と輸出の統計](/statistics.md#import-and-export-statistics)を参照してください。

## 相関型拡張統計の使用例 {#usage-examples-for-correlation-type-extended-statistics}

現在、TiDB は相関タイプの拡張統計のみをサポートしています。このタイプは、範囲クエリの行数を推定し、インデックス選択を改善するために使用されます。次の例は、相関タイプの拡張統計を使用して範囲クエリの行数を推定する方法を示しています。

### ステップ1. テーブルを定義する {#step-1-define-the-table}

表`t`を次のように定義します。

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

表`t`の`col1`と`col2`両方とも行の順序で単調に増加する制約に従っていると仮定します。これは、 `col1`と`col2`の値が順序で厳密に相関しており、相関係数が`1`であることを意味します。

### ステップ2. 拡張統計なしでサンプルクエリを実行する {#step-2-execute-an-example-query-without-extended-statistics}

拡張統計を使用せずに次のクエリを実行します。

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

上記のクエリを実行する場合、TiDB オプティマイザーにはテーブル`t`にアクセスするための次のオプションがあります。

-   `col1`のインデックスを使用してテーブル`t`にアクセスし、結果を`col2`でソートして`Top-1`を計算します。
-   `col2`のインデックスを使用して、 `col1 > 1`を満たす最初の行を見つけます。このアクセス方法のコストは、主に TiDB が`col2`の順序でテーブルをスキャンするときにフィルターされる行数によって決まります。

拡張統計がなければ、TiDB オプティマイザーは`col1`と`col2`が独立していると想定するだけなので、**大きな推定誤差が生じます**。

### ステップ3. 拡張統計を有効にする {#step-3-enable-extended-statistics}

`tidb_enable_extended_stats` `ON`に設定し、 `col1`と`col2`の拡張統計オブジェクトを登録します。

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

登録後に`ANALYZE`実行すると、TiDBはテーブル`t`の`col`と`col2` [ピアソン相関係数](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)を計算し、オブジェクトをテーブル`mysql.stats_extended`に書き込みます。

### ステップ4. 拡張統計がどのように違いを生むかを確認する {#step-4-see-how-extended-statistics-make-a-difference}

TiDB が相関関係の拡張統計を取得すると、オプティマイザーはスキャンする行数をより正確に見積もることができます。

この時点で、 [ステージ2. 拡張統計なしでサンプルクエリを実行する](#step-2-execute-an-example-query-without-extended-statistics)のクエリでは、 `col1`と`col2`順番に厳密に相関しています。TiDB が`col2`のインデックスを使用してテーブル`t`にアクセスし、 `col1 > 1`満たす最初の行を検索すると、TiDB オプティマイザは行数の推定を次のクエリに等価に変換します。

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

前のクエリ結果に 1 を加えたものが、行数の最終的な推定値になります。この方法では、独立した仮定を使用する必要がなくなり、**大きな推定誤差が回避されます**。

相関係数 (この例では`1` ) がシステム変数`tidb_opt_correlation_threshold`の値より小さい場合、オプティマイザは独立した仮定を使用しますが、推定値も経験的に増加します。 `tidb_opt_correlation_exp_factor`の値が大きいほど、推定結果は大きくなります。相関係数の絶対値が大きいほど、推定結果は大きくなります。
