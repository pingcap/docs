---
title: Explain Statements That Use Subqueries
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# サブクエリを使用するステートメントの説明 {#explain-statements-that-use-subqueries}

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

## 内部結合 (一意でないサブクエリ) {#inner-join-non-unique-subquery}

次の例では、 `IN`サブクエリがテーブル`t2`から ID のリストを検索します。セマンティックの正確性のために、TiDB は列`t1_id`が一意であることを保証する必要があります。 `EXPLAIN`を使用すると、重複を削除して`INNER JOIN`操作を実行するために使用される実行計画を確認できます。

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

上記のクエリ結果から、TiDB がインデックス結合操作`| IndexJoin_14`使用してサブクエリを結合および変換していることがわかります。実行計画では、実行プロセスは次のとおりです。

1.  TiKV 側のインデックススキャンオペレータ`└─IndexFullScan_31` `t2.t1_id`列の値を読み取ります。
2.  `└─StreamAgg_39`オペレーターの一部のタスクは、TiKV の`t1_id`の値を重複排除します。
3.  `├─StreamAgg_49(Build)`オペレーターのいくつかのタスクは、TiDB で`t1_id`の値を重複除去します。重複排除は集約機能`firstrow(test.t2.t1_id)`によって行われる。
4.  演算結果は`t1`テーブルの主キーに結合されます。結合条件は`eq(test.t1.id, test.t2.t1_id)`です。

## 内部結合 (一意のサブクエリ) {#inner-join-unique-subquery}

前の例では、テーブル`t1`に対して結合する前に、 `t1_id`の値が一意であることを確認するために集計が必要です。ただし、次の例では、 `UNIQUE`制約により、 `t3.t1_id`は既に一意であることが保証されています。

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

意味的に`t3.t1_id`は一意であることが保証されているため、 `INNER JOIN`として直接実行できます。

## 準結合 (相関サブクエリ) {#semi-join-correlated-subquery}

前の 2 つの例では、TiDB は、サブクエリ内のデータが ( `StreamAgg`によって) 一意になるか、一意であることが保証された後、 `INNER JOIN`操作を実行できます。両方の結合は、Index Join を使用して実行されます。

この例では、TiDB は別の実行計画を選択します。

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

上記の結果から、TiDB が`Semi Join`アルゴリズムを使用していることがわかります。半結合は内部結合とは異なります。半結合は右側のキー ( `t2.t1_id` ) の最初の値のみを許可します。つまり、重複は結合演算子タスクの一部として削除されます。結合アルゴリズムも Merge Join です。これは、演算子がソートされた順序で左側と右側の両方からデータを読み取るため、効率的なジッパー マージのようなものです。

サブクエリはサブクエリの外部に存在する列 ( `t1.int_col` ) を参照するため、元のステートメントは*相関サブクエリと*見なされます。ただし、 `EXPLAIN`の出力は、 [サブクエリ非相関最適化](/correlated-subquery-optimization.md)適用された後の実行計画を示しています。条件`t1_id != t1.int_col`を`t1.id != t1.int_col`に書き換える。 TiDB は、テーブルからデータを読み取るときに`└─Selection_21`でこれを実行できます`t1` 。

## 反準結合 ( <code>NOT IN</code>サブクエリ) {#anti-semi-join-code-not-in-code-subquery}

次の例では、サブクエリに`t3.t1_id`ない*限り、*クエリは意味的にテーブル`t3`からすべての行を返します。

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

このクエリは、最初にテーブル`t3`を読み取り、次に`PRIMARY KEY`に基づいてテーブル`t1`をプローブします。結合タイプは*アンチセミ結合*です。 anti-この例は値 ( `NOT IN` ) が存在しないためであり、半結合は、結合が拒否される前に最初の行のみが一致する必要があるためです。

## Null-aware semi join ( <code>IN</code>および<code>= ANY</code>サブクエリ) {#null-aware-semi-join-code-in-code-and-code-any-code-subqueries}

`IN`または`= ANY`セット演算子の値は、3 つの値 ( `true` 、 `false` 、および`NULL` ) です。 2 つの演算子のいずれかから変換された結合タイプの場合、TiDB は結合キーの両側の`NULL`を認識し、特別な方法で処理する必要があります。

`IN`と`= ANY`の演算子を含むサブクエリは、それぞれセミ ジョインと左外部セミ ジョインに変換されます。前の[セミジョイン](#semi-join-correlated-subquery)の例では、結合キーの両側の列`test.t1.id`と`test.t2.t1_id` `not NULL`であるため、セミ結合を null 認識と見なす必要はありません ( `NULL`は特別に処理されません)。 TiDB は、特別な最適化を行わずに、デカルト積とフィルターに基づいて null 認識セミ結合を処理します。次に例を示します。

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

最初のクエリ ステートメント`EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、 `IN`サブクエリによって変換された左外部セミ ジョインは NULL を認識します。具体的には、デカルト積が最初に計算され、次に`IN`または`= ANY`で接続された列が、フィルター処理のための通常の等価クエリとして別の条件に入れられます。

2 番目のクエリ ステートメント`EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、 `IN`サブクエリは NULL を認識するセミ ジョインに変換されているはずです。しかし、TiDB はセミ結合を内部結合と集約に変換することで最適化します。これは、非スカラー出力の`IN`サブクエリで`NULL`と`false`同等であるためです。プッシュダウン フィルターの`NULL`行は、 `WHERE`句の否定的なセマンティクスになります。したがって、これらの行は事前に無視できます。

> **ノート：**
>
> `Exists`演算子も準結合に変換されますが、null に対応していません。

## Null-aware anti semi join ( <code>NOT IN</code>および<code>!= ALL</code>サブクエリ) {#null-aware-anti-semi-join-code-not-in-code-and-code-all-code-subqueries}

`NOT IN`または`!= ALL`セット演算子の値は、3 つの値 ( `true` 、 `false` 、および`NULL` ) です。 2 つの演算子のいずれかから変換された結合タイプの場合、TiDB は結合キーの両側の`NULL`を認識し、特別な方法で処理する必要があります。

`NOT IN`と`! = ALL`の演算子を含むサブクエリは、それぞれ反セミ結合と反左外部セミ結合に変換されます。前の[アンチセミジョイン](#anti-semi-join-not-in-subquery)の例では、結合キーの両側の列`test.t3.t1_id`と`test.t1.id` `not NULL`であるため、アンチ セミ結合を null 認識と見なす必要はありません ( `NULL`は特別に処理されません)。

TiDB v6.3.0 は、次のように null-aware anti join (NAAJ) を最適化します。

-   null 認識等値条件 (NA-EQ) を使用してハッシュ結合を構築する

    セット演算子は、条件の両側の演算子の値が`NULL`場合に特別なプロセスを必要とする等式条件を導入します。 null 認識を必要とする等価条件は、NA-EQ と呼ばれます。以前のバージョンとは異なり、TiDB v6.3.0 は以前のように NA-EQ を処理しなくなりましたが、結合後に他の条件に配置し、デカルト積を照合した後に結果セットの正当性を判断します。

    TiDB v6.3.0 以降、弱められた等価条件である NA-EQ は、ハッシュ結合を構築するために引き続き使用されます。これにより、トラバースする必要がある照合データの量が減り、照合プロセスが高速化されます。ビルド テーブルの合計`DISTINCT()`値のパーセンテージがほぼ 100% になると、加速がより顕著になります。

-   `NULL`の特殊なプロパティを使用して、一致する結果を返す速度を上げます

    アンチセミ結合は結合正規形 (CNF) であるため、結合のいずれかの側に`NULL`があると、明確な結果が得られます。このプロパティを使用して、一致プロセス全体の戻りを高速化できます。

次に例を示します。

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

最初のクエリ ステートメント`EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、 `NOT IN`サブクエリによって変換された左外部セミ ジョインは NULL を認識します。違いは、NAAJ 最適化では NA-EQ もハッシュ結合条件として使用されるため、結合計算が大幅に高速化されることです。

2 番目のクエリ ステートメント`EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);`では、テーブル`t`と`s`の列`a`と`b` NULLABLE であるため、 `NOT IN`サブクエリによって変換されるアンチ セミ ジョインは null を認識します。違いは、NAAJ 最適化では NA-EQ もハッシュ結合条件として使用されるため、結合計算が大幅に高速化されることです。

現在、TiDB はアンチ セミ ジョインとアンチ レフト アウター セミ ジョインの null 認識のみ可能です。ハッシュ結合タイプのみがサポートされており、そのビルド テーブルは正しいテーブルに固定する必要があります。

> **ノート：**
>
> `Not Exists`演算子もアンチセミ結合に変換されますが、null 認識ではありません。

## 他のタイプのサブクエリを使用した Explain ステートメント {#explain-statements-using-other-types-of-subqueries}

-   [MPP モードの Explain ステートメント](/explain-mpp.md)
-   [インデックスを使用するステートメントの説明](/explain-indexes.md)
-   [テーブル結合を使用するステートメントの説明](/explain-joins.md)
-   [集計を使用するステートメントの説明](/explain-aggregation.md)
-   [ビューを使用してステートメントを説明する](/explain-views.md)
-   [パーティションを使用した Explain ステートメント](/explain-partitions.md)
-   [インデックス マージを使用したステートメントの説明](/explain-index-merge.md)
