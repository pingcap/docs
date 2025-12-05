---
title: 分析与调优性能
summary: 了解如何在 TiDB Cloud 中分析与调优性能。
aliases: ['/tidbcloud/index-insight']
---

# 分析与调优性能

<CustomContent plan="starter,essential,dedicated">

TiDB Cloud 提供了 [慢查询](#slow-query)、[语句分析](#statement-analysis) 和 [Key Visualizer](#key-visualizer) 用于性能分析。

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud 提供了 [慢查询](#slow-query) 和 [SQL 语句](#sql-statement) 用于性能分析。

</CustomContent>

- 慢查询可以让你搜索和查看 TiDB <CustomContent plan="starter,essential,dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent> 中的所有慢查询，并通过查看其执行计划、SQL 执行信息及其他详细信息，深入分析每条慢查询的瓶颈。

- <CustomContent plan="starter,essential,dedicated">语句分析</CustomContent><CustomContent plan="premium">SQL 语句</CustomContent> 使你能够直接在页面上观察 SQL 执行情况，无需查询系统表即可轻松定位性能问题。

<CustomContent plan="starter,essential,dedicated">

- Key Visualizer 帮助你观察 TiDB 的数据访问模式和数据热点。

> **Note:**
>
> 目前，**Key Visualizer** 仅在 TiDB Cloud Dedicated 集群中可用。

</CustomContent>

## 查看诊断页面

<CustomContent plan="starter,essential,dedicated">

1. 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Monitoring** > **Diagnosis**。

</CustomContent>

<CustomContent plan="premium">

1. 在组织的 [**TiDB Instances**](https://tidbcloud.com/tidbs) 页面，点击目标实例名称进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织和实例之间切换。

2. 在左侧导航栏，点击 **Monitoring**。

</CustomContent>

## 慢查询

默认情况下，执行时间超过 300 毫秒的 SQL 查询会被视为慢查询。

要在 TiDB <CustomContent plan="starter,essential,dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent> 中查看慢查询，请执行以下步骤：

<CustomContent plan="starter,essential,dedicated">

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **Slow Query** 标签页。

3. 点击列表中的任意慢查询以显示其详细的执行信息。

4. （可选）你可以根据目标时间范围、相关数据库和 SQL 关键字筛选慢查询，也可以限制显示的慢查询数量。

</CustomContent>

<CustomContent plan="premium">

1. 进入 TiDB 实例的概览页面，然后在左侧导航栏点击 **Monitoring** > **Slow Query**。

2. 从列表中选择一条慢查询以查看其详细的执行信息。

3. （可选）你可以根据目标时间范围和 SQL 关键字筛选慢查询，也可以限制显示的慢查询数量。

</CustomContent>

结果以表格形式展示，你可以根据不同的列对结果进行排序。

<CustomContent plan="starter,essential,dedicated">

更多信息，参见 [TiDB Dashboard 中的慢查询](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)。

</CustomContent>

<CustomContent plan="starter,essential,dedicated">

## 语句分析

要使用语句分析，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **SQL Statement** 标签页。

3. 在时间区间选择框中选择要分析的时间段。此时你可以获得该时间段内所有数据库的 SQL 语句执行统计信息。

4. （可选）如果你只关注某些数据库，可以在下一个选择框中选择对应的 schema 以筛选结果。

</CustomContent>

<CustomContent plan="premium">

## SQL 语句

要使用 **SQL Statement** 页面，请执行以下步骤：

1. 进入 TiDB 实例的概览页面，然后在左侧导航栏点击 **Monitoring** > **SQL Statement**。

2. 点击列表中的某条 SQL 语句以查看其详细的执行信息。

3. 在时间区间选择框中选择要分析的时间段。此时你可以获得该时间段内所有数据库的 SQL 语句执行统计信息。

4. （可选）如果你只关注某些数据库，可以在下一个选择框中选择对应的 schema 以筛选结果。

</CustomContent>

结果以表格形式展示，你可以根据不同的列对结果进行排序。

<CustomContent plan="starter,essential,dedicated">

更多信息，参见 [TiDB Dashboard 中的语句执行详情](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)。

## Key Visualizer

> **Note:**
>
> Key Visualizer 仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

要查看关键分析，请执行以下步骤：

1. 进入集群的 [**Diagnosis**](#view-the-diagnosis-page) 页面。

2. 点击 **Key Visualizer** 标签页。

在 **Key Visualizer** 页面上，会显示一个大型热力图，展示访问流量随时间的变化。热力图每个轴的平均值分别显示在下方和右侧。左侧显示表名、索引名及其他相关信息。

更多信息，参见 [Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)。

</CustomContent>