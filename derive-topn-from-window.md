---
title: Derive TopN or Limit from Window Functions
summary: ウィンドウ関数から TopN または Limit を導出する最適化ルールと、このルールを有効にする方法を紹介します。
---

# ウィンドウ関数からTopNまたはLimitを導出する {#derive-topn-or-limit-from-window-functions}

[ウィンドウ関数](/functions-and-operators/window-functions.md)は一般的なSQL関数です。行番号付けに`ROW_NUMBER()`や`RANK()`などのウィンドウ関数を使用する場合、ウィンドウ関数を評価した後に結果をフィルタリングするのが一般的です。例:

```sql
SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t) dt WHERE rownumber <= 3
```

一般的な SQL 実行プロセスでは、TiDB は最初にテーブル`t`内のすべてのデータをソートし、次に各行の`ROW_NUMBER()`結果を計算し、最後に`rownumber <= 3`でフィルタリングします。

バージョン7.0.0以降、TiDBはウィンドウ関数からTopN演算子またはLimit演算子を導出する機能をサポートしています。この最適化ルールにより、TiDBは元のSQLを以下のように同等の形式に書き換えることができます。

```sql
WITH t_topN AS (SELECT a FROM t1 ORDER BY a LIMIT 3) SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY a) AS rownumber FROM t_topN) dt WHERE rownumber <= 3
```

書き換え後、TiDBはウィンドウ関数とそれに続くフィルタ条件からTopN演算子を導出できます。元のSQL（ `ORDER BY` ）のSort演算子と比較して、TopN演算子は実行効率がはるかに高くなります。さらに、TiKVとTiFlashはどちらもTopN演算子のプッシュダウンをサポートしており、書き換えられたSQLのパフォーマンスをさらに向上させます。

ウィンドウ関数からTopNまたはLimitを導出することはデフォルトで無効になっています。この機能を有効にするには、セッション変数[tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700)を`ON`に設定します。

この機能を有効にした後、次のいずれかの操作を実行して無効にすることができます。

-   セッション変数[tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700)を`OFF`に設定します。
-   [最適化ルールと式プッシュダウンのブロックリスト](/blocklist-control-plan.md)に記載されている手順に従います。

## 制限事項 {#limitations}

-   SQL 書き換えでは`ROW_NUMBER()`ウィンドウ関数のみがサポートされます。
-   TiDB は、 `ROW_NUMBER()`結果をフィルタリングし、フィルタ条件が`<`または`<=`場合にのみ SQL を書き換えることができます。

## 使用例 {#usage-examples}

次の例は、最適化ルールの使用方法を示しています。

### PARTITION BYを使用しないウィンドウ関数 {#window-functions-without-partition-by}

#### 例1: ORDER BYのないウィンドウ関数 {#example-1-window-functions-without-order-by}

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER () AS rownumber FROM t) dt WHERE rownumber <= 3;
```

結果は次のとおりです。

    +----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
    | id                               | estRows | task      | access object | operator info                                                         |
    +----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+
    | Projection_9                     | 2.40    | root      |               | Column#5                                                              |
    | └─Selection_10                   | 2.40    | root      |               | le(Column#5, 3)                                                       |
    |   └─Window_11                    | 3.00    | root      |               | row_number()->Column#5 over(rows between current row and current row) |
    |     └─Limit_15                   | 3.00    | root      |               | offset:0, count:3                                                     |
    |       └─TableReader_26           | 3.00    | root      |               | data:Limit_25                                                         |
    |         └─Limit_25               | 3.00    | cop[tikv] |               | offset:0, count:3                                                     |
    |           └─TableFullScan_24     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                        |
    +----------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------+

このクエリでは、オプティマイザーはウィンドウ関数から Limit 演算子を導出し、それを TiKV にプッシュダウンします。

#### 例2: ORDER BYを使用したウィンドウ関数 {#example-2-window-functions-with-order-by}

```sql
CREATE TABLE t(id int, value int);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY value) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

結果は次のとおりです。

    +----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
    | id                               | estRows  | task      | access object | operator info                                                                               |
    +----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
    | Projection_10                    | 2.40     | root      |               | Column#5                                                                                    |
    | └─Selection_11                   | 2.40     | root      |               | le(Column#5, 3)                                                                             |
    |   └─Window_12                    | 3.00     | root      |               | row_number()->Column#5 over(order by test.t.value rows between current row and current row) |
    |     └─TopN_13                    | 3.00     | root      |               | test.t.value, offset:0, count:3                                                             |
    |       └─TableReader_25           | 3.00     | root      |               | data:TopN_24                                                                                |
    |         └─TopN_24                | 3.00     | cop[tikv] |               | test.t.value, offset:0, count:3                                                             |
    |           └─TableFullScan_23     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
    +----------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+

このクエリでは、オプティマイザーはウィンドウ関数から TopN 演算子を導出し、それを TiKV にプッシュダウンします。

### PARTITION BYを使用したウィンドウ関数 {#window-functions-with-partition-by}

> **注記：**
>
> `PARTITION BY`を含むウィンドウ関数の場合、パーティション列が主キーのプレフィックスであり、主キーがクラスター化インデックスである場合にのみ最適化ルールが有効になります。

#### 例3: ORDER BYのないウィンドウ関数 {#example-3-window-functions-without-order-by}

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

結果は次のとおりです。

    +------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
    | id                                 | estRows | task      | access object | operator info                                                                                 |
    +------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+
    | Projection_10                      | 2.40    | root      |               | Column#6                                                                                      |
    | └─Selection_11                     | 2.40    | root      |               | le(Column#6, 3)                                                                               |
    |   └─Shuffle_26                     | 3.00    | root      |               | execution info: concurrency:2, data sources:[TableReader_24]                                  |
    |     └─Window_12                    | 3.00    | root      |               | row_number()->Column#6 over(partition by test.t.id1 rows between current row and current row) |
    |       └─Sort_25                    | 3.00    | root      |               | test.t.id1                                                                                    |
    |         └─TableReader_24           | 3.00    | root      |               | data:Limit_23                                                                                 |
    |           └─Limit_23               | 3.00    | cop[tikv] |               | partition by test.t.id1, offset:0, count:3                                                    |
    |             └─TableFullScan_22     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                |
    +------------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------+

このクエリでは、オプティマイザはウィンドウ関数からLimit演算子を導出し、TiKVにプッシュダウンします。このLimitは実際にはパーティションLimitであり、同じ`id1`値を持つデータの各グループに適用されることに注意してください。

#### 例4: ORDER BYを使用したウィンドウ関数 {#example-4-window-functions-with-order-by}

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1 ORDER BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

結果は次のとおりです。

    +------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
    | id                                 | estRows  | task      | access object | operator info                                                                                                        |
    +------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+
    | Projection_10                      | 2.40     | root      |               | Column#6                                                                                                             |
    | └─Selection_11                     | 2.40     | root      |               | le(Column#6, 3)                                                                                                      |
    |   └─Shuffle_23                     | 3.00     | root      |               | execution info: concurrency:3, data sources:[TableReader_21]                                                         |
    |     └─Window_12                    | 3.00     | root      |               | row_number()->Column#6 over(partition by test.t.id1 order by test.t.value1 rows between current row and current row) |
    |       └─Sort_22                    | 3.00     | root      |               | test.t.id1, test.t.value1                                                                                            |
    |         └─TableReader_21           | 3.00     | root      |               | data:TopN_19                                                                                                         |
    |           └─TopN_19                | 3.00     | cop[tikv] |               | partition by test.t.id1 order by test.t.value1, offset:0, count:3                                                    |
    |             └─TableFullScan_18     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                                       |
    +------------------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------+

このクエリでは、オプティマイザはウィンドウ関数からTopN演算子を導出し、TiKVにプッシュダウンします。このTopNは実際にはパーティションTopNであり、同じ`id1`値を持つデータの各グループに適用されることに注意してください。

#### 例5: PARTITION BY列は主キーの接頭辞ではありません {#example-5-partition-by-column-is-not-a-prefix-of-the-primary-key}

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) clustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY value1) AS rownumber FROM t) dt WHERE rownumber <= 3;
```

結果は次のとおりです。

    +----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
    | id                               | estRows  | task      | access object | operator info                                                                                    |
    +----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+
    | Projection_9                     | 8000.00  | root      |               | Column#6                                                                                         |
    | └─Selection_10                   | 8000.00  | root      |               | le(Column#6, 3)                                                                                  |
    |   └─Shuffle_15                   | 10000.00 | root      |               | execution info: concurrency:5, data sources:[TableReader_13]                                     |
    |     └─Window_11                  | 10000.00 | root      |               | row_number()->Column#6 over(partition by test.t.value1 rows between current row and current row) |
    |       └─Sort_14                  | 10000.00 | root      |               | test.t.value1                                                                                    |
    |         └─TableReader_13         | 10000.00 | root      |               | data:TableFullScan_12                                                                            |
    |           └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                   |
    +----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------+

このクエリでは、 `PARTITION BY`列目が主キーのプレフィックスではないため、SQL は書き換えられません。

#### 例6: PARTITION BY列は主キーのプレフィックスですが、クラスター化インデックスではありません {#example-6-partition-by-column-is-a-prefix-of-the-primary-key-but-not-a-clustered-index}

```sql
CREATE TABLE t(id1 int, id2 int, value1 int, value2 int, primary key(id1,id2) nonclustered);
SET tidb_opt_derive_topn=on;
EXPLAIN SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY id1) AS rownumber FROM t use index()) dt WHERE rownumber <= 3;
```

結果は次のとおりです。

    +----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
    | id                               | estRows  | task      | access object | operator info                                                                                 |
    +----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+
    | Projection_9                     | 8000.00  | root      |               | Column#7                                                                                      |
    | └─Selection_10                   | 8000.00  | root      |               | le(Column#7, 3)                                                                               |
    |   └─Shuffle_15                   | 10000.00 | root      |               | execution info: concurrency:5, data sources:[TableReader_13]                                  |
    |     └─Window_11                  | 10000.00 | root      |               | row_number()->Column#7 over(partition by test.t.id1 rows between current row and current row) |
    |       └─Sort_14                  | 10000.00 | root      |               | test.t.id1                                                                                    |
    |         └─TableReader_13         | 10000.00 | root      |               | data:TableFullScan_12                                                                         |
    |           └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                |
    +----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------------+

このクエリでは、 `PARTITION BY`列目は主キーのプレフィックスですが、主キーがクラスター化インデックスではないため、SQL は書き換えられません。
