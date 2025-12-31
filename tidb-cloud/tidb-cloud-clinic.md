---
title: TiDB Cloud Clinic
summary: 学习如何使用 TiDB Cloud Clinic 进行高级监控与诊断。
---

# TiDB Cloud Clinic

TiDB Cloud Clinic 在 TiDB Cloud 上提供了高级监控和诊断能力，旨在帮助你快速定位性能问题，优化数据库，并通过详细分析和可操作的洞察提升整体性能。

![tidb-cloud-clinic](/media/tidb-cloud/tidb-cloud-clinic.png)

> **注意：**
>
> 目前，TiDB Cloud Clinic 仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

TiDB Cloud Clinic 仅对订阅了 **Enterprise** 或 **Premium** 支持计划的组织开放。

## 查看 Cluster 页面

要查看 **Cluster** 页面，请按照以下步骤操作：

1. 登录 [TiDB Cloud Clinic 控制台](https://clinic.pingcap.com/)，选择 **Continue with TiDB Account** 进入 TiDB Cloud 登录页面。

2. 在组织列表中，选择你的目标组织。所选项目下的集群会被展示出来。

3. 点击目标集群的名称。会显示集群概览页面，你可以在此查看集群的详细信息，包括：

    - 高级统计/指标（信息）
    - Top 慢查询（仅当集群的 TiDB 版本为 v8.1.1 或更高，v7.5.4 或更高时支持）
    - TopSQL（仅当集群的 TiDB 版本为 v8.1.1 或更高，v7.5.4 或更高时支持）
    - Benchmark Report

## 监控高级统计/指标（信息）

TiDB Cloud Clinic 使用 Grafana 为 TiDB 集群提供全面的统计/指标（信息）集。高级统计/指标（信息）的保留策略为 90 天。

要查看统计/指标（信息）面板，请按照以下步骤操作：

1. 在 [TiDB Cloud Clinic 控制台](https://clinic.pingcap.com/)中，进入某个集群的 **Cluster** 页面。

2. 点击 **Metrics**。

3. 点击你想要查看的面板名称，即可显示该面板。

面板及其内容可能会发生变化。目前，支持以下面板：

- Backup & Import
- DM-Professional
- DM-Standard
- Lightning
- Performance-Overview
- TiCDC-Summary
- TiDB
- TiDB-Resource-Control
- TiFlash-Summary
- TiKV-Details
- TiProxy-Summary
- User-Node-Info

## 分析 Top 慢查询

默认情况下，执行时间超过 300 毫秒的 SQL 查询会被视为慢查询。

在 TiDB Cloud 控制台默认的 [**Slow Queries**](/tidb-cloud/tune-performance.md#slow-query) 页面中，识别影响性能的查询可能较为困难，尤其是在慢查询数量较多的集群中。TiDB Cloud Clinic 的 **Top 慢查询** 功能基于慢查询日志提供聚合分析。通过该功能，你可以轻松定位存在性能问题的查询，将整体性能调优时间至少缩短一半。

Top 慢查询会按 SQL digest 聚合显示排名前 10 的查询，并按以下维度排序：

- 总延时
- 最大延时
- 平均延时
- 总内存
- 最大内存
- 平均内存
- 总次数

要在集群中查看慢查询，请按照以下步骤操作：

1. 在 [TiDB Cloud Clinic 控制台](https://clinic.pingcap.com/)中，进入某个集群的 **Cluster** 页面。

2. 点击 **Slow Query**。

3. Top 慢查询会以表格形式展示。你可以按不同列进行排序。

4. （可选）点击列表中的任意慢查询，查看其详细执行信息。

5. （可选）可按时间范围、数据库或语句类型筛选慢查询。

慢查询的保留策略为 7 天。

更多信息，参见 [TiDB Dashboard 中的 Slow Queries](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)。

## 监控 TopSQL

TiDB Cloud Clinic 提供 TopSQL 信息，使你能够实时监控并可视化分析数据库中每条 SQL 语句的 CPU 开销。这有助于你优化并解决数据库性能问题。

要查看 TopSQL，请按照以下步骤操作：

1. 在 [TiDB Cloud Clinic 控制台](https://clinic.pingcap.com/)中，进入某个集群的 **Cluster** 页面。

2. 点击 **TopSQL**。

3. 选择具体的 TiDB 或 TiKV 实例以观察其负载。你可以使用时间选择器或在图表中选择时间范围以细化分析。

4. 分析 TopSQL 展示的图表和表格。

更多信息，参见 [TiDB Dashboard 中的 TopSQL](https://docs.pingcap.com/tidb/stable/top-sql)。

## 生成 Benchmark Report

**Benchmark Report** 功能可帮助你在性能测试期间识别 TiDB 集群中的性能问题。完成压力测试后，你可以生成 Benchmark Report 以分析集群性能。报告会突出显示检测到的瓶颈并给出优化建议。应用这些建议后，你可以再次进行压力测试并生成新的 Benchmark Report，以对比性能提升。

要生成 Benchmark Report，请按照以下步骤操作：

1. 在 [TiDB Cloud Clinic 控制台](https://clinic.pingcap.com/)中，进入某个集群的 **Cluster** 页面。

2. 点击 **Benchmark Report**。

3. 选择要在 Benchmark Report 中分析的时间范围。

4. 点击 **Create Report** 生成 Benchmark Report。

5. 等待报告生成完成。报告准备好后，点击 **View** 打开报告。