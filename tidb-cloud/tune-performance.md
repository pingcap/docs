---
title: 分析与调优性能
summary: 了解如何分析和调优你的 TiDB Cloud 集群的性能。
---

# 分析与调优性能

TiDB Cloud 提供了 [慢查询](#slow-query)、[语句分析](#statement-analysis)、[Key Visualizer](#key-visualizer) 和 [Index Insight (beta)](#index-insight-beta) 等功能用于性能分析。

- 慢查询允许你搜索和查看 TiDB 集群中的所有慢查询，并通过查看其执行计划、SQL 执行信息及其他细节，深入分析每条慢查询的瓶颈。

- 语句分析使你可以直接在页面上观察 SQL 的执行情况，无需查询系统表即可轻松定位性能问题。

- Key Visualizer 帮助你观察 TiDB 的数据访问模式和数据热点。

- Index Insight 为你提供有意义且可操作的索引推荐。

> **Note:**
>
> 目前，**Key Visualizer** 和 **Index Insight (beta)** 不支持 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

## 查看 Diagnosis 页面

1. 在你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Monitoring** > **Diagnosis**。

## 慢查询

默认情况下，执行时间超过 300 毫秒的 SQL 查询会被视为慢查询。

要在集群中查看慢查询，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **Slow Query** 标签页。

3. 点击列表中的任意慢查询，可以显示其详细的执行信息。

4. （可选）你可以根据目标时间范围、相关数据库和 SQL 关键字筛选慢查询。你还可以限制显示的慢查询数量。

结果以表格形式展示，你可以根据不同的列对结果进行排序。

更多信息，参见 [TiDB Dashboard 中的慢查询](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)。

## 语句分析

要使用语句分析功能，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **SQL Statement** 标签页。

3. 在时间区间选择框中选择需要分析的时间段。此时你可以获得该时间段内所有数据库的 SQL 语句执行统计信息。

4. （可选）如果你只关注某些数据库，可以在下一个选择框中选择对应的 schema 进行结果筛选。

结果以表格形式展示，你可以根据不同的列对结果进行排序。

更多信息，参见 [TiDB Dashboard 中的语句执行详情](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)。

## Key Visualizer

> **Note:**
>
> Key Visualizer 仅支持 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

要查看关键分析，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **Key Visualizer** 标签页。

在 **Key Visualizer** 页面上，会显示一个大型热力图，展示访问流量随时间的变化。热力图每个轴的平均值分别显示在下方和右侧。左侧显示表名、索引名等信息。

更多信息，参见 [Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)。

## Index Insight (beta)

TiDB Cloud 的 Index Insight 功能通过为未有效利用索引的慢查询提供推荐索引，帮助你优化查询性能。

> **Note:**
>
> Index Insight 目前处于 beta 阶段，仅支持 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

更多信息，参见 [Index Insight](/tidb-cloud/index-insight.md)。