---
title: Best Practice of Data Migration in the Shard Merge Scenario
summary: Learn the best practice of data migration in the shard merge scenario.
category: reference
---
# Best Practice of Data Migration in the Shard Merge Scenario

This document details the supported functions and limitations of TiDB Data Migration (DM) in the shard merge scenario and provides a best practice guide to facilitate application for users.

## An independent data migration task

In [Merge and Replicate Data from Sharded Tables](/dev/reference/tools/data-migration/features/shard-merge.md#principles), the concept of sharding group is introduced. Simply put, a sharding group consists of all upstream tables that need to be merged and replicated into a same downstream table.

The current sharding DDL mechanism has some [usage restrictions](/dev/reference/tools/data-migration/features/shard-merge.md#restrictions) to coordinate the schema changes using DDL statements in different sharded tables. If these restrictions are found to be violated due to unexpected reasons, you need to [handle sharding DDL locks manually in DM](/dev/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md), or even redo the entire data migration.

Therefore, to mitigate the impact of exception handling on data migration, it is recommended to merge and replicate each sharding group in separate data migration task. *In this case, when an exception is thrown, only a small number of data migration tasks might need to be handled manually while others remain unaffected.*

## Handle sharding DDL locks manually

In [Merge and Replicate Data from Sharded Tables](/dev/reference/tools/data-migration/features/shard-merge.md#principles), it is clear that sharding DDL lock in DM is a mechanism for coordinating the execution of DDL statements from multiple upstream sharded tables.

Therefore, when you confirm there are sharding DDL locks on the DM-master through `show-ddl-locks` command, or some DM-workers have `unresolvedGroups` or `blockingDDLs` through `query-status` command, do not rush to unlock the sharding DDL lock manually using `unlock-ddl-lock` or `break-ddllock`.

Only when you confirm that the current failure to automatically unlock the sharding DDL lock is listed in the [supported scenarios](/dev/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md#supported-scenarios), can you follow the corresponding solution. For unsupported scenarios, it is recommended to redo the entire data migration. That is, redo the full and incremental data migration after emptying the data in the downstream database and the `dm_meta` information associated with the migration task.

## Handle conflicts of auto-increment primary key

DM offers [column mapping](/dev/reference/tools/data-migration/features/overview.md#column-mapping) to handle conflicts that might occur in merging the bigint type of auto-increment primary key. However, it is *strongly discouraged* to choose this approach. If it is acceptable in the production environment, the following two solutions are available.

### Remove the `PRIMARY KEY` attribute of a auto-increment primary key

Assume that the upstream schemas are as follows:

```sql
CREATE TABLE `tbl_no_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uk_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`),
  UNIQUE KEY `uk_c2` (`uk_c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

If the following requirements are satisfied:

- The `auto_pk_c1` column has no impact on the application and is unaffected by the `PRIMARY KEY` attribute of this column.
- The `uk_c2` column has the `UNIQUE KEY` attribute, and it is unique in all upstream sharded tables.

Then you can perform the following steps to fix the `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` error that possibly caused by the `auto_pk_c1` column when you merge sharded tables.

1. Create a table for merge and replicate data in the downstream database before the full data migration. Do not specify the `PRIMARY KEY` attribute of the `auto_pk_c1` column.

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uk_c2` bigint(20) NOT NULL,
      `content_c3` text,
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Execute the full and incremental data migration.

3. Run `query-status` to verify that whether the data migration is successfully processed and whether the data from the upstream have already been merged and replicated in the downstream database.

### Use a composite primary key

Assume that the upstream schemas are as follows:

```sql
CREATE TABLE `tbl_multi_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uuid_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

If the following requirements are satisfied:

* The `auto_pk_c1` column with `PRIMARY KEY` attribute has no impact on the application.
* The composite primary key that consists of column `auto_pk_c1` and `uuid_c2` is globally unique.
* It is acceptable to use a composite primary key in the application.

Then you can perform the following steps to fix the `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` error that possibly caused by the `auto_pk_c1` column when you merge sharded tables.

1. Create a table for merge and replicate data in the downstream database before the full data migration. Do not specify the `PRIMARY KEY` attribute for the `auto_pk_c1` column, but use column `auto_pk_c1` and `uuid_c2` to define the `PRIMARY KEY` instead.

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uuid_c2` bigint(20) NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Start the full and incremental data migration.

3. Run `query-status` to verify that whether the data migration is successfully processed and whether the data from upstream have already been merged and replicated in the downstream database.

## Create/drop tables in the upstream

From [Merge and Replicate Data from Sharded Tables](/dev/reference/tools/data-migration/features/shard-merge.md#principles), it is clear that the coordination of sharding DDL lock depends on whether the downstream database receives the corresponding DDL statements of all upstream sharded tables. In addition, currently DM *does not* support dynamically creating or dropping sharded tables in the upstream. Therefore, to create or drop sharded tables in the upstream, it is recommended to perform the following steps.

### Create sharded tables in the upstream

If you need to create a new sharded table in the upstream, perform the following steps:

1. Wait for the coordination of all executed sharding DDL in the upstream sharded tables to finish.

2. Run `stop-task` to stop the task.

3. Create a new sharded table in the upstream.

4. Make sure that the configuration in `task.yaml` file allows the newly-added sharded table to be merged in one downstream table with other existing sharded table.

5. Run `start-task` to start the task.

6. Run `query-status` to verify that whether the data migration is successfully processed and whether the data from upstream have already been merged and replicated in the downstream database.

### Drop sharded tables in the upstream

If you need to drop a sharded table in the upstream, perform the following steps:

1. Drop the existing sharded table, run [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html) to fetch the corresponding `End_log_pos` in the binlog of the `DROP TABLE` statement, and mark it as *Pos-M*.

2. Run `query-status` to fetch the position (`syncerBinlog`) corresponding to the binlog event that has been processed by DM, and mark it as *Pos-S*.

3. When *Pos-S* is greater than *Pos-M*, it means that DM has finished processing the `DROP TABLE` statement, and the data of the table has been replicated to the downstream, so the subsequent operation can be performed. Otherwise, wait for DM to finish replicating the data.

4. Run `stop-task` to stop the task.

5. Make sure that the configuration in `task.yaml` file ignores the dropped sharded table in the upstream.

6. Run `start-task` to start the task.

7. Run `query-status` to verify whether the data migration is successfully processed.

## Speed limits and traffic flow control

When data from multiple upstream MySQL or MariaDB instances is merged and replicated to the same TiDB cluster in the downstream, every corresponding DM-worker executes full and incremental data migration concurrently. This means that the default degree of concurrency (`pool-size` in full data migration and `worker-count` in incremental) gradually accumulates as the number of DM-workers increases, which causes excessive downstream pressure. In such case, you should conduct a preliminary performance analysis based on TiDB and DM monitoring metrics, and adjust the size of concurrency accordingly. In the future, DM might support partially-automated traffic flow control.