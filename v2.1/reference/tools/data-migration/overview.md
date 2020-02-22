---
title: Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components and features.
category: reference
---

# Data Migration Overview

[DM](https://github.com/pingcap/dm) (Data Migration) is an integrated data replication task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB into TiDB. It can help to reduce the operations cost and simplify the troubleshooting process.

## Architecture

The Data Migration tool includes three components: DM-master, DM-worker, and dmctl.

![Data Migration architecture](/media/dm-architecture.png)

### DM-master

DM-master manages and schedules the operation of data replication tasks.

- Storing the topology information of the DM cluster
- Monitoring the running state of DM-worker processes
- Monitoring the running state of data replication tasks
- Providing a unified portal for the management of data replication tasks
- Coordinating the DDL replication of sharded tables in each instance under the sharding scenario

### DM-worker

DM-worker executes specific data replication tasks.

- Persisting the binlog data to the local storage
- Storing the configuration information of the data replication subtasks
- Orchestrating the operation of the data replication subtasks
- Monitoring the running state of the data replication subtasks

After DM-worker is started, it automatically replicates the upstream binlog to the local configuration directory (the default replication directory is `<deploy_dir>/relay_log` if DM is deployed using `DM-Ansible`). For details about DM-worker, see [DM-worker Introduction](/v2.1/reference/tools/data-migration/dm-worker-intro.md). For details about the relay log, see [Relay Log](/v2.1/reference/tools/data-migration/relay-log.md).

### dmctl

dmctl is the command line tool used to control the DM cluster.

- Creating/Updating/Dropping data replication tasks
- Checking the state of data replication tasks
- Handling the errors during data replication tasks
- Verifying the configuration correctness of data replication tasks

## Data replication features

This section describes the data replication features provided by the Data Migration tool.

### Schema and table routing

The [schema and table routing](/v2.1/reference/tools/data-migration/features/overview.md#table-routing) feature means that DM can replicate a certain table of the upstream MySQL or MariaDB instance to the specified table in the downstream, which can be used to merge or replicate the sharding data.

### Black and white lists replication at the schema and table levels

The [black and white lists filtering rule](/v2.1/reference/tools/data-migration/features/overview.md#black-and-white-table-lists) of the upstream database instance tables is similar to MySQL `replication-rules-db`/`replication-rules-table`, which can be used to filter or only replicate all operations of some databases or some tables.

### Binlog event filtering

[Binlog event filtering](/v2.1/reference/tools/data-migration/features/overview.md#binlog-event-filter) is a more fine-grained filtering rule than the black and white lists filtering rule. You can use statements like `INSERT` or `TRUNCATE TABLE` to specify the binlog events of `schema/table` that you need to replicate or filter out.

### Sharding support

DM supports merging the original sharded instances and tables into TiDB, but with [some restrictions](/v2.1/reference/tools/data-migration/features/shard-merge.md#restrictions).

## Usage restrictions

Before using the DM tool, note the following restrictions:

+ Database version

    - 5.5 < MySQL version < 8.0
    - MariaDB version >= 10.1.2

    > **Note:**
    >
    > If there is a master-slave replication structure between the upstream MySQL/MariaDB servers, then choose the following version.
    >
    > - 5.7.1 < MySQL version < 8.0
    > - MariaDB version >= 10.1.3

    Data Migration [prechecks the corresponding privileges and configuration automatically](/v2.1/reference/tools/data-migration/precheck.md) while starting the data replication task using dmctl.

+ DDL syntax

    - Currently, TiDB is not compatible with all the DDL statements that MySQL supports. Because DM uses the TiDB parser to process DDL statements, it only supports the DDL syntax supported by the TiDB parser. For details, see [MySQL Compatibility](/v2.1/reference/mysql-compatibility.md#ddl).

    - DM reports an error when it encounters an incompatible DDL statement. To solve this error, you need to manually handle it using dmctl, either skipping this DDL statement or replacing it with a specified DDL statement(s). For details, see [Skip or replace abnormal SQL statements](/v2.1/reference/tools/data-migration/faq.md#how-to-handle-incompatible-ddl-statements).

+ Sharding

    - If conflict exists between sharded tables, solve the conflict by referring to [handling conflicts of auto-increment primary key](/v2.1/reference/tools/data-migration/usage-scenarios/best-practice-dm-shard.md#handle-conflicts-of-auto-increment-primary-key). Otherwise, data replication is not supported. Conflicting data can cover each other and cause data loss.

    - For other sharding restrictions, see [Sharding DDL usage restrictions](/v2.1/reference/tools/data-migration/features/shard-merge.md#restrictions).

+ Operations

    - After DM-worker is restarted, the data replication task cannot be automatically restored. You need to manually run `start-task`. For details, see [Manage the Data Replication Task](/v2.1/reference/tools/data-migration/manage-tasks.md).

    - After DM-worker is restarted, the DDL lock replication cannot be automatically restored in some conditions. You need to manually handle it. For details, see [Handle Sharding DDL Locks Manually](/v2.1/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md).

+ DM-worker connection switch to another MySQL instance

    When DM-worker connects the upstream MySQL instance via a virtual IP (VIP), if you switch the VIP connection to another MySQL instance, DM might connect to the new and old MySQL instances at the same time in different connections. In this situation, the binlog replicated to DM is not consistent with other upstream status that DM receives, causing unpredictable anomalies and even data damage. To make necessary changes to DM manually, refer to [Switch DM-worker connection via virtual IP](/v2.1/reference/tools/data-migration/cluster-operations.md#switch-dm-worker-connection-via-virtual-ip).
