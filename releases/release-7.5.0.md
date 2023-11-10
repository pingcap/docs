---
title: TiDB 7.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.5.0.
---

# TiDB 7.5.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.5.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.5.0#version-list)

TiDB 7.5.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 7.1.0, 7.5.0 not only includes new features, improvements, and bug fixes released in [7.2.0-DMR](/releases/release-7.2.0.md), [7.3.0-DMR](/releases/release-7.3.0.md), [7.4.0-DMR](/releases/release-7.4.0.md), but also introduces the following key features and improvements:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Scalability and Performance</td>
    <td>Support for running multiple <code>ADD INDEX</code> statements in parallel {/* tw@ran-huang */}</td>
    <td>Different from distributed and parallel DDL jobs, this feature allows for concurrent jobs to run where they were otherwise running synchronously. Where running DDL statements x, y at the same time used to take x-time +y-time, they now take significantly less.</td>
  </tr>
  <tr>
    <td rowspan="3">Reliability and Availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">Global sort</a> optimization {/* tw@ran-huang */}</td>
    <td>Laying the groundwork with the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">distributed framework</a> in v7.2, TiDB introduces global sorting to eliminate the unnecessary I/O, CPU, and memory spikes caused from temporarily out of order data during data re-organization tasks. The global sorting will take advantage of external shared object storage (S3 in this first iteration) to store intermediary files during the job, adding flexibility and cost savings.Operations like ADD INDEX and IMPORT INTO will be faster, more resilient, more stable, more flexible, and cost less to run.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-background-tasks" target="_blank">Resource control</a> for background tasks (experimental) {/* tw@Oreoxmt */}</td>
    <td>In v7.1.0, the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">Resource Control</a> feature was introduced to mitigate resource and storage access interference between workloads. TiDB v7.4.0 applies this control to background tasks as well. In v7.4.0, Resource Control now identifies and manages the resources produced by background tasks, such as auto-analyze, Backup & Restore, bulk load with TiDB Lightning, and online DDL. This will eventually apply to all background tasks.</td>
  </tr>
  <tr>
    <td>Resource groups support <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries"> managing runaway queries</a> (experimental) {/* tw@hfxsd */}</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">Resource Control</a> is a framework for resource-isolating workloads by Resource Groups, but it makes no calls on how individual queries affect work inside of each group. TiDB v7.2 introduced "runaway query conrol" to let operators control how TiDB identifies and treats these queries per Resource Group. Depending on need, long running queries may be terminated or throttled, and the queries can be identified by exact SQL text or their plan digests, for better generalization. In v7.4, TiDB allows operators to proactively watch for known bad queries, similar to a SQL blocklist at the database level.</td>
  </tr>
  <tr>
    <td>SQL</td>
    <td>MySQL 8.0 compatibility {/* tw@Oreoxmt */}</td>
    <td>In MySQL 8.0, the default characterset is utf8mb4, and the default collation of utf8mb4 is <code>utf8mb4_0900_ai_ci</code>. TiDB v7.4.0 adding support for this enhances compatibility with MySQL 8.0 so that migrations and replications from MySQL 8.0 databases with the default collation are now much smoother.</td>
  </tr>
  <tr>
    <td rowspan="3">DB Operations and Observability</td>
    <td>TiDB Lightning's physical import mode integrated into TiDB with <a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into">IMPORT INTO</a> {/* tw@qiancai */}</td>
    <td>Before v7.2, to import data based on the file system, you needed to install <a href="https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a> and use its physical import mode. Now, the same functionality is integrated into the `IMPORT INTO` statement so you can use this statement to quickly import data without installing any additional tool. This statement also supports the new <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">distributed execution framework</a> and the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">Global sort</a> feature, which improves import efficiency and provides greater stability during large-scale imports.</td>
  </tr>
  <tr>
    <td>Specify<a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_service_scope-new-in-v740" target="_blank"> the respective TiDB nodes</a> to execute the <code>IMPORT INTO</code> and <code>ADD INDEX</code> SQL statements (GA) {/* tw@hfxsd */}</td>
    <td>You have the flexibility to specify whether to execute <code>IMPORT INTO</code> or <code>ADD INDEX</code> SQL statements on some of the existing TiDB nodes or newly added TiDB nodes. This approach enables resource isolation from the rest of the TiDB nodes, preventing any impact on business operations while ensuring optimal performance for executing the preceding SQL statements. In v7.5.0, this feature becomes generally available (GA).</td>
  </tr>
  <tr>
    <td>DDL supports <a href="https://docs.pingcap.com/tidb/v7.5/ddl-introduction#ddl-related-commands">pause and resume operations</a> {/* tw@ran-huang */}</td>
    <td>Adding indexes can be big resource consumers and can affect online traffic. Even when throttled in a Resource Group or isolated to labeled nodes, there may still be a need to suspend these jobs in emergencies. As of v7.2, TiDB now natively supports suspending any number of these background jobs at once, freeing up needed resources while avoiding having to cancel and restart the jobs.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Support selecting the TiDB nodes to parallelly execute the backend `ADD INDEX` or `IMPORT INTO` tasks of the distributed execution framework (GA) [#46258](https://github.com/pingcap/tidb/issues/46258) @[ywqzzy](https://github.com/ywqzzy)<!--**tw@hfxsd** 1581-->

    Executing `ADD INDEX` or `IMPORT INTO` tasks in parallel in a resource-intensive cluster can consume a large amount of TiDB node resources, which can lead to cluster performance degradation. To avoid performance impact on existing services, v7.4.0 introduces the system variable [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) as an experimental feature to control the service scope of each TiDB node under the [TiDB Backend Task Distributed Execution Framework](/tidb-distributed-execution-framework.md). You can select several existing TiDB nodes or set the TiDB service scope for new TiDB nodes, and all parallel `ADD INDEX` and `IMPORT INTO` tasks only run on these nodes. In v7.5.0, this feature becomes generally available (GA).

    For more information, see [documentation](/system-variables.md#tidb_service_scope-new-in-v740).

### Performance

* The TiDB backend task distributed execution framework becomes generally available (GA). The cloud storage-based global sort capability also becomes GA, improving the performance and stability of `ADD INDEX` and `IMPORT INTO` tasks in parallel execution [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) <!--**tw@ran-huang** 1580-->

    Before v7.4.0, when executing tasks like `ADD INDEX` or `IMPORT INTO` in the distributed parallel execution framework, each TiDB node needs to allocate a significant amount of local disk space for sorting encoded index KV pairs and table data KV pairs. However, due to the lack of global sorting capability, there might be overlapping data between different TiDB nodes and within each individual node during the process. As a result, TiKV has to constantly perform compaction operations while importing these KV pairs into its storage engine, which impacts the performance and stability of `ADD INDEX` and `IMPORT INTO`.

    In v7.4.0, TiDB introduces the [Global Sort](/tidb-global-sort.md) feature. Instead of writing the encoded data locally and sorting it there, the data is now written to cloud storage for global sorting. Once sorted, both the indexed data and table data are imported into TiKV in parallel, thereby improving performance and stability.

    For more information, see [documentation](/tidb-global-sort.md).

* Improve the performance of adding multiple indexes in a single SQL statement [#41602](https://github.com/pingcap/tidb/issues/41602) @[tangenta](https://github.com/tangenta) <!--**tw@ran-huang** 1582-->

    Before v7.5.0, when you add multiple indexes (`ADD INDEX`) in a single SQL statement, the performance was similar to adding multiple indexes using separate SQL statements. Starting from v7.5.0, the performance of adding multiple indexes in a single SQL statement is significantly improved, improving XX, which greatly reduces the time required for adding indexes.

### DB operations

* DDL jobs support pause and resume operations (GA) [#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm) <!--**tw@ran-huang** 1611-->

    The pause and resume operations for DDL jobs introduced in v7.2.0 become generally available (GA). These operations let you pause resource-intensive DDL jobs (such as creating indexes) to save resources and minimize the impact on online traffic. When resources permit, you can seamlessly resume DDL jobs without canceling and restarting them. This feature improves resource utilization, enhances user experience, and simplifies the schema change process.

    You can pause and resume multiple DDL jobs using `ADMIN PAUSE DDL JOBS` or `ADMIN RESUME DDL JOBS`:

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    For more information, see [documentation](/ddl-introduction.md#ddl-related-commands).

* BR supports backing up and restoring statistics [#48008](https://github.com/pingcap/tidb/issues/48008) @[Leavrth](https://github.com/Leavrth) <!--**tw@hfxsd** 1437-->

    Starting from TiDB v7.5.0, the `br` command-line tool introduces the `--ignore-stats` parameter to back up and restore database statistics. When you set this parameter to `false`, the `br` command-line tool supports backing up and restoring statistics of columns, indexes, and tables. In this case, you do not need to manually run the statistics collection task for the TiDB database restored from the backup, or wait for the completion of the automatic collection task. This feature simplifies the database maintenance work and improves the query performance.

    For more information, see [documentation](/br/br-snapshot-manual.md#back-up-statistics).

### Data migration

* Support the `IMPORT INTO` SQL statement (GA) [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter)<!--**tw@qiancai** 1579-->

    In v7.5.0, the `IMPORT INTO` SQL statement becomes generally available (GA). This statement integrates the [Physical Import Mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) capability of TiDB Lightning and allows you to quickly import data in formats such as CSV, SQL, and PARQUET into an empty table in TiDB. This import method eliminates the need for a separate deployment and management of TiDB Lightning, thereby reducing the complexity of data import and greatly improving import efficiency.

    In addition, you can add the `CLOUD_STORAGE_URI` option in the `IMPORT INTO` statement to enable the [Global Sort](/tidb-global-sort.md) feature, which helps boost import performance and stability. In the `CLOUD_STORAGE_URI` option, you can specify a cloud storage address for the encoded data.

    For more information, see [documentation](/sql-statements/sql-statement-import-into.md).

* Data Migration (DM) supports blocking incompatible (data-consistency-corrupting) DDL changes [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD) <!--**tw@hfxsd** 1523-->

    Before v7.5.0, the DM Binlog Filter feature can only migrate or filter specified events, and the granularity is relatively coarse. For example, it can only filter large granularity of DDL events such as `ALTER`. This method is limited in some scenarios. For example, the application allows `ADD COLUMN` but not `DROP COLUMN`, but they are both filtered by `ALTER` events in the earlier DM versions.

    To address such issues, v7.5.0 refines the granularity of the supported DDL events, such as support filtering `MODIFY COLUMN` (modify the column data type), `DROP COLUMN`, and other fine-grained DDL events that lead to data loss, truncation of data, and loss of precision. You can configure it as needed. This feature also supports blocking incompatible DDL changes and reporting errors for such changes, so that you can intervene manually in time to avoid impacting downstream application data.

    For more information, see [documentation](/dm/dm-binlog-event-filter.md#parameter-descriptions).

* Support real-time update of checkpoint for continuous data validation [#8463](https://github.com/pingcap/tiflow/issues/8463) @[lichunzhu](https://github.com/lichunzhu) <!--**tw@ran-huang** 1496-->

    Before v7.5.0, the [continuous data validation feature](/dm/dm-continuous-data-validation.md) ensures the data consistency during replication from DM to downstream. This serves as the basis for cutting over business traffic from the upstream database to TiDB. However, due to various factors such as replication delay and waiting for re-validation of inconsistent data, the continuous validation checkpoint must be refreshed every few minutes. This is unacceptable for some business scenarios where the cutover time is limited to a few tens of seconds.

    With the introduction of real-time updating of checkpoint for continuous data validation, you can now provide the binlog position from the upstream database. Once the continuous validation program detects this binlog position in memory, it immediately refreshes the checkpoint instead of refreshing it every few minutes. Therefore, you can quickly perform cut-off operations based on this immediately updated checkpoint.

    For more information, see [documentation](/dm/dm-continuous-data-validation.md#set-the-cutover-point-for-continuous-data-validation).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.4.0 to the current version (v7.5.0). If you are upgrading from v7.3.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### System variables

| Variable name  | Change type    |  Description |
|--------|------------------------------|------|
| [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) | Newly added | Controls the sample concurrency of the `ANALYZE` process. |
| [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) | Newly added | This variable is used by TiDB to merge statistics asynchronously to avoid OOM issues. |
[`tidb_gogc_tuner_max_value`](/system-variables.md#tidb_gogc_tuner_max_value-new-in-v750) | Newly added | Controls the maximum value of GOGC that the GOGC Tuner can adjust. |
| [`tidb_gogc_tuner_min_value`](/system-variables.md#tidb_gogc_tuner_min_value-new-in-v750) | Newly added | Controls the minimum value of GOGC that the GOGC Tuner can adjust.|
| `tidb_enable_fast_analyze` | Deleted | Controls whether to enable the statistics `Fast Analyze` feature. This feature for statistics is deprecated in v7.5.0. |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| BR | [`--ignore-stats`](/br/br-snapshot-manual.md#back-up-statistics) | Newly added | Controls whether to back up and restore database statistics. When you set this parameter to `false`, the `br` command-line tool supports backing up and restoring statistics of columns, indexes, and tables. |
| TiCDC | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md) | Newly added | Controls the specified columns of data change events that TiCDC sends to Kafka when dispatching incremental data. |
| TiCDC | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md) | Modified | Controls how TiCDC dispatches incremental data to Kafka partitions. v7.5.0 introduces a new value option `columns`, which uses the explicitly specified column values to calculate the partition number. |
| TiCDC | [`sql-mode`](/ticdc/ticdc-changefeed-config.md) | Newly added | Specifies the SQL mode used by TiCDC when parsing DDL statements. The default value is the same as the default SQL mode of TiDB. |
| TiDB Lightning | Deleted | `--importer` | Specifies the address of TiKV-importer, which is deprecated in v7.5.0. |
|          |          |          |          |

### Others

## Offline package changes

Starting from v7.5.0, the following contents are removed from the `TiDB-community-toolkit` [binary package](/binary-package.md):<!--**tw@Oreoxmt** 1593+1594 -->

- `tikv-importer-{version}-linux-{arch}.tar.gz`
- `mydumper`
- `spark-{version}-any-any.tar.gz`
- `tispark-{version}-any-any.tar.gz`

## Deprecated features

* [Mydumper](https://docs.pingcap.com/tidb/v4.0/mydumper-overview) is deprecated in v7.5.0 and most of its features have been replaced by [Dumpling](/dumpling-overview.md). It is strongly recommended that you use Dumpling instead of mydumper.<!--**tw@Oreoxmt** 1593-->

* TiKV-importer is deprecated in v7.5.0. It is strongly recommended that you use the [Physical Import Mode of TiDB Lightning](/tidb-lightning/tidb-lightning-physical-import-mode.md) as an alternative.<!--**tw@Oreoxmt** 1594-->

* Starting from TiDB v7.5.0, technical support for the data replication feature of [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is no longer provided. It is strongly recommended to use [TiCDC](/ticdc/ticdc-overview.md) as an alternative solution for data replication. Although TiDB Binlog v7.5.0 still supports the Point-in-Time Recovery (PITR) scenario, this component will be completely deprecated in future versions. It is recommended to use [PITR](/br/br-pitr-guide.md) as an alternative solution for data recovery.<!--**tw@Oreoxmt** 1575-->

* The [`Fast Analyze`](https://docs.pingcap.com/tidb/v7.4/system-variables#tidb_enable_fast_analyze) feature (experimental) for statistics is deprecated in v7.5.0.<!--**tw@Oreoxmt** -->

* The [incremental collection](https://docs.pingcap.com/tidb/v7.4/statistics#incremental-collection) feature (experimental) for statistics is deprecated in v7.5.0.<!--**tw@Oreoxmt** -->

## Improvements

+ TiDB

    - Optimize the concurrency model of merging GlobalStats: introduce [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) to enable simultaneous loading and merging of statistics, which speeds up the generation of GlobalStats on partitioned tables. Optimize the memory usage of merging GlobalStats to avoid OOM and reduce memory allocations. [#47219](https://github.com/pingcap/tidb/issues/47219) @[hawkingrei](https://github.com/hawkingrei) <!--**tw@hfxsd** -->
    - Optimize the `ANALYZE` process: introduce [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) to better control the `ANALYZE` concurrency to reduce resource consumption. Optimize the memory usage of `ANALYZE` to reduce memory allocation and avoid frequent GC by reusing some intermediate results. [#47275](https://github.com/pingcap/tidb/issues/47275) @[hawkingrei](https://github.com/hawkingrei) <!--**tw@hfxsd** -->
    - 改进 Placement Policy 的使用：增加对全局范围的策略配置，完善常用场景的语法支持  [#45384](https://github.com/pingcap/tidb/issues/45384) @[nolouch](https://github.com/nolouch) <!--**tw@qiancai** -->

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Bug fixes

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Performance test

To learn about the performance of TiDB v7.5.0, you can refer to the [TPC-C performance test report](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc) and [Sysbench performance test report](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench) of the TiDB Dedicated cluster.

## Contributors

We would like to thank the following contributors from the TiDB community: