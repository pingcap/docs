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

* Support pushing down the following date functions to TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) [#18184](https://github.com/tikv/tikv/issues/18184) @[gengliqi](https://github.com/gengliqi) **tw@Oreoxmt** <!--1837-->

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

<!--
    For more information, see [documentation](/ticdc/ticdc-new-arch.md).
-->

* TiCDC supports DDL events and WATERMARK events for the Debezium protocol [#11566](https://github.com/pingcap/tiflow/issues/11566) @[wk989898](https://github.com/wk989898) **tw@lilin90** <!--2009-->

    TiCDC now supports DDL and WATERMARK event types in Debezium style output. After an upstream DDL operation is successfully executed, TiCDC encodes the DDL event into a Kafka message with the key and message in a Debezium style format. The WATERMARK event, a TiCDC extension (available when [`enable-tidb-extension`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) is enabled in the Kafka sink), represents a special point in time and indicates that the events received before this point are complete.

    For more information, see [documentation](/ticdc/ticdc-debezium.md).

* TiCDC adds safeguards to avoid replicating back to the same TiDB cluster [#11767](https://github.com/pingcap/tiflow/issues/11767) [#12062](https://github.com/pingcap/tiflow/issues/12062) @[wlwilliamx](https://github.com/wlwilliamx) **tw@qiancai** <!--2063-->

    TiCDC supports replicating data from an upstream TiDB cluster to multiple downstream systems, including other TiDB clusters. In versions before v9.0.0, if TiCDC is misconfigured to use the same TiDB cluster as both the source and the target, it could create a replication loop and cause data consistency issues. Starting from v9.0.0, TiCDC automatically checks whether the source and target TiDB clusters are the same, preventing this misconfiguration issue.

    For more information, see [documentation](/ticdc/ticdc-manage-changefeed.md#security-mechanism).

* Support query argument redaction in Data Migration (DM) logs [#11489](https://github.com/pingcap/tiflow/issues/11489) @[db-will](https://github.com/db-will) **tw@Oreoxmt** <!--2030-->

    Starting from v9.0.0, you can use the `redact-info-log` configuration item to enable the DM log redaction feature. When enabled, query arguments that contain sensitive data in DM logs are replaced with the `?` placeholder. To enable this feature, set `redact-info-log` to `true` in the DM-worker configuration file or pass `--redact-info-log=true` when starting DM. This feature only redacts query arguments, not the entire SQL statement, and requires a DM-worker restart to take effect.

<!--
    For more information, see [documentation](/dm/dm-worker-configuration-file.md#redact-info-log-new-in-v900).
-->

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

+ TiDB <!--tw@hfxsd: 28 notes-->

    - (dup): release-8.5.1.md > 改进提升> TiDB - 支持将只读的用户自定义变量折叠为常量 [#52742](https://github.com/pingcap/tidb/issues/52742) @[winoros](https://github.com/winoros)
    - (dup): release-8.5.1.md > 改进提升> TiDB - 将统计信息内存缓存的默认阈值调整为总内存的 20% [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.6.md > 改进提升> TiDB - 将 TTL 表的 GC 及相关统计信息收集任务限定在 owner 节点执行，从而降低开销 [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.5.1.md > 改进提升> TiDB - 将统计信息内存缓存的默认阈值调整为总内存的 20% [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    - 移除 TiDB 升级时对 `tidb_enable_dist_task` 变量的限制 [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    - 支持在创建索引前预先划分 Region [#57551](https://github.com/pingcap/tidb/issues/57551) @[tangenta](https://github.com/tangenta)
    - 优化了大量表的场景下 TiDB 重启时的 InfoSchema 加载速度 [#58821](https://github.com/pingcap/tidb/issues/58821) @[GMHDBJD](https://github.com/GMHDBJD)
    - 优化了系统表查询过程中的内存使用监控 [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)
    - 优化了分布式框架内部 SQL 语句的 CPU 使用率 [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)
    - 支持 from_unixtime 表达式下推 TiKV [#58940](https://github.com/pingcap/tidb/issues/58940) @[wshwsh12](https://github.com/wshwsh12)
    - 支持 timestampdiff 表达式下推 TiKV [#59365](https://github.com/pingcap/tidb/issues/59365) @[gengliqi](https://github.com/gengliqi)
    - 在 explain analyze 结果中支持更多 spill 的细节信息 [#59076](https://github.com/pingcap/tidb/issues/59076) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 支持 truncate 表达式下推 TiFlash [#59317](https://github.com/pingcap/tidb/issues/59317) @[guo-shaoge](https://github.com/guo-shaoge)
    - 支持 unix_timestamp 表达式下推 TiKV [#59497](https://github.com/pingcap/tidb/issues/59497) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 支持 aggregation window function 下推 TiFlash [#59509](https://github.com/pingcap/tidb/issues/59509) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 在 hash join v2 中支持 left outer anti semi join [#58479](https://github.com/pingcap/tidb/pull/58479) @[wshwsh12](https://github.com/wshwsh12)
    - 跳过自动提交的乐观语句的清锁阶段以提高性能 [#58675](https://github.com/pingcap/tidb/issues/58675) @[ekexium](https://github.com/ekexium)
    - 支持使用非唯一索引创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014)
    - TTL 关闭 `tidb_enable_paging`，以减少扫描行数 [#58342](https://github.com/pingcap/tidb/issues/58342) @[lcwangchao](https://github.com/lcwangchao)
    - 支持在构建 semi join 和 anti semi join 时候可以选择左侧作为 build 侧 [#58325](https://github.com/pingcap/tidb/issues/58325) @[hawkingrei](https://github.com/hawkingrei)
    - 支持对于形如 a = 1 and (b = 2 or c = 3 or d = 4) 的查询条件，TiDB 能够生成使用 (a,b), (a,c), (a,d) 的 IndexMerge 计划，用户不再需要人工展开表达式 [#58361](https://github.com/pingcap/tidb/issues/58361) @[time-and-fate](https://github.com/time-and-fate)
    - 支持由 IN 子查询而来的 semi join 使用 semi_join_rewrite 的 hint [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - 纠正收集统计信息失败时同步的耗时 [#58797](https://github.com/pingcap/tidb/issues/58797) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在用户创建不合法的 binding 的时候报错 [#51347](https://github.com/pingcap/tidb/issues/51347) @[qw4990](https://github.com/qw4990)
    - 修复自动删除由 OR 连接的过滤条件中的冗余表达式 [#58998](https://github.com/pingcap/tidb/issues/58998) @[time-and-fate](https://github.com/time-and-fate)
    - 修复异步统计信息加载时候可能会加载比当前同步加载更多的 item [#59107](https://github.com/pingcap/tidb/issues/59107)@[winoros]([https://github.com/winoros)
    - 修复在新 new-only-full-group 打开的情况下 union-all 语句不报错的问题 [#59211](https://github.com/pingcap/tidb/issues/59211) @[AilinKid](https://github.com/AilinKid)
    - 修复统计信息在使用的内部会话在遇到错误时可能没有被释放的问题，该问题可能导致内存泄漏  [#59524](https://github.com/pingcap/tidb/issues/59524) @[Rustin170506](https://github.com/Rustin170506)
    - 修复当 column hist ndv 大于 column topn num 时的统计信息评估错误的问题 [#59563](https://github.com/pingcap/tidb/issues/59563) @[AilinKid](https://github.com/AilinKid)
    - 修复了合并全局统计信息时候的 bucket 顺序 [#59274](https://github.com/pingcap/tidb/issues/59274)@[winoros](https://github.com/winoros)
    - 修复当 fixcontrol#44855 开启时，TiDB 的会话可能执行崩溃的问题 [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - 修复了只有在 hint 或者 join key 完全匹配的情况下才会选择 merge join [#20710](https://github.com/pingcap/tidb/issues/20710)@[winoros](https://github.com/winoros)

+ TiKV <!--tw@qiancai: 4 notes-->

    - (dup): release-6.5.12.md > 改进提升> TiKV - 增加对非法 `max_ts` 更新的检测机制 [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.2.0.md > 改进提升> TiKV - 默认开启[提前 apply](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-从-v810-版本开始引入) 特性，开启后，Raft leader 在多数 peer 完成 Raft log 持久化之后即可进行 apply，不再要求 leader 自身完成 Raft log 的持久化，降低少数 TiKV 抖动对写请求延迟的影响 [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    - 优化残留数据清理机制，减少对请求延迟的影响 [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化 TiKV MVCC 内存引擎在迁移 Leader 时的预热机制，减少迁移 Leader 对 Coprocessor 请求延时的影响 [#17782](https://github.com/tikv/tikv/issues/17782) @[overvenus](https://github.com/overvenus)
    - 优化 TiKV MVCC 内存的自动淘汰机制，减少对 Coprocessor 请求延时的影响 [#18130](https://github.com/tikv/tikv/issues/18130) @[overvenus](https://github.com/overvenus)

+ PD <!--tw@lilin90: 5 notes-->

    - 设置 max-replicas 小于当前副本数时打印警告信息 [#8959](https://github.com/tikv/pd/issues/8959) @[lhy1024](https://github.com/lhy1024)
    - 增加了 `gRPC Received commands rate` 监控面板 [#8920](https://github.com/tikv/pd/issues/8920) @[okJiang](https://github.com/okJiang)
    - Slow store 调度器支持设置 `batch` 大小 [#7156](https://github.com/tikv/pd/issues/7156) @[rleungx]
(https://github.com/rleungx)
    - 为更新 TSO 增加了重试机制 [#9020](https://github.com/tikv/pd/issues/9020) @[lhy1024](https://github.com/lhy1024)
    - 资源管控支持更多 BURSTABLE 模式 [#9057](https://github.com/tikv/pd/issues/9057) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@qiancai: 4 notes-->

    - 提升 TiFlash `TableScan` 算子性能，跳过不必要的数据读取 [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - 通过内存预取，提升特定 Aggregation 场景的性能 [#9680](https://github.com/pingcap/tiflash/issues/9680) @[guo-shaoge](https://github.com/guo-shaoge)
    - 引入 [HashJoinV2](/sql-statements/sql-statement-explain-analyze.md#hashjoinv2)，提升部分 inner join 场景的性能 [#9060](https://github.com/pingcap/tiflash/issues/9060) @[gengliqi](https://github.com/gengliqi)
    
+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 9 notes-->

        - 在测试用例中默认打开 --checksum 参数  [#57472](https://github.com/pingcap/tidb/issues/57472) @[Tristan1900](https://github.com/Tristan1900)
        - 给日志备份 advance owner 增加混沌测试用例 [#50458](https://github.com/pingcap/tidb/issues/50458) @[Tristan1900](https://github.com/Tristan1900)
        - 在全量备份日志中记录 TiKV 节点返回的错误信息，便于问题诊断 [#58666](https://github.com/pingcap/tidb/issues/58666) @[Leavrth](https://github.com/Leavrth)
        - 优化备份恢复 summary 日志的结构和内容 [#56493](https://github.com/pingcap/tidb/issues/56493) @[Leavrth](https://github.com/Leavrth)
        - 更新不可恢复的系统表列表 [#52530](https://github.com/pingcap/tidb/issues/52530) @[Leavrth](https://github.com/Leavrth)
        - 采用并行方式，提升 PITR 恢复过程中的索引修复速度 [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        - 备份扫描过程中支持忽略特定 lock，提高备份效率 [#53224](https://github.com/pingcap/tidb/issues/53224)@[3pointer](https://github.com/3pointer)
        - 在 TiKV 内存占用高时，对 BR 的日志恢复请求进行限流，防止 TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

    + TiCDC <!--tw@qiancai: 2 notes-->

        - Canal-JSON 协议支持在 TiDB 扩展字段中新增 `table_id` 和 `table_partition_id` 字段 [#11874](https://github.com/pingcap/tiflow/issues/11874) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM) <!--tw@lilin90: 1 note-->

        - (dup): release-6.6.0.md > 改进提升> Tools> TiDB Data Migration (DM) - 新增 async/batch relay writer 以优化 relay 性能 [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)
        - 为 dm 添加多安全配置的支持 [#11831](https://github.com/pingcap/tiflow/issues/11831) @[River2000i](https://github.com/River2000i)

    + TiDB Lightning

        - (dup): release-6.5.12.md > 改进提升> Tools> TiDB Lightning - 在解析 CSV 文件时，新增行宽检查以防止 OOM 问题 [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)
       
## Bug fixes

+ TiDB <!--tw@Oreoxmt: 28 notes-->

    - 修复了在 TiDB 升级过程中执行的 modify column 语句可能失败的问题 [#58843](https://github.com/pingcap/tidb/issues/58843) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了在 TiDB 升级过程中执行的 drop column 语句可能失败的问题 [#58863](https://github.com/pingcap/tidb/issues/58863) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了在添加索引过程中动态调整 Worker 数量可能导致的数据竞争问题 [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了在添加索引过程中减少 Worker 数量可能导致任务卡死的 bug [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了一个在添加索引期间杀死 PD Leader 可能导致的数据索引不一致问题 [#59701](https://github.com/pingcap/tidb/issues/59701) @[tangenta](https://github.com/tangenta)
    - 修复了一个使用 Global Sort 添加唯一索引失败的问题 [#59725](https://github.com/pingcap/tidb/issues/59725) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复了 `ADMIN SHOW DDL JOBS` 不能正确显示行数的问题 [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    - 修复了 `IMPORT INTO FROM SELECT` 导入 TiFlash 时发生错误的问题 [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了 `IMPORT INTO FROM SELECT` 没有正确转换负数的问题 [#58613](https://github.com/pingcap/tidb/issues/58613) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了在部分 TiDB 节点未同步 Schema Version 时，日志中没有打印相应节点的问题 [#58480](https://github.com/pingcap/tidb/issues/58480) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了一个可能导致创建多个同名视图的 bug [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复了在分布式框架下执行添加索引操作时没有正确更新行数的问题 [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)
    - 修复了当表存在大量索引时，Global Sort 可能导致 OOM 的问题 [#59508](https://github.com/pingcap/tidb/issues/59508) @[D3Hunter](https://github.com/D3Hunter)
    - 修复当 `truncate` 表达式的第一个参数为 0 且第二个值过大时，计算结果错误的问题 [#57651](https://github.com/pingcap/tidb/issues/57651) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 hash aggregation 算子潜在的 goroutine 泄漏问题 [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 Hash Join 算子中触发 spill 后统计信息不准确的问题 [#58571](https://github.com/pingcap/tidb/issues/58571) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `json_extract` 表达式计算结果不准确的问题 [#49513](https://github.com/pingcap/tidb/issues/49513) @[YangKeao](https://github.com/YangKeao)
    - 修复当 Hash Join 执行出错时，返回错误结果但未报错的问题 [#59377](https://github.com/pingcap/tidb/issues/59377) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当 json_keys 表达式包含 2 个参数且第 1 个参数为 JSONTypeCodeArray 类型时，计算结果错误的问题 [#56788](https://github.com/pingcap/tidb/issues/56788) @[zimulala](https://github.com/zimulala)
    - 修复 mpp coordinator 潜在的内存泄漏问题 [#59703](https://github.com/pingcap/tidb/issues/59703) @[yibin87](https://github.com/yibin87)
    - 修复多并发排序过程中潜在的卡住问题 [#59655](https://github.com/pingcap/tidb/issues/59655) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复在修改 `tidb_ttl_delete_rate_limit` 时，部分 TTL 任务可能挂起的问题 [#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.5.1.md > 错误修复> TiDB - 修复查询慢日志时，更改时区导致返回结果错误的问题 [#58452](https://github.com/pingcap/tidb/issues/58452) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复在构造 `IndexMerge` 时可能丢失部分谓词的问题 [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 DDL owner 变更时，作业状态被覆盖的问题 [#52747](https://github.com/pingcap/tidb/issues/52747) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复在查询包含生成列的分区表时报错的问题 [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复手动加载统计信息时，统计信息文件中包含 null 可能导致加载失败的问题 [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-8.4.0.md > 错误修复> TiDB - 废弃统计信息相关的无用配置，减少冗余代码 [#55043](https://github.com/pingcap/tidb/issues/55043) @[Rustin170506](https://github.com/Rustin170506)
    - (dup): release-8.5.1.md > 错误修复> TiDB - 修复在超过 3000 维向量类型的列上创建向量搜索索引报错 `KeyTooLong` 的问题 [#58836](https://github.com/pingcap/tidb/issues/58836) @[breezewish](https://github.com/breezewish)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复当集群中存在存算分离架构 TiFlash 节点时，执行 `ALTER TABLE ... PLACEMENT POLICY ...` 之后，Region peer 可能会被意外地添加到 TiFlash Compute 节点的问题 [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.1.md > 错误修复> TiDB - 修复执行 `REORGANIZE PARTITION` 时，数据回填可能导致并发更新被回滚的问题 [#58226](https://github.com/pingcap/tidb/issues/58226) @[mjonss](https://github.com/mjonss)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复查询 `cluster_slow_query` 表时，使用 `ORDER BY` 可能导致结果乱序的问题 [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复某些情况下查询临时表会产生 TiKV 请求的问题 [#58875](https://github.com/pingcap/tidb/issues/58875) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复在 Prepare 协议中，客户端使用非 UTF8 相关字符集报错的问题 [#58870](https://github.com/pingcap/tidb/issues/58870) @[xhebox](https://github.com/xhebox)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复创建两个相同名称的视图而没有报错的问题 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 TTL 任务可能被忽略或处理多次的问题 [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 exchange partition 错误判断导致执行失败的问题 [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 Join 的等值条件两边数据类型不同，可能导致 TiFlash 产生错误结果的问题 [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)
    - 修复 TiDB 可能不退出的问题 [#58418](https://github.com/pingcap/tidb/issues/58418) @[tiancaiamao](https://github.com/tiancaiamao)
    - 避免更新 Infoschema v2 时可能 panic 的问题 [#58712](https://github.com/pingcap/tidb/issues/58712) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复部分 gRPC 客户端连接不上 TiDB Server 状态接口的问题 [#59093](https://github.com/pingcap/tidb/issues/59093) @[iosmanthus](https://github.com/iosmanthus)
    - 修复使用 cursor 时可能 panic，且可能泄露文件的问题 [#59976](https://github.com/pingcap/tidb/issues/59976) [#59963](https://github.com/pingcap/tidb/issues/59963) @[YangKeao](https://github.com/YangKeao)
    - 修复向量化执行时 `json_search` 在搜索路径为 `NULL` 时不返回 `NULL` 的问题 [#59463](https://github.com/pingcap/tidb/issues/59463) @[YangKeao](https://github.com/YangKeao)
    - 修复慢日志在库名、表名包含 : 时无法解析的问题 [#39940](https://github.com/pingcap/tidb/issues/39940) @[Defined2014](https://github.com/Defined2014)
    - 修复 MOD 函数不支持表达式的问题 [#59000](https://github.com/pingcap/tidb/issues/59000) @[Defined2014](https://github.com/Defined2014)

+ TiKV <!--tw@lilin90: 3 notes-->

    - (dup): release-8.5.1.md > 错误修复> TiKV - 修复因 TiKV MVCC 内存引擎 (In-Memory Engine, IME) 预加载尚未初始化的副本导致 TiKV panic 的问题 [#18046](https://github.com/tikv/tikv/issues/18046) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复处理 GBK/GB18030 编码的数据时可能出现编码失败的问题 [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 Resolved-TS 监控和日志可能显示异常的问题 [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复在仅启用一阶段提交 (1PC) 而未启用异步提交 (Async Commit) 时，可能无法读取最新写入数据的问题 [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复时钟回退导致 RocksDB 流控异常，进而引发性能抖动的问题 [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 Region 合并时可能因 Raft index 匹配异常而导致 TiKV 异常退出的问题 [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复 GC Worker 负载过高时可能出现的死锁问题 [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 CDC 连接在遇到异常时可能发生资源泄漏的问题 [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - 修复错误的线程内存监控指标 [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)
    - 修复 TiKV 重启后非预期的 server is busy 状态 [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 Unsafe recovery 因 Tiflash learner 而卡住的问题 [#18197](https://github.com/tikv/tikv/issues/18197) @[v01dstar](https://github.com/v01dstar)

+ PD <!--tw@lilin90: 7 notes-->

    - (dup): release-6.5.12.md > 错误修复> PD - 修复设置 `tidb_enable_tso_follower_proxy` 系统变量可能不生效的问题 [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复启用 `tidb_enable_tso_follower_proxy` 系统变量后，PD 可能出现 panic 的问题 [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复在导入或添加索引场景中，因 PD 网络不稳定可能导致操作失败的问题 [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复重启后 `flow-round-by-digit` 配置项的值可能被覆盖的问题 [#8980](https://github.com/tikv/pd/issues/8980) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复 TSO 分配过程中可能出现的内存泄漏问题 [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复单个日志文件 `max-size` 默认值未被正确设置的问题 [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复长期运行的集群中可能出现的内存泄漏问题 [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复当某个 PD 节点不是 Leader 时，仍可能生成 TSO 的问题 [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复 PD Leader 切换过程中，Region syncer 未能及时退出的问题 [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - 修复 `minResolvedTS` 没有初始化导致的 panic 问题 [#8964](https://github.com/tikv/pd/issues/8964) @[rleungx](https://github.com/rleungx)
    - 修复 pd client 重试策略没有正确初始化的问题 [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - 修复通过 API 查询不存在的 Region 时的报错信息 [#8868](https://github.com/tikv/pd/issues/8868) @[lhy1024](https://github.com/lhy1024)
    - 修复 ping API 被错误转发的问题 [#9031](https://github.com/tikv/pd/issues/9031) @[rleungx](https://github.com/rleungx)
    - 修复 TTL cache goroutine 泄露的问题 [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - 修复微服务模式下转发 TSO 可能导致 panic 的问题 [#9091](https://github.com/tikv/pd/issues/9091) @[lhy1024](https://github.com/lhy1024)
    - 修复因为 PD 网络问题可能导致 TSO client 没有初始化的问题 [#58239](https://github.com/pingcap/tidb/issues/58239) @[okJiang](https://github.com/okJiang)

+ TiFlash <!--tw@qiancai: 7 notes-->

    - 修复 TiFlash 处理包含时区的 `IN(Timestamp)` 或 `IN(Time)` 表达式时结果错误的问题 [#9778](https://github.com/pingcap/tiflash/issues/9778) @[solotzg](https://github.com/solotzg)
    - 修复 TiFlash 在处理溢出错误时行为与 TiDB 不兼容，导致 `IMPORT INTO` 语句执行失败的问题 [#9752](https://github.com/pingcap/tiflash/issues/9752) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TiFlash 在执行 `Aggregation Window Function` 时出现内存泄漏的问题 [#9930](https://github.com/pingcap/tiflash/issues/9930) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 TiFlash 在执行 `Aggregation Window Function` 时可能出现空指针的问题 [#9964](https://github.com/pingcap/tiflash/issues/9964) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复 TiFlash 在内存占用较低的情况下，可能意外拒绝处理 Raft 消息的问题 [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在分区表上执行 `ALTER TABLE ... RENAME COLUMN` 后，查询该表可能报错的问题 [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.12.md > 错误修复> TiFlash - 修复在导入大量数据后，TiFlash 可能持续占用较高内存的问题 [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在存算分离架构下，TiFlash 计算节点可能被错误选为添加 Region peer 的目标节点的问题 [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在某些情况下 TiFlash 意外退出时无法打印错误堆栈的问题 [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复当 `profiles.default.init_thread_count_scale` 设置为 `0` 时，TiFlash 启动可能会卡住的问题 [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在查询涉及虚拟列并且触发远程读时，可能会出现 `Not found column` 错误的问题 [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在向包含向量索引的表中插入数据后，部分磁盘数据可能未能及时清理，从而导致磁盘空间异常占用的问题 [#9946](https://github.com/pingcap/tiflash/issues/9946) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当集群中表包含大量 `ENUM` 类型列时，TiFlash 内存占用异常升高的问题 [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在存算分离架构下 TiFlash 可能打印大量 `tag=EnumParseOverflowContainer` 日志的问题 [#9955](https://github.com/pingcap/tiflash/issues/9955) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@lilin90: 8 notes-->

        - (dup): release-6.5.12.md > 错误修复> Tools> Backup & Restore (BR) - 修复使用 `br log status --json` 查询日志备份任务时，返回结果中缺少任务状态 `status` 字段的问题 [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.12.md > 错误修复> Tools> Backup & Restore (BR) - 修复 BR 向 TiKV 发送请求时收到 `rpcClient is idle` 错误导致恢复失败的问题 [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - (dup): release-7.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复日志备份在无法访问 PD 时，遇到致命错误无法正确退出的问题 [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - 修复在断点恢复时额外检查存储节点可用空间的问题 [#54316](https://github.com/Leavrth))[)](https://github.com/Leavrth))
        - 修复全量备份过程中 RangeTree 存储结果内存效率问题 [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)
        - 修复没等待 info schema 加载结束后，就执行 pitr 后期的 sql 操作导致的问题 [#57743](https://github.com/pingcap/tidb/issues/57743) @[Leavrth](https://github.com/Leavrth)
        - 修复对 region 白名单检查的问题 [#18159](https://github.com/tikv/tikv/issues/18159) @[3pointer](https://github.com/3pointer)
        - 修复一个和 gc safepoint 相关的测试用例 [#59604](https://github.com/pingcap/tidb/issues/59604) @[RidRisR](https://github.com/RidRisR)
        - 修复一个解析外部存储 url 的问题 [#59548](https://github.com/pingcap/tidb/issues/59548) @[Leavrth](https://github.com/Leavrth)
        - 修复一个恢复过程中 table id 预分配的问题  [#59718](https://github.com/pingcap/tidb/issues/59718) @[Leavrth](https://github.com/Leavrth)
        - 修复一个单元测试用例 [#59925](https://github.com/pingcap/tidb/issues/59925) @[Leavrth](https://github.com/Leavrth)        

    + TiCDC <!--tw@qiancai: 2 notes-->

        - 修复 PD 切换 leader 后，changefeed 同步延迟显著增加的问题 [#11997](https://github.com/pingcap/tiflow/issues/11997) @[lidezhu](https://github.com/lidezhu)
        - 修复当 changefeed 下游的连接协议为 `pulsar + http` 或 `pulsar + https` 时，部分配置项未生效的问题 [#12068](https://github.com/pingcap/tiflow/issues/12068) @[SandeepPadhi](https://github.com/SandeepPadhi)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 同步 `CREATE TABLE IF NOT EXISTS` 或 `CREATE DATABASE IF NOT EXISTS` 语句时可能出现 panic 的问题 [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复在集群扩容出新的 TiKV 节点后 Changefeed 可能会卡住的问题 [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复由于 Sarama 客户端乱序重发消息导致 Kafka 消息乱序的问题 [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 在 `RENAME TABLE` 操作中使用了错误的表名进行过滤的问题 [#11946](https://github.com/pingcap/tiflow/issues/11946) @[wk989898](https://github.com/wk989898)
        - (dup): release-7.5.6.md > 错误修复> Tools> TiCDC - 修复在删除 Changefeed 后 goroutine 泄漏的问题 [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        - (dup): release-8.5.1.md > 错误修复> Tools> TiCDC - 修复 Debezium 协议中 NOT NULL timestamp 类型字段的默认值不正确的问题 [#11966](https://github.com/pingcap/tiflow/issues/11966) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 通过 Avro 协议同步 `default NULL` SQL 语句时报错的问题 [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 PD 缩容后 TiCDC 无法正确连接 PD 的问题 [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复当上游将一个新增的列的默认值从 `NOT NULL` 修改为 `NULL` 后，下游默认值错误的问题 [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)

    + TiDB Data Migration (DM) <!--tw@lilin90: 3 notes-->

        - 将系统表加入默认过滤列表 [#11984](https://github.com/pingcap/tiflow/issues/11984) @[River2000i](https://github.com/River2000i)
        - 修复 dm 仅检查 `LightningTableEmptyChecking` 会导致任务失败的问题 [#11945](https://github.com/pingcap/tiflow/issues/11945) @[River2000i](https://github.com/River2000i)
        - 修复 dm 不能备份至 azure 的问题 [#11912](https://github.com/pingcap/tiflow/issues/11912) @[River2000i](https://github.com/River2000i)

    + TiDB Lightning

        - (dup): release-6.5.12.md > 错误修复> Tools> TiDB Lightning - 修复日志没有正确脱敏的问题 [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)

## Performance test

<!--
To learn about the performance of TiDB v9.0.0, you can refer to the [performance test reports](https://docs.pingcap.com/tidbcloud/v9.0-performance-highlights) of the TiDB Cloud Dedicated cluster.
-->

## Contributors

We would like to thank the following contributors from the TiDB community:
