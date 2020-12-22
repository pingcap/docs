---
title: Clustered Indexes
summary: Learn how Clustered Indexes apply to TiDB.
---

# Clustered Indexes

> **Warning:**
>
> Clustered Indexes is an experimental feature introduced in TiDB 5.0.

Clustered Indexes provide the ability to organize tables in a way that can improve the performance of certain queries. The term _clustered_ in this context refers to the _organization of how data is stored_ and not _a group of database servers working together_. Some database management systems may also refer to clustered indexes as _index-organized tables_ (IOT).

TiDB only supports clustering by a table's `PRIMARY KEY`. With clustered indexes enabled, the terms _the_ `PRIMARY KEY` and _the clustered index_ might be used interchangeably.

## Default Behavior

TiDB has always supported clustered indexes, provided the following criteria are true:

- The table contains a `PRIMARY KEY`
- The primary key is an `INTEGER` or `BIGINT`
- The primary key consists of only one column

When any of these criteria are not met, TiDB will create a hidden 64-bit `handle` to organize the table. Querying table rows by a clustered index is more efficient than by a non-clustered index because it can be completed as a single step. The following `EXPLAIN` output compares a table that supports clustered indexes with one that does not:

```sql
CREATE TABLE always_clusters_in_all_versions (
 id BIGINT NOT NULL PRIMARY KEY auto_increment,
 b CHAR(100),
 INDEX(b)
);

CREATE TABLE does_not_cluster_by_default (
 guid CHAR(32) NOT NULL PRIMARY KEY,
 b CHAR(100),
 INDEX(b)
);

INSERT INTO always_clusters_in_all_versions VALUES (1, 'aaa'), (2, 'bbb');
INSERT INTO does_not_cluster_by_default VALUES ('02dd050a978756da0aff6b1d1d7c8aef', 'aaa'), ('35bfbc09cb3c93d8ef032642521ac042', 'bbb');

EXPLAIN SELECT * FROM always_clusters_in_all_versions WHERE id = 1;
EXPLAIN SELECT * FROM does_not_cluster_by_default WHERE guid = '02dd050a978756da0aff6b1d1d7c8aef';
```

```sql
Query OK, 0 rows affected (0.09 sec)

Query OK, 0 rows affected (0.10 sec)

Records: 2  Duplicates: 0  Warnings: 0

Records: 2  Duplicates: 0  Warnings: 0

+-------------+---------+------+---------------------------------------+---------------+
| id          | estRows | task | access object                         | operator info |
+-------------+---------+------+---------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:always_clusters_in_all_versions | handle:1      |
+-------------+---------+------+---------------------------------------+---------------+
1 row in set (0.00 sec)

+-------------+---------+------+--------------------------------------------------------+---------------+
| id          | estRows | task | access object                                          | operator info |
+-------------+---------+------+--------------------------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:does_not_cluster_by_default, index:PRIMARY(guid) |               |
+-------------+---------+------+--------------------------------------------------------+---------------+
1 row in set (0.00 sec)
```

The `EXPLAIN` results look similar, but in the second example TiDB must first read the `PRIMARY KEY` index on `guid` in order to find the `handle` value. This is more obvious in the following example where the value of the `PRIMARY KEY` is not in the index on `does_not_cluster_by_default.b`. An extra lookup must be performed on the table rows (`└─TableFullScan_5`) to convert the `handle` to the `PRIMARY KEY` value of `guid`:

```sql
EXPLAIN SELECT id FROM always_clusters_in_all_versions WHERE b = 'aaaa';
EXPLAIN SELECT guid FROM does_not_cluster_by_default WHERE b = 'aaaa';
```

```sql
+--------------------------+---------+-----------+---------------------------------------------------+-------------------------------------------------------+
| id                       | estRows | task      | access object                                     | operator info                                         |
+--------------------------+---------+-----------+---------------------------------------------------+-------------------------------------------------------+
| Projection_4             | 0.00    | root      |                                                   | test.always_clusters_in_all_versions.id               |
| └─IndexReader_6          | 0.00    | root      |                                                   | index:IndexRangeScan_5                                |
|   └─IndexRangeScan_5     | 0.00    | cop[tikv] | table:always_clusters_in_all_versions, index:b(b) | range:["aaaa","aaaa"], keep order:false, stats:pseudo |
+--------------------------+---------+-----------+---------------------------------------------------+-------------------------------------------------------+
3 rows in set (0.01 sec)

+---------------------------+---------+-----------+-----------------------------------+------------------------------------------------+
| id                        | estRows | task      | access object                     | operator info                                  |
+---------------------------+---------+-----------+-----------------------------------+------------------------------------------------+
| Projection_4              | 0.00    | root      |                                   | test.does_not_cluster_by_default.guid          |
| └─TableReader_7           | 0.00    | root      |                                   | data:Selection_6                               |
|   └─Selection_6           | 0.00    | cop[tikv] |                                   | eq(test.does_not_cluster_by_default.b, "aaaa") |
|     └─TableFullScan_5     | 2.00    | cop[tikv] | table:does_not_cluster_by_default | keep order:false, stats:pseudo                 |
+---------------------------+---------+-----------+-----------------------------------+------------------------------------------------+
4 rows in set (0.00 sec)
```

# Clustered Indexes

New to TiDB 5.0, clustering is permitted by any `PRIMARY KEY`. The following `EXPLAIN` output shows the previous example with clustered indexes now enabled:

```sql
SET tidb_enable_clustered_index = 1;
CREATE TABLE will_now_cluster (
 guid CHAR(32) NOT NULL PRIMARY KEY,
 b CHAR(100),
 INDEX(b)
);

INSERT INTO will_now_cluster VALUES (1, 'aaa'), (2, 'bbb');
INSERT INTO will_now_cluster VALUES ('02dd050a978756da0aff6b1d1d7c8aef', 'aaa'), ('35bfbc09cb3c93d8ef032642521ac042', 'bbb');

EXPLAIN SELECT * FROM will_now_cluster WHERE guid = '02dd050a978756da0aff6b1d1d7c8aef';
EXPLAIN SELECT guid FROM will_now_cluster WHERE b = 'aaaa';
```

```sql
Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.11 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------+---------+------+-------------------------------------------------------+---------------+
| id          | estRows | task | access object                                         | operator info |
+-------------+---------+------+-------------------------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:will_now_cluster, clustered index:PRIMARY(guid) |               |
+-------------+---------+------+-------------------------------------------------------+---------------+
1 row in set (0.00 sec)

+--------------------------+---------+-----------+------------------------------------+-------------------------------------------------------+
| id                       | estRows | task      | access object                      | operator info                                         |
+--------------------------+---------+-----------+------------------------------------+-------------------------------------------------------+
| Projection_4             | 10.00   | root      |                                    | test.will_now_cluster.guid                            |
| └─IndexReader_6          | 10.00   | root      |                                    | index:IndexRangeScan_5                                |
|   └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:will_now_cluster, index:b(b) | range:["aaaa","aaaa"], keep order:false, stats:pseudo |
+--------------------------+---------+-----------+------------------------------------+-------------------------------------------------------+
3 rows in set (0.00 sec)
```

Clustering by a composite `PRIMARY KEY` is also supported:

```sql
SET tidb_enable_clustered_index = 1;
CREATE TABLE composite_primary_key (
 key_a INT NOT NULL,
 key_b INT NOT NULL,
 b CHAR(100),
 PRIMARY KEY (key_a, key_b)
);

INSERT INTO composite_primary_key VALUES (1, 1, 'aaa'), (2, 2, 'bbb');
EXPLAIN SELECT * FROM composite_primary_key WHERE key_a = 1 AND key_b = 2;
```

```sql
Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.09 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------+---------+------+--------------------------------------------------------------------+---------------+
| id          | estRows | task | access object                                                      | operator info |
+-------------+---------+------+--------------------------------------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:composite_primary_key, clustered index:PRIMARY(key_a, key_b) |               |
+-------------+---------+------+--------------------------------------------------------------------+---------------+
1 row in set (0.00 sec)
```

This behavior is consistent with MySQL, where the InnoDB storage engine will by default cluster by any `PRIMARY KEY`.

## Storage Considerations

Because the `PRIMARY KEY` replaces a 64-bit `handle` as the internal pointer to table rows, using clustered indexes might increase storage requirements. This is particularly impactful on tables that contain many secondary indexes. Consider the following example:

```sql
CREATE TABLE t1 (
 guid CHAR(32) NOT NULL PRIMARY KEY,
 b BIGINT,
 INDEX(b)
);
```

Since the pointer to the `guid` is a `char(32)`, each index value for `b` will now require approximately `8 + 32 = 40 bytes` (a `BIGINT` value requires 8 bytes for storage). This compares to `8 + 8 = 16 bytes` for non-clustered tables. The exact storage requirements will differ after compression has been applied.