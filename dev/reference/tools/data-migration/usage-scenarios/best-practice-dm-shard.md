---
title: Best Practices of Data Migration in Sharding Scenario
summary: This document introduces the best practice of data migration in sharding scenarios.
category: reference
---
# Best Practices of Data Migration in Sharding Scenario

This document aims to provide a business best practice, which introduces the support and limitations of TiDB Data Migration (DM) in sharding scenario.

## An independent data migration task

In [Merge and Replicate Data from Sharded Tables](/dev/reference/tools/data-migration/features/shard-merge.md), the concept of sharding group is introduced. In simple terms, a sharding group consists of all upstream tables that need to be merged and replicated into the same downstream table.

The current sharding DDL mechanism has some [usage restrictions](/dev/reference/tools/data-migration/features/shard-merge.md#restrictions) to coordinate the schema changes using DDL statements in different sharded tables. When these restrictions are ineffective due to unexpected reasons, you need to [handle sharding DDL locks manually in DM](/dev/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md), or even redo the entire data migration.

Therefore, to mitigate the impact on the performance of data migration caused by exception handling, it is recommended to perform one independent data migration task for each sharding group. *In this case, when an exception is thrown, only a small number of data migration tasks might need to be handled manually while others remain unaffected.*

## Handle sharding DDL locks manually

In [Merge and Replicate Data from Sharded Tables](/dev/reference/tools/data-migration/features/shard-merge.md#principles), it is clear that sharding DDL lock in DM is a mechanism for coordinating the execution of DDL statements from multiple upstream sharded tables.

Therefore, when you confirm the sharding DDL lock is enabled on the DM-master through `show-ddl-locks`, or some DM-workers have `unresolvedGroups` or `blockingDDLs` through `query-status`, do not rush to unlock the sharding DDL lock manually using `unlock-ddl-lock` or `break-ddllock`.

Only when you confirm that the current failure to automatically unlock the sharding DDL lock is listed in the [supported scenarios](/dev/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md#supported-scenarios), can you follow the corresponding manual solution. For unsupported scenarios, it is recommended to redo the entire data migration. That is, redo the full and incremental data migration after emptying the data in the downstream database and the `dm_meta` information associated with the data migration.

## Handling conflicts of auto-increment primary key

DM offers [column mapping](/dev/reference/tools/data-migration/features/overview.md#column-mapping) to handling conflicts that might occur in merging the bigint type of auto-increment primary key. However, it is *strongly discouraged* to choose this approach. If condition permits, the following two solutions are available.

### Remove the `PRIMARY KEY` attribute of auto-increment primary key

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

- The `auto_pk_c1` column is meaningless to the business and does not depend on the `PRIMARY KEY` attribute of the column.
- The `uk_c2` column has the `UNIQUE KEY` attribute, and it is unique in all upstream sharded tables.

Then you can perform the following steps to fix the `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` error that possibly caused by `auto_pk_c1` when you merge and replicate sharded tables.

1. Create a table for merge and replicate data in the downstream database before starting the full data migration. Do not specify the `PRIMARY KEY` attribute of the `auto_pk_c1` column.

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uk_c2` bigint(20) NOT NULL,
      `content_c3` text,
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Start the full and incremental data migration.

3. Verify that whether the data migration is successfully processed through `query-status` and whether the data from upstream have already merged and replicated in the downstream database.

### Use composite primary key

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

* The business does not depend on the `PRIMARY KEY` attribute of the `auto_pk_c1` column.
* The composite primary key that consists of column `auto_pk_c1` and `uuid_c2` is globally unique.
* The business accepts a composite primary key that consists of column `auto_pk_c1` and `uuid_c2`.

Then you can perform the following steps to fix the `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` error that possibly caused by `auto_pk_c1` when you merge and replicate sharded tables.

1. Create a table for merge and replicate data in the downstream database before starting the full data migration. Do not specify the `PRIMARY KEY` attribute for the `auto_pk_c1` column, use column `auto_pk_c1` and `uuid_c2` to specify the `PRIMARY KEY` instead.

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uuid_c2` bigint(20) NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Start the full and incremental data migration.

3. Verify that whether the data migration is successfully processed through `query-status` and whether the data from upstream have already merged and replicated in the downstream database.

## Create/drop tables upstream in the upstream

From [Merge and Replicate Data from Sharded Tables](/dev/reference/tools/data-migration/features/shard-merge.md#principles), it is clear that the coordination of sharding DDL lock depends on whether the downstream receives the corresponding DDL statements of all upstream sharded tables. In addition, currently DM *does not* support dynamically creating or dropping sharded tables in the upstream. Therefore, to create or drop sharded tables in the upstream, it is recommended to perform the following steps.

### Create sharded tables in the upstream

If you need to create a new sharded table in the upstream, perform the following steps:

1. Wait for the coordination of all sharding DDL in upstream sharded tables to finish.

2. Stop the task by `stop-task`.

3. Create a new sharded table in the upstream.

4. Make sure that the configuration in `task.yaml` file allows the newly-added sharded table to be merged in one downstream table with other existing sharded table.

5. Start the task by `start-task`.

6. Verify that whether the data migration is successfully processed through `query-status` and whether the data from upstream have already merged and replicated in the downstream database.

### Drop sharded tables in the upstream

If you need to drop a sharded table in the upstream, perform the following steps:

1. Drop the existing sharded table, fetch the corresponding `End_log_pos` in the binlog of the `DROP TABLE` statement through [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html), and mark it as `Pos-M`.

2. Fetch the position (`syncerBinlog`) corresponding to the binlog event that has been processed by DM through `query-status`, and mark it as `Pos-S`.

3. When `Pos-S` is greater than `Pos-M`, it means that DM has finished processing the `DROP TABLE` statement, and the data of the table has been replicated to the downstream, so the subsequent operation can be performed. Otherwise, wait for DM to finish replicating the data.

4. Stop the task by `stop-task`.

5. Make sure that the configuration in `task.yaml` file ignores the dropped sharded table in the upstream.

6. Start the task by `start0task`.

7. Verify that whether the data migration is successfully processed by `query-status`.

## Speed limits and traffic flow control

When data from multiple upstream MySQL or MariaDB instances is merged and replicated to the same TiDB cluster in the downstream, every corresponding DM-worker executes full and incremental data migration concurrently. This means that the default degree of concurrency (`pool-size` in full data migration and `worker-count` in incremental) gradually accumulates as the number of DM-workers increases, which causes excessive downstream pressure. In such case, you should conduct a preliminary performance analysis based on TiDB and DM monitoring metrics, and appropriately adjust the size of concurrency. In the future, DM might support partially-automated traffic flow control.