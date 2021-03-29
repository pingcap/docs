---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
aliases: ['/tidb/dev/experimental-features-4.0/']
---

# TiDB Experimental Features

This document introduces the experimental features of TiDB in different versions. It is **NOT** recommended to use these features in the production environment.

## Stability

+ TiFlash 限制压缩或整理数据占用 I/O 资源，缓解后台任务与前端的数据读写对 I/O 资源的争抢（v5.0 实验特性）
+ 提升优化器选择索引的稳定性（v5.0 实验特性）
    + 扩展统计信息功能，收集多列 NDV (Number of Distinct Values)、多列顺序依赖性、多列函数依赖性等信息，帮助优化器选择相对较优的索引。
    + 重构统计信息模块，帮助优化器选择相对较优的索引，包括从 `CMSKetch` 中删除 `TopN` 值、重构 `TopN` 搜索逻辑及从直方图中删除 `TopN` 信息，建立直方图的索引，方便维护 Bucket NDV。

## Scheduling

+ Cascading Placement Rules feature. It is a replica rule system that guides PD to generate corresponding schedules for different types of data. By combining different scheduling rules, you can finely control the attributes of any continuous data range, such as the number of replicas, the storage location, the host type, whether to participate in Raft election, and whether to act as the Raft leader. See [Cascading Placement Rules](/configure-placement-rules.md) for details. (v4.0 experimental feature)
+ Elastic scheduling feature. It enables the TiDB cluster to dynamically scale out and in on Kubernetes based on real-time workloads, which effectively reduces the stress during your application's peak hours and saves overheads. See [Enable TidbCluster Auto-scaling](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling) for details. (v4.0 experimental feature)

## SQL

+ List Partition (v5.0 experimental feature)
+ List Column Partition (v5.0 experimental feature)
+ The expression index feature. The expression index is also called the function-based index. When you create an index, the index fields do not have to be a specific column but can be an expression calculated from one or more columns. This feature is useful for quickly accessing the calculation-based tables. See [Expression index](/sql-statements/sql-statement-create-index.md) for details. (v4.0 experimental feature)

## Configuration management

+ 将配置参数持久化存储到 PD 中，并且可以动态修改配置项的功能。（v4.0 实验特性）

## TiDB 数据共享订阅

+ [Integrate TiCDC with Kafka Connect (Confluent Platform)](/ticdc/integrate-confluent-using-ticdc.md) (v5.0 experimental feature)
+ [The cyclic replication feature of TiCDC](/ticdc/manage-ticdc.md#cyclic-replication) (v5.0 experimental feature)
