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
    <td>Point-in-time recovery (PITR) supports recovery from <a href="https://docs.pingcap.com/tidb/dev/br-compact-log-backup/">compacted log backups</a> for faster restores tw@lilin90</td>
    <td>Starting from v9.0.0, the log backup feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. These SST files can now be restored into the cluster much more quickly than reapplying the original logs, resulting in improved recovery performance.</td>
  </tr>
  <tr>
    <td rowspan="1">Reliability and availability</td>
    <td><a href="https://docs.pingcap.com/tidb/dev/tiproxy-traffic-replay/">The TiProxy traffic replay feature</a> is generally available (GA) (introduced in v8.4.0)</td>
    <td>Before performing critical operations such as cluster upgrades, migrations, or deployment changes, use TiProxy to capture the real workload from the production TiDB cluster and replay it on the target test cluster. It helps validate performance and ensure the success of the changes.</td>
  </tr>
  <tr>
    <td rowspan="3">DB Operations and Observability</td>
    <td>Add the <a href="https://docs.pingcap.com/tidb/dev/workload-repository/">TiDB Workload Repository</a> feature to support persisting historical workload data into TiKV tw@lilin90</td>
    <td>TiDB Workload Repository can persist the historical runtime status of the database, significantly improving the efficiency of diagnosing past failures and performance issues. It helps you quickly identify and resolve problems, while also providing critical data for health checks and automatic tuning.</td>
  </tr>
  <tr>
    <td>TiDB Index Advisor tw@Oreoxmt</td>
    <td>TiDB Index Advisor analyzes actual query workloads to automatically identify missing or redundant indexes. It helps you optimize indexes without requiring deep knowledge of your application. This feature reduces the cost of manual analysis and tuning, and improves query performance and system stability.</td>
  </tr>
  <tr>
    <td>SQL cross-AZ traffic monitoring tw@Oreoxmt</td>
    <td>This feature helps you identify cross-availability zone (AZ) network traffic caused by SQL queries in a TiDB cluster. It enables you to analyze traffic sources, optimize deployment architecture, and control cross-AZ data transfer costs in cloud environments, thus improving resource efficiency and cost visibility.</td>
  </tr>
  <tr>
    <td rowspan="3">Data Migration</td>
    <td>Query argument redaction in Data Migration (DM) logs tw@Oreoxmt</td>
    <td>Data Migration (DM) introduces the <code>redact-info-log</code> configuration item to redact query arguments in DM logs, preventing sensitive data from appearing in logs.</td>
  </tr>
  <tr>
    <td>TiDB Lightning supports compatibility with <code>sql_require_primary_key=ON</code> in TiDB tw@Oreoxmt</td>
    <td>When the <code>sql_require_primary_key</code> system variable is enabled in TiDB, TiDB Lightning automatically adds a default primary key to its internal error-logging and conflict-detection tables during data import to prevent table creation failures.</td>
  </tr>
  <tr>
    <td>Migrate sync-diff-inspector from <code>pingcap/tidb-tools</code> to <code>pingcap/tiflow</code> repository tw@Oreoxmt</td>
    <td>sync-diff-inspector is now maintained with other migration and replication tools such as DM and TiCDC in the <code>pingcap/tiflow</code> repository. You can now install sync-diff-inspector using TiUP or a dedicated Docker image.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* PD supports the microservice mode (GA) [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing) tw@hfxsd <!--2052-->

    In v8.0.0, the PD microservice mode is released as an experimental feature. Starting from v9.0.0, the PD microservice mode is generally available (GA). This mode splits the timestamp allocation and cluster scheduling functions of PD into separate microservices that can be deployed independently, thereby enhancing performance scalability for PD and addressing performance bottlenecks of PD in large-scale clusters.

    - `tso` microservice: provides monotonically increasing timestamp allocation for the entire cluster.
    - `scheduling` microservice: provides scheduling functions for the entire cluster, including but not limited to load balancing, hot spot handling, replica repair, and replica placement.

    Each microservice is deployed as an independent process. If you configure more than one replica for a microservice, the microservice automatically implements a primary-secondary fault-tolerant mode to ensure high availability and reliability of the service.

    For more information, see [documentation](/pd-microservices.md).

### Performance

* In scenarios with hundreds of thousands to millions of users, the performance of creating and modifying users has improved by 77 times [#55563](https://github.com/pingcap/tidb/issues/55563) @[tiancaiamao](https://github.com/tiancaiamao) tw@hfxsd <!--1941-->

    In previous versions, when the number of users in a cluster exceeded 200,000, the QPS for creating and modifying users drops to 1. In certain SaaS environments, if there is a need to create millions of users and periodically update user passwords in bulk, it can take up to 2 days or more, which is unacceptable for some SaaS businesses.

    TiDB v9.0.0 optimizes the performance of these DCL (Data Control Language) operations, allowing 2 million users to be created in just 37 minutes. This greatly enhances the execution performance of DCL statements and improves the user experience of TiDB in such SaaS scenarios.

    For more information, see [documentation](/system-variables.md#tidb_accelerate_user_creation_update-new-in-v900).

* Support pushing down the following function to TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1918-->

    * `TRUNCATE()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Support pushing down window functions that contain the following aggregation functions to TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**<!--1382-->

    * `MAX()`
    * `MIN()`
    * `COUNT()`
    * `SUM()`
    * `AVG()`

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
        - If [`format_version`](/tiflash/tiflash-configuration.md#format_version) is specified for TiFlash before the upgrade, the value of `format_version` remains unchanged after the upgrade, and TiFlash continues to use the storage format specified by `format_version`. To enable the new storage format in this case, set the `format_version` configuration item to `8` in the TiFlash configuration file. After the configuration takes effect, new data written to TiFlash will use the new storage format, while the storage format of existing data will remain unchanged.

  For more information, see [user documentation](/tiflash/tiflash-configuration.md#format_version).

* Point-in-time recovery (PITR) supports recovery from compacted log backups for faster restores [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen) **tw@lilin90** <!--2001-->

    Starting from v9.0.0, the compact log backup feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. This results in the following improvements:

    - SST files can be quickly imported into the cluster, **improving recovery performance**.
    - Redundant data is removed during compaction, **reducing storage space consumption**.
    - You can set longer full backup intervals while ensuring the Recovery Time Objective (RTO), **reducing the impact on applications**.

  For more information, see [documentation](/br/br-compact-log-backup.md).

### Availability

* TiProxy officially supports the traffic replay feature (GA) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832) tw@hfxsd<!--2062-->

    In TiProxy v1.3.0, the traffic replay feature is released as an experimental feature. In TiProxy v1.4.0, the traffic replay feature becomes generally available (GA). TiProxy provides specialized SQL commands for traffic capture and replay. This feature lets you easily capture access traffic from TiDB production clusters and replay it at a specified rate in test clusters, facilitating business validation.
    
    For more information, see [documentation](/tiproxy/tiproxy-traffic-replay.md).

### Reliability

* Introduce a new system variable `max_user_connections` to limit the number of connections that different users can establish [#59203](https://github.com/pingcap/tidb/issues/59203) @[joccau](https://github.com/joccau) tw@hfxsd<!--2017-->

    Starting from v9.0.0, you can use the `max_user_connections` system variable to limit the number of connections that a single user can establish to a single TiDB node. This helps prevent issues where excessive [token](/tidb-configuration-file.md#token-limit) consumption by one user causes delays in responding to requests from other users.
    
    For more information, see [documentation](/system-variables.md#max_user_connections-new-in-v900).

### SQL

* Support creating global indexes on non-unique columns of partitioned tables [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss) **tw@qiancai**<!--2057-->

    Starting from v8.3.0, you can create global indexes on unique columns of partitioned tables in TiDB to improve query performance. However, creating global indexes on non-unique columns was not supported. Starting from v9.0.0, TiDB removes this restriction, enabling you to create global indexes on non-unique columns of partitioned tables, enhancing the usability of global indexes.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

### DB operations

* TiDB Index Advisor [#12303](https://github.com/pingcap/tidb/issues/12303) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--2081-->

    Index design is essential for database performance optimization. Starting from v8.5.0, TiDB introduces the Index Advisor feature and continues to improve and enhance it. This feature analyzes high-frequency query patterns, recommends optimal indexing strategies, helps you tune performance more efficiently, and lowers the barrier to index design.

    You can use the [`RECOMMEND INDEX`](/index-advisor.md#recommend-indexes-using-the-recommend-index-statement) SQL statement to generate index recommendations for a single query or automatically analyze high-frequency SQL statements from historical workloads for batch recommendations. The recommendation results are stored in the `mysql.index_advisor_results` table. You can query this table to view the recommended indexes.

    For more information, see [documentation](/index-advisor.md).

* Improve the compatibility between ongoing log backup and snapshot restore [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    Starting from v9.0.0, when a log backup task is running, if the conditions are met, you can still perform snapshot restore and allow the restored data to be properly recorded by the ongoing log backup. This enables ongoing log backups to proceed without having to stop them during the restore procedure.

    For more information, see [documentation](/br/br-pitr-manual.md#compatibility-between-ongoing-log-backup-and-snapshot-restore).

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

    [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) executes SQL statements and records execution details in the `execution info` column. The same information is captured in the [slow query log](/identify-slow-queries.md). These details are crucial for analyzing and understanding the time spent on SQL execution.

    In v9.0.0, the `execution info` output is optimized for clearer representation of each metric. For example, `time` now refers to the wall-clock time for operator execution, `loops` indicates how many times the current operator is called by its parent operator, and `total_time` represents the cumulative duration of all concurrent executions. These optimizations help you better understand the SQL execution process and devise more targeted optimization strategies.

    For more information, see [documentation](/sql-statements/sql-statement-explain-analyze.md).

### Security

### Data migration

* TiCDC introduces a new architecture for improved performance, scalability, and stability (experimental) [#442](https://github.com/pingcap/ticdc/issues/442) @[CharlesCheung96](https://github.com/CharlesCheung96) **tw@qiancai** <!--2027-->

    In v9.0.0, TiCDC introduces a new architecture (experimental) that improves real-time data replication performance, scalability, and stability while reducing resource costs. This new architecture redesigns TiCDC core components and optimizes its data processing workflows.

    With this new architecture, TiCDC can now scale its replication capability nearly linearly and replicate millions of tables with lower resource costs. Changefeed latency is reduced and performance is more stable in scenarios with high traffic, frequent DDL operations, and during cluster scaling events.

    <!--For more information, see [documentation](/ticdc/ticdc-new-arch.md).-->

* TiCDC supports DDL events and WATERMARK events for the Debezium protocol [#11566](https://github.com/pingcap/tiflow/issues/11566) @[wk989898](https://github.com/wk989898) **tw@lilin90** <!--2009-->

    TiCDC now supports DDL and WATERMARK event types in Debezium style output. After an upstream DDL operation is successfully executed, TiCDC encodes the DDL event into a Kafka message with the key and message in a Debezium style format. The WATERMARK event, a TiCDC extension (available when [`enable-tidb-extension`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) is enabled in the Kafka sink), represents a special point in time and indicates that the events received before this point are complete.

    For more information, see [documentation](/ticdc/ticdc-debezium.md).

* TiCDC adds safeguards to avoid replicating back to the same TiDB cluster [#12062](https://github.com/pingcap/tiflow/issues/12062) @[wlwilliamx](https://github.com/wlwilliamx) **tw@qiancai** <!--2063-->

    TiCDC supports replicating data from an upstream TiDB cluster to multiple downstream systems, including other TiDB clusters. In versions before v9.0.0, if TiCDC is misconfigured to use the same TiDB cluster as both the source and the target, it could create a replication loop and cause data consistency issues. Starting from v9.0.0, TiCDC automatically checks whether the source and target TiDB clusters are the same, preventing this misconfiguration issue.

    For more information, see [documentation](/ticdc/ticdc-manage-changefeed.md#security-mechanism).

* Support query argument redaction in Data Migration (DM) logs [#11489](https://github.com/pingcap/tiflow/issues/11489) @[db-will](https://github.com/db-will) **tw@Oreoxmt** <!--2030-->

    Starting from v9.0.0, you can use the `redact-info-log` configuration item to enable the DM log redaction feature. When enabled, query arguments that contain sensitive data in DM logs are replaced with the `?` placeholder. To enable this feature, set `redact-info-log` to `true` in the DM-worker configuration file or pass `--redact-info-log=true` when starting DM. This feature only redacts query arguments, not the entire SQL statement, and requires a DM-worker restart to take effect.

    <!--For more information, see [documentation](/dm/dm-worker-configuration-file.md#redact-info-log-new-in-v900).-->

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
<!--
| TiCDC | [`newarch`](/ticdc/ticdc-server-config.md#newarch) | Newly added | Controls whether to enable the [TiCDC new architecture](/ticdc/ticdc-new-arch.md). By default, `newarch` is not specified, indicating that the old architecture is used. `newarch` applies only to the new architecture. If `newarch` is added to the configuration file of the TiCDC old architecture, it might cause parsing failures. |
| BR | [`--checkpoint-storage`](/br/br-checkpoint-restore.md#implementation-details-store-checkpoint-data-in-the-external-storage) | Newly added | Specifies the external storage for BR to store checkpoint data. | 
| DM | [`redact-info-log`](/dm/dm-worker-configuration-file.md#redact-info-log-new-in-v900) | Newly added | Controls whether to enable DM log redaction. |
-->
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

<!--
To learn about the performance of TiDB v9.0.0, you can refer to the [performance test reports](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights) of the TiDB Cloud Dedicated cluster.
-->

## Contributors

We would like to thank the following contributors from the TiDB community:
