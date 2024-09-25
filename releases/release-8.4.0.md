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
    <td rowspan="5">Scalability and Performance</td>
    <td> 执行计划缓存在实例内共享（实验特性）<!-- tw@Oreoxmt 1569 --></td>
    <td> 实例级执行计划缓存支持在内存中缓存更多的执行计划，消除 SQL 编译时所消耗的时间，从而减少 SQL 的运行时间，提升 OLTP 系统的性能和吞吐。同时，也能更好的控制内存占用，提升数据库稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.4/partitioned-table#global-indexes">Global indexes for partitioned tables (GA)</a><!-- tw@hfxsd 1961 --></td>
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned columns, and remove the restriction that a unique key must contain the partition key. This feature extends the usage scenarios of TiDB partitioned tables and avoids some of the application modification work that might be required for data migration.</td>
  </tr>
  <tr>
    <td> TiDB 并行获取 TSO<!-- tw@qiancai 1893 --></td>
    <td>在高并发场景下，并行获取 TSO 能够有效降低等待获取 TSO 的时间，提升集群的吞吐。</td>
  </tr>
  <tr>
    <td> Improve the execution efficiency of administrative SQL statements<!-- tw@hfxsd 1941 --></td>
    <td>In some SaaS systems, there is a need to create users in batch and rotate passwords regularly. TiDB enhances the performance of creating and modifying database users, ensuring these operations can be completed within the desired time window.</td>
  </tr>
  <tr>
    <td> Improve query performance for cached tables<!-- tw@hfxsd 1965 --></td>
    <td>Improve query performance for index scanning on cached tables, with improvements of up to 5.4 times in some scenarios. For high-speed queries on small tables, cached tables can significantly enhance overall performance.</td>
  </tr>
  <tr>
    <td rowspan="4">Reliability and Availability</td>
    <td> Support more triggers for runaway queries, and support switching resource groups<!-- tw@hfxsd 1832 --><!-- tw@lilin90 1800 --></td>
    <td>Runaway Queries offer an effective way to mitigate the impact of unexpected SQL performance issues on systems. TiDB v8.4.0 introduces the number of keys processed by the Coprocessor (<CODE>PROCESSED_KEYS</CODE>) and request units (<CODE>RU</CODE>) as identifying conditions, and puts identified queries into the specified resource group for more precise identification and control of runaway queries.</td>
  </tr>
  <tr>
    <td> Support setting resource usage caps for background tasks for resource control <!-- tw@hfxsd 1909 --></td>
    <td>By setting a percentage cap on background tasks of resource control, you can manage their resource consumption based on the needs of different business systems. This ensures background tasks consume minimal resources, maintaining the service quality of online operations.</td>
  </tr>
  <tr>
    <td> TiProxy 流量捕捉和回放<!-- tw@Oreoxmt 1942 --></td>
    <td>在做集群升级、迁移、部署变化等重要变更之前，通过捕捉真实负载来验证目标集群的性能，确保变更的成功。</td>
  </tr>
  <tr>
    <td> 统计信息收集自适应并发度<!-- tw@Oreoxmt 1739 --></td>
    <td>自动统计信息收集会根据节点规模和硬件规格自动决定采集并发度，提升统计信息收集效率，减少手工调优，保证集群性能稳定。</td>
  </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td>Foreign keys (GA)<!-- tw@lilin90 1894 --></td>
    <td>Support MySQL-compatible foreign key constraints to maintain data consistency and further enhance TiDB's compatibility with MySQL.</td>
  </tr>
  <tr>
    <td> 向量搜索功能（实验特性）<!-- tw@qiancai 1898 --></td>
    <td>加速向量搜索的性能，适用于检索增强生成（RAG）、语义搜索、推荐系统等应用类型。把 TiDB 应用场景扩展到 AI 和 大语言模型（LLM）领域。</td>
  </tr>
  <tr>
    <td rowspan="2">DB Operations and Observability</td>
    <td> Display TiKV and TiDB CPU times in memory tables<!-- tw@hfxsd 1877 --></td>
    <td>CPU times are now integrated into a system table and displayed alongside other session or SQL metrics, allowing for easier observation of operations with high CPU consumption from multiple perspectives, improving diagnostic efficiency. This is particularly useful for diagnosing instances with CPU spikes or read/write hotspots in the cluster.</td>
  </tr>
  <tr>
    <td> Support backing up TiKV instances with IMDSv2 service enabled<!-- tw@hfxsd 1945 --></td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">AWS EC2 now uses IMDSv2 as the default metadata service</a>. TiDB supports data backups from TiKV instances with IMDSv2 enabled, enhancing your ability to run TiDB clusters in public cloud environments.</td>
  </tr>
  <tr>
    <td rowspan="1">安全</td>
    <td> 备份数据加密成为正式功能<!-- tw@qiancai 1920 --></td>
    <td> 加密数据库备份是一种增强数据安全性的重要措施，既可以保护数据备份中敏感信息，又有助于合规，确保数据在存储和传输中的安全。</td>
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

* The performance of batch user creation and password changes has been improved by hundreds of times [#55604](https://github.com/pingcap/tidb/pull/55604) @[wjhuang2016](https://github.com/wjhuang2016) **tw@hfxsd** <!--1941-->

    In SaaS scenarios, you might need to batch-create a large number of users, rotate passwords periodically, and complete these tasks within a specific time window. Starting from v8.4.0, the performance of batch user creation and password rotation has been significantly improved. Additionally, you can further enhance performance by increasing concurrency through a higher number of session connections, which greatly reduces execution time for these operations.

* Instance-level execution plan cache (experimental) [#54057](https://github.com/pingcap/tidb/issues/54057) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1569-->

    TiDB v8.4.0 introduces instance-level execution plan cache as an experimental feature. This feature allows all sessions within the same TiDB instance to share the execution plan cache, significantly reducing TiDB latency, improving cluster throughput, decreasing the likelihood of execution plan fluctuations, and maintaining stable cluster performance. Compared with session-level execution plan cache, instance-level execution plan cache offers the following advantages:

    - Eliminates redundancy, caching more execution plans with the same memory consumption.
    - Allocates a fixed-size memory on the instance, limiting memory usage more effectively.

    In v8.4.0, instance-level execution plan cache only supports caching query execution plans and is disabled by default. You can enable this feature using [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840) and set its maximum memory usage using [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840). Before enabling this feature, disable [Prepared execution plan cache](/sql-prepared-plan-cache.md) and [Non-prepared execution plan cache](/sql-non-prepared-plan-cache.md).

    For more information, see [documentation](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840).

* TiDB Lightning 的逻辑导入支持 prepare 接口 [#54850](https://github.com/pingcap/tidb/issues/54850) @[dbsid](https://github.com/dbsid) @[qw4990](https://github.com/qw4990) **tw@lilin90** <!--1922-->

    通过开启配置项 `logical-import-prep-stmt`，TiDB Lightning 逻辑导入产生的 SQL 语句将通过 prepare 接口执行，可提升 SQL 执行效率，并有更大机会命中执行计划缓存，提升逻辑导入的速度。

    更多信息，请参考[用户文档](tidb-lightning/tidb-lightning-configuration.md)。

* Partitioned tables support global indexes (GA) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) @[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust) @[L-maple](https://github.com/L-maple) **tw@hfxsd** <!--1961-->

    In previous versions of partitioned tables, some limitations exist because global indexes are not supported. For example, the unique key must use every column in the table's partitioning expression. If the query condition does not use the partitioning key, the query will scan all partitions, resulting in poor performance. Starting from v7.6.0, the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) is introduced to enable the global index feature. But this feature was under development at that time and it is not recommended to enable it.

    Starting with v8.3.0, the global index feature is released as an experimental feature. You can explicitly create a global index for a partitioned table with the keyword `Global` to remove the restriction that the unique key must use every column in the table's partitioning expression, to meet flexible business needs. Global indexes also enhance the performance of queries that do not include partition keys.

    In v8.4.0, this feature becomes generally available (GA). You must use the keyword `GLOBAL` to create a global index, instead of setting the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) to enable the global index feature. From v8.4.0 this system variable is deprecated and is always `ON`.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

* Optimize query performance for cached tables in some scenarios [#43249](https://github.com/pingcap/tidb/issues/43249) @[tiancaiamao](https://github.com/tiancaiamao) **tw@hfxsd** <!--1965-->

    Optimize the query performance of cached tables by up to 5.4 times when using `IndexLookup` to execute `SELECT ... LIMIT 1` with `IndexLookup`. Improve the performance of `IndexLookupReader` in full table scan and primary key query scenarios.

### Reliability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

* 超出预期的查询 (Runaway Queries) 新增处理行数 和 RU 作为阈值 [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp) **tw@lilin90** <!--1800-->

    从 v8.4.0 开始， TiDB 可以依据处理行数 (`PROCESSED_KEYS`) 和 Request Unit (`RU`) 定义超出预期的查询。和执行时间 (`EXEC_ELAPSED`) 相比，新增阈值能够更准确地定义查询的资源消耗，避免整体性能下降时发生识别偏差。

    支持同时设置多个条件，满足任意条件即识别为 `Runaway Queries`。

    可以观测 [Statement Summary Tables](/statement-summary-tables.md) 中的几个对应字段 (`RESOURCE_GROUP`、`MAX_REQUEST_UNIT_WRITE`、`MAX_REQUEST_UNIT_READ`、`MAX_PROCESSED_KEYS`)，根据历史执行情况决定条件值的大小。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* Support runaway queries to switch resource groups [#54434](https://github.com/pingcap/tidb/issues/54434) @[JmPotato](https://github.com/JmPotato) **tw@hfxsd** <!--1832-->

    In TiDB v8.4.0, you can redirect runaway queries to a specific resource group. If the `COOLDOWN` mechanism fails to lower resource consumption, you can create a [resource group](/tidb-resource-control.md#create-a-resource-group) and set the `SWITCH_GROUP` parameter to move identified runaway queries to this group. Meanwhile, subsequent queries within the same session will continue to execute in the original resource group. By switching resource groups, you can more precisely manage resource usage and better control the impact of runaway queries.

    For more information, see [documentation](/tidb-resource-control.md#query_limit-parameters).

* The system variable `tidb_scatter_region` supports the cluster-level Region scattering strategy [#55184](https://github.com/pingcap/tidb/issues/55184) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1927-->
	
    In previous versions, the system variable `tidb_scatter_region` can only be enabled or disabled. When enabled, it applies a table-level scattering strategy during batch table creation. However, when creating hundreds of thousands of tables in a batch, this approach results in a concentration of regions on a few TiKV nodes, causing out-of-memory (OOM) issues on those nodes.

    To address this, starting from v8.4.0, `tidb_scatter_region` is changed to a string type. It now supports a cluster-level scattering strategy, helping scatter regions more evenly and preventing OOM problems on TiKV nodes.
	
    For more information, see [documentation](/system-variables.md#tidb_scatter_region).

* Support setting resource caps for background tasks of resource control [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv) **tw@hfxsd** <!--1909-->
	
    TiDB resource control can identify and lower the priority of background tasks. In certain scenarios, you might want to limit the resource consumption of these tasks, even when resources are available. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set a maximum percentage of resources that a background task can consume. Each node will ensure that the resource usage of all background tasks stays within this limit. This feature enables precise control over resource consumption for background tasks, enhancing cluster stability.

    For more information, see [documentation](/tidb-resource-control.md#manage-background-tasks).

* 优化资源组资源分配策略 [#50831](https://github.com/pingcap/tidb/issues/50831) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1833-->

    TiDB 在 v8.4.0 部分调整了资源分配策略，更好地满足用户对资源管控的预期。

    - 控制大查询在运行时的资源分配，避免超出资源组限额。配合 Runaway Queries 的 `COOLDOWN` 动作，识别并降低大查询并发度，降低瞬时资源消耗。
    - 调整默认的优先级调度策略。当不同优先级的任务同时运行时，高优先级的任务获得更多资源。

### Availability

* TiProxy supports traffic replay (experimental) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1942-->

    Starting from TiProxy v1.3.0, you can use TiProxy to capture access traffic in a TiDB production cluster and replay it in a test cluster at a specified rate. This feature enables you to reproduce actual workloads from the production cluster in a test environment, verifying SQL statement execution results and performance.

    Traffic replay is suitable for the following scenarios:

    - Validate TiDB version upgrades
    - Assess change impact
    - Validate performance before TiDB scaling
    - Test performance limits

    You can use `tiproxyctrl` to connect to the TiProxy instance and perform traffic capture and replay.

    For more information, see [documentation](/tiproxy/tiproxy-traffic-replay.md).

### SQL

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

* TiDB 外键约束检查功能成为正式功能 (GA) [#55861](https://github.com/pingcap/tidb/issues/55861) @[YangKeao](https://github.com/YangKeao) **tw@lilin90** <!--1894-->

    从 v6.6.0 开始，TiDB 支持通过系统变量 [`foreign_key_checks`](/system-variables.md#foreign_key_checks) 做外键约束检查，但一直为实验特性。v8.4.0 对外键特性在更多场景做了覆盖测试，提升了稳定性和性能，因此从 v8.4.0 开始，外键功能成为正式功能 (GA)。

    更多信息，请参考[用户文档](/foreign-key.md)。

* 支持字符集 `gb18030` 和排序规则 `gb18030_bin` 和 `gb18030_chinese_ci` [#17470](https://github.com/tikv/tikv/issues/17470) [#55791](https://github.com/pingcap/tidb/issues/55791) @[cbcwestwolf](https://github.com/cbcwestwolf) **tw@lilin90** <!--1962-->

    从 v8.4.0 开始，TiDB 支持 `gb18030` 字符集，以确保 TiDB 能够更好地处理中文相关的数据存储和查询需求。该字符集是一个广泛用于中文字符编码的标准。

    从 v8.4.0 开始，TiDB 支持 `gb18030_bin` 和 `gb18030_chinese_ci` 排序规则。`gb18030_bin` 提供了基于二进制的精准排序，而 `gb18030_chinese_ci` 则支持大小写不敏感的通用排序规则。这两种排序规则使得对 `gb18030` 编码文本的排序和比较更加灵活高效。

    通过支持 `gb18030` 字符集及其排序规则，TiDB v8.4.0 增强了与中文应用场景的兼容性，特别是在涉及多种语言和字符编码的场景下，可以更方便地进行字符集的选择和操作，提升了数据库的使用体验。

    更多信息，请参考[用户文档](/character-set-gb18030.md)。

### DB operations

* PITR adds client-side log backup data encryption support (experimental) [55834](https://github.com/pingcap/tidb/issues/55834) @[Tristan1900](https://github.com/Tristan1900) **tw@qiancai** <!--1920-->

    Previously only the data from a snapshot based backup could be encrypted (on the client side) with a data key provided by the user. With this feature, log backups may now also be encrypted, ensuring that the confidentiality of information within the backup data is secured.

    For more information, see [documentation](doc-link).

* BR reduces requires storage permissions for restores [#55870](https://github.com/pingcap/tidb/issues/55870) @[Leavrth](https://github.com/Leavrth) **tw@Oreoxmt** <!--1943-->

    Previously, when BR was restoring data, checkpoint information about the progress of the restore was recorded in the location hosting the backup data. These restore checkpoints enabled restoration to be quickly resumed if it was interrupted. With this feature, the restore checkpoints are now stored in the target TiDB cluster. This means that BR only requires read access to the backup dataset location for restores.

    For more information, see [documentation](doc-link).
  
* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Observability

* Display the CPU time of TiDB and TiKV in the system table [#55542](https://github.com/pingcap/tidb/issues/55542) @[yibin87](https://github.com/yibin87) **tw@hfxsd** <!--1877-->

      The [Top SQL page](/dashboard/top-sql.md) of [TiDB Dashboard](/dashboard/dashboard-intro.md) displays SQL statements with high CPU consumption. Starting from v8.4.0, TiDB includes CPU time consumption data in the system table, alongside other session or SQL metrics, allowing you to easily monitor high CPU usage from multiple perspectives. This information is especially useful in identifying the root cause of issues such as CPU spikes or hotspots in cluster read/write operations.

    - [STATEMENTS_SUMMARY](/statement-summary-tables.md) adds `AVG_TIDB_CPU_TIME` and `AVG_TIKV_CPU_TIME` to show the average CPU time consumed by individual SQL statements historically.
    - [INFORMATION_SCHEMA.PROCESSLIST](/information-schema/information-schema-processlist.md) adds `TIDB_CPU` and `TIKV_CPU` to display the cumulative CPU consumption of currently executing SQL statements in a session.
    - The [slow Log](/analyze-slow-queries.md) adds the `Tidb_cpu_time` and `Tikv_cpu_time` fields to show the CPU time of captured SQL statements.

  By default, TiKV CPU time is displayed. Collecting TiDB CPU time introduces an additional overhead (about 8%), so TiDB CPU time is only displayed as the actual value when the [Top SQL feature](https://github.com/dashboard/top-sql.md) is enabled; otherwise, it will always display as `0`.

    For more information, see [documentation](/information-schema/information-schema-processlist.md) and [documentation](information-schema/information-schema-slow-query.md).

* TOP SQL 支持按表或数据库维度查看聚合结果 [#55540](https://github.com/pingcap/tidb/issues/55540) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1878-->

    在 v8.4.0 之前，[TOP SQL](/dashboard/top-sql.md) 以 SQL 为单位来聚合 CPU 时间。如果 CPU 时间不是由少数几个 SQL 贡献，按 SQL 聚合并不能有效发现问题。从 v8.4.0 开始，你可以选择 **By TABLE** 或者 **By DB** 聚合 CPU 时间。在多系统融合的场景下，新的聚合方式能够更有效地识别来自某个特定系统的负载变化，提升问题诊断的效率。

    更多信息，请参考[用户文档](/dashboard/top-sql.md)。

### Security

* BR supports AWS IMDSv2 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu) **tw@hfxsd** <!--1945-->

    BR now supports AWS Instance Metadata Service Version 2 (IMDSv2) when deployed on AWS EC2. This allows you to configure the newer session-oriented method on EC2 instances, enabling BR to successfully use the instance's associated IAM role to access AWS S3 with the appropriate privileges.

    For more information, see [documentation](/backup-and-restore-storages#authentication).

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Data migration

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

* TiCDC claim check nows supports raw value format [#11396](https://github.com/pingcap/tiflow/issues/11396) @[3AceShowHand](https://github.com/3AceShowHand) **tw@Oreoxmt** <!--1919-->

    When TiCDC used the claim check capability to handle large messages it included both the Key and the Value are encoded and stored in the external storage system. With the new raw value option, TiCDC can now be configured to store the value format only in the external storage system, using the protocol encoding.

    For more information, see [documentation](ticdc-sink-to-kafka.md#send-large-messages-to-external-storage).

* TiCDC introduces new row checksum to verify old values after Add and Drop Column operations [#10969](https://github.com/pingcap/tiflow/issues/10969) @[3AceShowHand](https://github.com/3AceShowHand) **tw@Oreoxmt** <!--1917-->

    Starting from v8.4.0, TiDB and TiCDC introduce Checksum V2 to address issues with Checksum V1 in verifying old values in Update or Delete events after Add Column or Drop Column operations. For new clusters created in v8.4.0 or later, or clusters upgraded to v8.4.0, TiDB uses Checksum V2 by default when single-row data checksum verification is enabled. TiCDC supports handling both Checksum V1 and V2. This change only affects TiDB and TiCDC internal implementation and does not impact checksum calculation methods for downstream Kafka consumers.
  
    For more information, see [documentation](/ticdc-integrity-check.md).

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

    * TiDB Binlog replication is now removed from this version. Starting from v8.3.0, TiDB Binlog was fully deprecated. For incremental data replication, use [TiCDC](/ticdc-overview.md) instead. For point-in-time recovery (PITR), use [PITR](/br-pitr-guide.md). **tw@lilin90** <!--1946-->

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
  - 为日志表 [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#runaway-queries-相关系统表) 增加写入控制，降低大量并发写入引发的开销 [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp) <!--1908--> **tw@lilin90**

+ TiKV

  - Increase the default value of Region from 96 MiB to 256 MiB to avoid the extra overhead caused by too many Regions [#17309](https://github.com/tikv/tikv/issues/17309) [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1925-->
  - Introduce a new `spill-dir` configuration in Raft Engine to support multi-disk storage for Raft logs. When the disk containing the home directory (`dir`) runs out of space, Raft Engine automatically writes new logs to `spill-dir`, ensuring continuous operation. [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1970-->

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
