---
title: TiDB 8.4.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.4.0.
---

# TiDB 8.4.0 Release Notes

Release date: xx xx, 2024

TiDB version: 8.4.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.4/quick-start-with-tidb)

8.4.0 introduces the following key features and improvements:

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
    <td rowspan="4">Scalability and Performance</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_enable_instance_plan_cache-new-in-v840">Instance-level execution plan cache</a> (experimental)**tw@Oreoxmt 1569**</td>
    <td>Instance-level execution plan cache allows all sessions within the same TiDB instance to share the execution plan cache. This feature reduces SQL compilation time by caching more execution plans in memory, decreasing overall SQL execution time. It improves OLTP performance and throughput while providing better control over memory usage and enhancing database stability.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/partitioned-table#global-indexes">Global indexes for partitioned tables (GA)</a>**tw@hfxsd 1961**</td>
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned columns, and remove the restriction that a unique key must contain the partition key. This feature extends the usage scenarios of TiDB partitioned tables, and avoids some of the application modification work required for data migration.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_tso_client_rpc_mode-new-in-v840">Parallel mode for TSO requests</a>**tw@qiancai 1893**</td>
    <td>In high-concurrency scenarios, you can use this feature to reduce the wait time for retrieving TSO and improve the cluster throughput.</td>
  </tr>
  <tr>
    <td>Improve query performance for cached tables**tw@hfxsd 1965**</td>
    <td>Improve query performance for index scanning on cached tables, with improvements of up to 5.4 times in some scenarios. For high-speed queries on small tables, using cached tables can significantly enhance overall performance.</td>
  </tr>
  <tr>
    <td rowspan="4">Reliability and Availability</td>
    <td>Support more triggers for runaway queries, and support switching resource groups**tw@hfxsd 1832 tw@lilin90 1800**</td>
    <td>Runaway Queries offer an effective way to mitigate the impact of unexpected SQL performance issues on systems. TiDB v8.4.0 introduces the number of keys processed by the Coprocessor (<code>PROCESSED_KEYS</code>) and request units (<code>RU</code>) as identifying conditions, and puts identified queries into the specified resource group for more precise identification and control of runaway queries.</td>
  </tr>
  <tr>
    <td>Support setting the maximum limit on resource usage for background tasks of resource control **tw@hfxsd 1909**</td>
    <td>By setting a maximum percentage limit on background tasks of resource control, you can control their resource consumption based on the needs of different application systems. This keeps background task consumption at a low level and ensures the quality of online services.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/tiproxy-traffic-replay">TiProxy supports traffic capture and replay</a> (experimental)**tw@Oreoxmt 1942**</td>
    <td>Use TiProxy to capture real workloads from TiDB production clusters before major operations such as cluster upgrades, migrations, or deployment changes. Replay these workloads on target test clusters to validate performance and ensure successful changes.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_auto_analyze_concurrency-new-in-v840">Concurrent automatic statistics collection</a>**tw@Oreoxmt 1739**</td>
    <td>You can set the concurrency within a single automatic statistics collection task using the system variable <code>tidb_auto_analyze_concurrency</code>. TiDB automatically determines the concurrency of scanning tasks based on node scale and hardware specifications. This improves statistics collection efficiency by fully utilizing system resources, reduces manual tuning, and ensures stable cluster performance.</td>
  </tr>
  <tr>
    <td rowspan="1">SQL</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/vector-search-overview">Vector search</a> (experimental) **tw@qiancai 1898**</td>
    <td>Vector search is a search method based on data semantics, which provides more relevant search results. As one of the core functions of AI and large language models (LLMs), vector search can be used in various scenarios such as Retrieval-Augmented Generation (RAG), semantic search, and recommendation systems.</td>
  </tr>
  <tr>
    <td rowspan="3">DB Operations and Observability</td>
    <td>Display TiKV and TiDB CPU times in memory tables**tw@hfxsd 1877**</td>
    <td>The CPU time is now integrated into a system table, displayed alongside other metrics for sessions or SQL, letting you observe high CPU consumption operations from multiple perspectives, and improves diagnostic efficiency. This is especially useful for diagnosing scenarios such as CPU spikes in instances or read/write hotspots in clusters.</td>
  </tr>
  <tr>
    <td>Support viewing aggregated TiKV CPU time by table or database **tw@lilin90 1878**</td>
    <td>When hotspot issues are not caused by individual SQL statements, using the aggregated CPU time by table or database level in <a href="https://docs.pingcap.com/zh/tidb/v8.4/top-sql">TOP SQL</a> can help you quickly identify the tables or applications responsible for the hotspots, significantly improving the efficiency of diagnosing hotspot and CPU consumption issues.</td>
  </tr>
  <tr>
    <td>Support backing up TiKV instances with IMDSv2 service enabled**tw@hfxsd 1945**</td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">AWS EC2 now uses IMDSv2 as the default metadata service</a>. TiDB supports backing up data from TiKV instances that have IMDSv2 enabled, helping you run TiDB clusters more effectively in public cloud services.</td>
  </tr>
  <tr>
    <td rowspan="1">Security</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/br-pitr-manual#encrypt-log-backup-data">Client-side encryption of log backup data</a> (experimental) **tw@qiancai 1920**</td>
    <td>Before uploading log backup data to your backup storage, you can encrypt the backup data to ensure its security during storage and transmission.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Performance

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

* Introduces parallel batching modes for TSO requests, reducing TSO retrieval latency [#54960](https://github.com/pingcap/tidb/issues/54960) @[MyonKeminta](https://github.com/MyonKeminta) **tw@qiancai** <!--1893-->

    When requesting TSO from PD, TiDB collects multiple requests during a specific period and processes them in batches serially to decrease the number of Remote Procedure Call (RPC) requests and reduce PD workload. In latency-sensitive scenarios, however, the performance of this serial batching mode is not ideal.

    In v8.4.0, TiDB introduces parallel batching modes for TSO requests with different concurrency capabilities. Parallel modes reduce TSO retrieval latency but might increase the PD workload. To set a parallel RPC mode for retrieving TSO, configure the [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840) system variable.

    For more information, see [documentation](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840).

* Optimize the execution efficiency of the hash join operator for TiDB (experimental) [#55153](https://github.com/pingcap/tidb/issues/55153) [#53127](https://github.com/pingcap/tidb/issues/53127) @[windtalker](https://github.com/windtalker) @[xzhangxian1008](https://github.com/xzhangxian1008) @[XuHuaiyu](https://github.com/XuHuaiyu) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1633-->

    In v8.4.0, TiDB introduces an optimized version of the hash join operator to improve its execution efficiency. Currently, the optimized version of the hash join applies only to inner join and outer join operations and is disabled by default. To enable this optimized version, configure the [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840) system variable to `optimized`.

    For more information, see [documentation](/system-variables.md#tidb_hash_join_version-new-in-v840).

* Support pushing down the following date functions to TiKV [#17529](https://github.com/tikv/tikv/issues/17529) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1716-->

    * `DATE_ADD()`
    * `DATE_SUB()`
    * `ADDDATE()`
    * `SUBDATE()`

  For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* Support instance-level execution plan cache (experimental) [#54057](https://github.com/pingcap/tidb/issues/54057) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1569-->

    Instance-level execution plan cache allows all sessions within the same TiDB instance to share the execution plan cache. This feature significantly reduces TiDB query response time, increases cluster throughput, decreases the possibility of execution plan mutations, and maintains stable cluster performance. Compared with session-level execution plan cache, instance-level execution plan cache offers the following advantages:

    - Eliminates redundancy, caching more execution plans with the same memory consumption.
    - Allocates a fixed-size memory on the instance, limiting memory usage more effectively.

    In v8.4.0, instance-level execution plan cache only supports caching query execution plans and is disabled by default. You can enable this feature using [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840) and set its maximum memory usage using [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840). Before enabling this feature, disable [Prepared execution plan cache](/sql-prepared-plan-cache.md) and [Non-prepared execution plan cache](/sql-non-prepared-plan-cache.md).

    For more information, see [documentation](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840).

* TiDB Lightning's logical import mode supports prepared statements and client statement cache [#54850](https://github.com/pingcap/tidb/issues/54850) @[dbsid](https://github.com/dbsid) **tw@lilin90** <!--1922-->

    By enabling the `logical-import-prep-stmt` configuration item, the SQL statements executed in TiDB Lightning's logical import mode will use prepared statements and client statement cache. This reduces the cost of TiDB SQL parsing and compilation, improves SQL execution efficiency, and increases the likelihood of hitting the execution plan cache, thereby speeding up logical import.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md).

* Partitioned tables support global indexes (GA) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) @[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust) @[L-maple](https://github.com/L-maple) **tw@hfxsd** <!--1961-->

    In early TiDB versions, the partitioned table has some limitations because it does not support global indexes. For example, the unique key must use every column in the table's partition expression. If the query condition does not use the partition key, the query will scan all partitions, resulting in poor performance. Starting from v7.6.0, the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) is introduced to enable the global index feature. But this feature was under development at that time and it is not recommended to enable it.

    Starting from v8.3.0, the global index feature is released as an experimental feature. You can explicitly create a global index for a partitioned table with the `GLOBAL` keyword. This removes the restriction that a unique key in a partitioned table must include all columns used in the partition expression, allowing for more flexible application requirements. Additionally, global indexes also improve the performance of queries based on non-partitioned columns.

    In v8.4.0, this feature becomes generally available (GA). You must use the keyword `GLOBAL` to create a global index, instead of setting the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) to enable the global index feature. From v8.4.0 this system variable is deprecated and is always `ON`.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

* Improve query performance for cached tables in some scenarios [#43249](https://github.com/pingcap/tidb/issues/43249) @[tiancaiamao](https://github.com/tiancaiamao) **tw@hfxsd** <!--1965-->

    In v8.4.0, TiDB improves the query performance of cached tables by up to 5.4 times when executing `SELECT ... LIMIT 1` with `IndexLookup`. In addition, TiDB improves the performance of `IndexLookupReader` in full table scan and primary key query scenarios.

### Reliability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

* Runaway queries support the number of processed keys and request units as thresholds [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp) **tw@lilin90** <!--1800-->

    Starting from v8.4.0, TiDB can identify runaway queries based on the number of processed keys (`PROCESSED_KEYS`) and request units (`RU`). Compared with execution time (`EXEC_ELAPSED`), these new thresholds more accurately define the resource consumption of queries, avoiding identification bias when overall performance decreases.

    You can set multiple conditions simultaneously, and a query is identified as a runaway query if any condition is met.

    You can observe the corresponding fields (`RESOURCE_GROUP`, `MAX_REQUEST_UNIT_WRITE`, `MAX_REQUEST_UNIT_READ`, `MAX_PROCESSED_KEYS`) in the [Statement Summary Tables](/statement-summary-tables.md) to determine the condition values based on historical execution.

    For more information, see [documentation](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

* Support switching resource groups for runaway queries [#54434](https://github.com/pingcap/tidb/issues/54434) @[JmPotato](https://github.com/JmPotato) **tw@hfxsd** <!--1832-->

    Starting from TiDB v8.4.0, you can switch the resource group of runaway queries to a specific one. If the `COOLDOWN` mechanism fails to lower resource consumption, you can create a [resource group](/tidb-resource-control.md#create-a-resource-group) and set the `SWITCH_GROUP` parameter to move identified runaway queries to this group. Meanwhile, subsequent queries within the same session will continue to execute in the original resource group. By switching resource groups, you can manage resource usage more precisely, and control the resource consumption more strictly.

    For more information, see [documentation](/tidb-resource-control.md#query_limit-parameters).

* Support setting the cluster-level Region scattering strategy using the `tidb_scatter_region` system variable [#55184](https://github.com/pingcap/tidb/issues/55184) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1927-->

    Before v8.4.0, the `tidb_scatter_region` system variable can only be enabled or disabled. When it is enabled, TiDB applies a table-level scattering strategy during batch table creation. However, when creating hundreds of thousands of tables in a batch, this strategy results in a concentration of Regions in a few TiKV nodes, causing OOM (Out of Memory) issues in those nodes.

    Starting from v8.4.0, `tidb_scatter_region` is changed to the string type. It now supports a cluster-level scattering strategy, which can help avoid TiKV OOM issues in the preceding scenario.

    For more information, see [documentation](/system-variables.md#tidb_scatter_region).

* Support setting the maximum limit on resource usage for background tasks of resource control [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv) **tw@hfxsd** <!--1909-->

    TiDB resource control can identify and lower the priority of background tasks. In certain scenarios, you might want to limit the resource consumption of background tasks, even when resources are available. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set the maximum percentage of resources that background tasks can consume. Each node will keep the resource usage of all background tasks below this percentage. This feature enables precise control over resource consumption for background tasks, further enhancing cluster stability.

    For more information, see [documentation](/tidb-resource-control.md#manage-background-tasks).

* Optimize the resource allocation strategy of resource groups [#50831](https://github.com/pingcap/tidb/issues/50831) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1833-->

    TiDB improves the resource allocation strategy in v8.4.0 to better meet user expectations for resource management.

    - Controlling the resource allocation of large queries at runtime to avoid exceeding the resource group limit, combined with runaway queries `COOLDOWN`. This can help identify and reduce the concurrency of large queries, and reduce instantaneous resource consumption.
    - Adjusting the default priority scheduling strategy. When tasks of different priorities run simultaneously, high-priority tasks receive more resources.

### Availability

* TiProxy supports traffic replay (experimental) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1942-->

    Starting from TiProxy v1.3.0, you can use `tiproxyctrl` to connect to the TiProxy instance, capture access traffic in a TiDB production cluster, and replay it in a test cluster at a specified rate. This feature enables you to reproduce actual workloads from the production cluster in a test environment, verifying SQL statement execution results and performance.

    Traffic replay is useful in the following scenarios:

    - Validate TiDB version upgrades
    - Assess change impact
    - Validate performance before scaling TiDB
    - Test performance limits

    For more information, see [documentation](/tiproxy/tiproxy-traffic-replay.md).

### SQL

* Support vector search (experimental) [#54245](https://github.com/pingcap/tidb/issues/54245) [#9032](https://github.com/pingcap/tiflash/issues/9032) @[breezewish](https://github.com/breezewish) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[EricZequan](https://github.com/EricZequan) @[zimulala](https://github.com/zimulala) @[JaySon-Huang](https://github.com/JaySon-Huang) @[winoros](https://github.com/winoros) @[wk989898](https://github.com/wk989898) **tw@qiancai** <!--1898-->

    Vector search is a search method based on data semantics, which provides more relevant search results. As one of the core functions of AI and large language models (LLMs), vector search can be used in various scenarios such as Retrieval-Augmented Generation (RAG), semantic search, and recommendation systems.

    Starting from v8.4.0, TiDB supports [vector data types](/vector-search-data-types.md) and [vector search indexes](/vector-search-index.md), offering powerful vector search capabilities. TiDB vector data types support up to 16,383 dimensions and support various [distance functions](/vector-search-functions-and-operators.md#vector-functions), including L2 distance (Euclidean distance), cosine distance, negative inner product, and L1 distance (Manhattan distance).

    To start vector search, you only need to create a table with vector data types, insert vector data, and then perform a query of vector data. You can also perform mixed queries of vector data and traditional relational data.

    To enhance the performance of vector search, you can create and use [vector search indexes](vector-search-index.md). Note that TiDB vector search indexes rely on TiFlash. Before using vector search indexes, make sure that TiFlash nodes are deployed in your TiDB cluster.

    For more information, see [documentation](/vector-search-overview.md).

### DB operations

* BR supports client-side encryption of log backup data (experimental) [#55834](https://github.com/pingcap/tidb/issues/55834) @[Tristan1900](https://github.com/Tristan1900) **tw@qiancai** <!--1920-->

     In earlier TiDB versions, only snapshot backup data can be encrypted on the client side. Starting from v8.4.0, log backup data can also be encrypted on the client side. Before uploading log backup data to your backup storage, you can encrypt the backup data to ensure its security via one of the following methods:

    - Encrypt using a custom fixed key
    - Encrypt using a master key stored on a local disk
    - Encrypt using a master key managed by a Key Management Service (KMS)

  For more information, see [documentation](/br/br-pitr-manual.md#encrypt-log-backup-data).

* BR requires fewer privileges when restoring backup data in a cloud storage system [#55870](https://github.com/pingcap/tidb/issues/55870) @[Leavrth](https://github.com/Leavrth) **tw@Oreoxmt** <!--1943-->

    Before v8.4.0, BR writes checkpoint information about the restore progress to the backup storage system during restore. These checkpoints enable quick resumption of interrupted restores. Starting from v8.4.0, BR writes restore checkpoint information to the target TiDB cluster instead. This means that BR only requires read access to the backup directories during restore.

    For more information, see [documentation](/br/backup-and-restore-storages.md#authentication).

### Observability

* Display the CPU time consumed by TiDB and TiKV in the system table [#55542](https://github.com/pingcap/tidb/issues/55542) @[yibin87](https://github.com/yibin87) **tw@hfxsd** <!--1877-->

    The [Top SQL page](/dashboard/top-sql.md) of [TiDB Dashboard](/dashboard/dashboard-intro.md) displays SQL statements with high CPU consumption. Starting from v8.4.0, TiDB adds CPU time consumption information to the system table, presented alongside other metrics for sessions or SQL, making it easier to observe high CPU consumption operations from multiple perspectives. This information can help you quickly identify the causes of issues in scenarios like instance CPU spikes or read/write hotspots in clusters.

    - The [statement summary tables](/statement-summary-tables.md) add `AVG_TIDB_CPU_TIME` and `AVG_TIKV_CPU_TIME`, showing the average CPU time consumed by individual SQL statements historically.
    - The [INFORMATION_SCHEMA.PROCESSLIST](/information-schema/information-schema-processlist.md) table adds `TIDB_CPU` and `TIKV_CPU`, showing the cumulative CPU consumption of the SQL statements currently being executed in a session.
    - The [slow query Log](/analyze-slow-queries.md) adds the `Tidb_cpu_time` and `Tikv_cpu_time` fields, showing the CPU time of captured SQL statements.

  By default, the CPU time consumed by TiKV is displayed. Collecting the CPU time consumed by TiDB brings additional overhead (about 8%), so the CPU time consumed by TiDB only shows the actual value when [Top SQL](https://github.com/dashboard/top-sql.md) is enabled; otherwise, it always show as `0`.

    For more information, see [documentation](/information-schema/information-schema-processlist.md) and [documentation](information-schema/information-schema-slow-query.md).

* Top SQL supports viewing aggregated CPU time results by table or database [#55540](https://github.com/pingcap/tidb/issues/55540) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1878-->

    Before v8.4.0, [Top SQL](/dashboard/top-sql.md) aggregates CPU time by SQL. If CPU time is not consumed by a few SQL statements, aggregation by SQL cannot effectively identify issues. Starting from v8.4.0, you can choose to aggregate CPU time **By TABLE** or **By DB**. In scenarios with multiple systems, the new aggregation method can more effectively identify load changes from a specific system, improving diagnostic efficiency.

    For more information, see [documentation](/dashboard/top-sql.md).

### Security

* BR supports AWS IMDSv2 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu) **tw@hfxsd** <!--1945-->

    When deploying TiDB on Amazon EC2, BR supports AWS Instance Metadata Service Version 2 (IMDSv2). You can configure your EC2 instance to allow BR to use the IAM role associated with the instance for appropriate permissions to access Amazon S3.

    For more information, see [documentation](/backup-and-restore-storages#authentication).

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Data migration

* TiCDC Claim-Check supports sending only the `value` field of Kafka messages to external storage [#11396](https://github.com/pingcap/tiflow/issues/11396) @[3AceShowHand](https://github.com/3AceShowHand) **tw@Oreoxmt** <!--1919-->

    Before v8.4.0, when the Claim-Check feature is enabled (by setting `large-message-handle-option` to `claim-check`), TiCDC encodes and stores both the `key` and `value` fields in the external storage system when handling large messages.

    Starting from v8.4.0, TiCDC supports sending only the `value` field of Kafka messages to external storage. This feature is only applicable to non-Open Protocol protocols. You can control this feature by setting the `claim-check-raw-value` parameter.

    For more information, see [documentation](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only).

* TiCDC introduces Checksum V2 to verify old values in Update or Delete events [#10969](https://github.com/pingcap/tiflow/issues/10969) @[3AceShowHand](https://github.com/3AceShowHand) **tw@Oreoxmt** <!--1917-->

    Starting from v8.4.0, TiDB and TiCDC introduce the Checksum V2 algorithm to address issues of Checksum V1 in verifying old values in Update or Delete events after `ADD COLUMN` or `DROP COLUMN` operations. For clusters created in v8.4.0 or later, or clusters upgraded to v8.4.0, TiDB uses Checksum V2 by default when single-row data checksum verification is enabled. TiCDC supports handling both Checksum V1 and V2. This change only affects TiDB and TiCDC internal implementation and does not affect checksum calculation methods for downstream Kafka consumers.

    For more information, see [documentation](/ticdc/ticdc-integrity-check.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.3.0 to the current version (v8.4.0). If you are upgrading from v8.2.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* Behavior change

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`log_bin`](/system-variables.md#log_bin) | Deleted | In v8.4.0, [TiDB Binlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) is removed. This variable indicates whether TiDB Binlog is used, and is deleted starting from v8.4.0. |
| [`sql_log_bin`](/system-variables.md#sql_log_bin) | Deleted | In v8.4.0, [TiDB Binlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) is removed. This variable indicates whether to write changes to TiDB Binlog or not, and is deleted starting from v8.4.0. |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) | Deprecated | In v8.4.0, this variable is deprecated. Its value will be fixed to the default value `ON`, that is, [global index](/partitioned-table.md#global-indexes) is enabled by default. You only need to add the keyword `GLOBAL` to the corresponding column when executing `CREATE TABLE` or `ALTER TABLE` to create a global index. |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50) | Deprecated | In v8.4.0, this variable is deprecated. Its value will be fixed to the default value `ON`, that is, [list partitioning](/partitioned-table.md#list-partitioning) is enabled by default. |
| [`tidb_enable_table_partition`](/system-variables.md#tidb_enable_table_partition) | Deprecated | In v8.4.0, this variable is deprecated. Its value will be fixed to the default value `ON`, that is, [table partitioning](/partitioned-table.md) is enabled by default. |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency) | Modified | Changes the value range from `[1, 18446744073709551615]` to `[1, 128]`. |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) | Modified | Changes the default value from `OFF` to `ON`. Starting from v8.4.0, Index Join is supported by default when the inner table has `Selection`, `Aggregation`, or `Projection` operators on it. |
| [`tidb_opt_prefer_range_scan`](/system-variables.md#tidb_opt_prefer_range_scan-new-in-v50) | Modified | Changes the default value from `OFF` to `ON`. For tables with no statistics (pseudo-statistics) or empty tables (zero statistics), the optimizer prefers interval scans over full table scans. |
| [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) | Modified | Before v8.4.0, its type is boolean, only supports `ON` and `OFF`, and the Region of the newly created table only supports table level scattering after it is enabled. Starting from v8.4.0, the `SESSION` scope is added, the type is changed from boolean to enumeration, the default value is changed from `OFF` to null, and the optional values `TABLE` and `GLOBAL` are added. In addition, it now supports cluster-level scattering policy to avoid the TiKV OOM issues caused by uneven distribution of regions during fast table creation in batches.|
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) | Modified | Changes the default value from `0` to `536870912` (512 MiB), indicating that this feature is enabled by default. The minimum value allowed is set to `67108864` (64 MiB). |
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840)| Newly added | Sets the concurrency within a single automatic statistics collection task. Before v8.4.0, this concurrency is fixed at `1`. To speed up statistics collection tasks, you can increase this concurrency based on your cluster's available resources. |
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)| Newly added | Controls whether to enable the Instance Plan Cache feature. |
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-new-in-v840) | Newly added | Controls whether TiDB uses an optimized version of the Hash Join operator. The default value of `legacy` means that the optimized version is not used. If you set it to `optimized`, TiDB uses the optimized version of the Hash Join operator when executing it to improve Hash Join performance. |
| [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840) | Newly added | Sets the maximum memory usage for Instance Plan Cache. |
| [`tidb_instance_plan_cache_reserved_percentage`](/system-variables.md#tidb_instance_plan_cache_reserved_percentage-new-in-v840) | Newly added | Controls the percentage of idle memory reserved for Instance Plan Cache after memory eviction. |
| [`tidb_pre_split_regions`](/system-variables.md#tidb_pre_split_regions-new-in-v840) | Newly added | Before v8.4.0, setting the default number of row split slices for newly created tables required declaring `PRE_SPLIT_REGIONS` in each `CREATE TABLE` SQL statement, which is complicated once a large number of tables need to be similarly configured. This variable is introduced to solve such problems. You can set this system variable at the `GLOBAL` or `SESSION` level to improve usability. |
| [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-new-in-v840) | Newly added | Before v8.4.0, setting the default number of slices for row IDs for newly created tables required declaring `SHARD_ROW_ID_BITS` in each `CREATE TABLE` or `ALTER TABLE` SQL statement, which is complicated once a large number of tables need to be similarly configured. This variable is introduced to solve such problems. You can set this system variable at the `GLOBAL` or `SESSION` level to improve usability. |
| [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840) | Newly added | Switches the mode in which TiDB sends TSO RPC requests to PD. The mode determines whether TSO RPC requests can be processed in parallel and affects the time spent on batch-waiting for each TS retrieval operation, thereby helping reduce the wait time for retrieving TS during the execution of queries in certain scenarios. |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`grpc-keepalive-time`](/tidb-configuration-file.md#grpc-keepalive-time) | Modified | Adds the minimum value of `1'. |
| TiDB | [`grpc-keepalive-timeout`](/tidb-configuration-file.md#grpc-keepalive-timeout) | Modified | Before v8.4.0, the data type of this parameter is INT, and the minimum value is `1`. Starting from v8.4.0, the data type is changed to FLOAT64, and the minimum value becomes `0.05`. In scenarios where network jitter occurs frequently, you can reduce the impact of network jitter on performance by setting a smaller value to shorten the retry interval. |
| TiKV | [`region-split-keys`](/tikv-configuration-file.md#region-split-keys) | Modified | Changes the default value from `"960000"` to `"2560000"`. |
| TiKV | [`region-split-size`](/tikv-configuration-file.md#region-split-size) | Modified | Changes the default value from `"96MiB"` to `"256MiB"`. |
| TiKV | [`sst-max-size`](/tikv-configuration-file.md#sst-max-size) | Modified | Changes the default value from `"144MiB"` to `"384MiB"`. |
| TiKV | [`pessimistic-txn.in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840) | Newly added | Controls the memory usage limit for in-memory pessimistic locks in a TiKV instance. When this limit is exceeded, TiKV writes pessimistic locks persistently. |
| TiKV | [`pessimistic-txn.in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840) | Newly added | Controls the memory usage limit for in-memory pessimistic locks in a Region. When this limit is exceeded, TiKV writes pessimistic locks persistently. |
| TiKV | [`raft-engine.spill-dir`](/tikv-configuration-file.md#spill-dir-new-in-v840) | Newly added | Controls the secondary directory where TiKV instances store Raft log files for supporting multi-disk storage of Raft log files. |
| TiKV | [`resource-control.priority-ctl-strategy`](/tikv-configuration-file.md#priority-ctl-strategy-new-in-v840) | Newly added | Controls the management policies for low priority tasks. TiKV ensures that higher priority tasks are executed first by adding flow control to low priority tasks. |
| PD | [`cert-allowed-cn`](/enable-tls-between-components.md#verify-component-callers-identity) | Modified | Starting from v8.4.0, configuring multiple `Common Names` is supported. Before v8.4.0, only one `Common Name` can be set. |
| PD | [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys) | Modified | Changes the default value from `200000` to `540000`. 
| PD | [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size) | Modified | Changes the default value from `20` to `54`. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md) | Modified | Changes the default TiFlash storage format version from `5` to `7` to support vector index creation and storage. Due to this format change, TiFlash clusters upgraded to v8.4.0 or a later version do not support in-place downgrading to earlier versions. |
| TiDB Lightning | [`logical-import-prep-stmt`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | In Logical Import Mode, this parameter controls whether to use prepared statements and statement cache to improve performance. The default value is `false`. |
| TiCDC | [`claim-check-raw-value`](/ticdc/ticdc-sink-to-kafka.md#send-the-value-field-to-external-storage-only) | Newly added | Controls whether TiCDC sends only the `value` field of Kafka messages to external storage. This feature is only applicable to non-Open Protocol scenarios. |
| TiDB Binlog | [`--enable-binlog`](/command-line-flags-for-tidb-configuration.md#--enable-binlog) | Deleted | In v8.4.0, [TiDB Binlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) is removed. This parameter controls whether to enable TiDB binlog generation or not, and is deleted starting from v8.4.0. |
| BR | [`--log.crypter.key-file`](/br/br-pitr-manual.md#encrypt-the-log-backup-data) | Newly added | Specifies the the key file for log backup data. You can directly pass in the file path where the key is stored as a parameter without passing in the `crypter.key`. |
| BR | [`--log.crypter.key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data) | Newly added | Specifies the encryption key in hexadecimal string format for log backup data. It is a 128-bit (16 bytes) key for the algorithm `aes128-ctr`, a 24-byte key for the algorithm `aes192-ctr`, and a 32-byte key for the algorithm `aes256-ctr`. |
| BR | [`--log.crypter.method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data) | Newly added | Specifies the encryption algorithm for log backup data, which can be `aes128-ctr`, `aes192-ctr`, or `aes256-ctr`. The default value is `plaintext`, indicating that data is not encrypted. |
| BR | [`--master-key-crypter-method`](/br/br-pitr-manual.md#encrypt-the-log-backup-data) | Newly added | Specifies the encryption algorithm based on the master key for log backup data, which can be `aes128-ctr`, `aes192-ctr`, or `aes256-ctr`. The default value is `plaintext`, indicating that data is not encrypted. |
| BR | [`--master-key`](/br/br-pitr-manual.md#encrypt-the-log-backup-data) | Newly added | Specifies the master key for log backup data. It can be a master key stored on a local disk or a master key managed by a cloud Key Management Service (KMS). |

### System tables

## Offline package changes

Starting from v8.4.0, the following contents are removed from the `TiDB-community-toolkit` [binary package](/binary-package.md):

- `pump-{version}-linux-{arch}.tar.gz`
- `drainer-{version}-linux-{arch}.tar.gz`
- `binlogctl`
- `arbiter`

## Removed features

* The following features are removed starting from v8.4.0:

    * In v8.4.0, [TiDB Binlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) is removed. Starting from v8.3.0, TiDB Binlog is fully deprecated. For incremental data replication, use [TiCDC](/ticdc-overview.md) instead. For point-in-time recovery (PITR), use [PITR](/br-pitr-guide.md). Before you upgrade your TiDB cluster to v8.4.0 or later versions, be sure to switch to TiCDC and PITR. **tw@lilin90** <!--1946-->

* The following features are planned for removal in future versions:

    * Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Deprecated features

* The following features are deprecated starting from v8.4.0:

    * Deprecated feature

* The following features are planned for deprecation in future versions:

    * TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
    * TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
    * It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
    * In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
    * The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.
   * Starting from v6.3.0, partitioned tables use [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) by default. Compared with static pruning mode, dynamic pruning mode supports features such as IndexJoin and plan cache with better performance. Therefore, static pruning mode will be deprecated.
   
## Improvements

+ TiDB <!--tw@Oreoxmt: 11 notes-->

    - Optimize MEMDB implementation to reduce write latency in transactions and TiDB CPU usage [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->
    - Optimize the execution performance of DML statements when the system variable `tidb_dml_type` is set to `"bulk"` [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1860-->
    - Support using [Optimizer Fix Control 47400](/optimizer-fix-controls.md#47400-new-in-v840) to control whether the optimizer limits the minimum value estimated for `estRows` to `1`, which is consistent with databases such as Oracle and DB2 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell) **tw@Oreoxmt** <!--1929-->
    - Add write control to the [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#system-tables-related-to-runaway-queries) log table to reduce overhead caused by a large number of concurrent writes [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp) <!--1908--> **tw@lilin90**
    - Support Index Join by default when the inner table has `Selection`, `Projection`, or `Aggregation` operators on it [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1709-->
    - Reduce the number of column details fetched from TiKV for `DELETE` operations in certain scenarios, lowering the resource overhead of these operations [#38911](https://github.com/pingcap/tidb/issues/38911) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1798-->
    - Support setting the concurrency within a single automatic statistics collection task using the system variable `tidb_auto_analyze_concurrency` [#53460](https://github.com/pingcap/tidb/issues/53460) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1739-->
    - Optimize internal function logic to improve performance when querying tables with numerous columns [#52112](https://github.com/pingcap/tidb/issues/52112) @[Rustin170506](https://github.com/Rustin170506)
    - Simplify filter conditions like `a = 1 AND (a > 1 OR (a = 1 AND b = 2))` to `a = 1 AND b = 2` [#56005](https://github.com/pingcap/tidb/issues/56005) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - Increase the cost of Table Scan in the cost model for scenarios with high risk of suboptimal execution plans, making the optimizer to prefer indexes [#56012](https://github.com/pingcap/tidb/issues/56012) @[terry1purcell](https://github.com/terry1purcell)
    - TiDB supports the two-argument variant `MID(str, pos)` [#52420](https://github.com/pingcap/tidb/issues/52420) @[dveeden](https://github.com/dveeden)
    - Support splitting TTL tasks for tables with non-binary primary keys [#55660](https://github.com/pingcap/tidb/issues/55660) @[lcwangchao](https://github.com/lcwangchao)
    - Optimize performance of system metadata-related statements [#50305](https://github.com/pingcap/tidb/issues/50305) @[ywqzzy](https://github.com/ywqzzy) @[tangenta](https://github.com/tangenta) @[joechenrh](https://github.com/joechenrh) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Implement a new priority queue to improve performance and reduce the cost of rebuilding the auto-analyze operation queue [#55906](https://github.com/pingcap/tidb/issues/55906) @[Rustin170506](https://github.com/Rustin170506)
    - Introduce DDL notifier to allow statistics module to subscribe to DDL events [#55722](https://github.com/pingcap/tidb/issues/55722) @[fzzf678](https://github.com/fzzf678) @[lance6716](https://github.com/lance6716) @[Rustin170506](https://github.com/Rustin170506)
    - Force new TiDB nodes to take over DDL ownership during TiDB upgrades to avoid compatibility issues caused by old TiDB nodes taking ownership [#51285](https://github.com/pingcap/tidb/pull/51285) @[wjhuang2016](https://github.com/wjhuang2016)
    - Support cluster-level Scatter Region [#8424](https://github.com/tikv/pd/issues/8424) @[River2000i](https://github.com/River2000i)

+ TiKV <!--tw@qiancai: 5 notes-->

    - Increase the default value of Region from 96 MiB to 256 MiB to avoid the extra overhead caused by too many Regions [#17309](https://github.com/tikv/tikv/issues/17309) [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1925-->
    - Support setting memory usage limits for in-memory pessimistic locks in a Region or TiKV instance. When hot write scenarios cause a large number of pessimistic locks, you can increase the memory limits via configuration. This helps avoid CPU and I/O overhead caused by pessimistic locks being written to disk. [#17542](https://github.com/tikv/tikv/issues/17542) @[cfzjywxk](https://github.com/cfzjywxk) **tw@Oreoxmt** <!--1967-->
    - Introduce a new `spill-dir` configuration item in Raft Engine, supporting multi-disk storage for Raft logs; when the disk where the home directory (`dir`) is located runs out of space, the Raft Engine automatically writes new logs to `spill-dir`, ensuring continuous operation of the system [#17356](https://github.com/tikv/tikv/issues/17356) [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1970-->
    - (dup): release-6.5.11.md > 改进提升> TiKV - 优化存在大量 DELETE 版本时 RocksDB 的 compaction 触发机制，以加快磁盘空间回收 [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    - Support pushing down vector data types and related functions for calculation [#17290](https://github.com/tikv/tikv/issues/17290) @[breezewish](https://github.com/breezewish)
    - 支持 `date_add`/`date_sub` 函数的计算下推 [#17529](https://github.com/tikv/tikv/issues/17529) @[gengliqi](https://github.com/gengliqi)
    - Support dynamically modifying flow-control configurations for write operations [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - Improve the speed of Region Merge in scenarios with empty tables and small Regions [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    - Prevent [Pipelined DML](https://github.com/pingcap/tidb/blob/master/docs/design/2024-01-09-pipelined-DML.md) from blocking resolved-ts for long periods [#17459](https://github.com/tikv/tikv/issues/17459) @[ekexium](https://github.com/ekexium)

+ PD <!--tw@qiancai: 3 notes-->

    - Support graceful offline of TiKV nodes during data import by TiDB Lightning [#7853](https://github.com/tikv/pd/issues/7853) @[okJiang](https://github.com/okJiang) **tw@qiancai**  <!--1852-->
    - Rename `scatter-range` to `scatter-range-scheduler` in `pd-ctl` commands [#8379](https://github.com/tikv/pd/issues/8379) @[okJiang](https://github.com/okJiang)
    - Add conflict detection for `grant-hot-leader-scheduler` [#4903](https://github.com/tikv/pd/issues/4903) @[lhy1024](https://github.com/lhy1024)
    - The TSO client supports sending and receiving multiple TSO gRPC requests in parallel [#8432](https://github.com/tikv/pd/issues/8432) @[MyonKeminta](https://github.com/MyonKeminta)

+ TiFlash <!--tw@qiancai: 2 notes-->

    - (dup): release-6.5.11.md > 改进提升> TiFlash - 优化 `LENGTH()` 和 `ASCII()` 函数执行效率 [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Reduce the number of threads that TiFlash needs to create when processing disaggregated storage and compute requests, helping avoid crashes of TiFlash compute nodes when processing a large number of such requests [#9334](https://github.com/pingcap/tiflash/issues/9334) @[JinheLin](https://github.com/JinheLin)
    - Enhance the task waiting mechanism in the pipeline execution model [#8869](https://github.com/pingcap/tiflash/issues/8869) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-7.5.4.md > 改进提升> TiFlash - 改进 join 算子的 cancel 机制，使得 join 算子内部能及时响应 cancel 请求 [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - Disable splitting Regions by table to improve restore speed when restoring data to a cluster where the `split-table` and `split-region-on-table` configuration items are `false` (default value) [#53532](https://github.com/pingcap/tidb/issues/53532) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1914-->
        - Disable full data restoration to a non-empty cluster using the `RESTORE` SQL statement by default [#55087](https://github.com/pingcap/tidb/issues/55087) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1711-->

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## Bug fixes


+ TiDB <!--tw@lilin90: the following 13 notes-->

    - 修复当 `tidb_restricted_read_only` 变量设置为 `true` 时可能死锁的问题 [#53822](https://github.com/pingcap/tidb/issues/53822) [#55373](https://github.com/pingcap/tidb/issues/55373) @[Defined2014](https://github.com/Defined2014)
    - 修复 TiDB 优雅关闭时不等待 auto commit 事务完成的问题 [#55464](https://github.com/pingcap/tidb/issues/55464) @[YangKeao](https://github.com/YangKeao)
    - 修复在 TTL 任务执行过程中，减小 `tidb_ttl_delete_worker_count` 的值导致任务无法完成的问题 [#55561](https://github.com/pingcap/tidb/issues/55561) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当一张表的索引中包含生成列时，`ANALYZE` 这张表可能报错 `Unknown column 'column_name' in 'expression'` 的问题 [#55438](https://github.com/pingcap/tidb/issues/55438) @[hawkingrei](https://github.com/hawkingrei)
    - 废弃统计信息相关的无用配置，减少冗余代码 [#55043](https://github.com/pingcap/tidb/issues/55043) @[Rustin170506](https://github.com/Rustin170506)
    - 修复执行一条包含关联子查询和 CTE 的查询时，TiDB 可能卡住或返回错误结果的问题 [#55551](https://github.com/pingcap/tidb/issues/55551) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复禁用 `lite-init-stats` 可能导致统计信息同步加载失败的问题 [#54532](https://github.com/pingcap/tidb/issues/54532) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当 `UPDATE` 或 `DELETE` 语句包含递归的 CTE 时，语句可能报错或不生效的问题 [#55666](https://github.com/pingcap/tidb/issues/55666) @[time-and-fate](https://github.com/time-and-fate)
    - 修复当一条 SQL 绑定涉及窗口函数时，有一定概率不生效的问题 [#55981](https://github.com/pingcap/tidb/issues/55981) @[winoros](https://github.com/winoros)
    - 修复统计信息初始化时，使用非二进制排序规则的字符串类型列的统计信息可能无法正常加载的问题 [#55684](https://github.com/pingcap/tidb/issues/55684) @[winoros](https://github.com/winoros)
    - 修复当查询条件为 `column IS NULL` 访问唯一索引时，优化器将行数错误地估算为 1 的问题 [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当查询包含形如 `(... AND ...) OR (... AND ...) ...` 的过滤条件时，优化器没有使用最优的多列统计信息进行行数估算的问题 [#54323](https://github.com/pingcap/tidb/issues/54323) @[time-and-fate](https://github.com/time-and-fate)
    - 修复当一个查询有索引合并 (Index Merge) 执行计划可用时，`read_from_storage` hint 可能不生效的问题 [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    <!--tw@hfxsd: the following 13 notes-->
    - (dup): release-6.5.11.md > 错误修复> TiDB - 修复 `IndexNestedLoopHashJoin` 中存在数据竞争的问题 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - (dup): release-6.5.11.md > 错误修复> TiDB - 修复 `INFORMATION_SCHEMA.STATISTICS` 表中 `SUB_PART` 值为空的问题 [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-6.5.11.md > 错误修复> TiDB - 修复 DML 语句中包含嵌套的生成列时报错的问题 [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the INTEGER data type with minimum display width in the division operation might cause the division result to overflow [#55837](https://github.com/pingcap/tidb/issues/55837) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the operator that follows the TopN operator can not trigger the fallback action when the memory limit is exceeded [#56185](https://github.com/pingcap/tidb/issues/56185) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that the `ORDER BY` column in the Sort operator is stuck if it contains a constant [#55344](https://github.com/pingcap/tidb/issues/55344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that when adding an index, the `8223 (HY000)` error occurs after killing the PD leader and the data in the table is inconsistent [#55488](https://github.com/pingcap/tidb/issues/55488) @[tangenta](https://github.com/tangenta)
    - Fix the issue that too many DDL history tasks cause OOM when you request information about history DDL tasks [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)
    - Fix the issue that executing `IMPORT INTO` is stuck when Global Sort is enabled and the Region size exceeds 96 MiB [#55374](https://github.com/pingcap/tidb/issues/55374) @[lance6716](https://github.com/lance6716)
    - Fix the issue that executing `IMPORT INTO` on a temporary table causes TiDB to crash [#55970](https://github.com/pingcap/tidb/issues/55970) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that adding a unique index causes the `duplicate entry` error [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB Lightning does not ingest all KV pairs when TiKV is down for more than 810 seconds, resulting in inconsistent data in the table [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the `CREATE TABLE LIKE` statement can not be used for cached tables [#56134](https://github.com/pingcap/tidb/issues/56134) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the confusing warning message for `FORMAT()` expressions in CTE [#56198](https://github.com/pingcap/tidb/pull/56198) @[dveeden](https://github.com/dveeden)
    - Fix the issue that column type restrictions are inconsistent between `CREATE TABLE` and `ALTER TABLE` when creating a partitioned table [#56094](https://github.com/pingcap/tidb/issues/56094) @[mjonss](https://github.com/mjonss)
    - Fix the incorrect time type in `INFORMATION_SCHEMA.RUNAWAY_WATCHES` table [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.11.md > 错误修复> TiKV - 修复当主密钥存储于 KMS (Key Management Service) 时无法轮换主密钥的问题 [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-6.5.11.md > 错误修复> TiKV - 修复删除大表或分区后可能导致的流量控制问题 [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.11.md > 错误修复> TiKV - 修复过期副本处理 Raft 快照时，由于分裂操作过慢并且随后立即删除新副本，可能导致 TiKV panic 的问题 [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)

+ PD

+ TiFlash <!--tw@qiancai: 2 notes-->

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.4.md > 错误修复 > TiFlash - 修复当表里含 Bit 类型列并且带有表示非法字符的默认值时 TiFlash 无法解析表 schema 的问题 [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash might panic due to spurious Region overlap check failures that occur when multiple Regions are concurrently applying snapshots [#9329](https://github.com/pingcap/tiflash/issues/9329) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that some JSON functions unsupported by TiFlash are pushed down to TiFlash [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt: 1 note-->

        - Fix the issue that the PITR checkpoint interval in monitoring abnormally increased when TiDB nodes stopped, which does not reflect the actual situation [#42419](https://github.com/pingcap/tidb/issues/42419) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.11.md > 错误修复> Tools> Backup & Restore (BR) - 修复备份过程中由于 TiKV 没有响应导致备份任务无法结束的问题 [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.11.md > 错误修复> Tools> Backup & Restore (BR) - 修复开启日志备份时，BR 日志可能打印权限凭证敏感信息的问题 [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-6.5.11.md > 错误修复> Tools> Backup & Restore (BR) - 修复当 PITR 日志备份任务失败时，用户停止了该任务后，PD 中与该任务相关的 safepoint 未被正确清除的问题 [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - (dup): release-7.5.4.md > 错误修复 > TiDB Data Migration (DM) - 修复多个 dm-master 同时成为 Leader 的问题 [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
        - (dup): release-6.5.11.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在处理 `ALTER DATABASE` 语句时未设置默认数据库导致同步报错的问题 [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning <!--tw@Oreoxmt: 1 note-->

        - Fix the issue that TiDB Lightning reports a `verify allocator base failed` error when using parallel import mode with identical task IDs [#55384](https://github.com/pingcap/tidb/issues/55384) @[ei-sugimoto](https://github.com/ei-sugimoto)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Contributors

We would like to thank the following contributors from the TiDB community: