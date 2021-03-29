---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
aliases: ['/tidb/dev/experimental-features-4.0/']
---

# TiDB Experimental Features

This document introduces the experimental features of TiDB in different versions. It is **NOT** recommended to use these features in the production environment.

## 稳定性

+ TiFlash 限制压缩或整理数据占用 I/O 资源，缓解后台任务与前端的数据读写对 I/O 资源的争抢（v5.0 实验特性）
+ 提升优化器选择索引的稳定性（v5.0 实验特性）
    + 扩展统计信息功能，收集多列 NDV (Number of Distinct Values)、多列顺序依赖性、多列函数依赖性等信息，帮助优化器选择相对较优的索引。
    + 重构统计信息模块，帮助优化器选择相对较优的索引，包括从 `CMSKetch` 中删除 `TopN` 值、重构 `TopN` 搜索逻辑及从直方图中删除 `TopN` 信息，建立直方图的索引，方便维护 Bucket NDV。

## 调度功能

+ Cascading Placement Rules 是一套副本规则系统，用于指导 PD 针对不同类型的数据生成对应的调度。通过组合不同的调度规则，用户可以精细地控制任何一段连续数据的副本数量、存放位置、主机类型、是否参与 Raft 投票、是否可以担任 Raft leader 等属性。详情参阅：[Cascading Placement Rules](/configure-placement-rules.md)。（v4.0 实验特性）
+ 弹性调度功能。结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。详情参阅：[启用 TidbCluster 弹性伸缩](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)。（v4.0 实验特性）

## SQL 功能

+ List 分区表 （List Partition）（v5.0 实验特性）
+ List Column 分区表 （List Column Partition)（v5.0 实验特性）
+ 表达式索引 (Expression Index) 功能。表达式索引也叫函数索引，在创建索引时索引的字段不一定是一个具体的列，也可以是由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。（v4.0 实验特性）

## 配置管理

+ 将配置参数持久化存储到 PD 中，并且可以动态修改配置项的功能。（v4.0 实验特性）

## TiDB 数据共享订阅

+ TiCDC 集成第三方生态 [Kafka Connect (Confluent Platform)](/ticdc/integrate-confluent-using-ticdc.md)（v5.0 实验特性）
+ TiCDC [支持 TiDB 集群之间环形同步](/ticdc/manage-ticdc.md#环形同步)（v5.0 实验特性）

## Scheduling

+ Cascading Placement Rules is an experimental feature of the Placement Driver (PD) introduced in v4.0. It is a replica rule system that guides PD to generate corresponding schedules for different types of data. By combining different scheduling rules, you can finely control the attributes of any continuous data range, such as the number of replicas, the storage location, the host type, whether to participate in Raft election, and whether to act as the Raft leader. See [Cascading Placement Rules](/configure-placement-rules.md) for details.
+ Elastic scheduling is an experimental feature based on Kubernetes, which enables TiDB to dynamically scale out and scale in clusters. This feature can effectively mitigate the high workload during peak hours of an application and saves unnecessary overhead. See [Enable TidbCluster Auto-scaling](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling) for details.

## SQL feature

Support the expression index feature. The expression index is also called the function-based index. When you create an index, the index fields do not have to be a specific column but can be an expression calculated from one or more columns. This feature is useful for quickly accessing the calculation-based tables. See [Expression index](/sql-statements/sql-statement-create-index.md) for details.

## Service-level features

+ TiDB instances support caching the calculation results that the operator has pushed down to TiKV in the unit of Region, which improves the efficiency of SQL executions in the following scenarios. See [Coprocessor Cache](/coprocessor-cache.md) for details.
    - The SQL statements are the same.
    - The SQL statements contain a changing condition (limited to the primary key of tables or partitions), and the other parts are consistent.
    - The SQL statements contain multiple changing conditions and the other parts are consistent. The changing conditions exactly match a compound index column.
+ Support persisting configuration parameters in PD and dynamically modifying configuration items to improve product usability.
