---
title: Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components, and features.
aliases: ['/docs/tidb-data-migration/dev/overview/']
---

<!-- markdownlint-disable MD007 -->

# Data Migration Overview

[TiDB Data Migration](https://github.com/pingcap/dm) (DM) is an integrated data migration task management platform, which supports the full data migration and the incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB. It can help to reduce the operation cost of data migration and simplify the troubleshooting process. When using DM for data migration, you need to perform the following operations:

- Deploy a DM Cluster
- Create upstream data source and save data source access information
- Create data migration tasks to migrate data from data sources to TiDB

The data migration task includes two stages: full data migration and incremental data replication:

- Full data migration: Migrate the table structure of the corresponding table from the data source to TiDB, and then read the data stored in the data source and write it to the TiDB cluster.
- Incremental data replication: After the full data migration is completed, the corresponding table changes from the data source are read and then written to the TiDB cluster.

## DM versions

This document is applicable to DM v5.4, the latest stable version of DM.

Before v5.4, the DM documentation is independent of the TiDB documentation. To access these earlier versions of the DM documentation, click one of the following links:

- [DM v5.3 documentation](https://docs.pingcap.com/tidb-data-migration/v5.3)
- [DM v2.0 documentation](https://docs.pingcap.com/tidb-data-migration/v2.0/)
- [DM v1.0 documentation](https://docs.pingcap.com/tidb-data-migration/v1.0/) (Not recommended, because it the earliest stable version of DM)

> **Note:**
>
> - Since October 2021, DM's GitHub repository has been moved to [pingcap/tiflow](https://github.com/pingcap/tiflow/tree/master/dm). If you see any issues with DM, submit your issue to the `pingcap/tiflow` repository for feedback.
> - In earlier versions (v1.0 and v2.0), DM uses version numbers that are independent of TiDB. Since v5.3, DM uses the same version number as TiDB. The next version of DM v2.0 is DM v5.3. There are no compatibility changes from DM v2.0 to v5.3, and the upgrade process is no different from a normal upgrade, only an increase in version number.

## Basic features

This section describes the basic data migration features provided by DM.

![DM Core Features](/media/dm/dm-core-features.png)

### Block and allow lists migration at the schema and table levels

The [block and allow lists filtering rule](/dm/dm-key-features.md#block-and-allow-table-lists) is similar to the `replication-rules-db`/`replication-rules-table` feature of MySQL, which can be used to filter or replicate all operations of some databases only or some tables only.

### Binlog event filtering

The [binlog event filtering](/dm/dm-key-features.md#binlog-event-filter) feature means that DM can filter certain types of SQL statements from certain tables in the source database. For example, you can filter all `INSERT` statements in the table `test`.`sbtest` or filter all `TRUNCATE TABLE` statements in the schema `test`.

### Schema and table routing

The [schema and table routing](/dm/dm-key-features.md#table-routing) feature means that DM can migrate a certain table of the source database to the specified table in the downstream. For example, you can migrate the table structure and data from the table `test`.`sbtest1` in the source database to the table `test`.`sbtest2` in TiDB. This is also a core feature for merging and migrating sharded databases and tables.

## Advanced features

### Shard merge and migration

DM supports merging and migrating the original sharded instances and tables from the source databases into TiDB, but with some restrictions. For details, see [Sharding DDL usage restrictions in the pessimistic mode](/dm/feature-shard-merge-pessimistic.md#restrictions) and [Sharding DDL usage restrictions in the optimistic mode](/dm/feature-shard-merge-optimistic.md#restrictions).

### Optimization for third-party online-schema-change tools in the migration process

In the MySQL ecosystem, tools such as gh-ost and pt-osc are widely used. DM provides support for these tools to avoid migrating unnecessary intermediate data. For details, see [Online DDL Tools](/dm/dm-key-features.md#online-ddl-tools)

### Filter certain row changes using SQL expressions

In the phase of incremental replication, DM supports the configuration of SQL expressions to filter out certain row changes, which lets you replicate the data with a greater granularity. For more information, refer to [Filter Certain Row Changes Using SQL Expressions](/dm/feature-expression-filter.md).

## Usage restrictions

Before using the DM tool, note the following restrictions:

+ Database version requirements

    - MySQL version > 5.5
    - MariaDB version >= 10.1.2

    > **Note:**
    >
    > If there is a primary-secondary migration structure between the upstream MySQL/MariaDB servers, then choose the following version.
    >
    > - MySQL version > 5.7.1
    > - MariaDB version >= 10.1.3

    > **Warning:**
    >
    > Migrating data from MySQL 8.0 to TiDB using DM is an experimental feature (introduced since DM v2.0). It is **NOT** recommended that you use it in a production environment.

+ DDL syntax compatibility

    - Currently, TiDB is not compatible with all the DDL statements that MySQL supports. Because DM uses the TiDB parser to process DDL statements, it only supports the DDL syntax supported by the TiDB parser. For details, see [MySQL Compatibility](/mysql-compatibility.md#ddl).

    - DM reports an error when it encounters an incompatible DDL statement. To solve this error, you need to manually handle it using dmctl, either skipping this DDL statement or replacing it with a specified DDL statement(s). For details, see [Skip or replace abnormal SQL statements](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements).

+ Sharding merge with conflicts

    - If conflict exists between sharded tables, solve the conflict by referring to [handling conflicts of auto-increment primary key](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key). Otherwise, data migration is not supported. Conflicting data can cover each other and cause data loss.

    - For other sharding DDL migration restrictions, see [Sharding DDL usage restrictions in the pessimistic mode](/dm/feature-shard-merge-pessimistic.md#restrictions) and [Sharding DDL usage restrictions in the optimistic mode](/dm/feature-shard-merge-optimistic.md#restrictions).

+ Switch of MySQL instances for data sources

    When DM-worker connects the upstream MySQL instance via a virtual IP (VIP), if you switch the VIP connection to another MySQL instance, DM might connect to the new and old MySQL instances at the same time in different connections. In this situation, the binlog migrated to DM is not consistent with other upstream status that DM receives, causing unpredictable anomalies and even data damage. To make necessary changes to DM manually, see [Switch DM-worker connection via virtual IP](/dm/usage-scenario-master-slave-switch.md#switch-dm-worker-connection-via-virtual-ip).

+ GBK character set compatibility

    - DM does not support migrating `charset=GBK` tables to TiDB clusters earlier than v5.4.0.