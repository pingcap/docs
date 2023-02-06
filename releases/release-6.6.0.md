---
title: TiDB 6.6.0 Release Notes
---

# TiDB 6.6.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.6.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.6/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/)

在 6.6.0 版本中，你可以获得以下关键特性：

- MySQL 8.0 兼容的多值索引 (Multi-Valued Index) (实验特性)
- 基于资源组的资源管控 (实验特性)
- 悲观锁队列的稳定唤醒模型
- 数据请求的批量聚合

## 新功能

### SQL

* 支持 DDL 动态资源管控（实验性特性） [#issue](链接)  @[hawkingrei](https://github.com/hawkingrei) **tw@ran-huang**

    TiDB v6.6.0 版本引入了 DDL 动态资源管控， 通过自动控制 DDL 的 CPU 和内存使用量，尽量降低 DDL 变更任务对线上业务的影响。

    更多信息，请参考[用户文档](链接)。

* Support the foreign key constraint that is compatible with MySQL (experimental) [#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt**

    TiDB v6.6.0 introduces the foreign key constraint feature compatible with MySQL. This feature supports data correlation in a table or between tables, constraint validation, and supports cascade operations. This feature helps to maintain data consistency, improve data quality, and facilitate data modeling.

    For more information, see [documentation](/sql-statements/sql-statement-foreign-key.md).

* 支持通过`FLASHBACK CLUSTER TO TIMESTAMP` 命令闪回 DDL 操作 [#14088](https://github.com/tikv/tikv/pull/14088) @[Defined2014](https://github.com/Defined2014) @[JmPotato](https://github.com/JmPotato) **tw@ran-huang**

    [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) 语句支持在 Garbage Collection (GC) life time 内快速回退整个集群到指定的时间点，该功能在 TiDB v6.6.0 版本新增支持撤销 DDL 操作，适用于快速撤消集群的 DML 或 DDL 误操作、支持集群分钟级别的快速回退、支持在时间线上多次回退以确定特定数据更改发生的时间。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-to-timestamp.md)。

* 支持 DDL 分布式并行执行框架（实验性特性） [#issue](链接)  @[zimulala](https://github.com/zimulala) **tw@ran-huang**

    在过去的版本中，整个 TiDB 集群中仅允许一个 TiDB 实例作为 DDL Owner 有权处理 Schema 变更任务，为了进一步提升 DDL 的并发性，TiDB v6.6.0 版本引入了 DDL 分布式并行执行框架，支持集群中所有的 TiDB 实例都作为 Owner 并发执行同一个 Schema 变更子任务，加速 DDL 的执行。

    更多信息，请参考[用户文档](链接)。

* MySQL 兼容的多值索引(Multi-Valued Index) (实验特性) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) **tw@TomShawn**

    TiDB 在 v6.6.0 引入了 MySQL 兼容的多值索引 (Multi-Valued Index)。 过滤 JSON 类型中某个数组的值是一个常见操作， 但普通索引对这类操作起不到加速作用，而在数组上创建多值索引能够大幅提升过滤的性能。 如果 JSON 类型中的某个数组上存在多值索引，  带有`MEMBER OF()`，`JSON_CONTAINS()`，`JSON_OVERLAPS()` 这几个函数的检索条件可以利用多值索引进行过滤，减少大量的 I/O 消耗，提升运行速度。

    多值索引的引入， 是对 JSON 类型的进一步增强， 同时也提升了 TiDB 对 MySQL 8.0 的兼容性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-create-index.md#多值索引)。

* 绑定历史执行计划 GA [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678) **tw@TomShawn**

    在 v6.5 中，TiDB 扩展了 [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) 语句中的绑定对象，支持根据历史执行计划创建绑定。在 v6.6 中这个功能 GA， 执行计划的选择不仅限在当前 TiDB 节点，任意 TiDB 节点产生的历史执行计划都可以被选为 [SQL Binding]((/sql-statements/sql-statement-create-binding.md)) 的目标，进一步提升了功能的易用性。

    更多信息，请参考[用户文档](/sql-plan-management.md#根据历史执行计划创建绑定)。

* Support configuring `SURVIVAL_PREFERENCE` for [placement rules in SQL](/placement-rules-in-sql.md) [#38605](https://github.com/pingcap/tidb/issues/38605) @nolouch[https://github.com/nolouch] **tw@qiancai**

    `SURVIVAL_PREFERENCES` provides data survival preference settings to increase the disaster survivability of data. By specifying `SURVIVAL_PREFERENCE`, you can control the following:

    - For TiDB clusters deployed across regions, when a region with the specified databases or tables fails, another region can provide the service.
    - For TiDB clusters deployed in a single region, when an availability zone with the specified databases or tables fails, another availability zone can provide the service.

     For more information, see [documentation](/placement-rules-in-sql.md#survival-preference).

### Security

* TiFlash supports automatic rotations of TLS certificates [#5503](https://github.com/pingcap/tiflash/issues/5503) @[ywqzzy](https://github.com/ywqzzy) **tw@qiancai**

    For a TiDB cluster with encrypted data transmission between components enabled, when a TLS certificate of TiFlash expires and needs to be reissued with a new one, the new TiFlash TLS certificate can be automatically loaded without restarting the TiDB cluster. The rotation of a TLS certificate between components within a TiDB cluster does not affect the use of the TiDB cluster, which ensures the cluster high availability.

    For more information, see [documentation](/enable-tls-between-components.md).

### 可观测性

* 快速绑定执行计划 [#781](https://github.com/pingcap/tidb-dashboard/issues/781) @[YiniXu9506](https://github.com/YiniXu9506) **tw@ran-huang**

    TiDB 的执行计划快速绑定功能：允许用户在 TiDB Dashboard 中一分钟内完成 SQL 与特定计划的绑定。

    通过提供友好的界面简化在 TiDB 上绑定计划的过程，减少计划绑定过程的复杂性提高用户体验，提高计划绑定过程的效率。

    更多信息，请参考[用户文档](/dashboard/dashboard-statement-details.md)。

* 为执行计划缓存增加告警 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@TomShawn**

    当执行计划无法进入执行计划缓存时， TiDB 会通过 warning 的方式说明其无法被缓存的原因， 降低诊断的难度。例如：

    ```sql
    mysql> prepare st from 'select * from t where a<?';
    Query OK, 0 rows affected (0.00 sec)

    mysql> set @a='1';
    Query OK, 0 rows affected (0.00 sec)

    mysql> execute st using @a;
    Empty set, 1 warning (0.01 sec)

    mysql> show warnings;
    +---------+------+----------------------------------------------+
    | Level   | Code | Message                                      |
    +---------+------+----------------------------------------------+
    | Warning | 1105 | skip plan-cache: '1' may be converted to INT |
    +---------+------+----------------------------------------------+
    ```

    上述例子中， 优化器进行了非 INT 类型到 INT 类型的转换，产生的计划可能随着参数变化有风险，因此不缓存。

    更多信息，请参考[用户文档](/sql-prepared-plan-cache.md#prepared-plan-cache-诊断)。

* Add the `Warnings` field to the slow query log [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate) **tw@Oreoxmt**

    The `Warnings` field is added to the slow query log in JSON format to record the warnings generated during the execution of the slow query to help diagnose performance issues. You can also view this in the slow query page of TiDB Dashboard.

    For more information, see [documentation](/identify-slow-queries.md).

* 自动捕获执行计划的生成 [#38779](https://github.com/pingcap/tidb/issues/38779) @[Yisaer](https://github.com/Yisaer) **tw@ran-huang**

    在执行计划问题的排查过程中，`PLAN REPLAYER` 能够协助保存现场，提升诊断的效率。 但在个别场景中，一些执行计划的生成无法任意重现，给诊断工作增加了难度。 针对这类问题， `PLAN REPLAYER` 扩展了自动捕获的能力。 通过 `PLAN REPLAYER CAPTURE` 命令字，用户可提前注册目标 SQL，也可以同时指定目标执行计划， 当 TiDB 检测到执行的 SQL 和执行计划与注册目标匹配时， 会自动生成并打包 `PLAN REPLAYER` 的信息，提升执行计划不稳定问题的诊断效率。

    启用这个功能需要设置系统变量 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) 为 `ON`。

    更多信息，请参考[用户文档](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。

* Support persisting statements summary (experimental) [#40812](https://github.com/pingcap/tidb/issues/40812) @[mornyx](https://github.com/mornyx) **tw@shichun-0415**

    Before v6.6.0, statements summary data is maintained in memory. Once the TiDB server restarts, all the statements summary data gets lost. Starting from v6.6.0, TiDB supports enabling statements summary persistence, which allows historical data to be written to disks on a regular basis. In the meantime, the result of queries on system tables will derive from disks, instead of memory. After TiDB restarts, all historical data is still available.

    For more information, see [documentation](/statement-summary-tables.md#persist-statements-summary).

### 性能

* Use Witness to Save Costs in a highly reliable storage environment [#12876](https://github.com/tikv/tikv/issues/12876) @[Connor1996](https://github.com/Connor1996) @[ethercflow](https://github.com/ethercflow) **tw@Oreoxmt**

    In cloud environments, it is recommended to use Amazon Elastic Block Store or Persistent Disk of Google Cloud Platform as the storage of each TiKV node. In this case, it is not necessary to use three Raft replicas. To reduce costs, TiKV introduces the Witness feature, which is the "2 Replicas With 1 Log Only" mechanism. The 1 Log Only replica only stores Raft logs but does not apply data, and data consistency is still guaranteed through the Raft protocol. Compared with the standard three replica architecture, Witness can save storage resources and CPU usage.

    For more information, see [documentation](/use-witness-to-save-costs.md).

* TiFlash supports the Stale Read feature [#4483](https://github.com/pingcap/tiflash/issues/4483) @[hehechen](https://github.com/hehechen) **tw@qiancai**

   The Stale Read feature has been generally available (GA) since v5.1.1, which allows you to read historical data at a specific timestamp or within a specified time range. Stale read can reduce read latency and improve query performance by reading data from local TiKV replicas directly. Before v6.6.0, TiFlash does not support Stale Read. Even if a table has TiFlash replicas, Stale Read can only read its TiKV replicas.

   Starting from v6.6.0, TiFlash supports the Stale Read feature. When you query the historical data of a table using the `AS OF TIMESTAMP` syntax or the `tidb_read_staleness` system variable, if the table has a TiFlash replica, the optimizer now can choose to read the corresponding data from the TiFlash replica, thus further improving query performance.

    For more information, see [documentation](/stale-read.md).

* Support pushing down the `regexp_replace` string function to TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**

* 批量聚合数据请求 [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06) **tw@TomShawn**

    当 TiDB 向 TiKV 发送数据请求时， 会根据数据所在的 Region 将请求编入不同的子任务，每个子任务只处理单个 Region 的请求。 当访问的数据离散度很高时， 即使数据量不大，也会生成众多的子任务，进而产生大量 RPC 请求，消耗额外的时间。 在 v6.6.0 中，TiDB 支持将发送到相同 TiKV 实例的数据请求部分合并，减少子任务的数量和 RPC 请求的开销。 在数据离散度高且 gRPC 线程池资源紧张的情况下，批量化请求能够将性能提升 50% 以上。

    此特性默认打开， 通过系统变量 [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) 设置批量请求的大小。

* 新增一系列优化器 Hint [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent) **tw@TomShawn**

    TiDB 在新版本中增加了一系列优化器 Hint， 用来控制 `LIMIT` 操作的执行计划选择，以及 MPP 执行过程中的部分行为。 其中包括：

    - [`KEEP_ORDER()`](/optimizer-hints.md#keep_ordert1_name-idx1_name--idx2_name-): 提示优化器使用指定的索引，读取时保持索引的顺序。 生成类似 `Limit + IndexScan(keep order: true)` 的计划。
    - [`NO_KEEP_ORDER()`](/optimizer-hints.md#no_keep_ordert1_name-idx1_name--idx2_name-): 提示优化器使用指定的索引，读取时不保持顺序。 生成类似 `TopN + IndexScan(keep order: false)` 的计划。
    - [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name--tl_name-): 针对 MPP 生效。 提示优化器对指定表使用 Shuffle Join 算法。
    - [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name--tl_name-): 针对 MPP 生效。提示优化器对指定表使用 Broadcast Join 算法。
    - [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg): 针对 MPP 生效。提示优化器对指定查询块中所有聚合函数使用一阶段聚合算法。
    - [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg): 针对 MPP 生效。 提示优化器对指定查询块中所有聚合函数使用二阶段聚合算法。

    优化器 Hint 的持续引入，为用户提供了更多的干预手段，有助于 SQL 性能问题的解决，并提升了整体性能的稳定性。

* Remove the limit on `LIMIT` statements [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678) **tw@shichun-0415**

    Starting from v6.6.0, TiDB plan cache supports caching queries containing `?` after `Limit`, such as `Limit ?` or `Limit 10, ?`. This feature allows more SQL statements to benefit from plan cache, thus improving execution efficiency.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* 悲观锁队列的稳定唤醒模型 [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta) **tw@TomShawn**

    如果业务场景存在单点悲观锁冲突频繁的情况，原有的唤醒机制无法保证事务获取锁的时间，造成长尾延迟高，甚至获取超时。 在 v6.6.0 中，通过设置系统变量 [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) 为 `ON` 可以开启悲观锁的稳定唤醒模型。 在新的唤醒模型下， 队列的唤醒顺序可被严格控制，避免无效的唤醒造成的资源浪费，在锁冲突严重的场景中，能够减少长尾延时，降低 P99 响应时间。

    更多信息，请参考[用户文档](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入)。

### 事务

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* Resource control based on resource groups (experimental) #[38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw@hfxsd**

    TiDB clusters support creating resource groups, binding different database users to corresponding resource groups, and setting quotas for each resource group according to actual needs. When the cluster resources are limited, all resources used by sessions from the same resource group will be limited to the quota, so that one resource group will not be over-consumed and affect the normal operation of sessions in other resource groups. The built-in view of the system will display the actual usage of resources, assisting you to allocate resources more rationally.

    The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units. 

    With this feature, you can:

    - Combine multiple small and medium-sized applications from different systems into one TiDB cluster. If the load of an individual application grows larger, it does not affect the normal operation of other businesses. When the system load is low, busy applications can still be allocated the required system resources even if they exceed the set read and write quotas, so as to achieve the maximum utilization of resources.
    - Choose to combine all test environments into a single cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can still get the necessary resources.

    In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

    In v6.6, you need to enable both TiDB's global variable [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) and the TiKV configuration item [`resource_control.enabled`](/tikv-configuration-file.md#resource_control) to enable resource control. The currently supported quota method is based on "[Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru)". RU is TiDB's unified abstraction unit for system resources such as CPU and IO.

    For more information, see [documentation](/tidb-resource-control.md).

* Use a temporary Witness replica to spped up failover [#12876](https://github.com/tikv/tikv/issues/12876) @[Connor1996](https://github.com/Connor1996) @[ethercflow](https://github.com/ethercflow) **tw@Oreoxmt**

    The Witness feature can be used to quickly recover a failover to improve system availability and data durability. For example, in a 3-out-of-4 scenario, although it meets the majority requirement, the system is fragile and the time to completely recover a new member is often long (requires copying the snapshot first and then applying the latest log), especially when the Region snapshot is relatively large. In addition, the process of copying replicas might cause more pressure on unhealthy Group members. Therefore, adding a Witness can quickly bring down an unhealthy node and enmsure the security of logs during recovery.

    For more information, see [documentation](/use-witness-to-speed-up-failover.md)。

* Support configuring read-only storage nodes for resource-consuming tasks [#issue号](链接) @[v01dstar](https://github.com/v01dstar) **tw@Oreoxmt**

    In production environments, some read-only operations might consume a large amount of resources regularly, which might affect the performance of the entire cluster, such as backups and large-scale data analysis. TiDB v6.6.0 supports configuring read-only storage nodes to execute resource-consuming read-only tasks to reduce the impact on the online application. You can configure read-only storage nodes according to [steps](/readonly-nodes.md#操作步骤) and specify where to read data through a system variable or client parameter to ensure the stability of cluster performance.

    For more information, see [documentation](/best-practices/readonly-nodes.md).

### 易用性

* Support dynamically modifying `store-io-pool-size` [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator) **tw@shichun-0415**

    The TiKV configuration item [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) specifies the allowable number of threads that process Raft I/O tasks, which can be adjusted when tuning TiKV performance. Before v6.6.0, this configuration item cannot be modified dynamically. Starting from v6.6.0, you can modify this configuration without restarting the server, which means more flexible performance tuning.

    For more information, see [documentation](/dynamic-config.md).

* Support specifying the SQL script executed upon TiDB cluster intialization [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo) **tw@shichun-0415**

    When you start a TiDB cluster for the first time, you can specify the SQL script to be executed by configuring the CLI parameter `--initialize-sql-file`. You can use this feature when you need to perform such operations as modifying the value of a system variable, creating a user, or granting privileges.

    For more information, see the [configuration item `initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660).

### MySQL 兼容性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* Data Migration(DM) 集成了 Lightning 的 Physical Import Mode ，全量迁移性能最高提升  10 倍  @[lance6716](https://github.com/lance6716) **tw@ran-huang**

    功能描述 ：Data Migration (DM)的全量迁移能力，集成了 Lightning 的 Physical Import Mode ，使得 DM 做全量数据迁移时的性能最高可提升 10 倍，大大缩短了大数据量场景下的迁移时间。原先客户数据量较多时，客户得单独配置 Lightning 的 Physical Import Mode 的任务来做快速的全量数据迁移，之后再用 DM 来做增量数据迁移，配置复杂。现在集成该能力后，用户迁移大数据量的场景，无需再配置 Lightning 的任务，在一个 DM 任务里就可以搞定了。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/12296)。

### 数据共享与订阅

* The TiKV-CDC tool is now GA and supports subscribing to data changes of RawKV [#48](https://github.com/tikv/migration/issues/48) @[zeminzhou](https://github.com/zeminzhou) @[haojinming](https://github.com/haojinming) @[pingyu](https://github.com/pingyu) **tw@Oreoxmt**

    TiKV-CDC is a CDC (Change Data Capture) tool for TiKV clusters. TiKV can operate independently of TiDB and form a KV database with PD. In this case, the product is called RawKV. TiKV-CDC supports subscribing to data changes of RawKV and replicating them to a downstream TiKV cluster in real time, thus enabling cross-cluster replication of RawKV.

    For more information, see [documentation](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc-cn/).

* TiCDC supports scaling out a single table on Kafka changefeeds and distributing the changefeed to multiple TiCDC nodes [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus) **tw@Oreoxmt**

    Before v6.6.0, when the write throughput of the upstream table is large, the replication capability of a single table could not be scaled out, resulting in an increase in replication latency. Starting from TiCDC v6.6.0. the changefeed of a upstream table can be distributed to multiple TiCDC nodes in a Kafka sink, which enables scaling out the replication capability of a single table.

    For more information, see [documentation](/ticdc/ticdc-sink-to-kafka.md#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes).

### 部署及运维

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit--new-in-v660) | New | Controls whether Prepared Plan Cache caches execution plans that contain `count` after `Limit`. The default value is `ON`, which means Prepared Plan Cache supports caching such execution plans. Note that Prepared Plan Cache does not support caching execution plans with a `count` that is greater than 10000. |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) | 新增  | 该变量是资源管控特性的开关。该变量设置为 `ON` 后，集群支持应用按照资源组做资源隔离。 |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) | 修改 | 此变量可用于生产环境。 设置 `IndexLookUp` 算子回表时多个 Coprocessor Task 的 batch 大小。`0` 代表不使用 batch。当 `IndexLookUp` 算子的回表 Task 数量特别多，出现极长的慢查询时，可以适当调大该参数以加速查询。 |
| [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型。 |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) | 新增 | 这个变量用来控制是否开启 [`PLAN REPLAYER CAPTURE`](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。默认值 `OFF`， 代表关闭 `PLAN REPLAYER CAPTURE`。 |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | [`resource_control.enabled`](/tikv-configuration-file.md#tidb_enable_resource_control-%E4%BB%8E-v660-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) | 新增 | 是否支持按照资源组配额调度。 默认 `false` ，即关闭按照资源组配额调度。 |
| TiFlash |  [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)  |  Modified  |  Specifies the memory usage limit for the generated intermediate data in all queries. Starting from v6.6.0, the default value changes from 0 to 0.8, which means the limit is 80% of the total memory.|
| TiCDC  | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#prerequisites)  |  Modified  | Added to value options: GCS and Azure.  |
| TiDB  | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)  | New | Specifies the SQL script to be executed when the TiDB cluster is started for the first time. The default value is empty.  |
| TiDB  | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)  |  New  |  Controls whether to enable statements summary persistence. The default value is `false`, which means this feature is not enabled by default.  |
| TiDB | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660) | New | When statements summary persistence is enabled, this configuration specifies the file to which persistent data is written. |
| TiDB | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) | New | When statements summary persistence is enabled, this configuration specifies the maximum number of days to keep persistent data files. |
| TiDB | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) | New | When statements summary persistence is enabled, this configuration specifies the maximum size of a persistent data file (in MiB). |
| TiDB | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660) | New | When statements summary persistence is enabled, this configuration specifies the maximum number of data files that can be persisted. `0` means no limit on the number of files. |
| sync-diff-inspector | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description) | New | Controls whether to skip checking upstream and downstream data consistency when tables in the downstream do not exist in the upstream.  |
|          |          |          |          |

### Others

- Support dynamically modifying `store-io-pool-size`. This facilitate more flexible TiKV performance tuning.
- Remove the limit on `LIMIT` statements, thus improving the execution performance.

## 废弃功能

## 改进提升

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

    - Support an independent MVCC bitmap filter that decouples the MVCC filtering operations in the TiFlash data scanning process, which provides a foundation for subsequent optimization of the data scanning process [#6296](https://github.com/pingcap/tiflash/issues/6296) @[JinheLin] **tw@qiancai**
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

         Optimize DM alert rules and content. [7376](https://github.com/pingcap/tiflow/issues/7376) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd**
        
         Previously, alerts similar to "DM_XXX_process_exits_with_error" were raised whenever an error occured. But some alerts are actually caused by idle database connections, which can be recovered after reconnecting. To reduce this kind of alerts, the alerts are divided into two types: automatically recoverable errors and unrecoverable errors.
        
        - For errors that are automatically recoverable, report the alert only if the error occurs more than 3 times within 2 minutes.
        - For errors that are not automatically recoverable, maintain the original behavior and report the alert immediately.

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Sync-diff-inspector

        - Add a new parameter `skip-non-existing-table` to skip checking upstream and downstream data consistency when tables in the downstream do not exist in the upstream [#692](https://github.com/pingcap/tidb-tools/issues/692) @[lichunzhu](https://github.com/lichunzhu) @[liumengya94](https://github.com/liumengya9) **tw@shichun-0415**
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

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

        - Fix the issue that TiDB Lightning timeout hangs due to TiDB restart in some scenarios [#33714](https://github.com/pingcap/tidb/issues/33714) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
