---
title: TiDB 9.0.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 9.0.0.
---

# TiDB 9.0.0 Release Notes

<EmailSubscriptionWrapper />

Release date: xx xx, 2025

TiDB version: 9.0.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

9.0.0 introduces the following key features and improvements:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Data Migration</td>
    <td>Support query argument redaction in DM logs</td>
    <td>Introduces an optional <code>redact-info-log</code> parameter to mask query arguments in DM logs, preventing sensitive data from appearing in logs.</td>
  </tr>
  <tr>
    <td>Data Migration</td>
    <td>Ensure Lightning compatibility with TiDB <code>sql_require_primary_key=ON</code></td>
    <td>Ensures the internal error-logging tables have primary keys if <code>sql_require_primary_key=ON</code> is enabled in TiDB, avoiding creation failures during data imports.</td>
  </tr>
  <tr>
    <td>Data Migration</td>
    <td>Migrated sync-diff-inspector from <code>tidb-tools</code> to <code>tiflow</code> repository</td>
    <td>Consolidates sync-diff-inspector with other data migration and replication tools (DM and TiCDC) in the <code>tiflow</code> repository. Now available via TiUP and a dedicated Docker image.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability



### Performance

* In scenarios with hundreds of thousands to millions of users, the performance of creating and modifying users has improved by 77 times [#55563](https://github.com/pingcap/tidb/issues/55563) @[tiancaiamao](https://github.com/tiancaiamao) tw@hfxsd<!--1941-->

    In previous versions, when the number of users in a cluster exceeded 200,000, the QPS for creating and modifying users drops to 1. In certain SaaS environments, if there is a need to create millions of users and periodically update user passwords in bulk, it can take up to 2 days or more, which is unacceptable for some SaaS businesses.

    TiDB v9.0.0 optimizes the performance of these DCL (Data Control Language) operations, allowing 2 million users to be created in just 37 minutes. This greatly enhances the execution performance of DCL statements and improves the user experience of TiDB in such SaaS scenarios.

    For more information, see [documentation](/system-variables.md/#tidb_accelerate_user_creation_update-new-in-v900).
* Support pushing down the following functions to TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1918-->

    * `TRUNCATE()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Support pushing down the following date functions to TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) @[gengliqi](https://github.com/gengliqi) **tw@Oreoxmt** <!--1837-->

    * `FROM_UNIXTIME()`
    * `TIMESTAMPDIFF()`
    * `UNIX_TIMESTAMP()`

  For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

### Availability

* TiProxy officially supports the traffic replay feature (GA) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832) tw@hfxsd<!--2062-->

    In TiProxy v1.3.0, the traffic replay feature is released as an experimental feature. In TiProxy v1.4.0, the traffic replay feature becomes generally available (GA). TiProxy provides specialized SQL commands for traffic capture and replay. This feature lets you easily capture access traffic from TiDB production clusters and replay it at a specified rate in test clusters, facilitating business validation.
    
    For more information, see [documentation](/tiproxy/tiproxy-traffic-replay.md).

### Reliability

* Introduce a new system variable `MAX_USER_CONNECTIONS` to limit the number of connections that different users can establish [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau) tw@hfxsd<!--2017-->

    Starting from v9.0.0, you can use the `MAX_USER_CONNECTIONS` system variable to limit the number of connections a single user can establish to a single TiDB node. This helps prevent issues where excessive [token](/tidb-configuration-file.md/#token-limit) consumption by one user causes delays in responding to requests from other users.
    
    For more information, see [documentation](/system-variables.md/#max_user_connections-new-in-v900)

### SQL

### Observability

* SQL cross-AZ traffic monitoring [#57543](https://github.com/pingcap/tidb/issues/57543) @[nolouch](https://github.com/nolouch) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--2021-->

    Deploying TiDB clusters across Availability Zones (AZs) enhances the disaster recovery capability. However, in cloud environments, cross-AZ deployments incur additional network traffic costs. For example, AWS charges for both cross-region and cross-AZ traffic. Therefore, for TiDB clusters running on cloud services, accurately monitoring and analyzing network traffic is essential for cost control.

    Starting from v9.0.0, TiDB records the network traffic generated during SQL processing and distinguishes cross-AZ traffic. TiDB writes this data to the [`statements_summary` table](/statement-summary-tables.md) and [slow query logs](/identify-slow-queries.md). This feature helps you track major data transmission paths within TiDB clusters, analyze the sources of cross-AZ traffic, and better understand and control related costs.

    Note that the current version monitors only SQL query traffic **within the cluster** (between TiDB, TiKV, and TiFlash) and does not include DML or DDL operations. Additionally, the recorded traffic data represents unpacked traffic, which differs from actual physical traffic and  cannot be used directly for network billing.

    For more information, see [documentation](/statement-summary-tables.md#statements_summary-fields-description).

* Optimize the `execution info` in the output of `EXPLAIN ANALYZE` [#56232](https://github.com/pingcap/tidb/issues/56232) @[yibin87](https://github.com/yibin87) tw@hfxsd<!--1697-->

    [`EXPLAIN ANALYZE`](https://github.com/sql-statements/sql-statement-explain-analyze.md) executes SQL statements and records execution details in the `execution info` column. The same information is captured in the [slow query log](https://github.com/identify-slow-queries.md). These details are crucial for analyzing and understanding the time spent on SQL execution.

    In v9.0.0, the `execution info` output is optimized for clearer representation of each metric. For example, `time` now refers to the wall-clock time for operator execution, `loops` indicates how many times the current operator is called by its parent operator, and `total_time` represents the sum of all concurrent execution times. These optimizations help you better understand the SQL execution process and devise more targeted optimization strategies.

    For more information, see [documentation](/sql-statements/sql-statement-explain-analyze.md).
### Security

### Data migration

* Support query argument redaction in DM logs [#11489](https://github.com/pingcap/tiflow/issues/11489) @[db-will] **tw@Oreoxmt** <!--2030-->

    Introduces a new `redact-info-log` parameter, allowing DM to replace sensitive query arguments with `?` placeholders in DM logs. You can enable this feature by setting `redact-info-log = true` in the DM-worker configuration file or passing `--redact-info-log=true` at startup. This change only redacts query arguments (not entire SQL statements) and requires a DM-worker restart to take effect.

    For more information, see [documentation](/dm/dm-worker-configuration-file.md).

* Ensure TiDB Lightning compatibility with TiDB `sql_require_primary_key=ON` [#57479](https://github.com/pingcap/tidb/issues/57479) @[lance6716] **tw@Oreoxmt** <!--2026-->

    When `sql_require_primary_key=ON` is enabled in TiDB, tables must have a primary key. TiDB Lightning now adds a default primary key to its internal error-logging and conflict-detection tables (`conflict_error_v4`, `type_error_v2`, and `conflict_records_v2`), preventing table-creation failures. If you rely on these internal tables for automation, confirm the new naming and schema changes (primary key added), as scripts referencing older table names might need updates.

* Migrate sync-diff-inspector from `pingcap/tidb-tools` to `pingcap/tiflow` repository [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh) **tw@Oreoxmt** <!--2070-->

    Starting from v9.0.0, the sync-diff-inspector tool is moved from the [`pingcap/tidb-tools`](https://github.com/pingcap/tidb-tools) repository to [`pingcap/tiflow`](https://github.com/pingcap/tiflow). This change unifies replication and migration tools ([DM](/dm/dm-overview.md), [TiCDC](/ticdc/ticdc-overview.md), and [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)) into a single repository.

    For TiDB v9.0.0 and later versions, you can install sync-diff-inspector using one of the following methods:

    - TiUP: `tiup install sync-diff-inspector`
    - Docker image: `docker pull pingcap/sync-diff-inspector:latest`
    - Binary package: [TiDB Toolkit](/download-ecosystem-tools.md)

  The [`pingcap/tidb-tools`](https://github.com/pingcap/tidb-tools) repository is now archived. If you previously installed sync-diff-inspector from `tidb-tools`, switch to TiUP, Docker, or the TiDB Toolkit.

    For more information, see [documentation](/sync-diff-inspector/sync-diff-inspector-overview.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.5.0 to the current version (v9.0.0). If you are upgrading from v8.4.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* TiDB Lightning internal error-logging and conflict-detection tables names changed to `conflict_error_v4`, `type_error_v2`, and `conflict_records_v2`, and now have primary keys. If you rely on these internal tables for automation, confirm the new naming and schema changes [#57479](https://github.com/pingcap/tidb/issues/57479) @[lance6716]

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| DM | [--redact-info-log](/dm/dm-command-line-flags/#--redact-info-log) | Newly added | Controls whether DM replaces sensitive query arguments with ? placeholders in logs. The default value is false. When set to true, query arguments in DM logs are redacted. This parameter only redacts query arguments (not entire SQL statements), and requires a DM-worker restart to take effect. |
|  |  |  | |

### Offline package changes

Starting from v9.0.0, the offline package location of the [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) tool in the `TiDB-community-toolkit` [binary package](/binary-package.md) is changed from `sync_diff_inspector` to `tiflow-{version}-linux-{arch}.tar.gz`.

### Operating system and platform requirement changes

Before upgrading TiDB, ensure that your operating system version meets the [OS and platform requirements](/hardware-and-software-requirements.md#os-and-platform-requirements).

## Removed features

* The following feature has been removed:



* The following features are planned for removal in future versions:

    * Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Deprecated features

The following features are planned for deprecation in future versions:

* In v8.0.0, TiDB introduces the [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) system variable to control whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
* In v7.5.0, TiDB introduces the [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) system variable. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
* It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
* In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, this system variable will be deprecated.
* In v5.1, TiDB introduces the [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) system variable to control whether to enable the dynamic pruning mode for partitioned tables. Starting from v8.5.0, a warning is returned when you set this variable to `static` or `static-only`. In future versions, this system variable will be deprecated.
* The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.
* Starting from v6.3.0, partitioned tables use [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) by default. Compared with static pruning mode, dynamic pruning mode supports features such as IndexJoin and plan cache with better performance. Therefore, static pruning mode will be deprecated.

## Improvements

+ TiDB

  

+ TiKV



+ PD



+ TiFlash



+ Tools

    + Backup & Restore (BR)

        
    + TiDB Data Migration (DM)

       
## Bug fixes

+ TiDB

    

+ TiKV

    

+ PD

   

+ TiFlash

   

+ Tools

    + Backup & Restore (BR)

        

    + TiCDC

        

    + TiDB Lightning

        

## Performance test

To learn about the performance of TiDB v9.0.0, you can refer to the [performance test reports](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights) of the TiDB Cloud Dedicated cluster.

## Contributors

We would like to thank the following contributors from the TiDB community:
