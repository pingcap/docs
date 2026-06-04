---
title: Top RU
summary: 了解如何使用 Top RU 以一分钟粒度识别 Request Unit (RU) 消耗最高的 SQL 语句和数据库用户。
---

# Top RU

**Top RU** 按 Request Unit (RU) 消耗对 SQL 语句进行排名，帮助你快速识别哪些查询推动了 RU 使用量。当你在 {{{ .essential }}} 或 {{{ .premium }}} 实例指标中发现异常的 RU 峰值时，可以使用 Top RU 找出相关的 SQL 语句，并采取有针对性的措施。

> **Note:**
>
> - Top RU 以公开预览版形式提供给 {{{ .premium }}} 实例。
> - Top RU 正在分阶段推出，目前已在部分区域的 {{{ .essential }}} 实例中可用。

## 产品套餐对比 {#product-plan-comparison}

Top RU 的功能因 TiDB Cloud 套餐而异：

| Feature | {{{ .premium }}} | {{{ .essential }}} |
|---|---|---|
| **Overview** tab | Supported | Supported |
| **Sliced by Users** tab | Supported | Supported |
| **Top DB Users (RU)** panel | Supported | Supported |
| Top N options | 5, 10, 20, 100 | 5, 10, 20 |
| Data retention | 30 days | 7 days |

## 打开 Top RU {#open-top-ru}

1. 登录 [TiDB Cloud console](https://tidbcloud.com/)，然后进入你的 {{{ .essential }}} 或 {{{ .premium }}} 实例。
2. 在左侧导航栏中，点击 **Monitoring** > **Top RU**。

## 按 SQL 分析 RU 消耗 {#analyze-ru-consumption-by-sql}

**Overview** 标签页会显示所选时间范围内所有数据库用户中 RU 消耗最高的 SQL 语句。

### 设置筛选条件 {#set-filters}

使用页面顶部的筛选条件来缩小数据范围。

- **Time range**：选择预设时间区间或自定义时间范围。

    预设选项：**Last 15 min**、**30 min**、**1 hour**、**2 hours**、**6 hours**、**12 hours** 和 **1 day**。

    对于自定义时间范围：
    
    - 最早可选的开始日期取决于你的数据保留期：对于 {{{ .premium }}} 实例为 **30 days ago**，对于 {{{ .essential }}} 实例为 **7 days ago**。
    - 单次查询的最大时间窗口为 **24 hours**。

- **Top N**：选择要显示的 SQL 语句数量。

    - {{{ .premium }}} 实例：默认值为 **10**。可选项为 **5**、**20** 和 **100**。
    - {{{ .essential }}} 实例：默认值为 **10**。可选项为 **5** 和 **20**。

### 查看 SQL 列表 {#read-the-sql-list}

**Top N SQL list** 会显示符合所选筛选条件的 RU 消耗最高的 SQL 语句：

| Column | Description |
|---|---|
| SQL Statement | 归一化后的 SQL 模板 |
| Total RU | 该 SQL 语句在所选时间范围内消耗的总 RU |
| Mean RU | 该 SQL 语句在所选时间范围内消耗的平均 RU。该值等于总 RU 除以执行次数。 |
| Share | 该 SQL 语句在所选 {{{ .essential }}} 或 {{{ .premium }}} 实例中消耗的总 RU 占比。前 N 条 SQL 语句的占比之和可能不会达到 100%。将 **Others** 行计算在内后，才能覆盖剩余的 RU 消耗并达到 100%。 |
| Executions | 该 SQL 语句在所选时间范围内的执行次数 |
| Plans | 该 SQL 语句在所选时间范围内的执行计划数量。 |
| Total latency | 该 SQL 语句在所选时间范围内消耗的总执行时间 |
| Mean latency | 该 SQL 语句在所选时间范围内消耗的平均执行时间。该值等于总执行时间除以执行次数。 |

> **Note:**
>
> Top RU 按 SQL 语句的**累计 RU 消耗**进行排名，其中包括仍在执行中的查询。这使你能够在高开销查询完成之前就发现它们。对于仍在执行中的查询，执行计划不可用。

### 查看 RU 趋势 {#view-the-ru-trend}

将鼠标悬停在列表中的某条 SQL 语句上，可以在趋势图中高亮显示其 **RU trend line**。该图表以一分钟间隔展示所选时间范围内的 RU 消耗，帮助你识别峰值从何时开始，以及峰值是否仍在持续。

## 按用户识别 RU 消耗 {#identify-ru-consumption-by-user}

### Rank by Users 面板 {#rank-by-users-panel}

**Overview** 标签页包含一个 **Top 3 DB Users (RU)** 面板，按所选时间范围内的总 RU 消耗对数据库用户进行排名。你可以使用该面板判断是否是某个特定数据库用户导致了 RU 峰值。

### Sliced by Users 标签页 {#sliced-by-users-tab}

要进一步查看某个特定数据库用户的 SQL 语句，请执行以下操作：

1. 点击 **Sliced by Users** 标签页。
2. 在 **User** 筛选器中，选择你要调查的用户。该筛选器最多显示 100 个用户，超出的用户会归类为 **Other users**。
3. **Top N SQL list** 和趋势图将只显示所选用户的查询。

## 深入查看某条 SQL 语句 {#drill-down-into-a-sql-statement}

点击 **Top N SQL list** 中的某条 SQL 语句，可以打开其详情面板。

### 执行摘要 {#execution-summary}

| Section | Content |
|---|---|
| SQL Digest | 归一化后的 SQL 模板 ID |
| Total RU | 该 SQL 在所选时间范围内消耗的总 RU |
| Mean RU | 该 SQL 语句在所选时间范围内消耗的平均 RU。该值等于总 RU 除以执行次数。 |
| Share | 该 SQL 语句在所选 {{{ .essential }}} 或 {{{ .premium }}} 实例中消耗的总 RU 占比。 |
| Executions | 该 SQL 语句在所选时间范围内的执行次数。 |
| Plans | 该 SQL 语句在所选时间范围内的执行计划数量。 |
| Total latency | 该 SQL 语句在所选时间范围内消耗的总执行时间。 |
| Mean latency | 该 SQL 语句在所选时间范围内消耗的平均执行时间。该值等于总执行时间除以执行次数。 |

### 执行计划 {#execution-plans}

Top RU 会根据 SQL 语句拥有的执行计划数量以及计划数据是否可用来显示信息。

#### 执行计划不可用 {#plans-not-available}

当计划数据不可用时，Top RU 不会显示 **Plan digest**、**SQL RU Trend by Plan** 或 **Execution Plan**。其他字段仍然可见。

#### 多个执行计划 {#multiple-plans}

当 SQL 存在多个执行计划时，面板会先显示一个计划列表：

- 点击可用的计划以展开其完整详情。
- 点击不可用的计划以查看其摘要。不可用的计划无法展开。

## 典型工作流 {#typical-workflow}

你可以使用以下工作流来调查 RU 峰值：

1. 在 {{{ .essential }}} 或 {{{ .premium }}} 实例指标中发现 RU 峰值，或者收到触发的告警。
2. 前往 **Monitoring** > **Top RU**，点击 **Overview** 标签页，并选择覆盖该峰值的时间范围。
3. 找出 **Total RU** 最高的 SQL 语句。将鼠标悬停在每条 SQL 语句上查看其 RU 趋势，并识别峰值开始的时间。
4. 检查 **Rank by Users** 面板，查看是否是某个特定用户导致了峰值。
5. 如有需要，前往 **Sliced by Users** 标签页，选择该用户，并重点查看其 RU 消耗最高的 SQL 语句。
6. 点击某条 SQL 语句以打开其详情面板。查看执行计划，寻找优化机会，例如缺失索引。
7. 使用 **Query Template ID** 与 Slow Query 或 SQL Statement 进行交叉比对，以获取更多执行上下文。
8. 应用优化措施，例如添加索引、重写 SQL 或调整业务逻辑。
9. 返回 **Top RU** 页面，并选择最近的时间范围，以确认 RU 消耗是否已经下降。

## 限制 {#limitations}

- **不等同于计费 RU**：Top RU 数据用于近实时可观测性，可能与 TiDB Cloud 账单中报告的 RU 使用量不同。请勿将 Top RU 数据用于计费对账或审计。
- **Top N 聚合**：只有 RU 消耗最高的 SQL 语句会被单独显示。RU 消耗较低的 SQL 语句会被聚合到 **Others** 类别中。
- **数据新鲜度**：数据以分钟级粒度更新。
- **最大查询窗口**：一次最多可以查询 24 小时的数据。

## FAQ {#faq}

### Top RU 和 Top SQL 有什么区别？ {#what-is-the-difference-between-top-ru-and-top-sql}

[Top SQL](/tidb-cloud/tidb-cloud-clinic.md#monitor-top-sql) 按特定 TiDB 或 TiKV 节点上的 CPU 时间对 SQL 语句进行排名。它适用于 TiDB Cloud Dedicated 集群。

Top RU 按实例级别的 Request Unit (RU) 消耗对 SQL 语句进行排名，并支持按用户维度拆分。它适用于 {{{ .premium }}} 实例和 {{{ .essential }}} 实例。

### 为什么 Top RU 中没有数据？ {#why-is-there-no-data-in-top-ru}

- 确保所选时间范围内存在实际的 SQL 工作负载。
- 在运行工作负载至少 1 分钟后刷新页面。
- 查看 [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md)，确认你的 {{{ .essential }}} 或 {{{ .premium }}} 实例版本和区域支持 Top RU。

如果问题仍然存在，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

### Top RU 是否等同于计费 RU？ {#is-top-ru-the-same-as-billing-ru}

不是。Top RU 显示的是用于诊断高消耗 SQL 的近实时 RU 统计信息。对于计费和成本管理，请参考 TiDB Cloud 计费控制台中的 billing RU。

### 指标中的 RU 使用量与 Top RU 有什么区别？ {#what-is-the-difference-between-the-ru-usage-in-metrics-and-top-ru}

- RU/s 指标显示的是整个实例级别 1 分钟平均 RU 速率（RU/s）。
- Top RU 显示的是所选时间范围内每条 SQL 语句的累计 RU（RU/s × duration），帮助你识别哪些 SQL 语句总体上消耗了最多资源。