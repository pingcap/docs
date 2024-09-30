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
    <td><a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_tso_client_rpc_mode-new-in-v840">Concurrent TSO retrieval for TiDB</a>**tw@qiancai 1893**</td>
    <td>In high-concurrency scenarios, you can use this feature to reduce the wait time for obtaining TSO and improve the cluster throughput.</td>
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
    <td><a href="https://docs.pingcap.com/tidb/v8.4/system-variables#tidb_auto_analyze_concurrency-new-in-v840">Adaptive concurrency for statistics collection</a>**tw@Oreoxmt 1739**</td>
    <td>Automatic statistics collection determines the collection concurrency based on node scale and hardware specifications. This improves statistics collection efficiency, reduces manual tuning, and ensures stable cluster performance.</td>
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

* Add RPC mode for obtaining TSO, reducing TSO retrieval latency [#54960](https://github.com/pingcap/tidb/issues/54960) @[MyonKeminta](https://github.com/MyonKeminta) **tw@qiancai** <!--1893-->

    When TiDB requests TSO from PD, it consolidates multiple requests over a period of time and processes them in synchronous batches to decrease the number of RPC (Remote Procedure Call) requests and reduce PD workload. However, the performance of this synchronous batching mode is not ideal in latency-sensitive scenarios.

    In v8.4.0, TiDB introduces an asynchronous batching mode for TSO requests,  which provides various levels of concurrency. This asynchronous mode can reduce the latency for obtaining a TSO but might increase PD workload. To set the RPC mode for obtaining TSO, you can configure the [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-new-in-v840) system variable.

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

    Starting from v8.4.0, TiDB supports [vector data types](vector-search-data-types.md) and [vector search indexes](vector-search-index.md), offering powerful vector search capabilities. TiDB vector data types support up to 16,383 dimensions and support various [distance functions](/vector-search-functions-and-operators.md#vector-functions), including L2 distance (Euclidean distance), cosine distance, negative inner product, and L1 distance (Manhattan distance).

    To start vector search, you only need to create a table with vector data types, insert vector data, and then perform a query of vector data. You can also perform mixed queries of vector data and traditional relational data.

    To enhance the performance of vector search, you can create and use [vector search indexes](vector-search-index.md). Note that TiDB vector search indexes rely on TiFlash. Before using vector search indexes, make sure that TiFlash nodes are deployed in your TiDB cluster.

    For more information, see [documentation](/vector-search-overview.md).

* Support the `gb18030` character set and the `gb18030_bin` and `gb18030_chinese_ci` collations [#17470](https://github.com/tikv/tikv/issues/17470) [#55791](https://github.com/pingcap/tidb/issues/55791) @[cbcwestwolf](https://github.com/cbcwestwolf) **tw@lilin90** <!--1962-->

    Starting from v8.4.0, TiDB supports the `gb18030` character set to ensure that TiDB can better handle Chinese-related data storage and query requirements. This character set is a standard widely used for Chinese character encoding.

    Starting from v8.4.0, TiDB supports the `gb18030_bin` and `gb18030_chinese_ci` collations. `gb18030_bin` provides precise binary sorting, while `gb18030_chinese_ci` supports case-insensitive general sorting. These two collations make sorting and comparison of `gb18030` encoded text more flexible and efficient.

    By supporting the `gb18030` character set and its collations, TiDB v8.4.0 enhances compatibility with Chinese scenarios. In scenarios involving multiple languages and character encodings, you can select and operate on character sets with better user experience.

    For more information, see [documentation](/character-set-gb18030.md).

### DB operations

* BR supports client-side encryption of log backup data (experimental) [55834](https://github.com/pingcap/tidb/issues/55834) @[Tristan1900](https://github.com/Tristan1900) **tw@qiancai** <!--1920-->

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
| tidb_enable_table_partition | Deprecated | Always set to `ON`. Table partitioning has been GA since v5.1 and this experimental flag, if set to `OFF`, would cause create table with partitioning, just parse and ignore the partitioning clause. |
| tidb_enable_list_partition | Deprecated | Always set to ON. List partitioning has been GA since v6.1 |
| tidb_enable_global_index | Deprecated | Always set to `ON`. Global Index for partitioned tables is GA since v8.4.0, and needs explicit `GLOBAL` IndexOption to be used, so this system variable is no longer needed. |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### System tables

## Offline package changes

## Deprecated features

* The following features are removed starting from v8.4.0:

    * In v8.4.0, [TiDB Binlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) is removed. Starting from v8.3.0, TiDB Binlog is fully deprecated. For incremental data replication, use [TiCDC](/ticdc-overview.md) instead. For point-in-time recovery (PITR), use [PITR](/br-pitr-guide.md). Before you upgrade your TiDB cluster to v8.4.0 or later versions, be sure to switch to TiCDC and PITR. **tw@lilin90** <!--1946-->

* The following features are deprecated starting from v8.4.0:

    * Deprecated feature

* The following features are planned for deprecation in future versions:

    * TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
    * TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
    * It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
    * In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
    * The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.

* The following features are planned for removal in future versions:

    * Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Improvements

+ TiDB

    - Optimize MEMDB implementation to reduce write latency in transactions and TiDB CPU usage [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->
    - Optimize the execution performance of DML statements when the system variable `tidb_dml_type` is set to `"bulk"` [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1860-->
    - Support using [Optimizer Fix Control 47400](/optimizer-fix-controls.md#47400-new-in-v840) to control whether the optimizer limits the minimum value estimated for `estRows` to `1`, which is consistent with databases such as Oracle and DB2 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell) **tw@Oreoxmt** <!--1929-->
    - Add write control to the [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#system-tables-related-to-runaway-queries) log table to reduce overhead caused by a large number of concurrent writes [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp) <!--1908--> **tw@lilin90**
    - Support Index Join by default when the inner table has `Selection`, `Projection`, or `Aggregation` operators on it [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1709-->
    - Reduce the number of column details fetched from TiKV for `DELETE` operations in certain scenarios, lowering the resource overhead of these operations [#38911](https://github.com/pingcap/tidb/issues/38911) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1798-->
    - Improve automatic statistics collection by determining the collection concurrency based on node scale and hardware specifications [#53460](https://github.com/pingcap/tidb/issues/53460) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1739-->

+ TiKV

    - Increase the default value of Region from 96 MiB to 256 MiB to avoid the extra overhead caused by too many Regions [#17309](https://github.com/tikv/tikv/issues/17309) [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1925-->
    - Support setting memory usage limits for in-memory pessimistic locks in a Region or TiKV instance. When hot write scenarios cause a large number of pessimistic locks, you can increase the memory limits via configuration. This helps avoid CPU and I/O overhead caused by pessimistic locks being written to disk. [#17542](https://github.com/tikv/tikv/issues/17542) @[cfzjywxk](https://github.com/cfzjywxk) **tw@Oreoxmt** <!--1967-->
    - Introduce a new `spill-dir` configuration item in Raft Engine, supporting multi-disk storage for Raft logs; when the disk where the home directory (`dir`) is located runs out of space, the Raft Engine automatically writes new logs to `spill-dir`, ensuring continuous operation of the system [#17356](https://github.com/tikv/tikv/issues/17356) [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1970-->

+ PD

    - Support graceful offline of TiKV nodes during data import by TiDB Lightning [#7853](https://github.com/tikv/pd/issues/7853) @[okJiang](https://github.com/okJiang) **tw@qiancai**  <!--1852-->
+ TiFlash

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

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## Contributors

We would like to thank the following contributors from the TiDB community:
