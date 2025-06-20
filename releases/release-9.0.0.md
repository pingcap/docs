---
title: TiDB 9.0.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 9.0.0.
---

# TiDB 9.0.0 Release Notes

<EmailSubscriptionWrapper />

Release date: xx xx, 2025

TiDB version: 9.0.0

<!--
Quick access: [Quick start](https://docs.pingcap.com/tidb/v9.0/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v9.0/production-deployment-using-tiup)
-->

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
    <td rowspan="2">Scalability and Performance</td>
    <td><a href="https://docs.pingcap.com/tidb/dev/pd-microservices/">The microservice mode</a> supported by PD is generally available (GA) (introduced in v8.0.0)</td>
    <td>The PD microservice mode decouples different functional modules of PD into independent services, improving system scalability, stability, and deployment flexibility. It provides a more robust architectural foundation for large-scale cluster deployments.</td>
  </tr>
    <tr>
    <td>Point-in-time recovery (PITR) supports recovery from <a href="https://docs.pingcap.com/tidb/dev/br-compact-log-backup/">compacted log backups</a> for faster restores</td>
    <td>Starting from v9.0.0, the log backup feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. These SST files can now be restored into the cluster much more quickly than reapplying the original logs, resulting in improved recovery performance.</td>
  </tr>
  <tr>
    <td rowspan="1">Reliability and availability</td>
    <td><a href="https://docs.pingcap.com/tidb/dev/tiproxy-traffic-replay/">The TiProxy traffic replay feature</a> is generally available (GA) (introduced in v8.4.0)</td>
    <td>Before performing critical operations such as cluster upgrades, migrations, or deployment changes, use TiProxy to capture the real workload from the production TiDB cluster and replay it on the target test cluster. It helps validate performance and ensure the success of the changes.</td>
  </tr>
  <tr>
    <td rowspan="3">DB Operations and Observability</td>
    <td>Add the <a href="https://docs.pingcap.com/tidb/dev/workload-repository/">TiDB Workload Repository</a> feature to support persisting historical workload data into TiKV</td>
    <td>TiDB Workload Repository can persist the historical runtime status of the database, significantly improving the efficiency of diagnosing past failures and performance issues. It helps you quickly identify and resolve problems, while also providing critical data for health checks and automatic tuning.</td>
  </tr>
  <tr>
    <td>TiDB Index Advisor</td>
    <td>TiDB Index Advisor analyzes actual query workloads to automatically identify missing or redundant indexes. It helps you optimize indexes without requiring deep knowledge of your application. This feature reduces the cost of manual analysis and tuning, and improves query performance and system stability.</td>
  </tr>
  <tr>
    <td>SQL cross-AZ traffic monitoring</td>
    <td>This feature helps you identify cross-availability zone (AZ) network traffic caused by SQL queries in a TiDB cluster. It enables you to analyze traffic sources, optimize deployment architecture, and control cross-AZ data transfer costs in cloud environments, thus improving resource efficiency and cost visibility.</td>
  </tr>
  <tr>
    <td rowspan="3">Data Migration</td>
    <td>Query argument redaction in Data Migration (DM) logs</td>
    <td>Data Migration (DM) introduces the <code>redact-info-log</code> configuration item to redact query arguments in DM logs, preventing sensitive data from appearing in logs.</td>
  </tr>
  <tr>
    <td>TiDB Lightning supports compatibility with <code>sql_require_primary_key=ON</code> in TiDB</td>
    <td>When the <code>sql_require_primary_key</code> system variable is enabled in TiDB, TiDB Lightning automatically adds a default primary key to its internal error-logging and conflict-detection tables during data import to prevent table creation failures.</td>
  </tr>
  <tr>
    <td>Migrate sync-diff-inspector from <code>pingcap/tidb-tools</code> to <code>pingcap/tiflow</code> repository</td>
    <td>sync-diff-inspector is now maintained with other migration and replication tools such as DM and TiCDC in the <code>pingcap/tiflow</code> repository. You can now install sync-diff-inspector using TiUP or a dedicated Docker image.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* PD supports the microservice mode (GA) [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing)

    In v8.0.0, the PD microservice mode is released as an experimental feature. Starting from v9.0.0, the PD microservice mode is generally available (GA). This mode splits the timestamp allocation and cluster scheduling functions of PD into separate microservices that can be deployed independently, thereby enhancing performance scalability for PD and addressing performance bottlenecks of PD in large-scale clusters.

    - `tso` microservice: provides monotonically increasing timestamp allocation for the entire cluster.
    - `scheduling` microservice: provides scheduling functions for the entire cluster, including but not limited to load balancing, hot spot handling, replica repair, and replica placement.

    Each microservice is deployed as an independent process. If you configure more than one replica for a microservice, the microservice automatically implements a primary-secondary fault-tolerant mode to ensure high availability and reliability of the service.

    For more information, see [documentation](/pd-microservices.md).

### Performance

* In scenarios with hundreds of thousands to millions of users, the performance of creating and modifying users has improved by 77 times [#55563](https://github.com/pingcap/tidb/issues/55563) @[tiancaiamao](https://github.com/tiancaiamao)

    In previous versions, when the number of users in a cluster exceeded 200,000, the QPS for creating and modifying users drops to 1. In certain SaaS environments, if there is a need to create millions of users and periodically update user passwords in bulk, it can take up to 2 days or more, which is unacceptable for some SaaS businesses.

    TiDB v9.0.0 optimizes the performance of these DCL (Data Control Language) operations, allowing 2 million users to be created in just 37 minutes. This greatly enhances the execution performance of DCL statements and improves the user experience of TiDB in such SaaS scenarios.

    For more information, see [documentation](/system-variables.md#tidb_accelerate_user_creation_update-new-in-v900).

* Support pushing down the following function to TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge)

    * `TRUNCATE()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Support pushing down window functions that contain the following aggregation functions to TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) [#59509](https://github.com/pingcap/tidb/issues/59509) @[xzhangxian1008](https://github.com/xzhangxian1008)

    * `MAX()`
    * `MIN()`
    * `COUNT()`
    * `SUM()`
    * `AVG()`

    For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Support pushing down the following date functions to TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) [#18184](https://github.com/tikv/tikv/issues/18184) [#58940](https://github.com/pingcap/tidb/issues/58940) [#59497](https://github.com/pingcap/tidb/issues/59497) @[wshwsh12](https://github.com/wshwsh12) @[xzhangxian1008] @[gengliqi](https://github.com/gengliqi)

    * `FROM_UNIXTIME()`
    * `TIMESTAMPDIFF()`
    * `UNIX_TIMESTAMP()`

  For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* TiFlash supports a new storage format to improve the scanning efficiency of string data [#9673](https://github.com/pingcap/tiflash/issues/9673) @[JinheLin](https://github.com/JinheLin)

    Before v9.0.0, TiFlash stores string data in a format that requires to read each row individually when scanning the data, which is inefficient for short strings. In v9.0.0, TiFlash introduces a new storage format that optimizes the storage of strings, improving the scanning efficiency of strings shorter than 64 bytes without affecting the storage and scanning performance of other data.

    - For newly deployed TiDB clusters with v9.0.0 or a later version, TiFlash uses the new storage format by default.
    - For TiDB clusters upgraded to v9.0.0 or a later version, it is recommended to read [TiFlash upgrade guide](/tiflash-upgrade-guide.md) before the upgrade.
        - If [`format_version`](/tiflash/tiflash-configuration.md#format_version) is not specified for TiFlash before the upgrade, TiFlash uses the new storage format by default after the upgrade.
        - If [`format_version`](/tiflash/tiflash-configuration.md#format_version) is specified for TiFlash before the upgrade, the value of `format_version` remains unchanged after the upgrade, and TiFlash continues to use the storage format specified by `format_version`. To enable the new storage format in this case, set the `format_version` configuration item to `8` in the TiFlash configuration file. After the configuration takes effect, new data written to TiFlash will use the new storage format, while the storage format of existing data will remain unchanged.

  For more information, see [user documentation](/tiflash/tiflash-configuration.md#format_version).

* Point-in-time recovery (PITR) supports recovery from compacted log backups for faster restores [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen)

    Starting from v9.0.0, the compact log backup feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. This results in the following improvements:

    - SST files can be quickly imported into the cluster, **improving recovery performance**.
    - Redundant data is removed during compaction, **reducing storage space consumption**.
    - You can set longer full backup intervals while ensuring the Recovery Time Objective (RTO), **reducing the impact on applications**.

  For more information, see [documentation](/br/br-compact-log-backup.md).

### Availability

* TiProxy officially supports the traffic replay feature (GA) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832)

    In TiProxy v1.3.0, the traffic replay feature is released as an experimental feature. In TiProxy v1.4.0, the traffic replay feature becomes generally available (GA). TiProxy provides specialized SQL commands for traffic capture and replay. This feature lets you easily capture access traffic from TiDB production clusters and replay it at a specified rate in test clusters, facilitating business validation.
    
    For more information, see [documentation](/tiproxy/tiproxy-traffic-replay.md).

### Reliability

* Introduce a new system variable `max_user_connections` to limit the number of connections that different users can establish [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau)

    Starting from v9.0.0, you can use the `max_user_connections` system variable to limit the number of connections that a single user can establish to a single TiDB node. This helps prevent issues where excessive [token](/tidb-configuration-file.md#token-limit) consumption by one user causes delays in responding to requests from other users.
    
    For more information, see [documentation](/system-variables.md#max_user_connections-new-in-v900).

### SQL

* Support creating global indexes on non-unique columns of partitioned tables [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)

    Starting from v8.3.0, you can create global indexes on unique columns of partitioned tables in TiDB to improve query performance. However, creating global indexes on non-unique columns was not supported. Starting from v9.0.0, TiDB removes this restriction, enabling you to create global indexes on non-unique columns of partitioned tables, enhancing the usability of global indexes.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

### DB operations

* TiDB Index Advisor [#12303](https://github.com/pingcap/tidb/issues/12303) @[qw4990](https://github.com/qw4990)

    Index design is essential for database performance optimization. Starting from v8.5.0, TiDB introduces the Index Advisor feature and continues to improve and enhance it. This feature analyzes high-frequency query patterns, recommends optimal indexing strategies, helps you tune performance more efficiently, and lowers the barrier to index design.

    You can use the [`RECOMMEND INDEX`](/index-advisor.md#recommend-indexes-using-the-recommend-index-statement) SQL statement to generate index recommendations for a single query or automatically analyze high-frequency SQL statements from historical workloads for batch recommendations. The recommendation results are stored in the `mysql.index_advisor_results` table. You can query this table to view the recommended indexes.

    For more information, see [documentation](/index-advisor.md).

* Improve the compatibility between ongoing log backup and snapshot restore [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger)

    Starting from v9.0.0, when a log backup task is running, if the conditions are met, you can still perform snapshot restore and allow the restored data to be properly recorded by the ongoing log backup. This enables ongoing log backups to proceed without having to stop them during the restore procedure.

    For more information, see [documentation](/br/br-pitr-manual.md#compatibility-between-ongoing-log-backup-and-snapshot-restore).

### Observability

* Add the TiDB Workload Repository feature to support persisting historical workload data into TiKV [#58247](https://github.com/pingcap/tidb/issues/58247) @[xhebox](https://github.com/xhebox) @[henrybw](https://github.com/henrybw) @[wddevries](https://github.com/wddevries)

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

 * SQL cross-AZ traffic monitoring [#57543](https://github.com/pingcap/tidb/issues/57543) @[nolouch](https://github.com/nolouch) @[yibin87](https://github.com/yibin87)

    Deploying TiDB clusters across Availability Zones (AZs) enhances the disaster recovery capability. However, in cloud environments, cross-AZ deployments incur additional network traffic costs. For example, AWS charges for both cross-region and cross-AZ traffic. Therefore, for TiDB clusters running on cloud services, accurately monitoring and analyzing network traffic is essential for cost control.

    Starting from v9.0.0, TiDB records the network traffic generated during SQL processing and distinguishes cross-AZ traffic. TiDB writes this data to the [`statements_summary` table](/statement-summary-tables.md) and [slow query logs](/identify-slow-queries.md). This feature helps you track major data transmission paths within TiDB clusters, analyze the sources of cross-AZ traffic, and better understand and control related costs.

    Note that the current version includes only **query** traffic **within the cluster** (between TiDB, TiKV, and TiFlash) and does not include traffic caused by DML or DDL operations. Additionally, the recorded traffic data reflects unpacked bytes rather than the actual physical bytes transmitted, so it cannot be used for billing purposes.

    For more information, see [documentation](/statement-summary-tables.md#statements_summary-fields-description).

* Optimize the `execution info` in the output of `EXPLAIN ANALYZE` [#56232](https://github.com/pingcap/tidb/issues/56232) @[yibin87](https://github.com/yibin87)

    [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) executes SQL statements and records execution details in the `execution info` column. The same information is captured in the [slow query log](/identify-slow-queries.md). These details are crucial for analyzing and understanding the time spent on SQL execution.

    In v9.0.0, the `execution info` output is optimized for clearer representation of each metric. For example, `time` now refers to the wall-clock time for operator execution, `loops` indicates how many times the current operator is called by its parent operator, and `total_time` represents the cumulative duration of all concurrent executions. These optimizations help you better understand the SQL execution process and devise more targeted optimization strategies.

    For more information, see [documentation](/sql-statements/sql-statement-explain-analyze.md).

### Security

### Data migration

* TiCDC introduces a new architecture for improved performance, scalability, and stability (experimental) [#442](https://github.com/pingcap/ticdc/issues/442) @[CharlesCheung96](https://github.com/CharlesCheung96)

    In v9.0.0, TiCDC introduces a new architecture (experimental) that improves real-time data replication performance, scalability, and stability while reducing resource costs. This new architecture redesigns TiCDC core components and optimizes its data processing workflows.

    With this new architecture, TiCDC can now scale its replication capability nearly linearly and replicate millions of tables with lower resource costs. Changefeed latency is reduced and performance is more stable in scenarios with high traffic, frequent DDL operations, and during cluster scaling events.

    For more information, see [documentation](/ticdc/ticdc-new-arch.md).

* TiCDC supports DDL events and WATERMARK events for the Debezium protocol [#11566](https://github.com/pingcap/tiflow/issues/11566) @[wk989898](https://github.com/wk989898)

    TiCDC now supports DDL and WATERMARK event types in Debezium style output. After an upstream DDL operation is successfully executed, TiCDC encodes the DDL event into a Kafka message with the key and message in a Debezium style format. The WATERMARK event, a TiCDC extension (available when [`enable-tidb-extension`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) is enabled in the Kafka sink), represents a special point in time and indicates that the events received before this point are complete.

    For more information, see [documentation](/ticdc/ticdc-debezium.md).

* TiCDC adds safeguards to avoid replicating back to the same TiDB cluster [#11767](https://github.com/pingcap/tiflow/issues/11767) [#12062](https://github.com/pingcap/tiflow/issues/12062) @[wlwilliamx](https://github.com/wlwilliamx)

    TiCDC supports replicating data from an upstream TiDB cluster to multiple downstream systems, including other TiDB clusters. In versions before v9.0.0, if TiCDC is misconfigured to use the same TiDB cluster as both the source and the target, it could create a replication loop and cause data consistency issues. Starting from v9.0.0, TiCDC automatically checks whether the source and target TiDB clusters are the same, preventing this misconfiguration issue.

    For more information, see [documentation](/ticdc/ticdc-manage-changefeed.md#security-mechanism).

* Support query argument redaction in Data Migration (DM) logs [#11489](https://github.com/pingcap/tiflow/issues/11489) @[db-will](https://github.com/db-will)

    Starting from v9.0.0, you can use the `redact-info-log` configuration item to enable the DM log redaction feature. When enabled, query arguments that contain sensitive data in DM logs are replaced with the `?` placeholder. To enable this feature, set `redact-info-log` to `true` in the DM-worker configuration file or pass `--redact-info-log=true` when starting DM. This feature only redacts query arguments, not the entire SQL statement, and requires a DM-worker restart to take effect.

    For more information, see [documentation](/dm/dm-worker-configuration-file.md#redact-info-log-new-in-v900).

* TiDB Lightning supports compatibility with `sql_require_primary_key=ON` in TiDB [#57479](https://github.com/pingcap/tidb/issues/57479) @[lance6716](https://github.com/lance6716)

    When the system variable [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-new-in-v630) is enabled in TiDB, tables are required to have a primary key. To avoid table creation failures, TiDB Lightning adds a default primary key to its internal error-logging and conflict-detection tables (`conflict_error_v4`, `type_error_v2`, and `conflict_records_v2`). If you have automation scripts that depend on these internal tables, update them to accommodate the new schema, which now includes a primary key.

* Migrate sync-diff-inspector from `pingcap/tidb-tools` to `pingcap/tiflow` repository [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

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

* TiDB Lightning internal error-logging and conflict-detection tables names changed to `conflict_error_v4`, `type_error_v2`, and `conflict_records_v2`, and now have primary keys. If you rely on these internal tables for automation, confirm the new naming and schema changes [#57479](https://github.com/pingcap/tidb/issues/57479) @[lance6716](https://github.com/lance6716)
* Starting from v9.0.0, TiFlash changes the storage format of string data to optimize the string read and write performance. Therefore, after TiFlash is upgraded to v9.0.0 or a later version, in-place downgrading to the original version is not supported. For more information, see [TiFlash upgrade guide](/tiflash-upgrade-guide.md).
* Starting from v9.0.0, TiCDC introduces a [security mechanism](/ticdc/ticdc-manage-changefeed.md#security-mechanism) to prevent users from accidentally configuring the same TiDB cluster as both the upstream and downstream for data replication, which could lead to circular replication and data anomalies. When creating, updating, or resuming a replication task, TiCDC automatically checks whether the upstream and downstream TiDB clusters have the same `cluster_id`. If TiCDC detects the same `cluster_id` for both the upstream and downstream, it will reject the task.

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| `txn_scope` | Deleted | Starting from v9.0.0, this variable is removed. |
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840) | Modified | Changes the default value from `legacy` to `optimized` after further tests, meaning that TiDB uses the [optimized version of hash join](/sql-statements/sql-statement-explain-analyze.md#hashjoinv2) to execute hash join for better performance. |
| [`max_user_connections`](/system-variables.md#max_user_connections-new-in-v900) | Newly added | Controls the number of connections a single user can establish to a single TiDB node, preventing excessive [token](/tidb-configuration-file.md#token-limit) consumption by one user from delaying responses to other users' requests. |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660) | Newly added | Adds the `3` option, which enables the new string data exchange format for TiFlash. When this variable is not specified, TiDB automatically selects the latest version `3` of the MPP execution plan to improve the serialization and deserialization efficiency of strings, thereby enhancing query performance. |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) | Newly added | Changes the default value from `OFF` to `ON`. When it is `ON`, TiDB evenly distributes Region information requests to all PD servers, so PD followers can also handle Region requests, reducing the CPU pressure on the PD leader. Starting from v9.0.0, Region information requests from TiDB Lightning are also evenly sent to all PD nodes when the value is `ON`. |
| [`tidb_pipelined_dml_resource_policy`](/system-variables.md#tidb_pipelined_dml_resource_policy-new-in-v900) | Newly added | Controls the resource usage policy for [Pipelined DML](/pipelined-dml.md). It takes effect only when [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) is set to `bulk`. |
| [`tidb_accelerate_user_creation_update`](/system-variables.md#tidb_accelerate_user_creation_update-new-in-v900)| Newly added | Improves the performance of creating and modifying users in scenarios with hundreds of thousands to millions of users. |
| [`tidb_max_dist_task_nodes`](/system-variables.md#tidb_max_dist_task_nodes-new-in-v900)| Newly added | Controls the maximum number of TiDB nodes available for the Distributed eXecution Framework (DXF) tasks. The default value is `-1`, which enables automatic mode. In this mode, the system automatically selects an appropriate number of nodes. |
| [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval-new-in-v900) | Newly added | Controls the sampling interval for the [Workload Repository](/workload-repository.md)'s Time-based Sampling Process. |
| [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest-new-in-v900)| Newly added | Controls the destination of the [Workload Repository](/workload-repository.md). The default value is `''`, which means to disable the workload repository. The value `'table'` enables the workload repository to write data into TiKV.| 
| [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days-new-in-v900) | Newly added | Controls the number of days that [Workload Repository](/workload-repository.md) data is retained. |
| [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval-new-in-v900) | Newly added | Controls the sampling interval for the [Workload Repository](/workload-repository.md)'s Snapshot Sampling Process. |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`storage.max-ts.action-on-invalid-update`](/tikv-configuration-file.md#action-on-invalid-update-new-in-v900) | Newly added | Determines how TiKV handles invalid `max-ts` update requests. The default value is `"panic"`, which means that TiKV panics when it detects invalid `max-ts` update requests. |
| TiKV | [`storage.max-ts.cache-sync-interval`](/tikv-configuration-file.md#cache-sync-interval-new-in-v900) | Newly added | Controls the interval at which TiKV updates its local PD TSO cache. The default value is `"15s"`. |
| TiKV | [`storage.max-ts.max-drift`](/tikv-configuration-file.md#max-drift-new-in-v900) | Newly added | Specifies the maximum time by which the timestamp of a read or write request can exceed the PD TSO cached in TiKV. The default value is `"60s"`. |
| TiFlash | [`hashagg_use_magic_hash`](/tiflash/tiflash-configuration.md#hashagg_use_magic_hash-new-in-v900) | Newly added | Controls the hash function TiFlash uses for aggregation. |
| TiFlash| [`format_version`](/tiflash/tiflash-configuration.md#format_version) | Modified | Changes the default value from `7` to `8`, which means the default DTFile file format for v9.0.0 or a later version is `8`. This new format supports a new string serialization scheme that improves string read and write performance. |
| TiCDC | [`newarch`](/ticdc/ticdc-server-config.md#newarch) | Newly added | Controls whether to enable the [TiCDC new architecture](/ticdc/ticdc-new-arch.md). By default, `newarch` is not specified, indicating that the old architecture is used. `newarch` applies only to the new architecture. If `newarch` is added to the configuration file of the TiCDC old architecture, it might cause parsing failures. |
| BR | [`--checkpoint-storage`](/br/br-checkpoint-restore.md#implementation-details-store-checkpoint-data-in-the-external-storage) | Newly added | Specifies the external storage for BR to store checkpoint data. | 
| DM | [`redact-info-log`](/dm/dm-worker-configuration-file.md#redact-info-log-new-in-v900) | Newly added | Controls whether to enable DM log redaction. |
| TiProxy | [`enable-traffic-replay`](/tiproxy/tiproxy-configuration.md#enable-traffic-replay)  | Newly added | Specifies whether to enable [traffic replay](/tiproxy/tiproxy-traffic-replay.md). If it is set to `false`, traffic capture and replay operations will result in errors. |
| TiProxy | [`encryption-key-path`](/tiproxy/tiproxy-configuration.md#encryption-key-path)  | Newly added | Specifies the file path of the key used to encrypt the traffic files during traffic capture. |

### Offline package changes

Starting from v9.0.0, the offline package location of the [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) tool in the `TiDB-community-toolkit` [binary package](/binary-package.md) is changed from `sync_diff_inspector` to `tiflow-{version}-linux-{arch}.tar.gz`.

### System table changes

| System table | Change type | Description |
| -------- | -------- | -------- |
| [`mysql.tidb`](/mysql-schema/mysql-schema.md#cluster-status-system-tables) | Modified | Adds the `cluster_id` field, which represents the unique identifier of a TiDB cluster. Note that `cluster_id` is read-only and cannot be modified. |

### Operating system and platform requirement changes

Before upgrading TiDB, ensure that your operating system version meets the [OS and platform requirements](/hardware-and-software-requirements.md#os-and-platform-requirements).

## Removed features

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

    - (dup): release-8.5.1.md > Improvements> TiDB - Support folding read-only user-defined variables into constants [#52742](https://github.com/pingcap/tidb/issues/52742) @[winoros](https://github.com/winoros)
    - (dup): release-8.5.1.md > Improvements> TiDB - Adjust the default threshold of statistics memory cache to 20% of the total memory [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.6.md > Improvements> TiDB - Limit the execution of GC for TTL tables and related statistics collection tasks to the owner node, thereby reducing overhead [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.5.1.md > Improvements> TiDB - Adjust the default threshold of statistics memory cache to 20% of the total memory [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize the CPU usage of internal SQL statements in the Distributed eXecution Framework (DXF) [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)
    - Add more detailed spill information to the execution result of `EXPLAIN ANALYZE` [#59076](https://github.com/pingcap/tidb/issues/59076) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Support Left Outer Anti Semi Join in Hash Join v2 [#58479](https://github.com/pingcap/tidb/pull/58479) @[wshwsh12](https://github.com/wshwsh12)
    - Skip the lock cleanup phase for autocommitted statements in optimistic transactions to improve performance [#58675](https://github.com/pingcap/tidb/issues/58675) @[ekexium](https://github.com/ekexium)
    - Disable `tidb_enable_paging` in TTL to reduce the number of scanned rows and improve performance [#58342](https://github.com/pingcap/tidb/issues/58342) @[lcwangchao](https://github.com/lcwangchao)
    - Support choosing the left side as the build side when building Semi Join and Anti Semi Join [#58325](https://github.com/pingcap/tidb/issues/58325) @[hawkingrei](https://github.com/hawkingrei)    
    - Support generating `IndexMerge` plans using `(a, b), (a, c), (a, d)` for query conditions similar to `a = 1 AND (b = 2 OR c = 3 OR d = 4)`, without manually expanding the expression [#58361](https://github.com/pingcap/tidb/issues/58361) @[time-and-fate](https://github.com/time-and-fate)
    - Support applying the `semi_join_rewrite` hint to Semi Joins in `IN` subqueries [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - Automatically remove redundant expressions from filter conditions connected by `OR` [#58998](https://github.com/pingcap/tidb/issues/58998) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - (dup): release-6.5.12.md > Improvements> TiKV - Add the detection mechanism for invalid `max_ts` updates [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.2.0.md > Improvements> TiKV - Enable the [early apply](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v810) feature by default. With this feature enabled, the Raft leader can apply logs after quorum peers have persisted the logs, without waiting for the leader itself to persist the log, reducing the impact of jitter in a few TiKV nodes on write request latency [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    - Optimize the cleanup mechanism of residual data to mitigate the impact on request latency [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the warmup mechanism for TiKV MVCC in-memory engine (IME) when transferring the Leader to reduce the impact on Coprocessor request latency during the transfer [#17782](https://github.com/tikv/tikv/issues/17782) @[overvenus](https://github.com/overvenus)
    - Optimize the automatic eviction mechanism for TiKV MVCC in-memory engine (IME) to reduce the impact on Coprocessor request latency [#18130](https://github.com/tikv/tikv/issues/18130) @[overvenus](https://github.com/overvenus)
    - Throttle BR log restore requests when TiKV memory usage is high to prevent TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - Support printing a warning when `max-replicas` is set lower than the current number of replicas [#8959](https://github.com/tikv/pd/issues/8959) @[lhy1024](https://github.com/lhy1024)
    - Add a new `gRPC Received commands rate` monitoring panel [#8920](https://github.com/tikv/pd/issues/8920) @[okJiang](https://github.com/okJiang)
    - Support configuring the `batch` size for `evict-slow-store-scheduler` [#7156](https://github.com/tikv/pd/issues/7156) @[rleungx]
(https://github.com/rleungx)
    - Add a retry mechanism for `UpdateTSO` [#9020](https://github.com/tikv/pd/issues/9020) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - Improve the performance of the `TableScan` operator in TiFlash by skipping unnecessary data reads [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - Improve the aggregation performance in certain scenarios through memory prefetch [#9680](https://github.com/pingcap/tiflash/issues/9680) @[guo-shaoge](https://github.com/guo-shaoge)
    - Introduce [HashJoinV2](/sql-statements/sql-statement-explain-analyze.md#hashjoinv2) to improve the performance of some inner join scenarios [#9060](https://github.com/pingcap/tiflash/issues/9060) @[gengliqi](https://github.com/gengliqi)

+ Tools
    + Backup & Restore (BR)

        - Include error information returned by TiKV nodes in full backup logs to facilitate troubleshooting [#58666](https://github.com/pingcap/tidb/issues/58666) @[Leavrth](https://github.com/Leavrth)
        - Optimize the structure and content of backup and restore summary logs [#56493](https://github.com/pingcap/tidb/issues/56493) @[Leavrth](https://github.com/Leavrth)
        - Update the list of unrecoverable system tables [#52530](https://github.com/pingcap/tidb/issues/52530) @[Leavrth](https://github.com/Leavrth)
        - Improve the index restore speed during PITR by repairing indexes concurrently [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        - Support ignoring specific locks during backup scanning to improve backup efficiency [#53224](https://github.com/pingcap/tidb/issues/53224) @[3pointer](https://github.com/3pointer)
        - Remove the check on AWS region names to avoid backup errors caused by newly supported AWS regions failing the validation [#18159](https://github.com/tikv/tikv/issues/18159) @[3pointer](https://github.com/3pointer) <!--+ TiCDC  - Add `tableId` and `partitionId` fields to the TiDB extended fields for the Canal-JSON protocol [#11874](https://github.com/pingcap/tiflow/issues/11874) @[3AceShowHand](https://github.com/3AceShowHand)--> <!-- for-beta.2 -->

    + TiDB Data Migration (DM)

        - (dup): release-6.6.0.md > Improvements> Tools> TiDB Data Migration (DM) - Optimize relay performance by adding the async/batch relay writer [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)
        - DM supports multiple security configurations [#11831](https://github.com/pingcap/tiflow/issues/11831) @[River2000i](https://github.com/River2000i)

    + TiDB Lightning

        - (dup): release-6.5.12.md > Improvements> Tools> TiDB Lightning - Add a row width check when parsing CSV files to prevent OOM issues [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)


## Bug fixes

+ TiDB

    - Fix the issue that executing the `MODIFY COLUMN` statement might fail during TiDB upgrades [#58843](https://github.com/pingcap/tidb/issues/58843) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that executing the `DROP COLUMN` statement might fail during TiDB upgrades [#58863](https://github.com/pingcap/tidb/issues/58863) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that data race might occur when dynamically adjusting the number of workers during index creation [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that decreasing the number of workers during index creation might cause the task to hang [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that killing the PD Leader during index creation might lead to inconsistent index data [#59701](https://github.com/pingcap/tidb/issues/59701) @[tangenta](https://github.com/tangenta)
    - Fix the issue that adding a unique index with global sorting might fail [#59725](https://github.com/pingcap/tidb/issues/59725) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that the `ADMIN SHOW DDL JOBS` statement does not display the row count correctly [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    - Fix the issue that an error might occur when using `IMPORT INTO ... FROM SELECT` to import data into TiFlash [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that `IMPORT INTO ... FROM SELECT` does not convert negative numbers correctly [#58613](https://github.com/pingcap/tidb/issues/58613) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that logs do not display node information when some TiDB nodes do not synchronize the schema version [#58480](https://github.com/pingcap/tidb/issues/58480) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the potential issue that multiple views with the same name could be created [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the row count is not updated correctly when adding indexes in the TiDB Distributed eXecution Framework (DXF) [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)
    - Fix an out-of-memory (OOM) issue that might occur during global sorting on tables with many indexes [#59508](https://github.com/pingcap/tidb/issues/59508) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the `truncate` expression returns incorrect results when the first argument is `0` and the second argument is too large [#57651](https://github.com/pingcap/tidb/issues/57651) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix a potential goroutine leak issue in the Hash Aggregation operator [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that statistics become inaccurate after triggering a spill in the Hash Join operator [#58571](https://github.com/pingcap/tidb/issues/58571) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that the `json_extract` expression returns inaccurate results [#49513](https://github.com/pingcap/tidb/issues/49513) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the Hash Join operator returns incorrect results without reporting an error when execution fails [#59377](https://github.com/pingcap/tidb/issues/59377) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that the `json_keys` expression returns incorrect results when it has two parameters and the first is of type `JSONTypeCodeArray` [#56788](https://github.com/pingcap/tidb/issues/56788) @[zimulala](https://github.com/zimulala)
    - Fix the potential memory leak issue in the MPP coordinator [#59703](https://github.com/pingcap/tidb/issues/59703) @[yibin87](https://github.com/yibin87)
    - Fix the issue that parallel sorting might hang [#59655](https://github.com/pingcap/tidb/issues/59655) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that some TTL jobs might hang when modifying `tidb_ttl_delete_rate_limit` [#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.5.1.md > Bug fixes> TiDB - Fix the issue that changing the timezone causes incorrect query results when querying slow logs [#58452](https://github.com/pingcap/tidb/issues/58452) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.12.md > Bug fixes> TiDB - Fix the issue that some predicates might be lost when constructing `IndexMerge` [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that job status is overwritten when the DDL owner changes [#52747](https://github.com/pingcap/tidb/issues/52747) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that an error occurs when querying partitioned tables that contain generated columns [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - (dup): release-6.5.12.md > Bug fixes> TiDB - Fix the issue that loading statistics manually might fail when the statistics file contains null values [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-8.4.0.md > Bug fixes> TiDB - Deprecate unnecessary configurations related to statistics to reduce redundant code [#55043](https://github.com/pingcap/tidb/issues/55043) @[Rustin170506](https://github.com/Rustin170506)
    - (dup): release-8.5.1.md > Bug fixes> TiDB - Fix the issue that creating a vector search index on a column with more than 3000 dimensions causes the `KeyTooLong` error [#58836](https://github.com/pingcap/tidb/issues/58836) @[breezewish](https://github.com/breezewish)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that after executing `ALTER TABLE ... PLACEMENT POLICY ...` in a cluster with TiFlash nodes in the disaggregated storage and compute architecture, Region peers might be accidentally added to TiFlash Compute nodes [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.1.md > Bug fixes> TiDB - Fix the issue that data backfill during `REORGANIZE PARTITION` might cause concurrent updates to be rolled back [#58226](https://github.com/pingcap/tidb/issues/58226) @[mjonss](https://github.com/mjonss)
    - (dup): release-6.5.12.md > Bug fixes> TiDB - Fix the issue that using `ORDER BY` when querying `cluster_slow_query table` might generate unordered results [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-6.5.12.md > Bug fixes> TiDB - Fix the issue that querying temporary tables might trigger unexpected TiKV requests in some cases [#58875](https://github.com/pingcap/tidb/issues/58875) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.12.md > Bug fixes> TiDB - Fix the issue that in the Prepare protocol, an error occurs when the client uses a non-UTF8 character set [#58870](https://github.com/pingcap/tidb/issues/58870) @[xhebox](https://github.com/xhebox)
    - (dup): release-6.5.12.md > Bug fixes> TiDB - Fix the issue that creating two views with the same name does not report an error [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that TTL jobs might be ignored or processed multiple times [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that incorrect judgment in exchange partition causes execution failure [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that different data types on both sides of the equality condition in Join might cause incorrect results in TiFlash [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)
    - Fix the issue that TiDB does not exit properly in specific scenarios [#58418](https://github.com/pingcap/tidb/issues/58418) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB might panic when updating Infoschema v2 [#58712](https://github.com/pingcap/tidb/issues/58712) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that some gRPC clients cannot connect to the TiDB server status API [#59093](https://github.com/pingcap/tidb/issues/59093) @[iosmanthus](https://github.com/iosmanthus)
    - Fix the potential issue that TiDB panics and file leaks occur when using cursors [#59976](https://github.com/pingcap/tidb/issues/59976) [#59963](https://github.com/pingcap/tidb/issues/59963) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the `json_search` function does not return `NULL` when the search path is `NULL` during vectorized execution [#59463](https://github.com/pingcap/tidb/issues/59463) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that slow logs cannot be parsed correctly when database or table names contain colons (`:`) [#39940](https://github.com/pingcap/tidb/issues/39940) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the `MOD()` function does not support expressions as parameters [#59000](https://github.com/pingcap/tidb/issues/59000) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that enabling `tidb_enable_dist_task` causes TiDB upgrade to fail [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    - Fix the issue of write hotspots after creating indexes by supporting splitting Regions before creating indexes [#57551](https://github.com/pingcap/tidb/issues/57551) @[tangenta](https://github.com/tangenta)
    - Fix the issue that loading InfoSchema is slow when restarting TiDB in scenarios with a large number of tables [#58821](https://github.com/pingcap/tidb/issues/58821) @[GMHDBJD](https://github.com/GMHDBJD)
    - Fix the potential OOM issue when querying `information_schema.tables` by improving memory usage monitoring when quering system tables [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the duration is not collected when statistics collection fails [#58797](https://github.com/pingcap/tidb/issues/58797) @[hawkingrei](https://github.com/hawkingrei)    
    - Fix the issue that asynchronously loaded statistics might contain more information than the current synchronously loaded statistics [#59107](https://github.com/pingcap/tidb/issues/59107) @[winoros](https://github.com/winoros)   
    - Fix the issue that `UNION ALL` statements do not return an error when `sql_mode=only_full_group_by` is set [#59211](https://github.com/pingcap/tidb/issues/59211) @[AilinKid](https://github.com/AilinKid) 
    - Fix the issue that internal sessions used for statistics might not be released properly when errors occur, which might lead to memory leaks [#59524](https://github.com/pingcap/tidb/issues/59524) @[Rustin170506](https://github.com/Rustin170506)
    - Fix the issue that statistics estimation is incorrect when the value of `column.hist.NDV` is greater than that of `column.topN.num()` [#59563](https://github.com/pingcap/tidb/issues/59563) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that merging global statistics fails [#59274](https://github.com/pingcap/tidb/issues/59274) @[winoros](https://github.com/winoros)
    - Fix the issue that a TiDB session might crash when Fix Control #44855 is enabled [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - Fix the issue that TiDB chooses Merge Join when no hint is provided and the join keys do not fully match [#20710](https://github.com/pingcap/tidb/issues/20710) @[winoros](https://github.com/winoros)

+ TiKV

    - (dup): release-8.5.1.md > Bug fixes> TiKV - Fix the issue that TiKV panics due to uninitialized replicas when the TiKV MVCC In-Memory Engine (IME) preloads them [#18046](https://github.com/tikv/tikv/issues/18046) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.12.md > Bug fixes> TiKV - Fix the issue that encoding might fail when processing GBK/GB18030 encoded data [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-7.5.6.md > Bug fixes> TiKV - Fix the issue that Resolved-TS monitoring and logs might be abnormal [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - (dup): release-6.5.12.md > Bug fixes> TiKV - Fix the issue that the latest written data might not be readable when only one-phase commit (1PC) is enabled and Async Commit is not enabled [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.5.12.md > Bug fixes> TiKV - Fix the issue that time rollback might cause abnormal RocksDB flow control, leading to performance jitter [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.6.md > Bug fixes> TiKV - Fix the issue that Region merge might lead to TiKV abnormal exit due to Raft index mismatch [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - (dup): release-6.5.12.md > Bug fixes> TiKV - Fix the issue that a deadlock might occur when GC Worker is under heavy load [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.5.6.md > Bug fixes> TiKV - Fix the issue that CDC connections might cause resource leakage when encountering exceptions [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - Fix incorrect thread memory metrics [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the unexpected `Server is busy` error occurs after TiKV restarts [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that Online Unsafe Recovery gets stuck because of the TiFlash learner [#18197](https://github.com/tikv/tikv/issues/18197) @[v01dstar](https://github.com/v01dstar)

+ PD

    - (dup): release-6.5.12.md > Bug fixes> PD - Fix the issue that the `tidb_enable_tso_follower_proxy` system variable might not take effect [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-7.5.6.md > Bug fixes> PD - Fix the issue that PD might panic when the `tidb_enable_tso_follower_proxy` system variable is enabled [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.6.md > Bug fixes> PD - Fix the issue that operations in data import or adding index scenarios might fail due to unstable PD network [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.6.md > Bug fixes> PD - Fix the issue that the value of the `flow-round-by-digit` configuration item might be overwritten after a restart [#8980](https://github.com/tikv/pd/issues/8980) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.5.12.md > Bug fixes> PD - Fix the issue that memory leaks might occur when allocating TSOs [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.6.md > Bug fixes> PD - Fix the issue that the default value of `max-size` for a single log file is not correctly set [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > Bug fixes> PD - Fix the issue that memory leaks might occur in long-running clusters [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-6.5.12.md > Bug fixes> PD - Fix the issue that a PD node might still generate TSOs even when it is not the Leader [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > Bug fixes> PD - Fix the issue that Region syncer might not exit in time during the PD Leader switch [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - Fix the issue that uninitialized `minResolvedTS` causes TiDB to panic [#8964](https://github.com/tikv/pd/issues/8964) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the PD client retry policy is not properly initialized [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - Fix the issue that an incorrect error message is returned when querying a non-existent Region via API [#8868](https://github.com/tikv/pd/issues/8868) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the ping API is incorrectly forwarded [#9031](https://github.com/tikv/pd/issues/9031) @[rleungx](https://github.com/rleungx)
    - Fix the issue that TTL cache goroutines might leak [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that forwarding TSO requests in microservice mode might cause TiDB to panic [#9091](https://github.com/tikv/pd/issues/9091) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that network problems in PD might prevent the TSO client from initializing [#58239](https://github.com/pingcap/tidb/issues/58239) @[okJiang](https://github.com/okJiang)

+ TiFlash 

    - Fix the issue that TiFlash returns incorrect results when processing `IN(Timestamp)` or `IN(Time)` expressions with time zones [#9778](https://github.com/pingcap/tiflash/issues/9778) @[solotzg](https://github.com/solotzg)
    - Fix the issue that TiFlash behaves differently from TiDB when handling overflow errors, causing the execution failures of `IMPORT INTO` statements [#9752](https://github.com/pingcap/tiflash/issues/9752) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the memory leak issue that occurs when TiFlash executes aggregate functions used as window functions [#9930](https://github.com/pingcap/tiflash/issues/9930) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the null pointer issue that might occur when TiFlash executes aggregate functions used as window functions [#9964](https://github.com/pingcap/tiflash/issues/9964) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.6.md > Bug fixes> TiFlash - Fix the issue that TiFlash might unexpectedly reject processing Raft messages when memory usage is low [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-7.5.6.md > Bug fixes> TiFlash - Fix the issue that queries on a partitioned table might return errors after executing `ALTER TABLE ... RENAME COLUMN` on that partitioned table [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.12.md > Bug fixes> TiFlash - Fix the issue that TiFlash might maintain high memory usage after importing large amounts of data [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-7.5.6.md > Bug fixes> TiFlash - Fix the issue that in the disaggregated storage and compute architecture, TiFlash compute nodes might be incorrectly selected as target nodes for adding Region peers [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > Bug fixes> TiFlash - Fix the issue that TiFlash might fail to print error stack traces when it unexpectedly exits in certain situations [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > Bug fixes> TiFlash - Fix the issue that TiFlash startup might be blocked when `profiles.default.init_thread_count_scale` is set to `0` [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > Bug fixes> TiFlash - Fix the issue that a `Not found column` error might occur when a query involves virtual columns and triggers remote reads [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash might not clean up some disk data in time after inserting data into a table with vector indexes, leading to abnormal disk space usage [#9946](https://github.com/pingcap/tiflash/issues/9946) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash memory usage increases abnormally when tables in the cluster contain a large number of `ENUM` type columns [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash in the disaggregated storage and compute architecture might print a large number of `tag=EnumParseOverflowContainer` logs [#9955](https://github.com/pingcap/tiflash/issues/9955) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-6.5.12.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the `status` field is missing in the result when querying log backup tasks using `br log status --json` [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.6.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.12.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR fails to restore due to getting the `rpcClient is idle` error when sending requests to TiKV [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - (dup): release-7.5.6.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that log backup fails to exit properly when encountering a fatal error due to not being able to access PD [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that available space on storage nodes is unnecessarily rechecked during breakpoint recovery [#54316](https://github.com/pingcap/tidb/issues/54316) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that RangeTree results consume memory inefficiently during full backup [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)
        - Fix the issue that PITR tasks might return the `Information schema is out of date` error when a large number of tables exist in the cluster but the actual data size is small [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)
        - Fix the issue that parsing the external storage URL causes incorrect backends [#59548](https://github.com/pingcap/tidb/issues/59548) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that table ID pre-allocation is incorrect during the restore process [#59718](https://github.com/pingcap/tidb/issues/59718) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Fix the issue that the replication latency of changefeeds increases significantly after PD Leader migration [#11997](https://github.com/pingcap/tiflow/issues/11997) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that some configuration items of a changefeed do not take effect when the downstream connection protocol for the changefeed is `pulsar + http` or `pulsar + https` [#12068](https://github.com/pingcap/tiflow/issues/12068) @[SandeepPadhi](https://github.com/SandeepPadhi)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC might panic when replicating `CREATE TABLE IF NOT EXISTS` or `CREATE DATABASE IF NOT EXISTS` statements [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed might get stuck after new TiKV nodes are added to the cluster [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that out-of-order messages resent by the Sarama client cause Kafka message order to be incorrect [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC uses incorrect table names for filtering during `RENAME TABLE` operations [#11946](https://github.com/pingcap/tiflow/issues/11946) @[wk989898](https://github.com/wk989898)
        - (dup): release-7.5.6.md > Bug fixes> Tools> TiCDC - Fix the issue that goroutines leak occurs after a changefeed is deleted [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        - (dup): release-8.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the default value of the NOT NULL timestamp field in the Debezium protocol is incorrect [#11966](https://github.com/pingcap/tiflow/issues/11966) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC reports errors when replicating `default NULL` SQL statements via the Avro protocol [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC fails to properly connect to PD after PD scale-in [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that after the default value of a newly added column in the upstream is changed from `NOT NULL` to `NULL`, the default values of that column in the downstream are incorrect [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)

    + TiDB Data Migration (DM) 

        - Fix the issue that dump tasks fail because system tables are not included in the default filter list [#11984](https://github.com/pingcap/tiflow/issues/11984) @[River2000i](https://github.com/River2000i)
        - Fix the issue that DM tasks fail because only `LightningTableEmptyChecking` is checked [#11945](https://github.com/pingcap/tiflow/issues/11945) @[River2000i](https://github.com/River2000i)
        - Fix the issue that DM fails to back up data to Azure [#11912](https://github.com/pingcap/tiflow/issues/11912) @[River2000i](https://github.com/River2000i)

    + TiDB Lightning

        - (dup): release-6.5.12.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that logs are not properly desensitized [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)

## Performance test

<!--
To learn about the performance of TiDB v9.0.0, you can refer to the [performance test reports](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights) of the TiDB Cloud Dedicated cluster.
-->

## Contributors

We would like to thank the following contributors from the TiDB community:
