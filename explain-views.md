---
title: EXPLAIN Statements Using Views
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# ビューを使用しEXPLAINステートメント {#explain-statements-using-views}

`EXPLAIN`は、ビュー自体の名前ではなく、 [見る](/views.md)が参照するテーブルとインデックスを表示します。これは、ビューが単なる仮想テーブルであり、データ自体を格納しないためです。ビューの定義とステートメントの残りの部分は、SQLの最適化中に一緒にマージされます。

[バイクシェアサンプルデータベース](/import-example-data.md)から、次の2つのクエリが同様の方法で実行されていることがわかります。

{{< copyable "" >}}

```sql
ALTER TABLE trips ADD INDEX (duration);
CREATE OR REPLACE VIEW long_trips AS SELECT * FROM trips WHERE duration > 3600;
EXPLAIN SELECT * FROM long_trips;
EXPLAIN SELECT * FROM trips WHERE duration > 3600;
```

```sql
Query OK, 0 rows affected (2 min 10.11 sec)

Query OK, 0 rows affected (0.13 sec)

+--------------------------------+------------+-----------+---------------------------------------+-------------------------------------+
| id                             | estRows    | task      | access object                         | operator info                       |
+--------------------------------+------------+-----------+---------------------------------------+-------------------------------------+
| IndexLookUp_12                 | 6372547.67 | root      |                                       |                                     |
| ├─IndexRangeScan_10(Build)     | 6372547.67 | cop[tikv] | table:trips, index:duration(duration) | range:(3600,+inf], keep order:false |
| └─TableRowIDScan_11(Probe)     | 6372547.67 | cop[tikv] | table:trips                           | keep order:false                    |
+--------------------------------+------------+-----------+---------------------------------------+-------------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+-----------+-----------+---------------------------------------+-------------------------------------+
| id                            | estRows   | task      | access object                         | operator info                       |
+-------------------------------+-----------+-----------+---------------------------------------+-------------------------------------+
| IndexLookUp_10                | 833219.37 | root      |                                       |                                     |
| ├─IndexRangeScan_8(Build)     | 833219.37 | cop[tikv] | table:trips, index:duration(duration) | range:(3600,+inf], keep order:false |
| └─TableRowIDScan_9(Probe)     | 833219.37 | cop[tikv] | table:trips                           | keep order:false                    |
+-------------------------------+-----------+-----------+---------------------------------------+-------------------------------------+
3 rows in set (0.00 sec)
```

同様に、ビューの述語はベーステーブルにプッシュダウンされます。

{{< copyable "" >}}

```sql
EXPLAIN SELECT * FROM long_trips WHERE bike_number = 'W00950';
EXPLAIN SELECT * FROM trips WHERE bike_number = 'W00950';
```

```sql
+--------------------------------+---------+-----------+---------------------------------------+---------------------------------------------------+
| id                             | estRows | task      | access object                         | operator info                                     |
+--------------------------------+---------+-----------+---------------------------------------+---------------------------------------------------+
| IndexLookUp_14                 | 3.33    | root      |                                       |                                                   |
| ├─IndexRangeScan_11(Build)     | 3333.33 | cop[tikv] | table:trips, index:duration(duration) | range:(3600,+inf], keep order:false, stats:pseudo |
| └─Selection_13(Probe)          | 3.33    | cop[tikv] |                                       | eq(bikeshare.trips.bike_number, "W00950")         |
|   └─TableRowIDScan_12          | 3333.33 | cop[tikv] | table:trips                           | keep order:false, stats:pseudo                    |
+--------------------------------+---------+-----------+---------------------------------------+---------------------------------------------------+
4 rows in set (0.00 sec)

+-------------------------+-------------+-----------+---------------+-------------------------------------------+
| id                      | estRows     | task      | access object | operator info                             |
+-------------------------+-------------+-----------+---------------+-------------------------------------------+
| TableReader_7           | 43.00       | root      |               | data:Selection_6                          |
| └─Selection_6           | 43.00       | cop[tikv] |               | eq(bikeshare.trips.bike_number, "W00950") |
|   └─TableFullScan_5     | 19117643.00 | cop[tikv] | table:trips   | keep order:false                          |
+-------------------------+-------------+-----------+---------------+-------------------------------------------+
3 rows in set (0.00 sec)
```

上記の最初のステートメントでは、インデックスがビュー定義を満たすために使用され、TiDBがテーブル行を読み取るときに`bike_number = 'W00950'`が適用されることがわかります。 2番目のステートメントでは、ステートメントを満たすためのインデックスがなく、 `TableFullScan`が使用されています。

TiDBは、ビュー定義とステートメント自体の両方を満たすインデックスを利用します。次の複合インデックスについて考えてみます。

{{< copyable "" >}}

```sql
ALTER TABLE trips ADD INDEX (bike_number, duration);
EXPLAIN SELECT * FROM long_trips WHERE bike_number = 'W00950';
EXPLAIN SELECT * FROM trips WHERE bike_number = 'W00950';
```

```sql
Query OK, 0 rows affected (2 min 31.20 sec)

+--------------------------------+----------+-----------+-------------------------------------------------------+-------------------------------------------------------+
| id                             | estRows  | task      | access object                                         | operator info                                         |
+--------------------------------+----------+-----------+-------------------------------------------------------+-------------------------------------------------------+
| IndexLookUp_13                 | 63725.48 | root      |                                                       |                                                       |
| ├─IndexRangeScan_11(Build)     | 63725.48 | cop[tikv] | table:trips, index:bike_number(bike_number, duration) | range:("W00950" 3600,"W00950" +inf], keep order:false |
| └─TableRowIDScan_12(Probe)     | 63725.48 | cop[tikv] | table:trips                                           | keep order:false                                      |
+--------------------------------+----------+-----------+-------------------------------------------------------+-------------------------------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+----------+-----------+-------------------------------------------------------+---------------------------------------------+
| id                            | estRows  | task      | access object                                         | operator info                               |
+-------------------------------+----------+-----------+-------------------------------------------------------+---------------------------------------------+
| IndexLookUp_10                | 19117.64 | root      |                                                       |                                             |
| ├─IndexRangeScan_8(Build)     | 19117.64 | cop[tikv] | table:trips, index:bike_number(bike_number, duration) | range:["W00950","W00950"], keep order:false |
| └─TableRowIDScan_9(Probe)     | 19117.64 | cop[tikv] | table:trips                                           | keep order:false                            |
+-------------------------------+----------+-----------+-------------------------------------------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

最初のステートメントでは、TiDBは複合インデックス`(bike_number, duration)`の両方の部分を使用できます。 2番目のステートメントでは、インデックス`(bike_number, duration)`の`bike_number`である最初の部分のみが使用されます。
