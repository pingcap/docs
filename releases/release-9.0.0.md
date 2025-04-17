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

* Support pushing down the following function to TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1918-->

    * `TRUNCATE()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Support pushing down window functions that contain the following aggregation functions to TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**<!--1382-->

    * `MAX`
    * `MIN`
    * `COUNT`
    * `SUM`
    * `AVG`

    For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Support pushing down the following date functions to TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) @[gengliqi](https://github.com/gengliqi) **tw@Oreoxmt** <!--1837-->

    * `FROM_UNIXTIME()`
    * `TIMESTAMPDIFF()`
    * `UNIX_TIMESTAMP()`

  For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* TiFlash supports a new storage format to improve the scanning efficiency of string data [#9673](https://github.com/pingcap/tiflash/issues/9673) @[JinheLin](https://github.com/JinheLin) **tw@qiancai**<!--2066-->

    Before v9.0.0, TiFlash stores string data in a format that requires to read each row individually when scanning the data, which is inefficient for short strings. In v9.0.0, TiFlash introduces a new storage format that optimizes the storage of strings, improving the scanning efficiency of strings shorter than 64 bytes without affecting the storage and scanning performance of other data.

    - For newly deployed TiDB clusters with v9.0.0 or a later version, TiFlash uses the new storage format by default.
    - For TiDB clusters upgraded to v9.0.0 or a later version, it is recommended to read [TiFlash upgrade guide](/tiflash-upgrade-guide.md) before the upgrade.
        - If [`format_version`](/tiflash/tiflash-configuration.md#format_version) is not specified for TiFlash before the upgrade, TiFlash uses the new storage format by default after the upgrade.
        - If [`format_version`](/tiflash/tiflash-configuration.md#format_version) is specified for TiFlash before the upgrade, the value of `format_version` remains unchanged after the upgrade, and TiFlash continues to use the storage format specified by `format_version`. To enable the new storage format in this case, set the `format_version` parameter to `8` in the TiFlash configuration file. After the configuration takes effect, new data written to TiFlash will use the new storage format, while the storage format of existing data will remain unchanged.

  For more information, see [user documentation](/tiflash/tiflash-configuration.md#format_version).

### Availability

* TiProxy officially supports the traffic replay feature (GA) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832) tw@hfxsd<!--2062-->

    In TiProxy v1.3.0, the traffic replay feature is released as an experimental feature. In TiProxy v1.4.0, the traffic replay feature becomes generally available (GA). TiProxy provides specialized SQL commands for traffic capture and replay. This feature lets you easily capture access traffic from TiDB production clusters and replay it at a specified rate in test clusters, facilitating business validation.
    
    For more information, see [documentation](/tiproxy/tiproxy-traffic-replay.md).

### Reliability

* Introduce a new system variable `max_user_connections` to limit the number of connections that different users can establish [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau) tw@hfxsd<!--2017-->

    Starting from v9.0.0, you can use the `max_user_connections` system variable to limit the number of connections a single user can establish to a single TiDB node. This helps prevent issues where excessive [token](/tidb-configuration-file.md/#token-limit) consumption by one user causes delays in responding to requests from other users.
    
    For more information, see [documentation](/system-variables.md/#max_user_connections-new-in-v900)

### SQL

* Support creating global indexes on non-unique columns of partitioned tables [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss) **tw@qiancai**<!--2057-->

    Starting from v8.3.0, you can create global indexes on unique columns of partitioned tables in TiDB to improve query performance. However, creating global indexes on non-unique columns was not supported. Starting from v9.0.0, TiDB removes this restriction, enabling you to create global indexes on non-unique columns of partitioned tables, enhancing the usability of global indexes.

    For more information, see [documentation](/partitioned-table.md#global-index).

### DB operations

* TiDB Index Advisor [#12303](https://github.com/pingcap/tidb/issues/12303) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--2081-->

    Index design is essential for database performance optimization. Starting from v8.5.0, TiDB introduces the Index Advisor feature and continues to improve and enhance it. This feature analyzes high-frequency query patterns, recommends optimal indexing strategies, helps you tune performance more efficiently, and lowers the barrier to index design.

    You can use the [`RECOMMEND INDEX`](/index-advisor.md#recommend-indexes-using-the-recommend-index-statement) SQL statement to generate index recommendations for a single query or automatically analyze high-frequency SQL statements from historical workloads for batch recommendations. The recommendation results are stored in the `mysql.index_advisor_results` table. You can query this table to view the recommended indexes.

    For more information, see [documentation](/index-advisor.md).

### Observability

* Add the TiDB Workload Repository feature to support persisting historical workload data into TiKV [#58247](https://github.com/pingcap/tidb/issues/58247) @[xhebox](https://github.com/xhebox) @[henrybw](https://github.com/henrybw) @[wddevries](https://github.com/wddevries) **tw@lilin90**<!--1953-->

    Many frequently updated workload metrics and status information are maintained in the memory of the instance. Such historical workload data can be persisted as part of the database for the following purposes:

    * **Troubleshooting:** when diagnosing issues, it is necessary to review historical activities and events. Persisted workload data can help you revisit the state changes during a specific time period, identify anomalies, or precisely locate the specific behavior of a database session or SQL statement at a particular moment.
    * **Automation:** database autonomy is an inevitable trend to enhance user experience and lower usage barriers. Achieving automated database tuning requires historical data. Based on persisted historical workload data, TiDB can gradually move towards intelligent recommendations, such as Index Advisor, Statistics Advisor, and SQL Binding Advisor.     
    
  In v9.0.0, you can enable the Workload Repository by setting the [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest-new-in-v900) system variable. TiDB continuously writes snapshots of certain memory tables into the `workload_schema`, persisting them in TiKV. This feature is disabled by default. By persisting historical workload data, TiDB can better facilitate troubleshooting and recommendations. In the future, a series of automated tools based on historical workload data will be introduced to enhance the user experience in database operations and diagnostics. The persisted memory tables are categorized into two types:

    - **Memory tables storing cumulative metrics**: these tables are larger in size, and their snapshots and storage costs are relatively high. Snapshots are taken in batches based on the [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval-new-in-v900) setting, with a minimum interval of 15 minutes. By comparing the changes between any two snapshots, you can calculate the incremental metrics over a specific period. These tables include:

        - [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)
        - [`INFORMATION_SCHEMA.TIDB_STATEMENTS_STATS`](/statement-summary-tables.md) (Derived from `STATEMENTS_SUMMARY`, planned to replace it in the future.)
        - [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)
        - [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)
        - [`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)

    - **Memory tables storing real-time states**: these tables are updated frequently and are usually smaller in size. Snapshots with very short intervals are necessary for them to be effective. You can specify the interval using the [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval-new-in-v900) system variable, which defaults to 5 seconds. Setting it to `0` disables snapshots for this type of tables. These tables include:

        - [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
        - [`INFORMATION_SCHEMA.DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
        - [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)
        - [`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)
        - [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)

  Data in the Workload Repository is automatically cleaned up, with a default retention period of 7 days. You can modify the retention period by setting the [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days-new-in-v900) system variable.

      For more information, see [documentation](/workload-repository.md).

 * SQL cross-AZ traffic monitoring [#57543](https://github.com/pingcap/tidb/issues/57543) @[nolouch](https://github.com/nolouch) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--2021-->

    Deploying TiDB clusters across Availability Zones (AZs) enhances the disaster recovery capability. However, in cloud environments, cross-AZ deployments incur additional network traffic costs. For example, AWS charges for both cross-region and cross-AZ traffic. Therefore, for TiDB clusters running on cloud services, accurately monitoring and analyzing network traffic is essential for cost control.

    Starting from v9.0.0, TiDB records the network traffic generated during SQL processing and distinguishes cross-AZ traffic. TiDB writes this data to the [`statements_summary` table](/statement-summary-tables.md) and [slow query logs](/identify-slow-queries.md). This feature helps you track major data transmission paths within TiDB clusters, analyze the sources of cross-AZ traffic, and better understand and control related costs.

    Note that the current version includes only **query** traffic **within the cluster** (between TiDB, TiKV, and TiFlash) and does not include traffic caused by DML or DDL operations. Additionally, the recorded traffic data reflects unpacked bytes rather than the actual physical bytes transmitted, so it cannot be used for billing purposes.

    For more information, see [documentation](/statement-summary-tables.md#statements_summary-fields-description).

* Optimize the `execution info` in the output of `EXPLAIN ANALYZE` [#56232](https://github.com/pingcap/tidb/issues/56232) @[yibin87](https://github.com/yibin87) tw@hfxsd<!--1697-->

    [`EXPLAIN ANALYZE`](https://github.com/sql-statements/sql-statement-explain-analyze.md) executes SQL statements and records execution details in the `execution info` column. The same information is captured in the [slow query log](https://github.com/identify-slow-queries.md). These details are crucial for analyzing and understanding the time spent on SQL execution.

    In v9.0.0, the `execution info` output is optimized for clearer representation of each metric. For example, `time` now refers to the wall-clock time for operator execution, `loops` indicates how many times the current operator is called by its parent operator, and `total_time` represents the cumulative duration of all concurrent executions. These optimizations help you better understand the SQL execution process and devise more targeted optimization strategies.

    For more information, see [documentation](/sql-statements/sql-statement-explain-analyze.md).

### Security

### Data migration

* Support query argument redaction in Data Migration (DM) logs [#11489](https://github.com/pingcap/tiflow/issues/11489) @[db-will](https://github.com/db-will) **tw@Oreoxmt** <!--2030-->

    Starting from v9.0.0, you can use the `redact-info-log` configuration item to enable the DM log redaction feature. When enabled, query arguments that contain sensitive data in DM logs are replaced with the `?` placeholder. To enable this feature, set `redact-info-log` to `true` in the DM-worker configuration file or pass `--redact-info-log=true` when starting DM. This feature only redacts query arguments, not the entire SQL statement, and requires a DM-worker restart to take effect.

    For more information, see [documentation](/dm/dm-worker-configuration-file.md#redact-info-log-new-in-v900).

* TiDB Lightning supports compatibility with `sql_require_primary_key=ON` in TiDB [#57479](https://github.com/pingcap/tidb/issues/57479) @[lance6716](https://github.com/lance6716) **tw@Oreoxmt** <!--2026-->

    When the system variable [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-new-in-v630) is enabled in TiDB, tables are required to have a primary key. To avoid table creation failures, TiDB Lightning adds a default primary key to its internal error-logging and conflict-detection tables (`conflict_error_v4`, `type_error_v2`, and `conflict_records_v2`). If you have automation scripts that depend on these internal tables, update them to accommodate the new schema, which now includes a primary key.

* Migrate sync-diff-inspector from `pingcap/tidb-tools` to `pingcap/tiflow` repository [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh) **tw@Oreoxmt** <!--2070-->

    Starting from v9.0.0, the sync-diff-inspector tool is moved from the [`pingcap/tidb-tools`](https://github.com/pingcap/tidb-tools) repository to [`pingcap/tiflow`](https://github.com/pingcap/tiflow). With this change, sync-diff-inspector is now maintained in the same repository as [DM](/dm/dm-overview.md) and [TiCDC](/ticdc/ticdc-overview.md), which unifies the management of these replication and migration tools.

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
* Starting from v9.0.0, TiFlash changes the storage format of string data to optimize the string read and write performance. Therefore, after TiFlash is upgraded to v9.0.0 or a later version, in-place downgrading to the original version is not supported. For more information, see [TiFlash upgrade guide](/tiflash-upgrade-guide.md).
* Starting from v9.0.0, TiCDC introduces a [security mechanism](/ticdc/ticdc-manage-changefeed.md#security-mechanism) to prevent users from accidentally configuring the same TiDB cluster as both the upstream and downstream for data replication, which could lead to circular replication and data anomalies. When creating, updating, or resuming a replication task, TiCDC automatically checks whether the upstream and downstream TiDB clusters have the same `cluster_id`. If TiCDC detects the same `cluster_id` for both the upstream and downstream, it will reject the task.

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| `txn_scope` | Deleted | Starting from v9.0.0, this variable is removed. |
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840) | Modified | Changes the default value from `legacy` to `optimized` after further tests, meaning that TiDB uses the [optimized version of hash join](/sql-statements/sql-statement-explain-analyze.md#hashjoinv2) to execute hash join for better performance. |
| [`max_user_connections`](/system-variables.md/#max_user_connections-new-in-v900) | Newly added | Controls the number of connections a single user can establish to a single TiDB node, preventing excessive [token](/tidb-configuration-file.md/#token-limit) consumption by one user from delaying responses to other users' requests. |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660) | Newly added | Adds the `3` option, which enables the new string data exchange format for TiFlash. When this variable is not specified, TiDB automatically selects the latest version `3` of the MPP execution plan to improve the serialization and deserialization efficiency of strings, thereby enhancing query performance. |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) | Newly added | Changes the default value from `OFF` to `ON`. When it is `ON`, TiDB evenly distributes Region information requests to all PD servers, so PD followers can also handle Region requests, reducing the CPU pressure on the PD leader. Starting from v9.0.0, Region information requests from TiDB Lightning are also evenly sent to all PD nodes when the value is `ON`. |
| [`tidb_pipelined_dml_resource_policy`](/system-variables.md#tidb_pipelined_dml_resource_policy-new-in-v900) | Newly added | Controls the resource usage policy for [Pipelined DML](/pipelined-dml.md). It takes effect only when [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) is set to `bulk`. |
| [`tidb_accelerate_user_creation_update`](/system-variables.md/#tidb_accelerate_user_creation_update-new-in-v900)| Newly added | Improves the performance of creating and modifying users in scenarios with hundreds of thousands to millions of users. |
| [`tidb_max_dist_task_nodes`](/system-variables.md/#tidb_max_dist_task_nodes-new-in-v900)| Newly added | Controls the maximum number of TiDB nodes available for the Distributed eXecution Framework (DXF) tasks. The default value is `-1`, which enables automatic mode. In this mode, the system automatically selects an appropriate number of nodes. |
| [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval-new-in-v900) | Newly added | Controls the sampling interval for the [Workload Repository](/workloadrepo.md)'s Time-based Sampling Process. |
| [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest-new-in-v900)| Newly added | Controls the destination of the [Workload Repository](/workloadrepo.md. The default value is `''`, which means to disable the workload repository. The value `'table'` enables the workload repository to write data into TiKV.| 
| [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days-new-in-v900) | Newly added | Controls the number of days that [Workload Repository](/workloadrepo.md) data is retained. |
| [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval-new-in-v900) | Newly added | Controls the sampling interval for the [Workload Repository](/workloadrepo.md)'s Snapshot Sampling Process. |
|  |  |  |
|  |  |  |
|  |  |  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`hashagg_use_magic_hash`](/tikv-configuration-file.md#hashagg_use_magic_hash-new-in-v900) | Newly added | Controls the hash function TiFlash uses for aggregation. |
| TiKV | [`storage.max-ts.action-on-invalid-update`](/tikv-configuration-file.md#action-on-invalid-update-new-in-v900) | Newly added | Determines how TiKV handles invalid `max-ts` update requests. The default value is `"panic"`, which means that TiKV panics when it detects invalid `max-ts` update requests. |
| TiKV | [`storage.max-ts.cache-sync-interval`](/tikv-configuration-file.md#cache-sync-interval-new-in-v900) | Newly added | Controls the interval at which TiKV updates its local PD TSO cache. The default value is `"15s"`. |
| TiKV | [`storage.max-ts.max-drift`](/tikv-configuration-file.md#max-drift-new-in-v900) | Newly added | Specifies the maximum time by which the timestamp of a read or write request can exceed the PD TSO cached in TiKV. The default value is `"60s"`. |
| TiFlash| [`format_version`](/tiflash/tiflash-configuration.md#format_version) | Modified | Changes the default value from `7` to `8`, which means the default DTFile file format for v9.0.0 or a later version is `8`. This new format supports a new string serialization scheme that improves string read and write performance. |
| TiCDC | [`newarch`](/ticdc/ticdc-server-config.md#newarch) | Newly added | Controls whether to enable the [TiCDC new architecture](/ticdc/ticdc-new-arch.md). By default, `newarch` is not specified, indicating that the old architecture is used. `newarch` applies only to the new architecture. If `newarch` is added to the configuration file of the TiCDC old architecture, it might cause parsing failures. |
| BR | [`--checkpoint-storage`](br/br-checkpoint-restore.md#implementation-details-store-checkpoint-data-in-the-external-storage) | Newly added | Specifies the external storage for BR to store checkpoint data. |
| DM | [`redact-info-log`](/dm/dm-worker-configuration-file.md#redact-info-log-new-in-v900) | Newly added | Controls whether to enable DM log redaction. |
| TiProxy | [`enable-traffic-replay`](/tiproxy/tiproxy-configuration.md#enable-traffic-replay)  | Newly added | Specifies whether to enable [traffic replay](/tiproxy/tiproxy-traffic-replay.md). If it is set to `false`, traffic capture and replay operations will result in errors. |
| TiProxy | [`encryption-key-path`](/tiproxy/tiproxy-configuration.md#encryption-key-path)  | Newly added | Specifies the file path of the key used to encrypt the traffic files during traffic capture. |
|  |  |  | |

### Offline package changes

Starting from v9.0.0, the offline package location of the [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) tool in the `TiDB-community-toolkit` [binary package](/binary-package.md) is changed from `sync_diff_inspector` to `tiflow-{version}-linux-{arch}.tar.gz`.

### System table changes

| System table | Change type | Description |
| -------- | -------- | -------- |
| [`mysql.tidb`](/mysql-schema/mysql-schema.md#cluster-status-system-tables) | Modified | Adds the `cluster_id` field, which represents the unique identifier of a TiDB cluster. Note that `cluster_id` is read-only and cannot be modified. |

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
