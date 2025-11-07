---
title: Global Indexes
summary: Introduce the use cases, advantages, usage, working principles, and limitations of TiDB global indexes.
---

# Global Indexes

Before the introduction of global indexes, TiDB created a local index for each partition, leading to [a limitation](/partitioned-table.md#partitioning-keys-primary-keys-and-unique-keys) that primary keys and unique keys had to include the partition key to ensure data uniqueness. Additionally, when querying data across multiple partitions, TiDB needed to scan the data of each partition to return results.

To address these issues, TiDB introduces the global indexes feature in [v8.3.0](https://docs.pingcap.com/tidb/stable/release-8.3.0). A global index covers the data of the entire table with a single index, allowing primary keys and unique keys to maintain global uniqueness without including all partition keys. Moreover, global indexes can access index data across multiple partitions in a single operation instead of looking up the local index for each partition, significantly improving query performance for non-partitioning keys. <!--Starting from v9.0.0, non-unique indexes can also be created as global indexes.-->

## Advantages

Global indexes significantly improve query performance, enhance indexing flexibility, and reduce the cost of data migration and  modifying applications.

### Improved query performance

Global indexes greatly enhance the efficiency of queries involving non-partitioning columns. When a query involves a non-partitioning column, a global index can quickly locate the relevant data, avoiding full table scans across all partitions. This dramatically reduces the number of Coprocessor (cop) tasks, which is especially beneficial in scenarios with a large number of partitions.

In benchmark tests using sysbench `select_random_points`, performance improves by up to 53 times when the table contains 100 partitions.

### Enhanced indexing flexibility

Global indexes remove the restriction that unique keys in partitioned tables must include all partitioning columns. This provides greater flexibility in index design. You can now create indexes based on actual query patterns and business logic, rather than being constrained by the partitioning scheme. This flexibility not only improves query performance but also supports a wider range of application requirements.

### Reduced cost for data migration and modifying applications

Global indexes significantly simplify adjustments for data migration and modifying application. Without global indexes, you might need to modify partitioning schemes or rewrite queries to work around indexing limitations. With global indexes, such changes are unnecessary, reducing both development and maintenance overhead.
Global indexes significantly simplify adjustments for data migration and modifying applications. Without global indexes, you might need to modify partitioning schemes or rewrite queries to work around indexing limitations. With global indexes, such changes are unnecessary, reducing both development and maintenance overhead.
For example, when migrating a table from an Oracle database to TiDB, because Oracle supports global indexes, some tables might contain unique indexes that do not include partitioning columns. Before TiDB introduced global indexes, you had to modify the table schema to comply with TiDB's partitioning rules. Now, TiDB supports global indexes, you can simply define those indexes as global during migration, keeping schema behavior consistent with Oracle and greatly reducing migration costs.

## Limitations of global indexes

- If the `GLOBAL` keyword is not explicitly specified in the index definition, TiDB creates a local index by default.
- The `GLOBAL` and `LOCAL` keywords only apply to partitioned tables and do not affect non-partitioned tables. In other words, there is no difference between a global index and a local index in non-partitioned tables.
- DDL operations such as `DROP PARTITION`, `TRUNCATE PARTITION`, and `REORGANIZE PARTITION` also trigger updates to global indexes. These DDL operations need to wait for the global index updates to complete before returning results, which increases the execution time accordingly. This is particularly evident in data archiving scenarios, such as `DROP PARTITION` and `TRUNCATE PARTITION`. Without global indexes, these operations can typically complete immediately. However, with global indexes, the execution time increases as the number of indexes that need to be updated grows.
- Tables that contain global indexes do not support the `EXCHANGE PARTITION` operation.
- By default, the primary key of a partitioned table is a clustered index and must include the partition key. If you require the primary key to exclude the partition key, you can explicitly specify the primary key as a non-clustered global index when creating the table, for example, `PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`.
- If a global index is added to an expression column, or a global index is also a prefix index (for example `UNIQUE KEY idx_id_prefix (id(10)) GLOBAL`), you need to collect statistics manually for this global index.

## Feature evolution

- **Before v7.6.0**: TiDB only supports local indexes on partitioned tables. This means that unique keys on partitioned tables have to include all columns in the partition expression. Queries that do not use the partition key have to scan all partitions, resulting in degraded query performance.
- **[v7.6.0](https://docs.pingcap.com/tidb/stable/release-7.6.0)**: Introduces the [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new--in-v760) system variable to enable global indexes. However, at that time the feature is still under development and is not recommended for production use.
- **[v8.3.0](https://docs.pingcap.com/tidb/stable/release-8.3.0)**: Global indexes are released as an experimental feature. You can explicitly create a global index using the `GLOBAL` keyword when defining an index.
- **[v8.4.0](https://docs.pingcap.com/tidb/stable/release-8.4.0)**: The global indexes feature becomes generally available (GA). You can create global indexes directly using the `GLOBAL` keyword without setting the `tidb_enable_global_index` system variable. From this version onward, the system variable is deprecated and fixed to `ON`, meaning global indexes are enabled by default.
- **[v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0)**: Global indexes support including all columns from the partition expression.<!-- - **v9.0.0**: Global indexes support non-unique indexes. In partitioned tables, any index except clustered indexes can be created as a global index. -->

## Global indexes vs. local indexes

The following diagram shows the differences between global indexes and local indexes.

<img src="https://github.com/hfxsd/docs/blob/global-index-best-practices/media/global-index-vs-local-index.png" alt="Global Index vs. Local Index" width="60%" height="60%"/>

**Scenarios for global indexes**:

- **Infrequent data archiving**: For example, in the healthcare industry, some business data must be retained for up to 30 years. Data is often partitioned monthly, creating as many as 360 partitions at once, with very few `DROP` or `TRUNCATE` operations. In such scenarios, global indexes are more suitable, providing cross-partition consistency and improved query performance.
- **Queries that require cross-partition data**: When queries need to access data across multiple partitions, global indexes can avoid full scans across all partitions and enhance query efficiency.

**Scenarios for local indexes**:

- **Frequent data archiving**: If data archiving operations are frequent and queries are mostly confined to a single partition, local indexes can offer better performance.
- **Partition exchange requirements**: In industries like banking, processed data might first be written to a regular table and, after verification, exchanged into a partitioned table to minimize performance impact. In this case, local indexes are preferred, because enabling global indexes disables the partition exchange functionality on the table.

## Global indexes vs. clustered indexes

Due to the underlying principles of clustered indexes and global indexes, a single index cannot serve as both a clustered index and a global index. However, these two types of indexes provide different performance optimizations for different query scenarios. When you need to leverage the benefits of both, you can add the partitioning columns to the clustered index while also creating a global index that does not include the partitioning columns.

Suppose you have the following table structure:

```sql
CREATE TABLE `t` (
  `id` int DEFAULT NULL,
  `ts` timestamp NULL DEFAULT NULL,
  `data` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800)
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

In the preceding `t` table, the values in the `id` column are unique. To optimize both point queries and range queries, you can define a clustered index in the table creation statement as `PRIMARY KEY(id, ts)` and a global index without the partitioning column as `UNIQUE KEY id(id)`. This way, point queries based on `id` will use the global index `id` and choose a `PointGet` execution plan, while range queries will use the clustered index. The clustered index requires one less table lookup compared to the global index, improving query efficiency.

The modified table structure is as follows:

```sql
CREATE TABLE `t` (
  `id` int NOT NULL,
  `ts` timestamp NOT NULL,
  `data` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`, `ts`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `id` (`id`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800),
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

This approach optimizes point queries based on `id` while improving the performance of range queries, and also ensures that the table's partitioning columns are effectively utilized in timestamp-based queries.

## Usage

To create a global index, add the `GLOBAL` keyword in the index definition.

> **Note:**
>
> Global indexes affect partition management. Executing `DROP`, `TRUNCATE`, or `REORGANIZE PARTITION` operations will trigger updates to the table-level global indexes. This means that these DDL operations only return after the corresponding global index updates are completed, which might increase execution time.

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2) GLOBAL,
    UNIQUE KEY uidx3(col3),
    KEY idx1(col1) GLOBAL
)
PARTITION BY HASH(col3)
PARTITIONS 4;
```

In the preceding example, the unique index `uidx12` and the non-unique index `idx1` become global indexes, while `uidx3` remains a regular unique index.

Note that a clustered index cannot be a global index. For example:

```sql
CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    PRIMARY KEY (col2) CLUSTERED GLOBAL
) PARTITION BY HASH(col1) PARTITIONS 5;
```

```
ERROR 1503 (HY000): A CLUSTERED INDEX must include all columns in the table's partitioning function
```

A clustered index cannot simultaneously serve as a global index. This is because if a clustered index were global, the table would no longer be partitioned. The keys of a clustered index are at the partition level, while global indexes operate at the table level, creating a conflict. If you need to set the primary key as a global index, you must explicitly define it as a non-clustered index, for example: 

```sql
PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL
```

You can identify global indexes by the `GLOBAL` option in the output of [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md):

```sql
SHOW CREATE TABLE t1\G
```

```
       Table: t1
Create Table: CREATE TABLE `t1` (
  `col1` int NOT NULL,
  `col2` date NOT NULL,
  `col3` int NOT NULL,
  `col4` int NOT NULL,
  UNIQUE KEY `uidx12` (`col1`,`col2`) /*T![global_index] GLOBAL */,
  UNIQUE KEY `uidx3` (`col3`),
  KEY `idx1` (`col1`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY HASH (`col3`) PARTITIONS 4
1 row in set (0.00 sec)
```

Alternatively, you can query the [`INFORMATION_SCHEMA.TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md) table and check the `IS_GLOBAL` column in the output to identify global indexes.

```sql
SELECT * FROM information_schema.tidb_indexes WHERE table_name='t1';
```

```
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| TABLE_SCHEMA | TABLE_NAME | NON_UNIQUE | KEY_NAME | SEQ_IN_INDEX | COLUMN_NAME | SUB_PART | INDEX_COMMENT | Expression | INDEX_ID | IS_VISIBLE | CLUSTERED | IS_GLOBAL |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| test         | t1         |          0 | uidx12   |            1 | col1        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx12   |            2 | col2        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx3    |            1 | col3        |     NULL |               | NULL       |        2 | YES        | NO        |         0 |
| test         | t1         |          1 | idx1     |            1 | col1        |     NULL |               | NULL       |        3 | YES        | NO        |         1 |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
3 rows in set (0.00 sec)
```

When partitioning a regular table or repartitioning a partitioned table, you can update indexes to be either global indexes or local indexes as needed.

For example, the following SQL statement repartitions table `t1` based on column `col1` and updates the global indexes `uidx12` and `idx1` to local indexes, while updating the local index `uidx3` to a global index. `uidx3` is a unique index on column `col3`. To ensure the uniqueness of `col3` across all partitions, `uidx3` must be a global index. `uidx12` and `idx1` are indexes on column `col1` and can be either global or local indexes.

```sql
ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL, idx1 LOCAL);
```

## Working mechanism

This section explains the working mechanism of global indexes, including their design concept and implementation.

### Design concept

In TiDB partitioned tables, the key prefix of a local index is the partition ID, while the key prefix of a global index is the table ID. This design ensures that the data of a global index is stored continuously on TiKV, reducing the number of RPC requests when querying the index.

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  KEY idx(k),
  KEY global_idx(k) GLOBAL
) partition by hash(id) partitions 5;
```

Take the preceding table structure as an example: `idx` is a local index, and `global_idx` is a global index. The data of `idx` is distributed across 5 different ranges, such as `PartitionID1_i_xxx` and `PartitionID2_i_xxx`. Whereas the data of `global_idx` is concentrated in a single range (`TableID_i_xxx`).

When executing a query related to `k`, such as `SELECT * FROM sbtest WHERE k > 1`, using the local index `idx` results in 5 separate ranges being constructed, while using the global index `global_idx` only constructs a single range. Each range corresponds to one or more RPC requests in TiDB. Therefore, using a global index can reduce the number of RPC requests by several times, improving index query performance.

The following diagram illustrates the difference in RPC requests and data flow when executing `SELECT * FROM sbtest WHERE k > 1` using `idx` versus `global_idx`:

![Mechanism of Global Indexes](/media/global-index-mechanism.png)

### Encoding method

In TiDB, index entries are encoded as key-value pairs. For partitioned tables, each partition is treated as an independent physical table at the TiKV layer, with its own `partitionID`. Therefore, the encoding of index entries in a partitioned table is as follows:

```
Unique key
Key:
- PartitionID_indexID_ColumnValues

Value:
- IntHandle
 - TailLen_IntHandle

- CommonHandle
 - TailLen_IndexVersion_CommonHandle

Non-unique key
Key:
- PartitionID_indexID_ColumnValues_Handle

Value:
- IntHandle
 - TailLen_Padding

- CommonHandle
 - TailLen_IndexVersion
```

For global indexes, the encoding of index entries is different. To ensure compatibility with the current index key encoding, the new index encoding layout is as follows:

```
Unique key
Key:
- TableID_indexID_ColumnValues

Value:
- IntHandle
 - TailLen_PartitionID_IntHandle

- CommonHandle
 - TailLen_IndexVersion_CommonHandle_PartitionID

Non-unique key
Key:
- TableID_indexID_ColumnValues_Handle

Value:
- IntHandle
 - TailLen_PartitionID

- CommonHandle
 - TailLen_IndexVersion_PartitionID
```

This encoding scheme places the `TableID` at the beginning of the global index key, while the `PartitionID` is stored in the value. The advantage of this design is that it achieves compatibility with the existing index key encoding. However, it also introduces some challenges. For example, when executing DDL operations such as `DROP PARTITION` or `TRUNCATE PARTITION`, extra handling is required because the index entries are not stored contiguously.

## Performance test results

The following tests are based on the `select_random_points` scenario in sysbench, primarily used to compare query performance under different partitioning strategies and indexing methods.

The table structure used in the tests is as follows:

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `k_1` (`k`)
  /* Key `k_1` (`k`, `c`) GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
/* Partition by hash(`id`) partitions 100 */
/* Partition by range(`id`) xxxx */
```

The workload SQL is as follows:

```sql
SELECT id, k, c, pad
FROM sbtest
WHERE k IN (xx, xx, xx)
```

Range Partition (100 partitions):

| Table type                                                            | Concurrency 1 | Concurrency 32 | Concurrency 64 | Average RU |
| --------------------------------------------------------------------- | ------------- | -------------- | -------------- | ---------- |
| Clustered non-partitioned table                                       | 225           | 19,999         | 30,293         | 7.92       |
| Clustered table range partitioned by PK                               | 68            | 480            | 511            | 114.87     |
| Clustered table range partitioned by PK, with Global Index on `k`, `c` | 207           | 17,798         | 27,707         | 11.73      |

Hash Partition (100 partitions):

| Table type                                                           | Concurrency 1 | Concurrency 32 | Concurrency 64 | Average RU |
| -------------------------------------------------------------------- | ------------- | -------------- | -------------- | ---------- |
| Clustered non-partitioned table                                      | 166           | 20,361         | 28,922         | 7.86       |
| Clustered table hash partitioned by PK                               | 60            | 244            | 283            | 119.73     |
| Clustered table hash partitioned by PK, with Global Index on `k`, `c` | 156           | 18,233         | 15,581         | 10.77      |

From the preceding tests, it is evident that in high-concurrency environments, global indexes can significantly improve the query performance of partitioned tables, with performance gains of up to 50 times. Additionally, global indexes substantially reduce resource (RU) consumption. As the number of partitions increases, the performance benefits of global indexes become even more obvious.
