---
title: TiDB Cloud Lake Architecture
summary: TiDB Cloud Lake 架构。
---

# TiDB Cloud Lake 架构

本文介绍 TiDB Cloud Lake 的架构。

![TiDB Cloud Lake Architecture](/media/tidb-cloud-lake/architecture.png)

<SimpleTab groupId="databendlay">

<div label="Meta-Service Layer" value="Meta-Service Layer">

元信息服务是一个多租户服务，它将 {{{ .lake }}} 中每个租户的元信息存储在一个高可用的 Raft 集群中。这些元信息包括：

- 表结构：包括每张表的字段结构和存储位置信息，为查询规划提供优化信息，并为存储层写入提供事务原子性保证；
- 集群管理：当每个租户的集群启动时，集群内的多个实例会注册为元信息，并为这些实例提供健康检查，以确保集群整体健康；
- 安全管理：保存用户、角色和权限授予信息，以确保数据访问认证和授权过程的安全性与可靠性。

</div>

<div label="Compute Layer" value="Compute Layer">

存储与计算完全分离的架构赋予了 {{{ .lake }}} 独特的计算弹性。

{{{ .lake }}} 中的每个租户都可以拥有多个计算集群 (Warehouse)，每个计算集群都具有独占的计算资源，并且在空闲超过 1 分钟后可以自动释放，以降低使用成本。

在计算集群中，查询通过高性能的 {{{ .lake }}} 引擎执行。每个查询都会经过多个不同的子模块：

- Planner：在解析 SQL 语句后，它会根据不同的查询类型，将不同的运算符（如 Projection、Filter、Limit 等）组合成查询计划。
- Optimizer：{{{ .lake }}} 引擎提供了一个基于规则和基于成本的优化器框架，实现了一系列优化机制，例如谓词下推、Join 重排序和扫描裁剪，从而大幅加速查询。
- Processors：{{{ .lake }}} 实现了一个推拉结合的流水线执行引擎。它在 Processor 中将查询的物理执行组织为一系列流水线，并可根据查询任务的运行时信息动态调整流水线配置，结合向量化表达式计算框架，最大化 CPU 的计算能力。

此外，{{{ .lake }}} 还可以随着查询负载的变化动态增加或减少集群中的节点，使计算更快且更具成本效益。

</div>

<div label="Storage Layer" value="Storage Layer">

{{{ .lake }}} 的存储层基于 FuseEngine，后者专为低成本对象存储而设计和优化。FuseEngine 根据对象存储的特性高效组织数据，从而实现高吞吐的数据写入和读取。

FuseEngine 以列式格式压缩数据并将其存储在对象存储中，这显著减少了数据量和存储成本。

除了存储数据文件外，FuseEngine 还会生成索引信息，包括 MinMax index、Bloomfilter index 等。这些索引可在查询执行期间减少 IO 和 CPU 消耗，从而大幅提升查询性能。

</div>
</SimpleTab>