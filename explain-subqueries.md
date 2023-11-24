---
title: Explain Statements That Use Subqueries
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# サブクエリを使用する Explain ステートメント {#explain-statements-that-use-subqueries}

TiDB はサブクエリのパフォーマンスを向上させるために[いくつかの最適化](/subquery-optimization.md)を実行します。このドキュメントでは、一般的なサブクエリに対するこれらの最適化のいくつかと、 `EXPLAIN`の出力を解釈する方法について説明します。

このドキュメントの例は、次のサンプル データに基づいています。

```sql
CREATE TABLE t1 (id BIGINT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB, int_col INT NOT NULL DEFAULT 0);
CREATE TABLE t2 (id BIGINT NOT NULL PRIMARY KEY auto_increment, t1_id BIGINT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
CREATE TABLE t3 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 t1_id INT NOT NULL,
 UNIQUE (t1_id)
);

INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
UPDATE t1 SET int_col = 1 WHERE pad1 = (SELECT pad1 FROM t1 ORDER BY RAND() LIMIT 1);
INSERT INTO t3 SELECT NULL, id FROM t1 WHERE id < 1000;

SELECT SLEEP(1);
ANALYZE TABLE t1, t2, t3;
```

## 内部結合 (非一意のサブクエリ) {#inner-join-non-unique-subquery}

次の例では、 `IN`サブクエリはテーブル`t2`から ID のリストを検索します。セマンティックな正確性のために、TiDB は列`t1_id`が一意であることを保証する必要があります。 `EXPLAIN`を使用すると、重複を削除して`INNER JOIN`操作を実行するために使用される実行計画を確認できます。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2);
```

```sql
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                             | estRows  | task      | access object                | operator info                                                                                                             |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_15                   | 21.11    | root      |                              | inner join, inner:TableReader_12, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) |
| ├─StreamAgg_44(Build)          | 21.11    | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id                                                      |
| │ └─IndexReader_45             | 21.11    | root      |                              | index:StreamAgg_34                                                                                                        |
| │   └─StreamAgg_34             | 21.11    | cop[tikv] |                              | group by:test.t2.t1_id,                                                                                                   |
| │     └─IndexFullScan_26       | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                                           |
| └─TableReader_12(Probe)        | 21.11    | root      |                              | data:TableRangeScan_11                                                                                                    |
|   └─TableRangeScan_11          | 21.11    | cop[tikv] | table:t1                     | range: decided by [test.t2.t1_id], keep order:false                                                                       |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

上記のクエリ結果から、TiDB がインデックス結合操作`IndexJoin_15`使用してサブクエリを結合および変換していることがわかります。実行計画では、実行プロセスは次のようになります。

1.  TiKV 側のインデックス スキャン オペレータ`└─IndexFullScan_26` `t2.t1_id`列の値を読み取ります。
2.  `└─StreamAgg_34`オペレーターの一部のタスクは、TiKV の`t1_id`の値を重複排除します。
3.  `├─StreamAgg_44(Build)`オペレーターの一部のタスクは、TiDB の`t1_id`の値を重複排除します。重複排除は、集約関数`firstrow(test.t2.t1_id)`によって実行される。
4.  演算結果は`t1`テーブルの主キーと結合されます。結合条件は`eq(test.t1.id, test.t2.t1_id)`です。

## 内部結合 (一意のサブクエリ) {#inner-join-unique-subquery}

前の例では、テーブル`t1`に結合する前に`t1_id`の値が一意であることを確認するために集計が必要です。ただし、次の例では、 `UNIQUE`制約により、 `t3.t1_id`すでに一意であることが保証されています。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object                | operator info                                                                                                             |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_18                | 999.00  | root      |                              | inner join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─IndexReader_41(Build)     | 999.00  | root      |                              | index:IndexFullScan_40                                                                                                    |
| │ └─IndexFullScan_40        | 999.00  | cop[tikv] | table:t3, index:t1_id(t1_id) | keep order:false                                                                                                          |
| └─TableReader_15(Probe)     | 999.00  | root      |                              | data:TableRangeScan_14                                                                                                    |
|   └─TableRangeScan_14       | 999.00  | cop[tikv] | table:t1                     | range: decided by [test.t3.t1_id], keep order:false                                                                       |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

意味的には、 `t3.t1_id`は​​一意であることが保証されているため、 `INNER JOIN`として直接実行できます。

## セミジョイン（相関サブクエリ） {#semi-join-correlated-subquery}

前の 2 つの例では、サブクエリ内のデータが一意になる ( `StreamAgg`によって) か一意であることが保証された後、TiDB は`INNER JOIN`操作を実行できます。どちらの結合もインデックス結合を使用して実行されます。

この例では、TiDB は別の実行プランを選択します。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE t1_id != t1.int_col);
```

```sql
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object                | operator info                                                                                          |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| MergeJoin_9                 | 45446.40 | root      |                              | semi join, left key:test.t1.id, right key:test.t2.t1_id, other cond:ne(test.t2.t1_id, test.t1.int_col) |
| ├─IndexReader_24(Build)     | 90000.00 | root      |                              | index:IndexFullScan_23                                                                                 |
| │ └─IndexFullScan_23        | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                        |
| └─TableReader_22(Probe)     | 56808.00 | root      |                              | data:Selection_21                                                                                      |
|   └─Selection_21            | 56808.00 | cop[tikv] |                              | ne(test.t1.id, test.t1.int_col)                                                                        |
|     └─TableFullScan_20      | 71010.00 | cop[tikv] | table:t1                     | keep order:true                                                                                        |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
```

上記の結果から、TiDB は`Semi Join`アルゴリズムを使用していることがわかります。セミ結合は内部結合とは異なります。セミ結合では右側のキー ( `t2.t1_id` ) の最初の値のみが許可されます。これは、重複が結合演算子タスクの一部として削除されることを意味します。結合アルゴリズムも Merge Join であり、オペレーターがソートされた順序で左側と右側の両方からデータを読み取るため、効率的なジッパー マージに似ています。

サブクエリはサブクエリの外部に存在する列 ( `t1.int_col` ) を参照しているため、元のステートメントは*相関サブクエリと*みなされます。ただし、 `EXPLAIN`の出力には、 [サブクエリ非相関最適化](/correlated-subquery-optimization.md)適用された後の実行計画が表示されます。条件`t1_id != t1.int_col`は`t1.id != t1.int_col`に書き換えられます。 TiDB はテーブル`t1`からデータを読み込むときに`└─Selection_21`でこれを実行できるため、この非相関化と再書き込みにより実行が大幅に効率化されます。

## アンチセミ結合 ( <code>NOT IN</code>サブクエリ) {#anti-semi-join-code-not-in-code-subquery}

次の例では、サブクエリに`t3.t1_id`含まれていない*限り、*クエリは意味的にテーブル`t3`のすべての行を返します。

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                                                                 |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                | 799.20  | root      |               | anti semi join, inner:TableReader_12, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_28(Build)     | 999.00  | root      |               | data:TableFullScan_27                                                                                                         |
| │ └─TableFullScan_27        | 999.00  | cop[tikv] | table:t3      | keep order:false                                                                                                              |
| └─TableReader_12(Probe)     | 999.00  | root      |               | data:Selection_11                                                                                                             |
|   └─Selection_11            | 999.00  | cop[tikv] |               | lt(test.t1.int_col, 100)                                                                                                      |
|     └─TableRangeScan_10     | 999.00  | cop[tikv] | table:t1      | range: decided by [test.t3.t1_id], keep order:false                                                                           |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
```

このクエリは、テーブル`t3`の読み取りから開始し、次に`PRIMARY KEY`に基づいてテーブル`t1`を調査します。結合タイプは*アンチセミ結合*です。この例は値 ( `NOT IN` ) が存在しない場合のものであるため、アンチ、および結合が拒否される前に最初の行のみが一致する必要があるため、半結合です。

## Null 認識セミ結合 ( <code>IN</code>および<code>= ANY</code>サブクエリ) {#null-aware-semi-join-code-in-code-and-code-any-code-subqueries}

`IN`または`= ANY`集合演算子の値は 3 値 ( `true` 、 `false` 、および`NULL` ) です。 2 つの演算子のいずれかから変換された結合タイプの場合、TiDB は結合キーの両側の`NULL`を認識し、それを特別な方法で処理する必要があります。

`IN`つと`= ANY`演算子を含むサブクエリは、それぞれセミジョインと左外部セミジョインに変換されます。前述の[セミジョイン](#semi-join-correlated-subquery)の例では、結合キーの両側の列`test.t1.id`と`test.t2.t1_id` `not NULL`であるため、半結合を null 対応とみなす必要はありません ( `NULL`は特別に処理されません)。 TiDB は、特別な最適化を行わずに、デカルト積とフィルターに基づいてヌル認識セミ結合を処理します。以下は例です。

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                             |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| HashJoin_8                  | 1.00    | root      |               | CARTESIAN left outer semi join, other cond:eq(test.t.a, test.s.a), eq(test.t.b, test.s.b) |
| ├─TableReader_12(Build)     | 1.00    | root      |               | data:TableFullScan_11                                                                     |
| │ └─TableFullScan_11        | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                            |
| └─TableReader_10(Probe)     | 1.00    | root      |               | data:TableFullScan_9                                                                      |
|   └─TableFullScan_9         | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                            |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object | operator info                                                                                       |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| HashJoin_11                  | 1.00    | root      |               | inner join, equal:[eq(test.t.a, test.s.a) eq(test.t.b, test.s.b)]                                   |
| ├─TableReader_14(Build)      | 1.00    | root      |               | data:Selection_13                                                                                   |
| │ └─Selection_13             | 1.00    | cop[tikv] |               | not(isnull(test.t.a)), not(isnull(test.t.b))                                                        |
| │   └─TableFullScan_12       | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                      |
| └─HashAgg_17(Probe)          | 1.00    | root      |               | group by:test.s.a, test.s.b, funcs:firstrow(test.s.a)->test.s.a, funcs:firstrow(test.s.b)->test.s.b |
|   └─TableReader_24           | 1.00    | root      |               | data:Selection_23                                                                                   |
|     └─Selection_23           | 1.00    | cop[tikv] |               | not(isnull(test.s.a)), not(isnull(test.s.b))                                                        |
|       └─TableFullScan_22     | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                                      |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
8 rows in set (0.01 sec)
```

最初のクエリ ステートメント`EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、サブクエリ`IN`によって変換された左外部セミジョインは NULL 対応です。具体的には、最初にデカルト積を計算し、次に`IN`または`= ANY`で接続された列を通常の等式クエリとして他の条件に入れてフィルタリングします。

2 番目のクエリ ステートメント`EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、サブクエリ`IN`は NULL 対応のセミ結合に変換されているはずです。しかし、TiDB はセミ結合を内部結合と集計に変換することで最適化します。これは、非スカラー出力の`IN`サブクエリでは`NULL`と`false`が同等であるためです。プッシュダウン フィルター内の`NULL`行は、 `WHERE`句の否定的なセマンティクスになります。したがって、これらの行は事前に無視できます。

> **注記：**
>
> `Exists`演算子もセミ結合に変換されますが、null は認識されません。

## Null 対応アンチセミ結合 ( <code>NOT IN</code>および<code>!= ALL</code>サブクエリ) {#null-aware-anti-semi-join-code-not-in-code-and-code-all-code-subqueries}

`NOT IN`または`!= ALL`集合演算子の値は 3 値 ( `true` 、 `false` 、および`NULL` ) です。 2 つの演算子のいずれかから変換された結合タイプの場合、TiDB は結合キーの両側の`NULL`を認識し、それを特別な方法で処理する必要があります。

`NOT IN`つと`! = ALL`の演算子を含むサブクエリは、それぞれアンチセミ結合とアンチ左外部セミ結合に変換されます。前述の例[アンチセミ結合](#anti-semi-join-not-in-subquery)では、結合キーの両側の列`test.t3.t1_id`と列`test.t1.id` `not NULL`であるため、アンチセミ結合を null 対応とみなす必要はありません ( `NULL`は特別に処理されません)。

TiDB v6.3.0 は、次のように null 対応アンチ結合 (NAAJ) を最適化します。

-   Null 対応等価条件 (NA-EQ) を使用してハッシュ結合を構築する

    集合演算子は等価条件を導入します。これには、条件の両側の演算子の値`NULL`に対して特別なプロセスが必要です。 Null 認識を必要とする等価条件は NA-EQ と呼ばれます。以前のバージョンとは異なり、TiDB v6.3.0 は以前のように NA-EQ を処理しなくなり、結合後に NA-EQ を他の条件に置き、デカルト積の照合後に結果セットの正当性を判断します。

    TiDB v6.3.0 以降、弱められた等価条件である NA-EQ がハッシュ結合の構築に引き続き使用されています。これにより、走査する必要がある照合データの量が減り、照合プロセスが高速化されます。ビルド テーブルの合計`DISTINCT()`の値の割合がほぼ 100% になると、加速はより顕著になります。

-   `NULL`の特別なプロパティを使用して、一致する結果を返す速度を高速化します。

    アンチセミ結合は結合正規形 (CNF) であるため、結合のどちらかの側に`NULL`があると明確な結果が得られます。このプロパティを使用すると、マッチング プロセス全体の戻りを高速化できます。

以下は例です。

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                               |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| HashJoin_8                  | 10000.00 | root      |               | Null-aware anti left outer semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                                       |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                              |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                                        |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                    |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| HashJoin_8                  | 8000.00  | root      |               | Null-aware anti semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                            |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                   |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                             |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                   |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

最初のクエリ ステートメント`EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、サブクエリ`NOT IN`によって変換された左外部セミジョインは NULL 対応です。違いは、NAAJ 最適化ではハッシュ結合条件として NA-EQ も使用するため、結合計算が大幅に高速化されることです。

2 番目のクエリ ステートメント`EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、サブクエリ`NOT IN`によって変換されたアンチセミ結合は NULL 対応です。違いは、NAAJ 最適化ではハッシュ結合条件として NA-EQ も使用するため、結合計算が大幅に高速化されることです。

現在、TiDB はアンチ セミ ジョインとアンチ レフト アウタ セミ ジョインのみを null 認識できます。ハッシュ結合タイプのみがサポートされており、その構築テーブルは正しいテーブルに固定される必要があります。

> **注記：**
>
> `Not Exists`演算子もアンチセミ結合に変換されますが、null は認識されません。

## 他のタイプのサブクエリを使用した Explain ステートメント {#explain-statements-using-other-types-of-subqueries}

-   [MPP モードでの Explain ステートメント](/explain-mpp.md)
-   [インデックスを使用する Explain ステートメント](/explain-indexes.md)
-   [テーブル結合を使用する Explain ステートメント](/explain-joins.md)
-   [集計を使用する Explain ステートメント](/explain-aggregation.md)
-   [ビューを使用したステートメントの説明](/explain-views.md)
-   [パーティションを使用した Explain ステートメント](/explain-partitions.md)
-   [インデックス マージを使用した Explain ステートメント](/explain-index-merge.md)
