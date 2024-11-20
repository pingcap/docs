---
title: TiDB 8.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.5.0.
---

# TiDB 8.5.0 Release Notes

<EmailSubscriptionWrapper />

Release date: xx xx, 2024

TiDB version: 8.5.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

TiDB 8.5.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 8.1.0, 8.5.0 includes new features, improvements, and bug fixes released in [8.2.0-DMR](/releases/release-8.2.0.md), [8.3.0-DMR](/releases/release-8.3.0.md), and [8.4.0-DMR](/releases/release-8.4.0.md). When you upgrade from 8.1.x to 8.5.0, you can download the [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v8.1-to-v8.5-en-release-notes.pdf) to view all release notes between the two LTS versions. The following table lists some highlights from 8.1.0 to 8.5.0:

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="6">可扩展性与性能</td>
    <td> 多维度降低数据处理延迟 **tw@qiancai**</td>
    <td>通过不断挖掘数据处理的细节，TiDB 持续提升自身性能，力求满足金融场景对 SQL 处理时延的要求。 包括以下关键更新：
    <li> 并行排序 (v8.2.0 引入) </li>
    <li> 优化 KV 请求批处理策略 (v8.3.0 引入) </li>
    <li> 并行获取 TSO (v8.4.0 引入) </li>
    <li> 删除语句只获取必要的列 (v8.4.0 引入) </li>
    <li> 优化缓存表场景性能 (v8.4.0 引入) </li>
    <li> Hash Join 算法演进 (v8.4.0 引入) </li>
    </td>
  </tr>
  <tr>
    <td>Active PD Follower 成为正式功能  **tw@Oreoxmt 2015**</td>
    <td>TiDB v7.6.0 引入了 Active PD Follower 特性，允许 PD follower 提供 Region 信息查询服务。在 TiDB 节点数量较多和 Region 数量较多的集群中，该特性可以提升 PD 集群处理 <code>GetRegion</code>、<code>ScanRegions</code> 请求的能力，减轻 PD leader 的 CPU 压力。在 v8.5.0，Active PD Follower 成为正式功能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-从-v840-版本开始引入">实例级执行计划缓存</a>（实验特性）（v8.4.0 引入）</td>
    <td>实例级执行计划缓存允许同一个 TiDB 实例的所有会话共享执行计划缓存。与现有的会话级执行计划缓存相比，实例级执行计划缓存能够在内存中缓存更多执行计划，减少 SQL 编译时间，从而降低 SQL 整体运行时间，提升 OLTP 的性能和吞吐，同时更好地控制内存使用，提升数据库稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/partitioned-table#全局索引">分区表全局索引</a>（v8.4.0  起成为正式功能）</td>
    <td>全局索引可以有效提高检索非分区列的效率，并且消除了唯一键必须包含分区键的限制。该功能扩展了 TiDB 分区表的使用场景，避免了数据迁移过程中的一些应用修改工作。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_opt_projection_push_down-从-v610-版本开始引入">默认允许将 <code>Projection</code> 算子下推到存储引擎</a>（v8.3.0 引入）</td>
    <td> <code>Projection</code> 算子下推可以将负载分散到存储节点，同时减少节点间的数据传输。这有助于降低部分 SQL 的执行时间，提升数据库的整体性能。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#收集部分列的统计信息">统计信息收集忽略不必要的列</a>（v8.3.0 引入）</td>
    <td> 在保证优化器能够获取到必要信息的前提下，加快了统计信息收集的速度，提升统计信息的时效性，进而保证选择最优的执行计划，提升集群性能。同时也降低了系统开销，改善了资源利用率。</td>
  </tr>
  <tr>
    <td rowspan="5">稳定性与高可用</td>
    <td>提升超大规模集群的稳定性 **tw@hfxsd 1976**</td>
    <td>对于使用 TiDB 运行多租户应用或者 SaaS 应用的公司，经常需要存储大量的表，TiDB 在 v8.5.0 着力增强了大规模集群的稳定性。 <a href="https://docs.pingcap.com/zh/tidb/v8.5/schema-cache">Schema 缓存控制</a>以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-从-v610-版本开始引入">Stats 缓存控制</a>已经成为正式功能，减少了内存过度消耗带来的稳定性问题。 PD 通过 <a href="https://docs.pingcap.com/zh/tidb/v8.5/tune-region-performance#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力">Active Follower</a> 应对大量 Region 带来的压力，并<a href="https://docs.pingcap.com/zh/tidb/v8.5/pd-microservices">将 PD 所承担的服务逐步解耦</a>，独立部署。通过<a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-从-v840-版本开始引入">增加并发度</a>，以及<a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#收集部分列的统计信息">减少收集对象的数量</a>，统计信息收集和加载效率得到提升，保证了大集群执行计划的稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-resource-control#query_limit-参数说明">Runaway Queries 支持更多触发条件，并能够切换资源组</a> （v8.4.0 引入）</td>
    <td>Runaway Queries 提供了有效的手段来降低突发的 SQL 性能问题对系统产生的影响。v8.4.0 中新增 Coprocessor 处理的 Key 的数量 (PROCESSED_KEYS) 和 Request Unit (RU) 作为识别条件，并可以将识别到的查询置入指定资源组，对 Runaway Queries 进行更精确的识别与控制。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-resource-control#background-参数说明">支持为资源管控的后台任务设置资源使用上限</a> (实验特性)（v8.4.0 引入）</td>
    <td>为资源管控的后台任务设置百分比上限，针对不同业务系统的需求，控制后台任务的消耗，从而将后台任务的消耗限制在一个很低的水平，保证在线业务的服务质量。</td>
  </tr>
  <tr>
    <td>增强并扩展 TiProxy 的使用场景 **tw@Oreoxmt**</td>
    <td>作为 TiDB 高可用的重要组成，TiProxy 在做好 SQL 流量接入和转发的同时，开始尝试对集群变更进行评估。主要包括：
    <li> TiProxy 流量捕获和回放（实验特性）（v8.4.0 引入）</li>
    <li> TiProxy 内置虚拟 IP 管理（v8.3.0 引入）</li>
    <li> TiProxy 支持多种负载均衡策略 （v8.2.0 引入）</li>
    </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入">并行 HashAgg 算法支持数据落盘</a> （v8.2.0 起成为正式功能）</td>
    <td>HashAgg 是 TiDB 中常用的聚合算子，用于快速聚合具有相同字段值的行。TiDB v8.0.0 引入并行 HashAgg 作为实验特性，以进一步提升处理速度。当内存资源不足时，并行 HashAgg 可以将临时排序数据落盘，避免因内存使用过度而导致的 OOM 风险，从而提升查询性能和节点稳定性。该功能在 v8.2.0 成为正式功能，并默认开启，用户可以通过 <code>tidb_executor_concurrency</code> 安全地设置并行 HashAgg 的并发度。</td>
  </tr>
  <tr>
    <td rowspan="2"> SQL </td>
    <td>外键约束成为正式功能 **tw@lilin90 1894**</td>
    <td>外键（Foreign Key）是数据库中的一种约束，用于建立表与表之间的关联关系，确保数据一致性和完整性。它可以限制子表中引用的数据必须存在于主表中，防止无效数据插入。同时，外键支持级联操作（如删除或更新时自动同步），简化了业务逻辑的实现，减少了手动维护数据关联的复杂性。</td>
  </tr>
  <tr>
    <td>支持<a href="https://docs.pingcap.com/zh/tidb/v8.5/vector-search-overview">向量搜索功能</a>（实验特性）(v8.4.0 引入）</td>
    <td>向量搜索是一种基于数据语义的搜索方法，可以提供更相关的搜索结果。作为 AI 和大语言模型 (LLM) 的核心功能之一，向量搜索可用于检索增强生成 (Retrieval-Augmented Generation, RAG)、语义搜索、推荐系统等多种场景。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理与可观测性</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/information-schema-processlist">在内存表中显示 TiKV 和 TiDB 的 CPU 时间</a> （v8.4.0 引入）</td>
    <td>将 CPU 时间合入系统表中展示，与会话或 SQL 的其他指标并列，方便你从多角度对高 CPU 消耗的操作进行观测，提升诊断效率。尤其适用于诊断实例 CPU 飙升或集群读写热点等场景。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/top-sql#使用-top-sql">按表或数据库维度聚合 TiKV 消耗的 CPU 时间</a>（v8.4.0 引入）</td>
    <td>当热点问题不是由个别 SQL 语句引起时，利用 Top SQL 中按表或者数据库聚合的 CPU 时间，能够协助用户快速发现造成热点的表或者应用程序，从而大大提升热点问题和 CPU 消耗问题的诊断效率。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/backup-and-restore-storages#鉴权">支持对开启了 IMDSv2 服务的 TiKV 实例做备份</a> （v8.4.0 引入）</td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">目前 AWS EC2 的默认元数据服务是 IMDSv2</a>。TiDB 支持从开启了 IMDSv2 的 TiKV 实例中备份数据，协助你更好地在公有云服务中运行 TiDB 集群。</td>
  </tr>
  <tr>
    <td rowspan="1">安全</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.5/br-pitr-manual#加密日志备份数据">日志备份数据支持客户端加密</a></td>
    <td>在上传日志备份到备份存储之前，你可以对日志备份数据进行加密，确保数据在存储和传输过程中的安全性。</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* The schema cache memory limit feature is now generally available (GA), reducing memory usage in scenarios with hundreds of thousands or even millions of databases or tables. [#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--1976-->

    In some SaaS scenarios, when the number of tables reaches hundreds of thousands or even millions, the schema meta can consume significant memory. Enabling this feature allows TiDB to use the LRU algorithm to cache and evict the corresponding schema meta information, effectively reducing memory usage. 
    
    Starting from v8.4.0, this feature is enabled by default with a default value of `536870912` (that is, 512MiB). You can adjust it as needed through the variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).

    For more information, see [Documentation](/schema-cache.md).

* Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (General Availability) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang)

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    To ensure high availability and also enhance the scalability of PD's Region information query service. You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)

### Performance

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

* TiDB accelerated table creation becomes generally available (GA), significantly reducing data migration and cluster initialization time [#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd) tw@Oreoxmt <!--1977-->

    TiDB v7.6.0 introduces accelerated table creation as an experimental feature, controlled by the system variable [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760). Staring from v8.0.0, this system variable is renamed to [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).

    In v8.5.0, TiDB accelerated table creation becomes generally available (GA) and is enabled by default. During data migration and cluster initialization, this feature supports rapid creation of millions of tables, significantly reducing operation time.

    For more information, see [Documentation](/accelerated-table-creation.md).

### Reliability

* Enabling rate limiter can protect PD from being crash under a large number of sudden requests and improve the stability of PD [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx)

    You can adjust the rate limiter configuration through pd-ctl. 
    
    For more information, see [Documentation](/stable/pd-control.md).

### Availability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### SQL

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

* The Foreign Key feature is now Generally Available (GA) [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520) tw@lilin90 <!--1894-->

    The Foreign Key feature is now GA, enabling the use of foreign key constraints to enhance data consistency and integrity. Users can easily create foreign key constraints between tables, with support for cascading updates and deletions, making data management more convenient. This feature provides better support for applications with complex data constraints.

    For more information, see [Documentation](link).

* Introduce the `ADMIN ALTER DDL JOBS` statement to support modifying the DDL jobs online [#57229](https://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--2016--> 

    Starting from v8.3.0, you can set the variables [`tidb_ddl_reorg_batch_size`](/system-variables#tidb_ddl_reorg_batch_size)  and [`tidb_ddl_reorg_worker_cnt`](/system-variables#tidb_ddl_reorg_worker_cnt) at the session level. As a result, setting these two variables globally no longer affects all running DDL jobs. To modify the values of these variables, you need to cancel the DDL job first, adjust the variables, and then resubmit the job.

    TiDB v8.5.0 introduces the `ADMIN ALTER DDL JOBS` statement, allowing online adjustment of variable values for specific DDL jobs. This enables flexible balancing of resource consumption and performance, with changes limited to an individual job, making the impact more controllable. For example:

    - `ADMIN ALTER DDL JOBS job_id THREAD = 8;`: adjusts the `tidb_ddl_reorg_worker_cnt` for the specified DDL task.
    - `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;`: adjusts the `tidb_ddl_reorg_batch_size` for the specified DDL task.
    - `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';`: adjusts the write traffic size for index data on each TiKV node.

  For more information, see [Documentation](/sql-statements/sql-statement-admin-alter-ddl.md).

### DB operations

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Observability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Security

* BR supports client-side encryption of full backup (GA) [#28640](https://github.com/pingcap/tidb/issues/28640) @[joccau](https://github.com/joccau) and log backup data (GA) [#56433] (https://github.com/pingcap/tidb/issues/56433) @[Tristan1900](https://github.com/Tristan1900) tw@qiancai <!--1998-->
TiDB V5.3.0 introduced an experimental feature to encrypt full backup data on the client side, you can encrypt the backup data using a custom fixed key. This feature is Generally Available in v8.5.0

For more information, see [documentation](/br/br-snapshot-manual.md#encrypt-the-backup-data).
    TiDB v8.4.0 introduced an experimental feature to encrypt log backup data on the client side. Starting from v8.5.0, this feature is now Generally Available. Before uploading log backup data to your backup storage, you can encrypt the log backup data to ensure its security via one of the following methods:

    - Encrypt using a custom fixed key
    - Encrypt using a master key stored on a local disk
    - Encrypt using a master key managed by a Key Management Service (KMS)

  For more information, see [documentation](/br/br-pitr-manual.md#encrypt-the-log-backup-data).

* TiKV encryption at rest supports Google [Key Management Service (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl) (GA) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv)

    In v8.0.0, TiKV has supported this feature as an experimental feature. TiKV supports configuring Google Cloud KMS-based master keys for encryption at rest. Starting from v8.5.0, this feature is now Generally Avaialble.
    To enable encryption at rest based on Google Cloud KMS, you need to create a key on Google Cloud and then configure the `[security.encryption.master-key]` section in the TiKV configuration file.
  
    For more information, see [documentation](/encryption-at-rest.md#tikv-encryption-at-rest).

### Data migration

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.1.0 to the current version (v8.2.0). If you are upgrading from v8.0.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### MySQL compatibility

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|tidb_ddl_reorg_max_write_speed  | Newly added |Used to control the speed at which TiDB writes index data to a single TiKV node. For example, setting the value to 200 MiB limits the maximum write speed to 200 MiB/s.  |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the [accelerated table creation](/accelerated-table-creation.md) feature is enabled by default. |
|  |  |  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### System tables

### Other changes

## Offline package changes

## Removed features

## Deprecated features

The following features are planned for deprecation in future versions:

* TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
* TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
* It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
* In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
* The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.
* Starting from v6.3.0, partitioned tables use [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) by default. Compared with static pruning mode, dynamic pruning mode supports features such as IndexJoin and plan cache with better performance. Therefore, static pruning mode will be deprecated.

## Improvements

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## Bug fixes

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [Contributor-GitHub-ID](id-link)
