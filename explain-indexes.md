---
title: Explain Statements That Use Indexes
summary: TiDB のEXPLAINステートメントによって返される実行プラン情報について学習します。
---

# インデックスを使用するステートメントを説明する {#explain-statements-that-use-indexes}

TiDB は、インデックスを利用してクエリの実行を高速化するいくつかの演算子をサポートしています。

-   [`IndexLookup`](#indexlookup)
-   [`IndexReader`](#indexreader)
-   [`Point_Get`と`Batch_Point_Get`](#point_get-and-batch_point_get)
-   [`IndexFullScan`](#indexfullscan)

このドキュメントの例は、次のサンプル データに基づいています。

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 intkey INT NOT NULL,
 pad1 VARBINARY(1024),
 INDEX (intkey)
);

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
```

## インデックスルックアップ {#indexlookup}

TiDBは、セカンダリインデックスからデータを取得する際に`IndexLookup`演算子を使用します。この場合、以下のクエリはすべて、 `intkey`インデックスに対して`IndexLookup`演算子を使用します。

```sql
EXPLAIN SELECT * FROM t1 WHERE intkey = 123;
EXPLAIN SELECT * FROM t1 WHERE intkey < 10;
EXPLAIN SELECT * FROM t1 WHERE intkey BETWEEN 300 AND 310;
EXPLAIN SELECT * FROM t1 WHERE intkey IN (123,29,98);
EXPLAIN SELECT * FROM t1 WHERE intkey >= 99 AND intkey <= 103;
```

```sql
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 1.00    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[123,123], keep order:false |
| └─TableRowIDScan_9(Probe)     | 1.00    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 3.60    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 3.60    | cop[tikv] | table:t1, index:intkey(intkey) | range:[-inf,10), keep order:false |
| └─TableRowIDScan_9(Probe)     | 3.60    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 5.67    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 5.67    | cop[tikv] | table:t1, index:intkey(intkey) | range:[300,310], keep order:false |
| └─TableRowIDScan_9(Probe)     | 5.67    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+-----------------------------------------------------+
| id                            | estRows | task      | access object                  | operator info                                       |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------------------------+
| IndexLookUp_10                | 4.00    | root      |                                |                                                     |
| ├─IndexRangeScan_8(Build)     | 4.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[29,29], [98,98], [123,123], keep order:false |
| └─TableRowIDScan_9(Probe)     | 4.00    | cop[tikv] | table:t1                       | keep order:false                                    |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+----------------------------------+
| id                            | estRows | task      | access object                  | operator info                    |
+-------------------------------+---------+-----------+--------------------------------+----------------------------------+
| IndexLookUp_10                | 6.00    | root      |                                |                                  |
| ├─IndexRangeScan_8(Build)     | 6.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[99,103], keep order:false |
| └─TableRowIDScan_9(Probe)     | 6.00    | cop[tikv] | table:t1                       | keep order:false                 |
+-------------------------------+---------+-----------+--------------------------------+----------------------------------+
3 rows in set (0.00 sec)
```

`IndexLookup`演算子には 2 つの子ノードがあります。

-   `├─IndexRangeScan_8(Build)`演算子は`intkey`インデックスの範囲スキャンを実行し、内部の`RowID` (このテーブルの場合は主キー) の値を取得します。
-   次に、 `└─TableRowIDScan_9(Probe)`演算子はテーブル データから完全な行を取得します。

`IndexLookup`タスクには2つのステップが必要なため、多数の行が一致するシナリオでは、SQLオプティマイザーは[統計](/statistics.md)に基づいて`TableFullScan`演算子を選択する可能性があります。次の例では、多数の行が`intkey > 100`条件に一致するため、 `TableFullScan`が選択されます。

```sql
EXPLAIN SELECT * FROM t1 WHERE intkey > 100;
```

```sql
+-------------------------+---------+-----------+---------------+-------------------------+
| id                      | estRows | task      | access object | operator info           |
+-------------------------+---------+-----------+---------------+-------------------------+
| TableReader_7           | 898.50  | root      |               | data:Selection_6        |
| └─Selection_6           | 898.50  | cop[tikv] |               | gt(test.t1.intkey, 100) |
|   └─TableFullScan_5     | 1010.00 | cop[tikv] | table:t1      | keep order:false        |
+-------------------------+---------+-----------+---------------+-------------------------+
3 rows in set (0.00 sec)
```

`IndexLookup`演算子は、インデックス付き列の`LIMIT`効率的に最適化するためにも使用できます。

```sql
EXPLAIN SELECT * FROM t1 ORDER BY intkey DESC LIMIT 10;
```

```sql
+--------------------------------+---------+-----------+--------------------------------+------------------------------------+
| id                             | estRows | task      | access object                  | operator info                      |
+--------------------------------+---------+-----------+--------------------------------+------------------------------------+
| IndexLookUp_21                 | 10.00   | root      |                                | limit embedded(offset:0, count:10) |
| ├─Limit_20(Build)              | 10.00   | cop[tikv] |                                | offset:0, count:10                 |
| │ └─IndexFullScan_18           | 10.00   | cop[tikv] | table:t1, index:intkey(intkey) | keep order:true, desc              |
| └─TableRowIDScan_19(Probe)     | 10.00   | cop[tikv] | table:t1                       | keep order:false, stats:pseudo     |
+--------------------------------+---------+-----------+--------------------------------+------------------------------------+
4 rows in set (0.00 sec)

```

上記の例では、インデックス`intkey`から最後の10行が読み取られます。その後、テーブルデータからこれらの`RowID`値が取得されます。

## インデックスリーダー {#indexreader}

TiDBは*カバーインデックス最適化*をサポートしています。インデックスからすべての行を取得できる場合、TiDBは通常`IndexLookup`で必要な2番目のステップを省略します。次の2つの例を考えてみましょう。

```sql
EXPLAIN SELECT * FROM t1 WHERE intkey = 123;
EXPLAIN SELECT id FROM t1 WHERE intkey = 123;
```

```sql
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 1.00    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[123,123], keep order:false |
| └─TableRowIDScan_9(Probe)     | 1.00    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+--------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                       | estRows | task      | access object                  | operator info                     |
+--------------------------+---------+-----------+--------------------------------+-----------------------------------+
| Projection_4             | 1.00    | root      |                                | test.t1.id                        |
| └─IndexReader_6          | 1.00    | root      |                                | index:IndexRangeScan_5            |
|   └─IndexRangeScan_5     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[123,123], keep order:false |
+--------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)
```

`id`内部的には`RowID`でもあるため、インデックス`intkey`に格納されます。インデックス`intkey`を`└─IndexRangeScan_5`の一部として使用することで、インデックス`RowID`の値を直接返すことができます。

## Point_Get と Batch_Point_Get {#point-get-and-batch-point-get}

TiDBは、主キーまたは一意キーから直接データを取得する際に、 `Point_Get`または`Batch_Point_Get`演算子を使用します。これらの演算子は`IndexLookup`よりも効率的です。例えば、

```sql
EXPLAIN SELECT * FROM t1 WHERE id = 1234;
EXPLAIN SELECT * FROM t1 WHERE id IN (1234,123);

ALTER TABLE t1 ADD unique_key INT;
UPDATE t1 SET unique_key = id;
ALTER TABLE t1 ADD UNIQUE KEY (unique_key);

EXPLAIN SELECT * FROM t1 WHERE unique_key = 1234;
EXPLAIN SELECT * FROM t1 WHERE unique_key IN (1234, 123);
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1234   |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)

+-------------------+---------+------+---------------+-------------------------------------------------+
| id                | estRows | task | access object | operator info                                   |
+-------------------+---------+------+---------------+-------------------------------------------------+
| Batch_Point_Get_1 | 2.00    | root | table:t1      | handle:[1234 123], keep order:false, desc:false |
+-------------------+---------+------+---------------+-------------------------------------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.27 sec)

Query OK, 1010 rows affected (0.06 sec)
Rows matched: 1010  Changed: 1010  Warnings: 0

Query OK, 0 rows affected (0.37 sec)

+-------------+---------+------+----------------------------------------+---------------+
| id          | estRows | task | access object                          | operator info |
+-------------+---------+------+----------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1, index:unique_key(unique_key) |               |
+-------------+---------+------+----------------------------------------+---------------+
1 row in set (0.00 sec)

+-------------------+---------+------+----------------------------------------+------------------------------+
| id                | estRows | task | access object                          | operator info                |
+-------------------+---------+------+----------------------------------------+------------------------------+
| Batch_Point_Get_1 | 2.00    | root | table:t1, index:unique_key(unique_key) | keep order:false, desc:false |
+-------------------+---------+------+----------------------------------------+------------------------------+
1 row in set (0.00 sec)
```

## インデックスフルスキャン {#indexfullscan}

インデックスは順序付けられているため、 `IndexFullScan`演算子を使用して、インデックス付けされた値の`MIN`または`MAX`値などの一般的なクエリを最適化できます。

```sql
EXPLAIN SELECT MIN(intkey) FROM t1;
EXPLAIN SELECT MAX(intkey) FROM t1;
```

```sql
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| id                           | estRows | task      | access object                  | operator info                       |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| StreamAgg_12                 | 1.00    | root      |                                | funcs:min(test.t1.intkey)->Column#4 |
| └─Limit_16                   | 1.00    | root      |                                | offset:0, count:1                   |
|   └─IndexReader_29           | 1.00    | root      |                                | index:Limit_28                      |
|     └─Limit_28               | 1.00    | cop[tikv] |                                | offset:0, count:1                   |
|       └─IndexFullScan_27     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | keep order:true                     |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
5 rows in set (0.00 sec)

+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| id                           | estRows | task      | access object                  | operator info                       |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| StreamAgg_12                 | 1.00    | root      |                                | funcs:max(test.t1.intkey)->Column#4 |
| └─Limit_16                   | 1.00    | root      |                                | offset:0, count:1                   |
|   └─IndexReader_29           | 1.00    | root      |                                | index:Limit_28                      |
|     └─Limit_28               | 1.00    | cop[tikv] |                                | offset:0, count:1                   |
|       └─IndexFullScan_27     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | keep order:true, desc               |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
5 rows in set (0.00 sec)
```

上記の文では、各TiKVリージョンに対してタスク`IndexFullScan`が実行されます。3 `FullScan`名前にもかかわらず、読み取る必要があるのは最初の行（ `└─Limit_28` ）のみです。各TiKVリージョンは`MIN`または`MAX`値をTiDBに返し、TiDBはストリーム集計を実行して単一行をフィルタリングします。また、集約関数`MAX`または`MIN`使用したストリーム集計により、テーブルが空の場合に`NULL`返されることも保証されます。

対照的に、インデックスなしの値に対して関数`MIN`実行すると、結果は`TableFullScan`になります。このクエリではTiKV内のすべての行をスキャンする必要がありますが、各TiKVリージョンがTiDBに1行のみを返すように、 `TopN`計算が実行されます。 `TopN` TiKVとTiDB間で過剰な行が転送されるのを防ぎますが、この文は、インデックスを利用できる上記の例`MIN`よりもはるかに効率が悪いと考えられます。

```sql
EXPLAIN SELECT MIN(pad1) FROM t1;
```

```sql
+--------------------------------+---------+-----------+---------------+-----------------------------------+
| id                             | estRows | task      | access object | operator info                     |
+--------------------------------+---------+-----------+---------------+-----------------------------------+
| StreamAgg_13                   | 1.00    | root      |               | funcs:min(test.t1.pad1)->Column#4 |
| └─TopN_14                      | 1.00    | root      |               | test.t1.pad1, offset:0, count:1   |
|   └─TableReader_23             | 1.00    | root      |               | data:TopN_22                      |
|     └─TopN_22                  | 1.00    | cop[tikv] |               | test.t1.pad1, offset:0, count:1   |
|       └─Selection_21           | 1008.99 | cop[tikv] |               | not(isnull(test.t1.pad1))         |
|         └─TableFullScan_20     | 1010.00 | cop[tikv] | table:t1      | keep order:false                  |
+--------------------------------+---------+-----------+---------------+-----------------------------------+
6 rows in set (0.00 sec)
```

次のステートメントは、 `IndexFullScan`演算子を使用してインデックス内のすべての行をスキャンします。

```sql
EXPLAIN SELECT SUM(intkey) FROM t1;
EXPLAIN SELECT AVG(intkey) FROM t1;
```

```sql
+----------------------------+---------+-----------+--------------------------------+-------------------------------------+
| id                         | estRows | task      | access object                  | operator info                       |
+----------------------------+---------+-----------+--------------------------------+-------------------------------------+
| StreamAgg_20               | 1.00    | root      |                                | funcs:sum(Column#6)->Column#4       |
| └─IndexReader_21           | 1.00    | root      |                                | index:StreamAgg_8                   |
|   └─StreamAgg_8            | 1.00    | cop[tikv] |                                | funcs:sum(test.t1.intkey)->Column#6 |
|     └─IndexFullScan_19     | 1010.00 | cop[tikv] | table:t1, index:intkey(intkey) | keep order:false                    |
+----------------------------+---------+-----------+--------------------------------+-------------------------------------+
4 rows in set (0.00 sec)

+----------------------------+---------+-----------+--------------------------------+----------------------------------------------------------------------------+
| id                         | estRows | task      | access object                  | operator info                                                              |
+----------------------------+---------+-----------+--------------------------------+----------------------------------------------------------------------------+
| StreamAgg_20               | 1.00    | root      |                                | funcs:avg(Column#7, Column#8)->Column#4                                    |
| └─IndexReader_21           | 1.00    | root      |                                | index:StreamAgg_8                                                          |
|   └─StreamAgg_8            | 1.00    | cop[tikv] |                                | funcs:count(test.t1.intkey)->Column#7, funcs:sum(test.t1.intkey)->Column#8 |
|     └─IndexFullScan_19     | 1010.00 | cop[tikv] | table:t1, index:intkey(intkey) | keep order:false                                                           |
+----------------------------+---------+-----------+--------------------------------+----------------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

上記の例では、インデックス`(intkey + RowID)`値の幅が行全体の幅よりも狭いため、 `IndexFullScan`が`TableFullScan`よりも効率的です。

次のステートメントでは、テーブルから追加の列が必要であるため、 `IndexFullScan`演算子の使用はサポートされません。

```sql
EXPLAIN SELECT AVG(intkey), ANY_VALUE(pad1) FROM t1;
```

```sql
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object | operator info                                                                                                         |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------+
| Projection_4                 | 1.00    | root      |               | Column#4, any_value(test.t1.pad1)->Column#5                                                                           |
| └─StreamAgg_16               | 1.00    | root      |               | funcs:avg(Column#10, Column#11)->Column#4, funcs:firstrow(Column#12)->test.t1.pad1                                    |
|   └─TableReader_17           | 1.00    | root      |               | data:StreamAgg_8                                                                                                      |
|     └─StreamAgg_8            | 1.00    | cop[tikv] |               | funcs:count(test.t1.intkey)->Column#10, funcs:sum(test.t1.intkey)->Column#11, funcs:firstrow(test.t1.pad1)->Column#12 |
|       └─TableFullScan_15     | 1010.00 | cop[tikv] | table:t1      | keep order:false                                                                                                      |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```
