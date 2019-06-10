---
title: Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components and features.
category: reference
aliases: ['/docs/tools/dm/overview/']
---

# Data Migration Overview

[DM](https://github.com/pingcap/dm) (Data Migration) is an integrated data synchronization task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB into TiDB. It can help to reduce the operations cost and simplify the troubleshooting process.

## Architecture

The Data Migration tool includes three components: DM-master, DM-worker, and dmctl.

![Data Migration architecture](/media/dm-architecture.png)

### DM-master

DM-master manages and schedules the operation of data synchronization tasks.

- Storing the topology information of the DM cluster
- Monitoring the running state of DM-worker processes
- Monitoring the running state of data synchronization tasks
- Providing a unified portal for the management of data synchronization tasks
- Coordinating the DDL synchronization of sharded tables in each instance under the sharding scenario

### DM-worker

DM-worker executes specific data synchronization tasks.

- Persisting the binlog data to the local storage
- Storing the configuration information of the data synchronization subtasks
- Orchestrating the operation of the data synchronization subtasks
- Monitoring the running state of the data synchronization subtasks

After DM-worker is started, it automatically synchronizes the upstream binlog to the local configuration directory (the default synchronization directory is `<deploy_dir>/relay_log` if DM is deployed using `DM-Ansible`). For details about DM-worker, see [DM-worker Introduction](/tools/dm/dm-worker-intro.md). For details about the relay log, see [Relay Log](/tools/dm/relay-log.md).

### dmctl 

dmctl is the command line tool used to control the DM cluster.

- Creating/Updating/Dropping data synchronization tasks
- Checking the state of data synchronization tasks
- Handling the errors during data synchronization tasks
- Verifying the configuration correctness of data synchronization tasks

## Data synchronization features

This section describes the data synchronization features provided by the Data Migration tool.

### Schema and table routing

The [schema and table routing](/dev/reference/tools/data-migration/features/overview.md#table-routing) feature means that DM can synchronize a certain table of the upstream MySQL or MariaDB instance to the specified table in the downstream, which can be used to merge or synchronize the sharding data.

### Black and white lists synchronization at the schema and table levels

The [black and white lists filtering rule](/dev/reference/tools/data-migration/features/overview.md#black-and-white-table-lists) of the upstream database instance tables is similar to MySQL `replication-rules-db`/`replication-rules-table`, which can be used to filter or only synchronize all operations of some databases or some tables.

### Binlog event filtering

[Binlog event filtering](/dev/reference/tools/data-migration/features/overview.md#binlog-event-filtering) is a more fine-grained filtering rule than the black and white lists filtering rule. You can use statements like `INSERT` or `TRUNCATE TABLE` to specify the binlog events of `schema/table` that you need to synchronize or filter out.

### Column mapping

The [column mapping](/dev/reference/tools/data-migration/features/overview.md#column-mapping) feature means that the table column value can be modified according to the built-in expression specified by the user, which can be used to resolve the conflicts of the sharding auto-increment primary key IDs.

### Sharding support

DM supports merging the original sharded instances and tables into TiDB, but with [some restrictions](/dev/reference/tools/data-migration/features/shard-merge.md#restrictions).

## Usage restrictions

Before using the DM tool, note the following restrictions:

+ Database version

    - 5.5 < MySQL version < 5.8
    - MariaDB version >= 10.1.2

    > **Note:** 
    >
    > If there is a master-slave replication structure between the upstream MySQL/MariaDB servers, then choose the following version.
    >
    > - 5.7.1 < MySQL version < 5.8
    > - MariaDB version >= 10.1.3

    Data Migration [prechecks the corresponding privileges and configuration automatically](/tools/dm/precheck.md) while starting the data synchronization task using dmctl.

+ DDL syntax

    - Currently, TiDB is not compatible with all the DDL statements that MySQL supports. Because DM uses the TiDB parser to process DDL statements, it only supports the DDL syntax supported by the TiDB parser. For details, see [MySQL Compatibility](/dev/reference/mysql-compatibility.md#ddl).

    - DM reports an error when it encounters an incompatible DDL statement. To solve this error, you need to manually handle it using dmctl, either skipping this DDL statement or replacing it with a specified DDL statement(s). For details, see [Skip or replace abnormal SQL statements](/dev/how-to/troubleshoot/data-migration.md#skip-or-replace-abnormal-sql-statements).

+ Sharding

    - If conflict exists between sharded tables, *only columns with the auto increment primary key* encounter the conflict, and the *column type is bigint*, solve the conflict using [column mapping](/dev/reference/tools/data-migration/features/overview.md#column-mapping). Otherwise, data synchronization is not supported. Conflicting data can cover each other and cause data loss.

    - For other sharding restrictions, see [Sharding DDL usage restrictions](/dev/reference/tools/data-migration/features/shard-merge.md#restrictions).

+ Operations

    - After DM-worker is restarted, the data synchronization task cannot be automatically restored. You need to manually run `start-task`. For details, see [Manage the Data Synchronization Task](/dev/reference/tools/data-migration/manage-tasks.md).

    - After DM-worker is restarted, the DDL lock synchronization cannot be automatically restored in some conditions. You need to manually handle it. For details, see [Handle Sharding DDL Locks Manually](/dev/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md).
