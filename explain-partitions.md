---
title: Partitions
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Partitions

`EXPLAIN` will display the partitions that TiDB needs to access in order to execute a query. Because of [partition pruning](/partition-pruning.md), this will often only be a subset of the partitions.

Because TiDB currently requires tables to be created with partitions already defined, the following SQL is used to create a new partitioned table with a subset of the rows from the [bikeshare example database](/import-example-data.md):

```sql
DROP TABLE IF EXISTS trips_partitioned;
CREATE TABLE `trips_partitioned` (
  `duration` int(11) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `start_station_number` int(11) DEFAULT NULL,
  `start_station` varchar(255) DEFAULT NULL,
  `end_station_number` int(11) DEFAULT NULL,
  `end_station` varchar(255) DEFAULT NULL,
  `bike_number` varchar(255) DEFAULT NULL,
  `member_type` varchar(255) DEFAULT NULL
)
PARTITION BY RANGE ( YEAR(start_date) ) (
 PARTITION p2010 VALUES LESS THAN (2011),
 PARTITION p2011 VALUES LESS THAN (2012),
 PARTITION p2012 VALUES LESS THAN (2013),
 PARTITION p2013 VALUES LESS THAN (2014),
 PARTITION p2014 VALUES LESS THAN (2015),
 PARTITION p2015 VALUES LESS THAN (2016),
 PARTITION p2016 VALUES LESS THAN (2017),
 PARTITION p2017 VALUES LESS THAN (2018),
 PARTITION p2018 VALUES LESS THAN (2019),
 PARTITION p2019 VALUES LESS THAN (2020),
 PARTITION pmax VALUES LESS THAN MAXVALUE
);

-- sample 0.01% of rows for simplicity
INSERT INTO trips_partitioned SELECT duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type FROM trips WHERE trip_id % 10000 = 1;

SELECT SLEEP(1);
ANALYZE TABLE trips_partitioned;
```

The following example shows a statement against our newly created partitioned table:

```sql
EXPLAIN SELECT COUNT(*) FROM trips_partitioned WHERE start_date = '2017-06-01';
```

```sql
+------------------------------+----------+-----------+-------------------------+------------------------------------------------------------------------+
| id                           | estRows  | task      | access object           | operator info                                                          |
+------------------------------+----------+-----------+-------------------------+------------------------------------------------------------------------+
| StreamAgg_20                 | 1.00     | root      |                         | funcs:count(Column#13)->Column#11                                      |
| └─TableReader_21             | 1.00     | root      | partition:p2017         | data:StreamAgg_9                                                       |
|   └─StreamAgg_9              | 1.00     | cop[tikv] |                         | funcs:count(1)->Column#13                                              |
|     └─Selection_19           | 10.00    | cop[tikv] |                         | eq(bikeshare.trips_partitioned.start_date, 2017-06-01 00:00:00.000000) |
|       └─TableFullScan_18     | 10000.00 | cop[tikv] | table:trips_partitioned | keep order:false, stats:pseudo                                         |
+------------------------------+----------+-----------+-------------------------+------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

Starting from the child operators and working backwards, the output shows that:

* TiDB successfully identified that only one partition (`p2017`) needed to be accessed. This is noted under `access object`.
* The partition itself was scanned in the operator `└─TableFullScan_18` and then `└─Selection_19` was applied to filter for rows that have a start date of `2017-06-01 00:00:00.000000`.
* The rows that match `└─Selection_19` are then stream aggregated in the coprocessor, which natively understands the `count` function.
* Each coprocessor request then sends back one row to  `└─TableReader_21` inside TiDB, which is then stream aggregated under `StreamAgg_20` and one row is returned to the client.


The following naive example shows partition pruning has not applied:

```sql
EXPLAIN SELECT COUNT(*) FROM trips_partitioned WHERE YEAR(start_date) = 2017;
```

```sql
+------------------------------+----------+-----------+-------------------------+--------------------------------------------------------+
| id                           | estRows  | task      | access object           | operator info                                          |
+------------------------------+----------+-----------+-------------------------+--------------------------------------------------------+
| StreamAgg_20                 | 1.00     | root      |                         | funcs:count(Column#13)->Column#11                      |
| └─TableReader_21             | 1.00     | root      | partition:all           | data:StreamAgg_9                                       |
|   └─StreamAgg_9              | 1.00     | cop[tikv] |                         | funcs:count(1)->Column#13                              |
|     └─Selection_19           | 8000.00  | cop[tikv] |                         | eq(year(bikeshare.trips_partitioned.start_date), 2017) |
|       └─TableFullScan_18     | 10000.00 | cop[tikv] | table:trips_partitioned | keep order:false, stats:pseudo                         |
+------------------------------+----------+-----------+-------------------------+--------------------------------------------------------+
5 rows in set (0.00 sec)
```

From the output above:

* The access object is `partition: all`, noting that all partitions need to be accessed.
* TiDB believes that it needs to apply the function `year` on each of the rows to see if they match the criteria (`└─Selection_19`).

The predicate `YEAR(start_date) = 2017` is considered [non-sargable](https://en.wikipedia.org/wiki/Sargable). Similar to MySQL (and other databases), TiDB requires the query to be written in the following form:

```sql
EXPLAIN SELECT COUNT(*) FROM trips_partitioned WHERE start_date >= '2017-01-01' AND start_date < '2018-01-01';
```




`
The following example shows partition pruning apply, and only the partition `p2017` needs to be accessed (see `access object`):


In the above example, we can see that 



SELECT COUNT(*) FROM trips_partitioned PARTITION (p2017);



mysql> EXPLAIN SELECT COUNT(*) FROM trips_partitioned WHERE bike_number = 'W20761';
+------------------------------+----------+-----------+-------------------------+-------------------------------------------------------+
| id                           | estRows  | task      | access object           | operator info                                         |
+------------------------------+----------+-----------+-------------------------+-------------------------------------------------------+
| StreamAgg_20                 | 1.00     | root      |                         | funcs:count(Column#13)->Column#11                     |
| └─TableReader_21             | 1.00     | root      | partition:all           | data:StreamAgg_9                                      |
|   └─StreamAgg_9              | 1.00     | cop[tikv] |                         | funcs:count(1)->Column#13                             |
|     └─Selection_19           | 10.00    | cop[tikv] |                         | eq(bikeshare.trips_partitioned.bike_number, "W20761") |
|       └─TableFullScan_18     | 10000.00 | cop[tikv] | table:trips_partitioned | keep order:false, stats:pseudo                        |
+------------------------------+----------+-----------+-------------------------+-------------------------------------------------------+
5 rows in set (0.00 sec)
```

Currently partition pruning only applies to fixed conditions. i.e. in the following example, the range on start_date prevents pruning from being used:

```sql
mysql> EXPLAIN SELECT COUNT(*) FROM trips_partitioned WHERE bike_number = 'W20761' and start_date > '2017-03-01';
+------------------------------+----------+-----------+-------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object           | operator info                                                                                                                 |
+------------------------------+----------+-----------+-------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20                 | 1.00     | root      |                         | funcs:count(Column#13)->Column#11                                                                                             |
| └─TableReader_21             | 1.00     | root      | partition:all           | data:StreamAgg_9                                                                                                              |
|   └─StreamAgg_9              | 1.00     | cop[tikv] |                         | funcs:count(1)->Column#13                                                                                                     |
|     └─Selection_19           | 3.33     | cop[tikv] |                         | eq(bikeshare.trips_partitioned.bike_number, "W20761"), gt(bikeshare.trips_partitioned.start_date, 2017-03-01 00:00:00.000000) |
|       └─TableFullScan_18     | 10000.00 | cop[tikv] | table:trips_partitioned | keep order:false, stats:pseudo                                                                                                |
+------------------------------+----------+-----------+-------------------------+-------------------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```