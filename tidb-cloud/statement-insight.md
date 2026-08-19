---
title: Statement Insight（预览版）
summary: 了解如何使用 Statement Insight 按 DB user、DB、table、SQL type 或 SQL digest 分析历史 RU 消耗、延时和执行次数，并为你的 TiDB Cloud 实例建立 RU 和性能基线。
---

# Statement Insight（预览版）

**Statement Insight** 为你的 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .premium }}} and {{{ .byoc }}}</CustomContent> 实例提供 SQL 资源消耗的多维度分析。它按 **DB User**、**DB**、**Table**、**SQL Type** 或 **SQL Digest** 拆分 Request Unit（RU）消耗、延时和执行次数，并通过排行榜和趋势图让你一目了然地查看主要贡献项。你可以使用 Statement Insight 基于历史数据建立 RU 和性能基线，并定位导致 RU 消耗增加或性能变慢的原因。

Statement Insight 是一个面向历史数据和基线分析的视图。

> **Note:**
>
> Statement Insight 目前处于公开预览阶段，仅适用于 8 月 19 日及之后创建的有限数量的 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .premium }}} and {{{ .byoc }}}</CustomContent> 实例，后续版本将逐步扩大可用范围。如需申请抢先体验，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
> 对于尚未提供 Statement Insight 的实例，你仍可暂时使用 [SQL Statement](/tidb-cloud/tune-performance.md#statement-analysis) 标签页进行语句分析。

## 开始之前 {#before-you-begin}

由于 Statement Insight 仅会在为你的实例启用后才开始收集数据，因此你首次打开该页面时请注意以下事项：

- 不会回填历史数据。你只能看到从该功能在你的实例上激活时开始的数据。
- 可用时间范围会逐日增长。例如，当该功能运行一天后，你将看到大约一天的数据。

## 打开 Statement Insight {#open-statement-insight}

1. 登录 [TiDB Cloud console](https://tidbcloud.com/)，并进入你的 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .premium }}} or {{{ .byoc }}}</CustomContent> 实例。
2. 在左侧导航栏中，点击 **Monitoring** > **Diagnosis**。
3. 在 **Diagnosis** 页面上，点击 **Statement Insight** 标签页。

## 设置筛选条件 {#set-filters}

使用页面顶部的筛选条件缩小数据范围：

- **Time range**：选择预设时间区间或自定义范围。
- **DB User**：按执行 SQL 语句的数据库用户进行筛选。
- **SQL Type**：按 SQL 语句类型进行筛选，例如 `SELECT`、`INSERT` 或 `UPDATE`。
- **Database**：按 SQL 语句所运行的数据库进行筛选。
- **Table**：按 SQL 语句所运行的表进行筛选。
- **Keyword**：按与 SQL digest 文本匹配的关键字进行筛选。

所有筛选条件都可以组合使用，以便将分析范围缩小到你关注的 SQL 语句。

## 分析 RU 消耗、延时和执行次数 {#analyze-ru-consumption-latency-and-execution-counts}

**Top Contributors** 面板按多个维度汇总与你筛选条件匹配的 SQL 语句。对于每个维度，你都可以切换 **Measured by** 控件，以更改排行榜和趋势图所依据的指标：

- **Total RU**：消耗的 RU 总和。
- **Mean RU**：总 RU 除以执行次数。
- **Total latency**：执行延时总和。
- **Mean latency**：总延时除以执行次数。
- **Execution count**：SQL 语句的执行次数。

### 按 DB user、SQL type、SQL digest、DB 和 table 查看主要贡献项 {#top-contributors-by-db-user-sql-type-sql-digest-db-and-table}

对于每个维度（DB User、SQL Type、SQL Digest、DB 或 Table），该面板会显示：

- **Total count**：在所选 SQL 语句中，该维度不同取值的总数。例如，执行所选 SQL 语句的不同 DB user 总数。
- **Top values**：按 **Measured by** 中所选指标排序后的前几项取值。例如，如果 **Measured by** 设置为 **Total RU**，则该面板会显示消耗 RU 最多的 DB user、SQL type、SQL digest、DB 或 Table。

### 趋势图 {#trend-charts}

**Resource Usage Over Time** 趋势图展示了你当前查看的维度下，所选指标随时间变化的情况。

## 限制 {#limitations}

- Statement Insight 适用于历史分析以及 RU 或性能基线建立。由于数据收集和聚合方式不同，页面中显示的 RU 与 TiDB Cloud 账单中报告的 RU 用量并不相同（Statement Insight 显示的是累计 RU 消耗）。请勿使用 Statement Insight 数据进行账单对账。
- 数据新鲜度间隔最长可达 **10 分钟**，与底层采集周期一致。

## FAQ {#faq}

### 为什么 Statement Insight 中没有数据，或者只有很短时间范围的数据？ {#why-is-there-no-data-or-only-a-short-time-range-of-data-in-statement-insight}

Statement Insight 不会回填历史数据。数据会从该功能在你的实例上启用的那一刻开始累积，可用时间范围也会随着时间推移而增长。如果你的实例是最近才启用该功能，这是预期行为，并不表示数据缺失或损坏。

### Statement Insight 和 Top RU 有什么区别？ {#what-is-the-difference-between-statement-insight-and-top-ru}

[Top RU](/tidb-cloud/top-ru.md) 是一个接近实时的工具，用于诊断正在发生的 RU 峰值：它按累计 RU 消耗对 SQL 语句进行排序，并在一个较短且最近的时间窗口内，重点展示 RU 消耗最高的 SQL 语句及其关键字段，包括仍在执行中的语句。

Statement Insight 是一个历史分析工具。它会收集并展示更多数量的 SQL 语句（每个采集间隔最多 3,000 个 SQL digest）以及更详细的字段，并帮助你在更长的时间范围内，按 DB User、SQL Type、SQL Digest、DB 或 Table 维度了解 RU 消耗、延时和执行次数的趋势，从而建立 RU 和性能基线，并识别可持续优化的机会。

### Statement Insight 中显示的 RU 与计费 RU 相同吗？ {#is-the-ru-shown-in-statement-insight-the-same-as-the-billed-ru}

不同。Statement Insight 用于可观测性和优化，而非计费。如需了解计费和成本管理，请参阅你的 TiDB Cloud billing console。