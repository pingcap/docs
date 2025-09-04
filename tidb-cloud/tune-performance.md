---
title: Analyze and Tune Performance
summary: 了解如何分析和调优你的 TiDB Cloud 集群的性能。
aliases: ['/tidbcloud/index-insight']
---

# Analyze and Tune Performance

TiDB Cloud 提供了 [Slow Query](#slow-query)、[Statement Analysis](#statement-analysis) 和 [Key Visualizer](#key-visualizer) 用于性能分析。

- Slow Query 允许你搜索和查看 TiDB 集群中的所有慢查询，并通过查看其执行计划、SQL 执行信息及其他细节，分析每条慢查询的瓶颈。

- Statement Analysis 使你可以直接在页面上观察 SQL 执行情况，无需查询系统表即可轻松定位性能问题。

- Key Visualizer 帮助你观察 TiDB 的数据访问模式和数据热点。

> **Note:**
>
> 目前，**Key Visualizer** 仅在 TiDB Cloud Dedicated 集群中可用。

## 查看 Diagnosis 页面

1. 在你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Monitoring** > **Diagnosis**。

## Slow Query

默认情况下，执行时间超过 300 毫秒的 SQL 查询会被视为慢查询。

要在集群中查看慢查询，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **Slow Query** 标签页。

3. 点击列表中的任意慢查询以显示其详细的执行信息。

4. （可选）你可以根据目标时间范围、相关数据库和 SQL 关键字筛选慢查询。你还可以限制显示的慢查询数量。

结果以表格形式展示，你可以根据不同的列对结果进行排序。

更多信息，参见 [Slow Queries in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)。

## Statement Analysis

要使用语句分析功能，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **SQL Statement** 标签页。

3. 在时间区间框中选择需要分析的时间段。此时你可以获得该时间段内所有数据库的 SQL 语句执行统计信息。

4. （可选）如果你只关注某些数据库，可以在下一个框中选择对应的 schema 以筛选结果。

结果以表格形式展示，你可以根据不同的列对结果进行排序。

更多信息，参见 [Statement Execution Details in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)。

## Key Visualizer

> **Note:**
>
> Key Visualizer 仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

要查看关键分析，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **Key Visualizer** 标签页。

在 **Key Visualizer** 页面上，会显示一个大型热力图，展示访问流量随时间的变化。热力图每个轴的平均值分别显示在下方和右侧。左侧显示表名、索引名等信息。

更多信息，参见 [Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)。