---
title: TiDB 7.4.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.4.0.
---

# TiDB 7.4.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.4.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.4/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.4.0#version-list)

7.4.0 introduces the following key features and improvements:

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
    <td>Enhance the performance of adding multiple indexes for a table in a single <code>ADD INDEX</code> statement (experimental) <!--Frank, tw@ran-huang--></td>
    <td>Since v6.2.0, you can add multiple indexes for a table in a single <code>ADD INDEX</code> statement. However, the performance is the same as running multiple <code>ADD INDEX</code> statements. After optimization in v7.4.0, the performance of adding multiple indexes in a single SQL statement has been greatly improved.</td>
    </td>
  </tr>
  <tr>
    <td rowspan="3">Reliability and Availability</td>
    <td>Improve the performance and stability of <code>IMPORT INTO</code> and <code>ADD INDEX</code> operations via global sort <!--Frank, tw@ran-huang--></td>
    <td>Before v7.4.0, tasks such as <code>ADD INDEX</code> or <code>IMPORT INTO</code> in the distributed execution framework required TiDB nodes to allocate local disk space for sorting data before importing it into TiKV. This approach involves partial and localized sorting, and often results in data overlaps, leading to increased resource consumption and lower performance and stability of TiKV. With the introduction of the Global Sorting feature in v7.4.0, data is temporarily stored in S3 for global sorting before being imported into TiKV in an orderly manner. This eliminates the need for TiKV to consume extra resources on compactions and significantly improves the performance and stability of operations like <code>ADD INDEX</code> and <code>IMPORT INTO</code>.</td>
  </tr>
  <tr>
    <td>Resource control for background tasks (experimental) <!--Roger, tw@Oreoxmt--></td>
    <td>In v7.1.0, the resource control feature becomes generally available and this feature helps mitigate resource and storage access interference between workloads. TiDB v7.4.0 applies this contorl to background tasks as well. Resource control identifies and manages the resources produced by background tasks, such as auto-analyze, Backup & Restore, load data, and online DDL. This will eventually apply to all background tasks.</td>
  </tr>
  <tr>
    <td>TiFlash supports <a href="https://docs.pingcap.com/tidb/v7.4/tiflash-disaggregated-and-s3" target="_blank">storage-computing separation and S3</a> (GA) <!--Zhang Ye, tw@qiancai--></td>
    <td>TiFlash disaggregated storage and compute architecture and S3 shared storage becomes generally available:
      <ul>
        <li>Disaggregates TiFlash's compute and storage, which is a milestone for elastic HTAP resource utilization.</li>
        <li>Supports using S3-based storage engine, which can provide shared storage at a lower cost.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="4">SQL</td>
    <td>TiDB fully supports partition management <!--Zhang Ye, tw@qiancai--></td>
    <td>Before v7.4.0, Range/List partitioned tables support partition management operations such as <code>TRUNCATE</code>, <code>EXCHANGE</code>, <code>ADD</code>, <code>DROP</code>, and <code>REORGANIZE</code>, and Hash/Key partitioned tables support partition management operations such as <code>ADD</code> and <code>COALESCE</code>.
    
    Now TiDB also supports the following partition management operations:
      <ul>
        <li>Convert partitioned tables to non-partitioned tables</li>
        <li>Partition existing non-partitioned tables</li>
        <li>Modify partition types for existing tables</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>MySQL 8.0 compatibility: support collation <code>utf8mb4_0900_ai_ci</code> <!--Roger, tw@Oreoxmt--></td>
    <td>One notable change in MySQL 8.0 is that the default character set is utf8mb4, and the default collation of utf8mb4 is <code>utf8mb4_0900_ai_ci</code>. TiDB v7.4.0 enhances the compatibility with MySQL 8.0. If you create a database in MySQL 8.0 with the default collation, you can smoothly migrate or replicate it to TiDB.</td>
  </tr>
  <tr>
    <td>TiDB and TiFlash support the <code>ROLLUP</code> modifier and the <code>GROUPING()</code> function <!--Zhang Ye, tw@qiancai--></td>
    <td>The <code>ROLLUP</code> modifier is commonly used in data analysis to summarize data in multiple dimensions. With the <code>ROLLUP</code>modifier, the output of the <code>GROUP BY</code> clause can include additional rows that represent higher-level summary operations, thus enabling you to answer questions at multiple levels of analysis with a single query.  </td>
  </tr>
  <tr>
    <td>TiFlash supports resource control <!--Zhang Ye, tw@Oreoxmt --></td>
    <td>Before v7.4.0, TiDB resource control cannot manage resources of TiFlash. Starting from v7.4.0, TiFlash can manage resources better, improving the overall resource management capabilities of TiDB.</td>
  </tr>
  <tr>
    <td>DB Operations and Observability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.4/system-variables#tidb_service_scope-new-in-v740" target="_blank">Specify the respective TiDB nodes to execute the <code>IMPORT INTO<code> and <code>ADD INDEX<code> SQL statements (experimental)</a> <!--Frank, tw@hfxsd--></td>
    <td>You have the flexibility to specify whether to execute <code>IMPORT INTO</code> or <code>ADD INDEX</code> SQL statements on some of the existing TiDB nodes or newly added TiDB nodes. This approach enables resource isolation from the rest of the TiDB nodes, preventing any impact on business operations while ensuring optimal performance for executing the preceding SQL statements.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Support selecting the TiDB nodes to parallelly execute the backend `ADD INDEX` or `IMPORT INTO` tasks of the distributed execution framework (experimental) [#46453](https://github.com/pingcap/tidb/pull/46453) @[ywqzzy](https://github.com/ywqzzy) **tw@hfxsd** <!--1505-->

    Executing `ADD INDEX` or `IMPORT INTO` tasks in parallel in a resource-intensive cluster can consume a large amount of TiDB node resources, which can lead to cluster performance degradation. Starting from v7.4.0, you can use the system variable [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) to control the service scope of each TiDB node under the [TiDB Backend Task Distributed Execution Framework](/tidb-distributed-execution- framework.md). You can select several existing TiDB nodes or set the TiDB service scope for new TiDB nodes, and all parallel `ADD INDEX` and `IMPORT INTO` tasks only run on these nodes. This mechanism can avoid performance impact on existing services.
    
    For more information, see [documentation](/system-variables.md#tidb_service_scope-new-in-v740).

* Enhance the Partitioned Raft KV storage engine (experimental) [#issue号](链接) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch)  **tw@Oreoxmt** <!--1292-->

    TiDB v6.6.0 introduces the Partitioned Raft KV storage engine as an experimental feature, which uses multiple RocksDB instances to store TiKV Region data, and the data of each Region is independently stored in a separate RocksDB instance.

    In v7.4.0, TiDB further improves the compatibility and stability of the Partitioned Raft KV storage engine. Through large-scale data testing, the compatibility with TiDB ecosystem tools and features such as DM, Dumpling, TiDB Lightning, TiCDC, BR, and PITR is ensured. Additionally, the Partitioned Raft KV storage engine provides more stable performance under mixed read and write workloads, making it especially suitable for write-heavy scenarios. Furthermore, each TiKV node now supports 8 core CPUs and can be configured with 8 TB data storage, and 64 GB memory.

    For more information, see [documentation](/partitioned-raft-kv.md).

* TiFlash supports the disaggregated storage and compute architecture (GA) [#6882](https://github.com/pingcap/tiflash/issues/6882) @[JaySon-Huang](https://github.com/JaySon-Huang) @[JinheLin](https://github.com/JinheLin) @[breezewish](https://github.com/breezewish) @[lidezhu](https://github.com/lidezhu) @[CalvinNeo](https://github.com/CalvinNeo) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) **tw@qiancai** <!--1360-->

    In v7.0.0, TiFlash introduces the disaggregated storage and compute architecture as an experimental feature. With a series of improvements, the disaggregated storage and compute architecture for TiFlash becomes GA starting from v7.4.0.

    In this architecture, TiFlash nodes are divided into two types (Compute Nodes and Write Nodes) and support object storage that is compatible with S3 API. Both types of nodes can be independently scaled for computing or storage capacities. In the disaggregated storage and compute architecture, you can use TiFlash in the same way as the coupled storage and compute architecture, such as creating TiFlash replicas, querying data, and specifying optimizer hints.

    Note that the TiFlash **disaggregated storage and compute architecture** and **coupled storage and compute architecture** cannot be used in the same cluster or converted to each other. You can configure which architecture to use when you deploy TiFlash.

    For more information, see [documentation](/tiflash/tiflash-disaggregated-and-s3.md).

### Performance

* Support pushing down the JSON operator `MEMBER OF` to TiKV [#46307](https://github.com/pingcap/tidb/issues/46307) @[wshwsh12](https://github.com/wshwsh12)  **tw@qiancai** <!--1551-->

    * `value MEMBER OF(json_array)`

    For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* Support pushing down window functions with any frame definition type to TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008)  **tw@qiancai** <!--1381-->

    Before v7.4.0, TiFlash does not support window functions containing `PRECEDING` or `FOLLOWING`, and all window functions containing such frame definitions cannot not be pushed down to TiFlash. Starting from v7.4.0, TiFlash supports frame definitions of all window functions. This feature is enabled automatically, and window functions containing frame definitions will be automatically pushed down to TiFlash for execution when the related requirements are met.

* Introduce cloud storage-based global sort capability to improve the performance and stability of `ADD INDEX` and `IMPORT INTO` tasks in parallel execution [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) **tw@ran-huang** <!--1456-->

    Before v7.4.0, when executing tasks like `ADD INDEX` or `IMPORT INTO` in the distributed parallel execution framework, each TiDB node needs to allocate a significant amount of local disk space for sorting encoded index KV pairs and table data KV pairs. However, due to the lack of global sorting capability, there might be overlapping data between different TiDB nodes and within each individual node during the process. As a result, TiKV has to constantly perform compaction operations while importing these KV pairs into its storage engine, which impacts the performance and stability of `ADD INDEX` and `IMPORT INTO`.

    In v7.4.0, TiDB introduces the [Global Sort](/tidb-global-sort.md) feature. Instead of writing the encoded data locally and sorting it there, the data is now written to cloud storage for global sorting. Once sorted, both the indexed data and table data are imported into TiKV in parallel, thereby improving performance and stability.

    For more information, see [documentation](/tidb-global-sort.md).

* Improve the performance of adding multiple indexes in a single SQL statement by optimizing parallel multi schema change [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@ran-huang** <!--1307-->

    Before v7.4.0, when you use parallel multi schema change to commit multiple `ADD INDEX` operations in a single SQL statement, the performance is the same as using multiple independent SQL statements for `ADD INDEX` operations. However, after optimization in v7.4.0, the performance of adding multiple indexes in a single SQL statement has been greatly improved.

    For more information, see [documentation](链接).

* Support caching execution plans for non-prepared statements (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1355-->

    TiDB v7.0.0 introduces non-prepared plan cache as an experimental feature to improve the load capacity of concurrent OLTP. In v7.4.0, this feature becomes GA. The execution plan cache will be applied to more scenarios, thereby improving the concurrent processing capacity of TiDB.

    Enabling the non-prepared plan cache might incur additional memory and CPU overhead and might not be suitable for all situations. Starting from v7.4.0, this feature is disabled by default. You can enable it using [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) and control the cache size using [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710).

    Additionally, this feature does not support DML statements by default and has certain restrictions on SQL statements. For more details, see [Restrictions](/sql-non-prepared-plan-cache.md#restrictions).

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

### Reliability

* TiFlash supports query-level data spilling [#7738](https://github.com/pingcap/tiflash/issues/7738) @[windtalker](https://github.com/windtalker)  **tw@qiancai** <!--1493-->

    Starting from v7.0.0, TiFlash supports controlling data spilling for three operators: `GROUP BY`, `ORDER BY`, and `JOIN`. This feature prevents issues such as query termination or system crashes when the data size exceeds the available memory. However, managing spilling for each operator individually can be cumbersome and ineffective for overall resource control.

    In v7.4.0, TiFlash introduces the query-level data spilling. By setting the memory limit for a query on a TiFlash node using [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) and the memory ratio that triggers data spilling using [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740), you can conveniently manage the memory usage of a query and have better control over TiFlash memory resources.

    For more information, see [documentation](/tiflash/tiflash-spill-disk.md).

* Support user-defined TiKV read timeout [#45380](https://github.com/pingcap/tidb/issues/45380) @[crazycs520](https://github.com/crazycs520) **tw@hfxsd** <!--1560-->

    Normally, TiKV processes requests very quickly, in a matter of milliseconds. However, when a TiKV node encounters disk I/O jitter or network latency, the request processing time can increase significantly. In versions earlier than v7.4.0, the timeout limit for TiKV requests is fixed and unadjustable. Hence, TiDB has to wait for a fixed-duration timeout response when a TiKV node encounters issues, which results in a noticeable impact on application query performance during jitter.
     
    TiDB v7.4.0 introduces a new system variable [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740), which lets you customize the timeout for RPC read requests that TiDB sends to TiKV in a query. It means that when the request sent to a TiKV node is delayed due to disk or network issues, TiDB can time out faster and resend the request to other TiKV nodes, thus reducing query latency. If timeouts occur for all TiKV nodes, TiDB will retry using the default timeout. Additionally, you can set the timeout for TiDB to send TiKV RPC read requests in a query via the hint [`TIDB_KV_READ_TIMEOUT(N)`](/optimizer-hints.md#tidb_kv_read_timeoutn). This enhancement gives TiDB the flexibility to adapt to unstable network or storage environments, improving query performance and enhancing the user experience.

    For more information, see [documentation](/system-variables.md#tikv_client_read_timeout-new-in-v740).

* Support temporarily modifying some system variable values using an optimizer hint [#issue号](链接) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--923-->

    TiDB v7.4.0 introduces the optimizer hint `SET_VAR()`, which is similar to that of MySQL 8.0. By including the hint `SET_VAR()` in SQL statements, you can temporarily modify the value of system variables during statement execution. This helps you set the environment for different statements. For example, you can actively increase the parallelism of resource-intensive SQL statements or change the optimizer behavior through variables.

    You can find the system variables that can be modified using the hint `SET_VAR()` in [System variables](/system-variables.md). It is strongly recommended not to modify variables that are not explicitly supported, as this might cause unpredictable behavior.

    For more information, see [documentation](/optimizer-hints.md).

* TiFlash supports resource control [#7660](https://github.com/pingcap/tiflash/issues/7660) @[guo-shaoge](https://github.com/guo-shaoge)  **tw@Oreoxmt** <!--1506-->

    In TiDB v7.1.0, the resource control feature becomes generally available and provides resource management capabilities for TiDB and TiKV. In v7.4.0, TiFlash supports the resource control feature, improving the overall resource management capabilities of TiDB. The resource control of TiFlash is fully compatible with the existing TiDB resource control feature, and the existing resource groups will manage the resources of TiDB, TiKV, and TiFlash at the same time.

    To control whether to enable the TiFlash resource control feature, you can configure the TiFlash parameter `enable_resource_control`. After enabling this feature, TiFlash performs resource scheduling and management based on the resource group configuration of TiDB, ensuring the reasonable allocation and use of overall resources.

    For more information, see [documentation](/tidb-resource-control.md).

* TiFlash supports the pipeline execution model (GA) [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@Oreoxmt** <!--1549-->

    Starting from v7.2.0, TiFlash introduces a pipeline execution model. This model centrally manages all thread resources and schedules task execution uniformly, maximizing the utilization of thread resources while avoiding resource overuse. In v7.4.0, TiFlash improves the statistics of thread resource usage, and the pipeline execution model becomes a GA feature and is enabled by default. Since this feature is mutually dependent with the TiFlash resource control feature, TiDB v7.4.0 removes the variable `tidb_enable_tiflash_pipeline_model` used to control whether to enable the pipeline execution model in previous versions. Instead, you can enable or disable the pipeline execution model and the TiFlash resource control feature by configuring the TiFlash parameter `tidb_enable_resource_control`.

    For more information, see [documentation](/tiflash/tiflash-pipeline-model.md).

* Add the option of optimizer mode [#46080](https://github.com/pingcap/tidb/issues/46080) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1527-->

    In v7.4.0, TiDB introduces a new system variable [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740), which controls the estimation method used by the optimizer. The default value `moderate` maintains the previous behavior of the optimizer, where it uses runtime statistics to adjust estimations based on data changes. If this variable is set to `determinate`, the optimizer generates execution plans solely based on statistics without considering runtime corrections.

    For long-term stable OLTP applications or situations where you are confident in the existing execution plans, it is recommended to switch to `determinate` mode after testing. This reduces potential plan changes.

    For more information, see [documentation](/system-variables.md#tidb_opt_objective-new-in-v740).

* TiDB resource control supports managing background tasks (experimental) [#issue号](链接) @[glorv](https://github.com/glorv) **tw@Oreoxmt** <!--1448-->

    Background tasks, such as data backup and automatic statistics collection, are low-priority but consume many resources. These tasks are usually triggered periodically or irregularly. During execution, they consume a lot of resources, thus affecting the performance of online high-priority tasks. Starting from v7.4.0, the TiDB resource control feature supports managing background tasks. This feature reduces the performance impact of low-priority tasks on online application, enabling rational resource allocation, and greatly improving cluster stability.

    TiDB supports the following types of background tasks:

    - `lightning`: perform import tasks using [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md). Both physical and logical import modes of TiDB Lightning are supported.
    - `br`: perform backup and restore tasks using [BR](/br/backup-and-restore-overview.md). PITR is not supported.
    - `ddl`: control the resource usage during the batch data write back phase of Reorg DDLs.
    - `stats`: the [collect statistics](/statistics.md#collect-statistics) tasks that are manually executed or automatically triggered by TiDB.

    By default, the task types that are marked as background tasks are empty, and the management of background tasks is disabled. This default behavior is the same as that of versions prior to TiDB v7.4.0. To manage background tasks, you need to manually modify the background task types of the `default` resource group.

    For more information, see [documentation](/tidb-resource-control.md).

* Enhance the ability to lock statistics [#issue号](链接) @[hi-rustin](https://github.com/hi-rustin) **tw@ran-huang** <!--1557-->

    In v7.4.0, TiDB has enhanced the ability to [lock statistics](/statistics.md#lock-statistics). Now, to ensure operational security, locking and unlocking statistics require the same privileges as collecting statistics. In addition, TiDB supports locking and unlocking statistics for specific partitions, providing greater flexibility. If you are confident in queries and execution plans in the database and want to prevent any changes from occurring, you can lock statistics to enhance stability.

    For more information, see [documentation](/statistics.md#锁定统计信息).

### SQL

* TiDB fully supports partition type management [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss) **tw@qiancai** <!--1370-->

    Before v7.4.0, partition types of partitioned tables in TiDB cannot be modified. Starting from v7.4.0, TiDB supports modifying partitioned tables to non-partitioned tables or non-partitioned tables to partitioned tables, and supports changing partition types. Hence, now you can flexibly adjust the partition type and number for a partitioned table. For example, you can use the `ALTER TABLE t PARTITION BY ...` statement to modify the partition type.

    For more information, see [documentation](/partitioned-table.md#convert-a-partitioned-table-to-a-non-partitioned-table).

* TiDB supports using the `ROLLUP` modifier and the `GROUPING` function [#44487](https://github.com/pingcap/tidb/issues/44487) @[AilinKid](https://github.com/AilinKid) **tw@qiancai** <!--1287-->

    The `WITH ROLLUP` modifier and `GROUPING` function are commonly used in data analysis for multi-dimensional data summarization. Starting from v7.4.0, you can use the `WITH ROLLUP` modifier and `GROUPING` function in the `GROUP BY` clause. For example, you can use the `WITH ROLLUP` modifier in the `SELECT ... FROM ... GROUP BY ... WITH ROLLUP` syntax.

   For more information, see [documentation](functions-and-operators/group-by-modifier.md).

### DB operations

- note 1

* Support collation `utf8mb4_0900_ai_ci` and `utf8mb4_0900_bin` [#37566](https://github.com/pingcap/tidb/issues/37566) @[YangKeao](https://github.com/YangKeao) @[zimulala](https://github.com/zimulala) @[bb7133](https://github.com/bb7133) **tw@Oreoxmt** <!--1186-->

    TiDB v7.4.0 enhances the support for migrating data from MySQL 8.0 and adds two collations: `utf8mb4_0900_ai_ci` and `utf8mb4_0900_bin`. `utf8mb4_0900_ai_ci` is the default collation in MySQL 8.0.

    TiDB v7.4.0 also introduces the system variable `default_collation_for_utf8mb4` which is compatible with MySQL 8.0. This enables you to specify the default collation for the utf8mb4 character set and provides compatibility with migration or data replication from MySQL 5.7 or earlier versions.

    For more information, see [documentation](/character-set-and-collation#character-sets-and-collations-supported-by-tidb).

### Observability

* Support adding session connection IDs and session aliases to logs [#46071](https://github.com/pingcap/tidb/issues/46071) @[lcwangchao](https://github.com/lcwangchao) **tw@hfxsd** <!--无 FD 及用户文档，只提供 release notes-->
   
     When you troubleshoot a SQL execution problem, it is often necessary to correlate the contents of TiDB component logs to pinpoint the root cause. Starting from v7.4.0, TiDB can write session connection IDs (`CONNECTION_ID`) to session-related logs, including TiDB logs, slow query logs, and slow logs from the coprocessor on TiKV. You can correlate the contents of several types of logs based on session connection IDs to improve troubleshooting and diagnostic efficiency. 

     In addition, by setting the session-level system variable [`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740), you can add custom identifiers to the logs mentioned above. With this ability to inject your application identification information into the logs, you can correlate the contents of the logs with the application, build the link from the application to the logs, and reduce the difficulty of diagnosis.     

* TiDB Dashboard supports displaying execution plans in a table view [#1589](https://github.com/pingcap/tidb-dashboard/issues/1589) @[baurine](https://github.com/baurine) **tw@Oreoxmt** <!--1434-->

    In v7.4.0, TiDB Dashboard supports displaying execution plans on the **Slow Query** and **SQL Statement** pages in a table view to improve the diagnosis experience.

    For more information, see [documentation](链接).

### Data migration

* Support real-time update of checkpoint for continuous data validation [#issue号](链接) @[lichunzhu](https://github.com/lichunzhu) **tw@ran-huang** <!--1496-->

    Before v7.4.0, the continuous data validation feature ensures the data consistency during replication from DM to downstream. This serves as the basis for cutting over business traffic from the upstream database to TiDB. However, due to various factors such as replication delay and waiting for re-validation of inconsistent data, the continuous validation checkpoint must be refreshed every few minutes. This is unacceptable for some business scenarios where the cutover time is limited to a few tens of seconds.

    With the introduction of real-time updating of checkpoint for continuous data validation, you can now provide the binlog position from the upstream database. Once the continuous validation program detects this binlog position in memory, it immediately refreshes the checkpoint instead of refreshing it every few minutes. Therefore, you can quickly perform cut-off operations based on this immediately updated checkpoint.

    For more information, see [documentation](链接).

* Enhance the `IMPORT INTO` feature [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1494-->

    Starting from v7.4.0, you can add the `CLOUD_STORAGE_URI` option in the `IMPORT INTO` statement to enable the [global sorting](/tidb-global-sort.md) feature (experimental), which helps boost import performance and stability. In the `CLOUD_STORAGE_URI` option, you can specify a cloud storage address for the encoded data.

    In addition, in v7.4.0, the `IMPORT INTO` feature introduces the following functionalities:

    - Support configuring the `Split_File` option, which allows you to split a large CSV file into multiple 256 MiB small CSV files for parallel processing, improving import performance.
    - Support importing compressed CSV and SQL files. The supported compression formats include `.gzip`, `.gz`, `.zstd`, `.zst`, and `.snappy`.

    For more information, see [documentation](sql-statements/sql-statement-import-into.md).

* Dumpling supports the user-defined terminator when exporting data to CSV files [#46982](https://github.com/pingcap/tidb/issues/46982) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1571-->

    Before v7.4.0, Dumpling uses "\r\n" as the line terminator when exporting data to a CSV file. As a result, certain downstream systems that only recognize "\n" as the terminator cannot parse the exported CSV file, or have to use a third-party tool for conversion before parsing the file.
    
    Starting from v7.4.0, Dumpling introduces a new parameter `--csv-line-terminator`. This parameter allows you to specify a desired terminator when you export data to a CSV file. This parameter supports `\r\n' and `\n'. The default terminator is `\r\n' to keep consistent with earlier versions.
     
    For details, see [documentation](/dumpling-overview.md#option-list-of-dumpling).

* TiCDC supports replicating data to Pulsar [#9413](https://github.com/pingcap/tiflow/issues/9413) @[yumchina](https://github.com/yumchina) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1552-->

    Pulsar is a cloud-native and distributed message streaming platform that significantly enhances your real-time data streaming experience. Starting from v7.4.0, TiCDC supports replicating change data to Pulsar in `canal-json` format to achieve seamless integration with Pulsar. With this feature, TiCDC provides you with the ability to easily capture and replicate TiDB changes to Pulsar, offering new possibilities for data processing and analytics capabilities. You can develop your own consumer applications that read and process newly generated change data from Pulsar to meet specific business needs.

    For details, see [documentation](/ticdc/ticdc-sink-to-pulsar.md).

- TiCDC improves large message handling with claim-check pattern [#9153](https://github.com/pingcap/tiflow/issues/9153) @[3AceShowHand](https://github.com/3AceShowHand) **tw@ran-huang** <!--1550-->

    Before v7.4.0, TiCDC is unable to send large messages exceeding the maximum message size (`max.message.bytes`) of Kafka to downstream. Starting from v7.4.0, when configuring a changefeed with Kafka as the downstream, you can specify an external storage location for storing the large message, and send a reference message containing the address of the large message in the external storage to Kafka. When consumers receive this reference message, they can retrieve the message content from the external storage address. 
    
    For more information, see [documentation]().

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.3.0 to the current version (v7.4.0). If you are upgrading from v7.2.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

* Starting with v7.4.0, TiDB is compatible with core MySQL 8.0 features, and `version()` returns the version prefixed with `8.0.11`.  

### Behavior changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740) | Newly added | Controls the default collation for the `utf8mb4` character set. The default value is `utf8mb4_bin`. |
| [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v740) | Newly added | Controls whether the optimizer will select hash joins for tables. The value is `ON` by default. If set to `OFF`, the optimizer avoids selecting a hash join of a table unless there is no execution plan available. |
| [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740) | Newly added | This variable controls the objective of the optimizer. `moderate` maintains the default behavior in versions prior to TiDB v7.4.0, where the optimizer tries to use more information to generate better execution plans. `determinate` mode tends to be more conservative and makes the execution plan more stable. |
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) | Newly added | This variable is an instance-level system variable. You can use it to control the service scope of TiDB nodes under the [TiDB distributed execution framework](/tidb-distributed-execution-framework.md). When you set `tidb_service_scope` of a TiDB node to `background`, the TiDB distributed execution framework schedules that TiDB node to execute background tasks, such as [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) and [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md). |
| [`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740) |  Newly added | Controls the value of the `session_alias` column in the logs related to the current session. |
| [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740) | Newly added | Controls the timeout for TiDB to send a TiKV RPC read request in a query. The default value `0` indicates that the default timeout (usually 40 seconds) is used. |
|        |                              |      |
| [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) | Newly added | Limits the maximum memory usage for a query on a TiFlash node. When the memory usage of a query exceeds this limit, TiFlash returns an error and terminates the query. The default valus is `0`, which means no limit.|
| [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) | Newly added | Controls the threshold for TiFlash [query-level spilling](/tiflash/tiflash-spill-disk.md#query-level-spilling). The default value is `0.7`. |
[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | Modified |  Changes the default value from `ON` to `OFF` after further tests, meaning that non-prepared execution plan cache is disabled. |
| `tidb_enable_tiflash_pipeline_model` | Deleted | This variable was used to control whether to enable the TiFlash pipeline execution model. Starting from v7.4.0, the TiFlash pipeline execution model is automatically enabled when the TiFlash resource control feature is enabled. |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [enable-stats-cache-mem-quota](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610) | Modified | The default value is changed from `false` to `true`, which means the memory limit for caching TiDB statistics is enabled by default. |
| TiFlash | [`profiles.default.enable_resource_control`](/tiflash/tiflash-configuration.md) | Newly added | Controls whether to enable the TiFlash resource control feature. |
| TiFlash | [`flash.compact_log_min_gap`](/tiflash/tiflash-configuration.md) | Newly added | When the gap between the `applied_index` advanced by the current Raft state machine and the `applied_index` at the last disk spilling exceeds `compact_log_min_gap`, TiFlash executes the `CompactLog` command from TiKV and spills data to disk. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md) | Modified | Change the default value from `4` to `5`. The new format can reduce the number of physical files by merging smaller files. |
| Dumpling  | [`--csv-line-terminator`](/dumpling-overview.md#option-list-of-dumpling) | Newly added | Specify the desired terminator with this option. This option supports "\r\n" and "\n". The default value is "\r\n", which is consistent with the earlier versions. |
| TiCDC | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage) | Modified | This configuration item adds a new value `claim-check`. When it is set to `claim-check`, TiCDC Kafka sink supports sending the message to external storage when the message size exceeds the limit and sends a message to Kafka containing the address of this large message in external storage. |
| TiCDC | [`claim-check-storage-uri`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage) | Newly added | When `large-message-handle-option` is set to `claim-check`, `claim-check-storage-uri` must be set to a valid external storage address. Otherwise, creating a changefeed results in an error. |
| TiCDC | [`large-message-handle-compression`](/ticdc/ticdc-sink-to-kafka.md#ticdc-data-compression) | Newly added | Controls whether to enable compression during encoding. The default value is empty, which means not enabled. |

## Deprecated features

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - Improve write performance during random write workloads by optimizing the spilling policy of the TiFlash write process [#7564](https://github.com/pingcap/tiflash/issues/7564) @[CalvinNeo](https://github.com/CalvinNeo) **tw@qiancai** <!--1309-->
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

## Contributors

We would like to thank the following contributors from the TiDB community:

- [yumchina](https://github.com/yumchina)
