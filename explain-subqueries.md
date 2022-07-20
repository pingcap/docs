---
title: Explain Statements That Use Subqueries
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# サブクエリを使用するステートメントを説明する {#explain-statements-that-use-subqueries}

TiDBは、サブクエリのパフォーマンスを向上させるために[いくつかの最適化](/subquery-optimization.md)を実行します。このドキュメントでは、一般的なサブクエリに対するこれらの最適化のいくつかと、 `EXPLAIN`の出力を解釈する方法について説明します。

このドキュメントの例は、次のサンプルデータに基づいています。

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

## 内部結合（一意でないサブクエリ） {#inner-join-non-unique-subquery}

次の例では、 `IN`サブクエリがテーブル`t2`からIDのリストを検索します。セマンティックを正確にするために、TiDBは列`t1_id`が一意であることを保証する必要があります。 `EXPLAIN`を使用すると、重複を削除して`INNER JOIN`操作を実行するために使用される実行プランを確認できます。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2);
```

```sql
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object                | operator info                                                                                                             |
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_14                     | 5.00     | root      |                              | inner join, inner:IndexLookUp_13, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) |
| ├─StreamAgg_49(Build)            | 5.00     | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id                                                      |
| │ └─IndexReader_50               | 5.00     | root      |                              | index:StreamAgg_39                                                                                                        |
| │   └─StreamAgg_39               | 5.00     | cop[tikv] |                              | group by:test.t2.t1_id,                                                                                                   |
| │     └─IndexFullScan_31         | 50000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                                           |
| └─IndexLookUp_13(Probe)          | 1.00     | root      |                              |                                                                                                                           |
|   ├─IndexRangeScan_11(Build)     | 1.00     | cop[tikv] | table:t1, index:PRIMARY(id)  | range: decided by [eq(test.t1.id, test.t2.t1_id)], keep order:false                                                       |
|   └─TableRowIDScan_12(Probe)     | 1.00     | cop[tikv] | table:t1                     | keep order:false                                                                                                          |
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

上記のクエリ結果から、TiDBがインデックス結合操作`| IndexJoin_14`を使用して、サブクエリを結合および変換していることがわかります。実行計画では、実行プロセスは次のとおりです。

1.  TiKV側のインデックススキャンオペレータ`└─IndexFullScan_31`は、 `t2.t1_id`列の値を読み取ります。
2.  `└─StreamAgg_39`オペレーターの一部のタスクは、TiKVの`t1_id`の値を重複排除します。
3.  `├─StreamAgg_49(Build)`オペレーターの一部のタスクは、TiDBの`t1_id`の値を重複排除します。重複排除は、集計関数`firstrow(test.t2.t1_id)`によって実行されます。
4.  操作結果は、 `t1`テーブルの主キーと結合されます。結合条件は`eq(test.t1.id, test.t2.t1_id)`です。

## 内部結合（一意のサブクエリ） {#inner-join-unique-subquery}

前の例では、テーブル`t1`に対して結合する前に、 `t1_id`の値が一意であることを確認するために集計が必要です。ただし、次の例では、 `UNIQUE`の制約があるため、 `t3.t1_id`はすでに一意であることが保証されています。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                               | estRows | task      | access object               | operator info                                                                                                             |
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_17                     | 1978.13 | root      |                             | inner join, inner:IndexLookUp_16, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_44(Build)          | 1978.00 | root      |                             | data:TableFullScan_43                                                                                                     |
| │ └─TableFullScan_43             | 1978.00 | cop[tikv] | table:t3                    | keep order:false                                                                                                          |
| └─IndexLookUp_16(Probe)          | 1.00    | root      |                             |                                                                                                                           |
|   ├─IndexRangeScan_14(Build)     | 1.00    | cop[tikv] | table:t1, index:PRIMARY(id) | range: decided by [eq(test.t1.id, test.t3.t1_id)], keep order:false                                                       |
|   └─TableRowIDScan_15(Probe)     | 1.00    | cop[tikv] | table:t1                    | keep order:false                                                                                                          |
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.01 sec)
```

意味的には、 `t3.t1_id`は一意であることが保証されているため、 `INNER JOIN`として直接実行できます。

## 半結合（相関サブクエリ） {#semi-join-correlated-subquery}

前の2つの例では、サブクエリ内のデータが（ `StreamAgg`を介して）一意になるか、一意であることが保証された後、TiDBは`INNER JOIN`操作を実行できます。両方の結合は、インデックス結合を使用して実行されます。

この例では、TiDBは別の実行プランを選択します。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE t1_id != t1.int_col);
```

```sql
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| id                          | estRows   | task      | access object                | operator info                                                                                          |
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| MergeJoin_9                 | 45446.40  | root      |                              | semi join, left key:test.t1.id, right key:test.t2.t1_id, other cond:ne(test.t2.t1_id, test.t1.int_col) |
| ├─IndexReader_24(Build)     | 180000.00 | root      |                              | index:IndexFullScan_23                                                                                 |
| │ └─IndexFullScan_23        | 180000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                        |
| └─TableReader_22(Probe)     | 56808.00  | root      |                              | data:Selection_21                                                                                      |
|   └─Selection_21            | 56808.00  | cop[tikv] |                              | ne(test.t1.id, test.t1.int_col)                                                                        |
|     └─TableFullScan_20      | 71010.00  | cop[tikv] | table:t1                     | keep order:true                                                                                        |
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

上記の結果から、TiDBが`Semi Join`アルゴリズムを使用していることがわかります。半結合は内部結合とは異なります。半結合では、右キー（ `t2.t1_id` ）の最初の値のみが許可されます。これは、結合演算子タスクの一部として重複が排除されることを意味します。結合アルゴリズムもマージ結合です。これは、オペレーターが左側と右側の両方から並べ替えられた順序でデータを読み取るため、効率的なジッパーマージのようなものです。

サブクエリはサブクエリの外部に存在する列（ `t1.int_col` ）を参照するため、元のステートメントは*相関サブクエリ*と見なされます。ただし、 `EXPLAIN`の出力は、 [サブクエリの無相関化の最適化](/correlated-subquery-optimization.md)が適用された後の実行プランを示しています。条件`t1_id != t1.int_col`は`t1.id != t1.int_col`に書き換えられます。 TiDBはテーブル`t1`からデータを読み取るため、 `└─Selection_21`でこれを実行できるため、この非相関化と書き換えにより、実行がはるかに効率的になります。

## アンチセミジョイン（サブクエリで<code>NOT IN</code> ） {#anti-semi-join-code-not-in-code-subquery}

次の例では、サブクエリに`t3.t1_id`が含まれてい*ない限り*、クエリはテーブル`t3`からすべての行を意味的に返します。

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                       |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| IndexMergeJoin_20           | 1598.40 | root      |               | anti semi join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id |
| ├─TableReader_28(Build)     | 1998.00 | root      |               | data:TableFullScan_27                                                               |
| │ └─TableFullScan_27        | 1998.00 | cop[tikv] | table:t3      | keep order:false                                                                    |
| └─TableReader_15(Probe)     | 1.00    | root      |               | data:Selection_14                                                                   |
|   └─Selection_14            | 1.00    | cop[tikv] |               | lt(test.t1.int_col, 100)                                                            |
|     └─TableRangeScan_13     | 1.00    | cop[tikv] | table:t1      | range: decided by [test.t3.t1_id], keep order:true                                  |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

このクエリは、テーブル`t3`を読み取ることから始まり、 `PRIMARY KEY`に基づいてテーブル`t1`をプローブします。結合タイプは*反半結合*です;この例は、値（ `NOT IN` ）が存在しないためのものであり、結合が拒否される前に最初の行のみが一致する必要があるため、半結合するためです。
