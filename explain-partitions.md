---
title: Explain Statements Using Partitions
summary: TiDBの`EXPLAIN`ステートメントは、クエリ実行時にアクセスする必要があるパーティションを表示します。パーティションのプルーニングにより、表示されるパーティションはサブセットに過ぎません。パーティションテーブルの最適化と`EXPLAIN`出力の解釈方法について説明します。新しいパーティションテーブルに対するステートメントの例を示し、パーティションのプルーニングによってパーティションが削除されない場合の例も示します。
---

# パーティションを使用した Explain ステートメント {#explain-statements-using-partitions}

`EXPLAIN`ステートメントは、クエリを実行するために TiDB がアクセスする必要があるパーティションを表示します。 [パーティションのプルーニング](/partition-pruning.md)のため、表示されるパーティションは、多くの場合、パーティション全体のサブセットにすぎません。このドキュメントでは、一般的なパーティション テーブルの最適化のいくつかと、 `EXPLAIN`の出力を解釈する方法について説明します。

このドキュメントで使用されるサンプル データ:

```sql
CREATE TABLE t1 (
 id BIGINT NOT NULL auto_increment,
 d date NOT NULL,
 pad1 BLOB,
 pad2 BLOB,
 pad3 BLOB,
 PRIMARY KEY (id,d)
) PARTITION BY RANGE (YEAR(d)) (
 PARTITION p2016 VALUES LESS THAN (2017),
 PARTITION p2017 VALUES LESS THAN (2018),
 PARTITION p2018 VALUES LESS THAN (2019),
 PARTITION p2019 VALUES LESS THAN (2020),
 PARTITION pmax VALUES LESS THAN MAXVALUE
);

INSERT INTO t1 (d, pad1, pad2, pad3) VALUES 
 ('2016-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2016-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2016-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2017-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2017-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2017-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2018-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2018-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2018-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2019-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2019-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2019-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2020-01-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2020-06-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024)),
 ('2020-09-01', RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024));

INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, a.d, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;

SELECT SLEEP(1);
ANALYZE TABLE t1;
```

次の例は、新しく作成されたパーティションテーブルに対するステートメントを示しています。

```sql
EXPLAIN SELECT COUNT(*) FROM t1 WHERE d = '2017-06-01';
```

```sql
+------------------------------+---------+-----------+---------------------------+-------------------------------------------+
| id                           | estRows | task      | access object             | operator info                             |
+------------------------------+---------+-----------+---------------------------+-------------------------------------------+
| StreamAgg_21                 | 1.00    | root      |                           | funcs:count(Column#8)->Column#6           |
| └─TableReader_22             | 1.00    | root      |                           | data:StreamAgg_10                         |
|   └─StreamAgg_10             | 1.00    | cop[tikv] |                           | funcs:count(1)->Column#8                  |
|     └─Selection_20           | 8.87    | cop[tikv] |                           | eq(test.t1.d, 2017-06-01 00:00:00.000000) |
|       └─TableFullScan_19     | 8870.00 | cop[tikv] | table:t1, partition:p2017 | keep order:false                          |
+------------------------------+---------+-----------+---------------------------+-------------------------------------------+
5 rows in set (0.01 sec)
```

最も内側の演算子 ( `└─TableFullScan_19` ) から開始して、ルート演算子 ( `StreamAgg_21` ) に向かって作業を戻します。

-   TiDB は、1 つのパーティション ( `p2017` ) のみにアクセスする必要があることを正常に識別しました。これについては`access object`に記載されています。
-   パーティション自体は演算子`└─TableFullScan_19`でスキャンされ、開始日が`2017-06-01 00:00:00.000000`である行をフィルターするために`└─Selection_20`適用されました。
-   `└─Selection_20`に一致する行は、コプロセッサでストリーム集約され、コプロセッサは`count`関数をネイティブに理解します。
-   次に、各コプロセッサー要求は 1 行を TiDB 内の`└─TableReader_22`に送り返し、それが`StreamAgg_21`の下にストリーム集約され、1 行がクライアントに返されます。

次の例では、パーティションのプルーニングによってパーティションは削除されません。

```sql
EXPLAIN SELECT COUNT(*) FROM t1 WHERE YEAR(d) = 2017;
```

```sql
+------------------------------------+----------+-----------+---------------------------+----------------------------------+
| id                                 | estRows  | task      | access object             | operator info                    |
+------------------------------------+----------+-----------+---------------------------+----------------------------------+
| HashAgg_20                         | 1.00     | root      |                           | funcs:count(Column#7)->Column#6  |
| └─PartitionUnion_21                | 5.00     | root      |                           |                                  |
|   ├─StreamAgg_36                   | 1.00     | root      |                           | funcs:count(Column#9)->Column#7  |
|   │ └─TableReader_37               | 1.00     | root      |                           | data:StreamAgg_25                |
|   │   └─StreamAgg_25               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#9         |
|   │     └─Selection_35             | 6000.00  | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_34       | 7500.00  | cop[tikv] | table:t1, partition:p2016 | keep order:false                 |
|   ├─StreamAgg_55                   | 1.00     | root      |                           | funcs:count(Column#11)->Column#7 |
|   │ └─TableReader_56               | 1.00     | root      |                           | data:StreamAgg_44                |
|   │   └─StreamAgg_44               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#11        |
|   │     └─Selection_54             | 14192.00 | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_53       | 17740.00 | cop[tikv] | table:t1, partition:p2017 | keep order:false                 |
|   ├─StreamAgg_74                   | 1.00     | root      |                           | funcs:count(Column#13)->Column#7 |
|   │ └─TableReader_75               | 1.00     | root      |                           | data:StreamAgg_63                |
|   │   └─StreamAgg_63               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#13        |
|   │     └─Selection_73             | 3977.60  | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_72       | 4972.00  | cop[tikv] | table:t1, partition:p2018 | keep order:false                 |
|   ├─StreamAgg_93                   | 1.00     | root      |                           | funcs:count(Column#15)->Column#7 |
|   │ └─TableReader_94               | 1.00     | root      |                           | data:StreamAgg_82                |
|   │   └─StreamAgg_82               | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#15        |
|   │     └─Selection_92             | 20361.60 | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|   │       └─TableFullScan_91       | 25452.00 | cop[tikv] | table:t1, partition:p2019 | keep order:false                 |
|   └─StreamAgg_112                  | 1.00     | root      |                           | funcs:count(Column#17)->Column#7 |
|     └─TableReader_113              | 1.00     | root      |                           | data:StreamAgg_101               |
|       └─StreamAgg_101              | 1.00     | cop[tikv] |                           | funcs:count(1)->Column#17        |
|         └─Selection_111            | 8892.80  | cop[tikv] |                           | eq(year(test.t1.d), 2017)        |
|           └─TableFullScan_110      | 11116.00 | cop[tikv] | table:t1, partition:pmax  | keep order:false                 |
+------------------------------------+----------+-----------+---------------------------+----------------------------------+
27 rows in set (0.00 sec)
```

上記の出力から:

-   TiDB は、すべてのパーティションにアクセスする必要があると考えています`(p2016..pMax)` 。これは、述語`YEAR(d) = 2017`が[検索対象外](https://en.wikipedia.org/wiki/Sargable)とみなされるためです。この問題は TiDB に固有のものではありません。
-   各パーティションがスキャンされると、 `Selection`演算子によって 2017 年に一致しない行が除外されます。
-   各パーティションでストリーム集約が実行され、一致する行の数がカウントされます。
-   演算子`└─PartitionUnion_21`は、各パーティションへのアクセスの結果を結合します。
