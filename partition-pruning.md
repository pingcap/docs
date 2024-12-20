---
title: Partition Pruning
summary: TiDB パーティション プルーニングの使用シナリオについて学習します。
---

# パーティションのプルーニング {#partition-pruning}

パーティション プルーニングは、パーティション テーブルに適用されるパフォーマンス最適化です。クエリ ステートメントのフィルター条件を分析し、必要なデータが含まれていないパーティションを考慮から除外 (*プルーニング*) します。不要なパーティションを除外することで、TiDB はアクセスする必要のあるデータの量を削減し、クエリ実行時間を大幅に短縮できます。

次に例を示します。

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY,
 pad VARCHAR(100)
)
PARTITION BY RANGE COLUMNS(id) (
 PARTITION p0 VALUES LESS THAN (100),
 PARTITION p1 VALUES LESS THAN (200),
 PARTITION p2 VALUES LESS THAN (MAXVALUE)
);

INSERT INTO t1 VALUES (1, 'test1'),(101, 'test2'), (201, 'test3');
EXPLAIN SELECT * FROM t1 WHERE id BETWEEN 80 AND 120;
```

```sql
+----------------------------+---------+-----------+------------------------+------------------------------------------------+
| id                         | estRows | task      | access object          | operator info                                  |
+----------------------------+---------+-----------+------------------------+------------------------------------------------+
| PartitionUnion_8           | 80.00   | root      |                        |                                                |
| ├─TableReader_10           | 40.00   | root      |                        | data:TableRangeScan_9                          |
| │ └─TableRangeScan_9       | 40.00   | cop[tikv] | table:t1, partition:p0 | range:[80,120], keep order:false, stats:pseudo |
| └─TableReader_12           | 40.00   | root      |                        | data:TableRangeScan_11                         |
|   └─TableRangeScan_11      | 40.00   | cop[tikv] | table:t1, partition:p1 | range:[80,120], keep order:false, stats:pseudo |
+----------------------------+---------+-----------+------------------------+------------------------------------------------+
5 rows in set (0.00 sec)
```

## パーティションプルーニングの使用シナリオ {#usage-scenarios-of-partition-pruning}

パーティション プルーニングの使用シナリオは、範囲パーティション テーブルとハッシュ パーティション テーブルという 2 種類のパーティション テーブルで異なります。

### ハッシュパーティションテーブルでパーティションプルーニングを使用する {#use-partition-pruning-in-hash-partitioned-tables}

このセクションでは、ハッシュ パーティション テーブルでのパーティション プルーニングの適用可能な使用シナリオと適用できない使用シナリオについて説明します。

#### ハッシュパーティションテーブルに適用可能なシナリオ {#applicable-scenario-in-hash-partitioned-tables}

パーティション プルーニングは、ハッシュ パーティション テーブル内の等価比較のクエリ条件にのみ適用されます。

```sql
create table t (x int) partition by hash(x) partitions 4;
explain select * from t where x = 1;
```

```sql
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| id                      | estRows  | task      | access object         | operator info                  |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| TableReader_8           | 10.00    | root      |                       | data:Selection_7               |
| └─Selection_7           | 10.00    | cop[tikv] |                       | eq(test.t.x, 1)                |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
```

上記のSQL文では、条件`x = 1`からすべての結果が1つのパーティションに収まることがわかります。値`1` `p3` 、ハッシュパーティションを通過した後、 `p1`パーティションにあることが確認できます。したがって、スキャンする必要があるのは`p1`パーティションのみであり、一致する結果がない`p2`パーティションにアクセスする必要はありません。実行プランからは、 `TableFullScan`演算子が1つだけ登場し、 `access object`で`p4`パーティションが指定されているため、 `p1` `partition pruning`有効になることが確認できます。

#### ハッシュパーティションテーブルに適用できないシナリオ {#inapplicable-scenarios-in-hash-partitioned-tables}

このセクションでは、ハッシュ パーティション テーブルでのパーティション プルーニングの適用できない 2 つの使用シナリオについて説明します。

##### シナリオ1 {#scenario-one}

クエリ結果が 1 つのパーティション ( `in` 、 `between` 、 `>` 、 `<` 、 `>=` 、 `<=`など) のみに該当するという条件を確認できない場合は、パーティション プルーニング最適化を使用できません。例:

```sql
create table t (x int) partition by hash(x) partitions 4;
explain select * from t where x > 2;
```

```sql
+------------------------------+----------+-----------+-----------------------+--------------------------------+
| id                           | estRows  | task      | access object         | operator info                  |
+------------------------------+----------+-----------+-----------------------+--------------------------------+
| Union_10                     | 13333.33 | root      |                       |                                |
| ├─TableReader_13             | 3333.33  | root      |                       | data:Selection_12              |
| │ └─Selection_12             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
| │   └─TableFullScan_11       | 10000.00 | cop[tikv] | table:t, partition:p0 | keep order:false, stats:pseudo |
| ├─TableReader_16             | 3333.33  | root      |                       | data:Selection_15              |
| │ └─Selection_15             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
| │   └─TableFullScan_14       | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo |
| ├─TableReader_19             | 3333.33  | root      |                       | data:Selection_18              |
| │ └─Selection_18             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
| │   └─TableFullScan_17       | 10000.00 | cop[tikv] | table:t, partition:p2 | keep order:false, stats:pseudo |
| └─TableReader_22             | 3333.33  | root      |                       | data:Selection_21              |
|   └─Selection_21             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
|     └─TableFullScan_20       | 10000.00 | cop[tikv] | table:t, partition:p3 | keep order:false, stats:pseudo |
+------------------------------+----------+-----------+-----------------------+--------------------------------+
```

この場合、対応するハッシュ パーティションが`x > 2`条件によって確認できないため、パーティション プルーニングは適用できません。

##### シナリオ2 {#scenario-two}

パーティション プルーニングのルール最適化はクエリ プランの生成フェーズで実行されるため、パーティション プルーニングは、フィルター条件が実行フェーズでのみ取得できるシナリオには適していません。例:

```sql
create table t (x int) partition by hash(x) partitions 4;
explain select * from t2 where x = (select * from t1 where t2.x = t1.x and t2.x < 2);
```

```sql
+--------------------------------------+----------+-----------+------------------------+----------------------------------------------+
| id                                   | estRows  | task      | access object          | operator info                                |
+--------------------------------------+----------+-----------+------------------------+----------------------------------------------+
| Projection_13                        | 9990.00  | root      |                        | test.t2.x                                    |
| └─Apply_15                           | 9990.00  | root      |                        | inner join, equal:[eq(test.t2.x, test.t1.x)] |
|   ├─TableReader_18(Build)            | 9990.00  | root      |                        | data:Selection_17                            |
|   │ └─Selection_17                   | 9990.00  | cop[tikv] |                        | not(isnull(test.t2.x))                       |
|   │   └─TableFullScan_16             | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo               |
|   └─Selection_19(Probe)              | 0.80     | root      |                        | not(isnull(test.t1.x))                       |
|     └─MaxOneRow_20                   | 1.00     | root      |                        |                                              |
|       └─Union_21                     | 2.00     | root      |                        |                                              |
|         ├─TableReader_24             | 2.00     | root      |                        | data:Selection_23                            |
|         │ └─Selection_23             | 2.00     | cop[tikv] |                        | eq(test.t2.x, test.t1.x), lt(test.t2.x, 2)   |
|         │   └─TableFullScan_22       | 2500.00  | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo               |
|         └─TableReader_27             | 2.00     | root      |                        | data:Selection_26                            |
|           └─Selection_26             | 2.00     | cop[tikv] |                        | eq(test.t2.x, test.t1.x), lt(test.t2.x, 2)   |
|             └─TableFullScan_25       | 2500.00  | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo               |
+--------------------------------------+----------+-----------+------------------------+----------------------------------------------+
```

このクエリは、 `t2`から行を読み取るたびに、 `t1`にパーティションテーブルに対してクエリを実行します。理論的には、この時点で`t1.x = val`のフィルタ条件が満たされますが、実際には、パーティション プルーニングはクエリ プランの生成フェーズでのみ有効であり、実行フェーズでは有効になりません。

### 範囲パーティション化されたテーブルでパーティションプルーニングを使用する {#use-partition-pruning-in-range-partitioned-tables}

このセクションでは、範囲パーティション化されたテーブルでのパーティション プルーニングの適用可能な使用シナリオと適用できない使用シナリオについて説明します。

#### 範囲パーティションテーブルに適用可能なシナリオ {#applicable-scenarios-in-range-partitioned-tables}

このセクションでは、範囲パーティション化されたテーブルでのパーティション プルーニングの適用可能な 3 つの使用シナリオについて説明します。

##### シナリオ1 {#scenario-one}

パーティション プルーニングは、範囲パーティション テーブル内の等価比較のクエリ条件に適用されます。例:

```sql
create table t (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10),
    partition p2 values less than (15)
    );
explain select * from t where x = 3;
```

```sql
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| id                      | estRows  | task      | access object         | operator info                  |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| TableReader_8           | 10.00    | root      |                       | data:Selection_7               |
| └─Selection_7           | 10.00    | cop[tikv] |                       | eq(test.t.x, 3)                |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p0 | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
```

パーティション プルーニングは、 `in`クエリ条件を使用する等価比較にも適用されます。例:

```sql
create table t (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10),
    partition p2 values less than (15)
    );
explain select * from t where x in(1,13);
```

```sql
+-----------------------------+----------+-----------+-----------------------+--------------------------------+
| id                          | estRows  | task      | access object         | operator info                  |
+-----------------------------+----------+-----------+-----------------------+--------------------------------+
| Union_8                     | 40.00    | root      |                       |                                |
| ├─TableReader_11            | 20.00    | root      |                       | data:Selection_10              |
| │ └─Selection_10            | 20.00    | cop[tikv] |                       | in(test.t.x, 1, 13)            |
| │   └─TableFullScan_9       | 10000.00 | cop[tikv] | table:t, partition:p0 | keep order:false, stats:pseudo |
| └─TableReader_14            | 20.00    | root      |                       | data:Selection_13              |
|   └─Selection_13            | 20.00    | cop[tikv] |                       | in(test.t.x, 1, 13)            |
|     └─TableFullScan_12      | 10000.00 | cop[tikv] | table:t, partition:p2 | keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+-----------------------+--------------------------------+
```

上記の SQL ステートメントでは、条件`x in(1,13)`から、すべての結果がいくつかのパーティションに分かれていることがわかります。分析後、 `x = 1`のすべてのレコードは`p0`パーティションにあり、 `x = 13`のすべてのレコードは`p2`パーティションにあることがわかったので、 `p0`と`p2`パーティションのみにアクセスする必要があります。

##### シナリオ2 {#scenario-two}

パーティション プルーニングは、 `between` 、 `>` 、 `<` 、 `=` 、 `>=` 、 `<=`などの間隔比較のクエリ条件に適用されます。次に例を示します。

```sql
create table t (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10),
    partition p2 values less than (15)
    );
explain select * from t where x between 7 and 14;
```

```sql
+-----------------------------+----------+-----------+-----------------------+-----------------------------------+
| id                          | estRows  | task      | access object         | operator info                     |
+-----------------------------+----------+-----------+-----------------------+-----------------------------------+
| Union_8                     | 500.00   | root      |                       |                                   |
| ├─TableReader_11            | 250.00   | root      |                       | data:Selection_10                 |
| │ └─Selection_10            | 250.00   | cop[tikv] |                       | ge(test.t.x, 7), le(test.t.x, 14) |
| │   └─TableFullScan_9       | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo    |
| └─TableReader_14            | 250.00   | root      |                       | data:Selection_13                 |
|   └─Selection_13            | 250.00   | cop[tikv] |                       | ge(test.t.x, 7), le(test.t.x, 14) |
|     └─TableFullScan_12      | 10000.00 | cop[tikv] | table:t, partition:p2 | keep order:false, stats:pseudo    |
+-----------------------------+----------+-----------+-----------------------+-----------------------------------+
```

##### シナリオ3 {#scenario-three}

パーティション プルーニングは、パーティション式が`fn(col)`の単純な形式であり、クエリ条件が`>` 、 `<` 、 `=` 、 `>=` 、および`<=`のいずれかであり、 `fn`関数が単調であるシナリオに適用されます。

`fn`関数が単調である場合、 `x`および`y`に対して、 `x > y`であれば`fn(x) > fn(y)` 。この場合、この`fn`関数は厳密に単調であると言えます。 `x`および`y`に対して、 `x > y`であれば`fn(x) >= fn(y)`です。この場合、 `fn`も「単調」であると言えます。理論的には、厳密にかどうかに関係なく、すべての単調関数はパーティション プルーニングによってサポートされます。現在、 TiDB は次の単調関数のみをサポートしています。

-   [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
-   [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)
-   `DATE`と`DATETIME`列の場合、 `YEAR`と`YEAR_MONTH`時間単位は単調関数と見なされます。10 列の場合、 `HOUR` 、 `HOUR_MINUTE` 、 `HOUR_SECOND` 、および`HOUR_MICROSECOND`単調関数と見なされます。パーティション[`EXTRACT(&#x3C;time unit> FROM &#x3C;DATETIME/DATE/TIME column>)`](/functions-and-operators/date-and-time-functions.md)では、 `EXTRACT`では`WEEK`時間単位として`TIME`されていないことに注意してください。

たとえば、パーティションプルーニングは、パーティション式が`fn(col)`の形式であり、 `fn`単調関数`to_days`である場合に有効になります。

```sql
create table t (id datetime) partition by range (to_days(id)) (
    partition p0 values less than (to_days('2020-04-01')),
    partition p1 values less than (to_days('2020-05-01')));
explain select * from t where id > '2020-04-18';
```

```sql
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
| id                      | estRows  | task      | access object         | operator info                             |
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
| TableReader_8           | 3333.33  | root      |                       | data:Selection_7                          |
| └─Selection_7           | 3333.33  | cop[tikv] |                       | gt(test.t.id, 2020-04-18 00:00:00.000000) |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo            |
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
```

#### 範囲パーティションテーブルでは適用できないシナリオ {#inapplicable-scenario-in-range-partitioned-tables}

パーティション プルーニングのルール最適化はクエリ プランの生成フェーズで実行されるため、パーティション プルーニングは、フィルター条件が実行フェーズでのみ取得できるシナリオには適していません。例:

```sql
create table t1 (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10));
create table t2 (x int);
explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
```

```sql
+--------------------------------------+----------+-----------+------------------------+-----------------------------------------------------------+
| id                                   | estRows  | task      | access object          | operator info                                             |
+--------------------------------------+----------+-----------+------------------------+-----------------------------------------------------------+
| Projection_13                        | 9990.00  | root      |                        | test.t2.x                                                 |
| └─Apply_15                           | 9990.00  | root      |                        | CARTESIAN inner join, other cond:lt(test.t2.x, test.t1.x) |
|   ├─TableReader_18(Build)            | 9990.00  | root      |                        | data:Selection_17                                         |
|   │ └─Selection_17                   | 9990.00  | cop[tikv] |                        | not(isnull(test.t2.x))                                    |
|   │   └─TableFullScan_16             | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                            |
|   └─Selection_19(Probe)              | 0.80     | root      |                        | not(isnull(test.t1.x))                                    |
|     └─MaxOneRow_20                   | 1.00     | root      |                        |                                                           |
|       └─Union_21                     | 2.00     | root      |                        |                                                           |
|         ├─TableReader_24             | 2.00     | root      |                        | data:Selection_23                                         |
|         │ └─Selection_23             | 2.00     | cop[tikv] |                        | lt(test.t2.x, 2), lt(test.t2.x, test.t1.x)                |
|         │   └─TableFullScan_22       | 2.50     | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo                            |
|         └─TableReader_27             | 2.00     | root      |                        | data:Selection_26                                         |
|           └─Selection_26             | 2.00     | cop[tikv] |                        | lt(test.t2.x, 2), lt(test.t2.x, test.t1.x)                |
|             └─TableFullScan_25       | 2.50     | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo                            |
+--------------------------------------+----------+-----------+------------------------+-----------------------------------------------------------+
14 rows in set (0.00 sec)
```

このクエリは、 `t2`から行を読み取るたびに、 `t1`にパーティションテーブルに対してクエリを実行します。理論的には、この時点で`t1.x> val`フィルタ条件が満たされますが、実際には、パーティション プルーニングはクエリ プランの生成フェーズでのみ有効であり、実行フェーズでは有効ではありません。
