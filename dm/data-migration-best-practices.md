---
title: Data Migration (DM) Best Practices
summary: Learn about best practices when you use TiDB Data Migration (DM) to migrate data.
---

# Data Migration (DM) Best Practices

TiDB Data Migration (DM) is an data migration tool developed by PingCAP. It supports the full data migration and the incremental data replication from MySQL-compatible databases such as MySQL, Percona MySQL, MariaDB, AWS MySQL RDS, AWS Aurora into TiDB.

You can use DM in the following scenarios:

- Perform full and incremental data migration from a single MySQL-compatible database instance to TiDB
- Migrate and merge MySQL shards of small datasets to TiDB
- In the Data HUB scenario, such as the middle platform of business data, and real-time aggregation of business data, use DM as the middleware for data migration

This document introduces how to use DM in an elegant and efficient way, and how to avoid the common mistakes when using DM.

## Performance limitations

| Performance item  | Limitation |
| ----------------- | :--------: |
|  Max Work Nodes              |  1000           |
|  Max Task number             |  600            |
|  Max QPS                     |  30k QPS/worker |
|  Max Binlog throughput       |  20 MB/s/worker |
|  Table number limit per task | Unlimited       |

- DM supports managing 1000 work nodes simultaneously, and the maximum number of tasks is 600. To ensure the high availability of work nodes, you should reserve some work nodes as standby nodes. Reserve 20% to 50% of the number of the work nodes that have run migration task.
- A single work node can theoretically support replication QPS of up to 30K QPS/worker. It varies for different schemas and workloads. The ability to handle upstream binlog is up to 20 MB/s/worker.
- If you use DM as a data replication middleware that will be used for a long time, you need to carefully design the deployment architecture of DM components. For more information, see [Deploy DM-master and DM-worker](#deploy-dm-master-and-dm-worker)

## Before data migration

Before data migration, the design of the overall solution is critical. Especially the design of the scheme before migration is the most important part of the whole scheme. The following sections describe best practices and scenarios from the business side and the implementation side.

### Best practices for the business side

To distribute workloads evenly on multiple nodes, the schema design for the distributed database is very different from traditional databases. It is designed for both low migration cost and logic correctness after migration. The following sections describe best practices before data migration.

#### Business impact of AUTO_INCREMENT in Schema design

`AUTO_INCREMENT` in TiDB is compatible with `AUTO_INCREMENT` in MySQL. However, as a distributed database, TiDB usually has multiple computing nodes (entry on the client end). When the application data is written, the workload is evenly distributed. This leads to the result that when there is an `AUTO_INCREMENT` column in the table, the auto-increment ID may not be consecutive. For more details, see [AUTO_INCREMENT](/auto-increment.md#implementation-principles).

If your business has a strong dependence on the auto-increment ID, consider using the [SEQUENCE function](/sql-statements/sql-statement-create-sequence.md#sequence-function).

#### Usage of Clustered indexes

When you create a table, you can state that the primary key is either a clustered index or a non-clustered index. The following sections describe the pros and cons of each solution.

- Clustered indexes

    [Clustered indexes](/clustered-indexes.md) use the primary key as the handle ID (row ID) for data storage. Querying using the primary key can avoid table lookup, which effectively improves the query performance. However, if the table is write-intensive and the primary key uses [`AUTO_INCREMENT`](/auto-increment.md), it is very likely to cause the [write hotspot problem](/best-practices/high-concurrency-best-practices.md#highly-concurrent-write-intensive-scenario) of data storage, resulting in a mediocre performance of the cluster and the performance bottleneck of a single storage node.

- Non-clustered indexes + `shard row id bit`

    Using non-clustered indexes and `shard row id bit`, you can avoid the write hotspot problem when using `AUTO_INCREMENT`. However, table lookup in this scenario can affect the query performance when querying using the primary key.

- Clustered indexes + external distributed ID generators

    If you want to use clustered indexes and keep the IDs consecutive, consider using external distributed ID generators, such as Snowflake and Leaf. The application program generates sequence IDs, which can guarantee the IDs consecutive to a certain extent. It also retains the benefits of using clustered indexes. But you need to customize the related applications.

- Clustered indexes + `AUTO_RANDOM`

    This solution can retain the benefits of using clustered indexes and avoid the write hotspot problem. It requires less effort for customization. You can modify the schema attribute when you switch to use TiDB as the write database. In the subsequent queries, you can sort using the ID column. You can use the [`AUTO_RANDOM`](/auto-random.md) ID column to left shift 5 bits to ensure the order of the query data. For example:

    ```sql
    CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM, b varchar(255));
    Select  a, a<<5 ,b from t order by a <<5 desc
    ```

The following table summarizes the pros and cons of each solution.

| Scenario | Recommended solution | Pros | Cons |
| :--- | :--- | :--- | :--- |
| TIDB will act as the primary and write-intensive database. The business logic is strongly dependent on the continuity of the primary key IDs. | Create the table with non-clustered indexes and set `SHARD_ROW_ID_BIT`. Use `SEQUENCE` as the primary key column.  | It can avoid data writing hotspots and ensure the continuity and monotonic increment of business data. | The throughput capacity of data write is reduced (to ensure data write continuity). The performance of primary key queries is reduced. |
| TIDB will act as the primary and write-intensive database. The business logic is strongly dependent on the increment of the primary key IDs.  | Create the table with non-clustered indexes and set `SHARD_ROW_ID_BIT`. Use the application ID generator to define the primary key IDs. | It can avoid data writing hotspots, guarantees the performance of data write, guarantees the increment of business data, but cannot guarantees continuity. | Need code customization. External ID generators strongly depend on the clock accuracy and might introduce failure risks |
| **Recommended solution for data migration**<br/>TIDB will act as the primary and write-intensive database. The business logic does not depend on the continuity of the primary key IDs. | Create the table with clustered indexes and set `AUTO_RANDOM` for the primary key column. | It can avoid data writing hotspots. Limited write throughput ability. Excellent query performance of the primary keys. You can smoothly switch `AUTO_INCREMENT` to `AUTO_RANDOM`. | The primary key ID is random. It is recommended to sort the business data by using inserting the time column. If you have to use the primary key ID to sort data, you can left shift 5 bits to query, which can guarantee the increment of the data. |
| **Recommended solution for middle platforms**<br/>TIDB will act as the read-only database. | Create the table with non-clustered indexes and set `SHARD_ROW_ID_BIT`. Keep the primary key column consistent with the data source. | It can avoid data writing hotspots. Low customization cost. | The query performance of the primary keys is impacted. |

### Key points for MySQL shards

#### Splitting and merging

It is recommended that you use DM to [migrate and merge MySQL shards of small datasets to TiDB](/migrate-small-mysql-shards-to-tidb.md). The benefits are not described here.

This section only introduces the scenario of data archiving. Data is constantly being written. As time goes by, large amounts of data gradually change from hot data to warm or even cold data. Fortunately, in TiDB, you can use [placement rules](/configure-placement-rules.md) to set different placement rules for data. The minimum granularity is [partitioned tables](/partitioned-table.md).

Therefore, it is recommended that for write-intensive scenarios, you need to evaluate from the beginning whether you need to archive data and store hot and cold data on different media separately. If you need to archive data, you need to set the partition rules before migration (TiDB does not support Table Rebuild operations yet). This can save you from the need to create tables and import data in future.

#### The pessimistic mode and the optimistic mode

DM uses the pessimistic mode by default. In scenarios of migrating and merging MySQL shards, changes in upstream shard schemas can block DML writing to downstream databases. You need to wait for all the schemas to change and have the same structure, and then continue migration from the break point.

- If the upstream schema changes take a long time, it can cause the upstream Binlog to be cleaned up. You can enable the Relay log to avoid this problem.

- If you do not want to block data write due to upstream schema changes, consider using the optimistic mode. In this case, DM will not block the data migration even when it spots changes in the upstream shard schemas, but will continue to migrate the data. However, if incompatible formats are spotted in upstream and downstream, the migration task will stop. You need to resolve this issue manually.

The following table summarizes the pros and cons of optimistic mode and pessimistic mode.

| Scenario | Pros | Cons |
| :--- | :--- | :--- |
| Optimistic mode (Default) | It can ensure that the data migrated to the downstream will not go wrong.  | If there are a large number of shards, the migration task will be blocked for a long time, or even stopped if the upstream Binlogs have been cleaned up. You can enable the Relay log to avoid this problem. For more limitations, see [Use Relay log](#use-relay-log). |
| Pessimistic mode| Data can not be blocked during migration. | In this mode, ensure that schema changes are compatible (whether the incremental column has a default value). It is possible that inconsistent data can be overlooked. For more limitations, see [Merge and Migrate Data from Sharded Tables in Optimistic Mode](/dm/feature-shard-merge-optimistic.md#restrictions).|

### Other restrictions and impact

#### Data types in upstream and downstream

TiDB supports most MySQL data types. However, some special types are not supported yet (such as `SPATIAL`). For the compatibility of data types, see [Data Types](/data-type-overview.md).

#### Character sets and collations

If you want TiDB to support utf8_general_ci, utf8mb4_general_ci, utf8_unicode_ci, utf8mb4_unicode_ci, gbk_chinese_ci and gbk_bin, you need explicitly state it when creating the cluster by setting the value of `new_collations_enabled_on_first_bootstrap` to `true`. For more information, see [New framework for collations](/character-set-and-collation.md#new-framework-for-collations)

The default character set in TiDB is utf8mb4. It is recommended that you use utf8mb4 for the upstream and downstream databases and applications. If the upstream database has explicitly specified a character set or collation, you need to check whether TiDB supports it. Since TiDB v6.0.0, GBK is supported. For more information, see the following documents:

- [Character Set and Collation](/character-set-and-collation.md)
- [GBK compatibility](/character-set-gbk.md#mysql-compatibility)

### Best practices for deployment

#### Deploy DM-master and DM-worker

DM consists of DM-master and DM-worker.

- DM-master manages the metadata of migration tasks and is the central scheduling of DM-worker. It is the core of the whole DM platform. Therefore, DM-master can be deployed as clusters to ensure the availability of the DM platform.
- DM-worker executes upstream and downstream migration tasks. It is a stateless node. You can deploy at most 1000 DM-worker nodes. When using DM, you can reserve some idle DM-workers to ensure high availability.

#### Plan the migration tasks

Splitting the migration task can only guarantee the final consistency of data. Real-time consistency may deviate significantly due to various reasons.

- When migrating and merging MySQL shards, you can split the migration task according to the types of shards in the upstream. For example, if `usertable_1~50` and `Logtable_1~50` are two types of shards, you can create two migration tasks. It can simplify the migration task template and effectively control the impact of interruption in data migration.

- For large-scale data migration, you can refer to the following to split the migration task:
    - If you need to migrate multiple databases in the upstream, you can split the migration task in terms of databases.
    - Split the task according to the write pressure in the upstream. That is, split the tables with frequent DML operations in the upstream to a separate migration task. Use another migration task to migrate the tables without frequent DML operations. This method can speed up the progress of the migration task to some extent. Especially when there are a large number of logs written to a table in the upstream. But if this table does not matter, this method can effectively solve such problems.

The following table gives the recommended deployment plans for DM-master and DM-worker in different data migration scenarios.

| Scenario | DM-master deployment | DM-worker deployment |
| :--- | :--- | :--- |
| Small dataset (less than 1 TB) and one-time data migration | Deploy 1 DM-master node | Deploy 1~N DM-worker nodes according to the number of upstream data sources. Generally, 1 DM-worker node is recommended. |
| Large dataset (more than 1 TB) and MySQL shards, one-time data migration | It is recommended to deploy 3 DM-master nodes to ensure the availability of the DM cluster during long-time data migration. | Deploy DM-worker nodes according to the number of data sources or migration tasks. It is recommended to deploy 1~3 idle DM-worker nodes. |
| Long-term data migration | It is necessary to deploy 3 DM-master nodes. If you deploy DM-master nodes on the cloud, try to deploy them in different availability zones (AZ). | Deploy DM-worker nodes according to the number of data sources or migration tasks. It is necessary to deploy 1.5~2 times the number of DM-worker nodes that are actually needed. |

#### Choose and configure the upstream data source

DM supports full data migration, but when doing it, it backs up the full data of the entire database. DM uses the parallel logical backup method. During the backup, it uses a relatively heavy lock [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock). At this time, DML and DDL operations of the upstream database will be blocked for a short time. Therefore, it is strongly recommended to use a backup database to perform the full data backup, and enable the GTID function of the data source at the same time (`enable-gtid: true`). This way, you can not only avoid the impact of the upstream during migration, but also switch to the master node in the upstream to reduce the delay during the incremental migration. For the method of switching the upstream MySQL data source, see [Switch DM-worker Connection between Upstream MySQL Instances](/dm/usage-scenario-master-slave-switch.md#switch-dm-worker-connection-via-virtual-ip).

Note the following:

- You can only perform full data backup on the master node of the upstream database.

    In this scenario, you can set the consistency parameter to `none` in the configuration file, `mydumpers.global.extra-args: "--consistency none"`, to avoid adding a heavy lock to the master node. But this may damage the data consistency of the full backup, which may lead to inconsistent data between the upstream and downstream.

- Use backup snapshots to perform full data migration (only applicable to the migration of MySQL RDS and Aurora RDS on AWS)

    If the database to be migrated is AWS MySQL RDS or Aurora RDS, you can use RDS snapshots to directly migrate the backup data in Amazon S3 to TiDB to ensure data consistency. For more information, see [Migrate Data from Amazon Aurora to TiDB](/migrate-aurora-to-tidb.md).

### Details of configurations

#### Capitalization

TiDB is case-insensitive to Schema name by default, that is, `lower_case_table_names:2`. But most upstream MySQL use Linux systems that are case-sensitive by default. In this case, you need to set `case-sensitive` to `true` to ensure that the schema can be correctly migrated from the upstream.

In a special case, for example, if there is a database in the upstream that has both uppercase tables such as `Table` and lowercase tables such as `table`, then an error occurs when creating the schema:

`ERROR 1050 (42S01): Table '{tablename}' already exists`

#### Filter rules

This section does not introduce the filter rules in detail. It is reminded that you configure the filter rules as soon as you configure the data source. The benefits of configuring the filter rules are:

- Reduce the number of Binlog events that the downstream needs to process, thereby improving migration efficiency.
- Reduce unnecessary Relay log storage, saving disk space.

> **Note:**
>
> When you migrate and merge MySQL shards, if you have configured filter rules in the data source, you must make sure that the rules match between the data source and the migration task. If they do not match, it may cause the issue that the migration task can not receive incremental data for a long time.

### Use Relay log

In the MySQL master/secondary mechanism, the secondary node saves a copy of the Relay logs to ensure the reliability and efficiency of asynchronous replication. DM also supports saving a copy of Relay logs on DM-worker. You can configure information such as the storage location and expiration time. This feature applies to the following scenarios:

- During full and incremental data migration, because the amount of full data is large, the entire process takes more time than the time for the upstream Binlog to be archived. It causes the incremental replication task fail to start normally. If you enable Relay log, DM-worker will start receiving Relay log when the full migration is started. This avoids the failure of the incremental task.

- When you use DM to perform long-time data migration, sometimes the migration task is blocked for a long time due to various reasons. If you enable Relay log, you can effectively deal with the problem of upstream Binlog being recycled due to the blocking of the migration task.

There are some restrictions using Relay log. DM supports high availability. When a DM-worker fails, it will try to promote an idle DM-worker instance to a working instance. If the upstream Binlog does not contain the necessary migration logs, it may cause interruption. You need to intervene manually to copy the Relay log to the new DM-worker node as soon as possible, and modify the corresponding Relay meta file. For details, see [Troubleshooting](/dm/dm-error-handling.md#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-migration-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned).

#### Use PT-osc/GH-ost in upstream

In daily MySQL operation and maintenance, usually you use tools such as PT-osc/GH-ost to change the schema online to minimize impact on the business. However, the whole process will be logged to MySQL Binlog. Migrating such data to TiDB downstream will result in a lot of write operations, which is neither efficient nor economical. DM supports third-party data tools such as PT-osc or GH-ost when you configure the migration task. After the configuration, DM will not migrate redundant data and ensure data consistency. For details, see [Migrate from Databases that Use GH-ost/PT-osc](/dm/feature-online-ddl.md).

## Best practices during migration

This section introduce how to troubleshoot problems you encounter during migration.

### Inconsistent schemas in upstream and downstream

Common errors include:

- `messages: Column count doesn't match value count: 3 (columns) vs 2 (values)`
- `Schema/Column doesn't match`

Usually such issues are caused by changed or added indexes in the downstream TiDB, or there are more columns in the downstream. When such errors occur, check whether the upstream and downstream schemas are inconsistent.

To resolve such issues, update the schema information cached in DM to be consistent with the downstream TiDB Schema. For details, see [Manage Table Schemas of Tables to be Migrated](/dm/dm-manage-schema.md).

If the downstream has more columns, see [Migrate Data to a Downstream TiDB Table with More Columns](/migrate-with-more-columns-downstream.md).

### Interrupted migration task due to failed DDL

DM supports skipping or replacing DDL statements that cause the migration task to interrupt. For details, see [Handle Failed DDL Statements](/dm/handle-failed-ddl-statements.md#usage-examples).

## Data validation after data migration

Usually you need to validate the consistency of data after data migration. TiDB provides [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to help you complete the data validation.

Now sync-diff-inspector can automatically manage the table list to be checked for data consistency through DM tasks. Compared with the previous manual configuration, it is more efficient. For details, see [Data Check in the DM Replication Scenario](/sync-diff-inspector/dm-diff.md).

Since DM v6.2, data validation is also supported for incremental replication. For details, see [Continuous Data Validation in DM](/dm/dm-continuous-data-validation.md).

## Long-term data replication

If you use DM as a long-term data replication platform, it is necessary to back up the metadata. On the one hand, it ensures the ability to rebuild the migration cluster. On the other hand, it can implement the version control of the migration task through the version control capability. For details, see [Export and Import Data Sources and Task Configuration of Clusters](/dm/dm-export-import-config.md).
