---
title: Migration Task Precheck
summary: Learn the precheck that DM performs when a migration task is started.
aliases: ['/docs/tidb-data-migration/dev/precheck/']
---

# Migration Task Precheck

This document introduces the DM precheck feature, which detects errors in the upstream MySQL instance configurations before the migration task is executed.

## Usage scenario

To run the data migration task smoothly, when a migration task is started, DM triggers the precheck automatically and returns the check results. Only after the precheck passes, does DM start executing the migration.

If you want to trigger the precheck manually, you can run the `check-task` command.

For example:

{{< copyable "" >}}

```bash
tiup dmctl check-task ./task.yaml
```

## Checking items

When the task precheck is triggered, DM checks the corresponding checking items according to the migration mode configured in the task.

This section lists all the checking items in the precheck.

> **Note:**
>
> For the checking items that must be passed in the precheck, "(required)" is indicated before the checking item names in this document.
>
> + For a required checking item, if the corresponding check does not pass, DM returns an error after the check and does not proceed with the migration task. In this case, modify the configurations according to the error message and retry the task after meeting the precheck requirements.
> + For a non-required checking item, if the corresponding check does not pass, DM returns a warning after the check. If the check result has no errors but only warnings, DM automatically starts executing the migration task.

### Common checking items

Regardless of which migration mode you choose, the precheck always includes the following common checking items:

- Database version

    - MySQL version > 5.5
    - MariaDB version >= 10.1.2

    > **Warning:**
    >
    > - Migrating data from MySQL 8.0 to TiDB using DM is an experimental feature (introduced since DM v2.0). It is NOT recommended that you use it in a production environment.
    > - Migrating data from MariaDB to TiDB using DM is an experimental feature. It is NOT recommended that you use it in a production environment.

- Compatibility of the upstream MySQL table schema

    - Check whether the upstream tables have foreign keys. TiDB does not support foreign keys and returns a warning if the upstream tables have foreign keys.
    - (Required) Check whether there are compatibility differences in character sets. For more information, see [TiDB Supported Character Sets](/character-set-and-collation.md).
    - Check whether the upstream tables have a primary key or unique key restrictions (introduced from v1.0.7)

### Full data migration checking items

For the full data migration mode (`task-mode: full`), in addition to the [common checking items](#common-checking-items), the precheck also includes the following checking items:

* (Required) dump permissions of the upstream database

    - Check for the SELECT permission on INFORMATION_SCHEMA and dump tables.
    - If `consistency=flush`, check for the RELOAD permission.
    - If `consistency=flush/lock`, check for the LOCK TABLES permission on the dump tables.

* (Required) Consistency of upstream MySQL multi-instance sharding tables

    - In the pessimistic mode, check whether the table schemas of all sharded tables are consistent, including the following items:

        - Number of columns
        - Column name
        - Column order
        - Column type
        - Primary key
        - Unique index

    - In the optimistic mode, check whether the schemas of all sharded tables meet the [optimistic compatibility](https://github.com/pingcap/tiflow/blob/master/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types).

    - If a migration task was started successfully by the `start-task` command, the precheck of this task skips the consistency check.

* Auto-increment primary key in sharded tables

    - If sharded tables have auto-increment primary keys, the precheck returns a warning. If there are conflicts in auto-increment primary keys, see [Handle conflicts of auto-increment primary key](/dm/shard-merge-best-practices.md#Handling-auto-increment-primary-key-conflicts) for solutions.

### Incremental data migration checking items

For the incremental data migration mode (`task-mode: incremental`), in addition to the [common checking items](#common-checking-items), the precheck also includes the following checking items:

* (Required) REPLICATION permission of the upstream database

    - Check for the REPLICATION CLIENT permission.
    - Check for the REPLICATION SLAVE permission.

* (Required) Database primary-secondary configuration

    - The database ID `server_id` must be configured for the upstream database (GTID is recommended for non-AWS Aurora environments).

* (Required) MySQL binlog configuration

    - Check whether binlog is enabled (DM requires binlog to be enabled).
    - Check whether `binlog_format=ROW` is configured (DM only supports the migration of binlog in the ROW format).
    - Check whether `binlog_row_image=FULL` is configured (DM only supports `binlog_row_image=FULL`).
    - If `binlog_do_db` or `binlog_ignore_db` is configured, check whether the database tables to be migrated meet the conditions of `binlog_do_db` and `binlog_ignore_db`.

* (Required) Check if the upstream database is in an [Online-DDL](/dm/feature-online-ddl.md) process (in which the `ghost` table is created but the `rename` phase is not executed yet). If the upstream is in the online-DDL process, the precheck returns errors. In this case, wait until the DDL to complete and retry.

### Full and incremental data migration checking items

For the full and incremental data migration mode (`task-mode: all`), in addition to the [common checking items](#common-checking-items), the precheck also includes the [full data migration checking items](#full-data-migration-checking-items) and the [incremental data migration checking items](#incremental-data-migration-checking-items).

## Configure precheck arguments

The migration task precheck supports multi-thread processing in parallel. Even if the number of rows in sharded tables reaches a million level, the check can be completed in minutes.

To specify the number of threads for the precheck, you can configure the `threads` argument of the `mydumpers` field in the migration task configuration file.

```yaml
mydumpers:                           # Configuration arguments of the dump processing unit
  global:                            # Configuration name
    threads: 4                       # The number of threads that access the upstream when the dump processing unit performs the precheck and exports data from the upstream database (4 by default)
    chunk-filesize: 64               # The size of the file generated by the dump processing unit (64 in MB by default)
    extra-args: "--consistency none" # Other arguments of the dump processing unit. You do not need to manually configure table-list in `extra-args`, because table-list is automatically generated by DM.

```

> **Note:**
>
> The value of `threads` determines the number of physical connections between the upstream database and DM. A too large `threads` value might increase the load of the upstream. Therefore, you need to control the `threads` value carefully.
