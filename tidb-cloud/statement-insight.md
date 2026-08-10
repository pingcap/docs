---
title: Statement Insight
summary: Learn how to use Statement Insight to analyze historical RU consumption, latency, and execution counts by DB User, SQL Type, or SQL Digest, and to build cost and performance baselines for your TiDB Cloud Premium instance.
---

# Statement Insight

**Statement Insight** provides multi-dimensional analysis of SQL resource consumption for your {{{ .premium }}} instance. It breaks down Request Unit (RU) consumption, latency, and execution counts by **DB User**, **SQL Type**, or **SQL Digest**, with leaderboards and trend charts that surface your top contributors at a glance. Use Statement Insight to establish cost and performance baselines from historical data and pinpoint what is driving RU spend or slowdowns.

Statement Insight is a historical, baseline-oriented view. If you are reacting to a live RU spike and need near-real-time diagnosis, use [Top RU](/tidb-cloud/top-ru.md) instead.

> **Note:**
>
> Statement Insight is in public preview and available only for a limited number of {{{ .premium }}} instances, with broader rollout to {{{ .premium }}} instances planned in a subsequent release. To request early access, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Before you begin

Statement Insight uses a high-fidelity data collection pipeline that is designed to capture 100% of SQL executions and their RU consumption, even under high-concurrency workloads. This avoids the row eviction behavior of the in-memory statement summary tables, where short-lived or high-frequency SQL statements can be dropped before they are recorded.

Because Statement Insight only starts collecting data after it is enabled for your instance, keep the following in mind when you first open the page:

- No historical data is backfilled. You only see data from the time the feature was activated on your instance.
- The available time range grows day by day. For example, you see about one week of data after the feature has been running for a week.

## Open Statement Insight

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to your {{{ .premium }}} instance.
2. In the left navigation pane, click **Monitoring** > **Statement Insight**.

## Set filters

Use the filters at the top of the page to narrow down the data:

- **Time range**: select a preset interval or a custom range.

    - The earliest available start date depends on your data retention: **90 days ago** for {{{ .premium }}} instances.
    - The minimum time granularity for trend charts is **30 minutes**, matching the underlying data collection cycle.

- **DB User**: filter by the database user that executed the SQL statements. In the current preview, this filter supports selecting a single user; support for selecting multiple users is planned for a future release.
- **SQL Type**: filter by SQL statement type, such as `SELECT`, `INSERT`, or `UPDATE`.
- **Database**: filter by the database that the SQL statements ran against.
- **SQL Digest**: filter by a specific SQL digest.

All filters can be combined to narrow the analysis to the SQL statements you care about.

## Analyze RU consumption, latency, and execution counts

The **SQL Overview** panel summarizes the SQL statements that match your filters, sliced by **DB User**, **SQL Type**, and **SQL Digest**. For each dimension, you can switch the **Measured by** control to change which metric drives both the leaderboard and the trend chart:

- **Total RU**: the sum of RU consumed.
- **Mean RU**: total RU divided by execution count.
- **Total latency**: the sum of execution latency.
- **Mean latency**: total latency divided by execution count.
- **Execution count**: the number of times the SQL statements were executed.

### DB Users, SQL Types, and SQL Digests summary

For each dimension (DB User, SQL Type, or SQL Digest), the panel shows:

- **Total count**: the total number of distinct values for the dimension among the selected SQL statements. For example, the total number of distinct DB users that ran the selected SQL statements.
- **Top 3**: the top three values ranked by the metric selected in **Measured by**. For example, if **Measured by** is set to **Total RU**, the panel shows the top three DB users, SQL types, or SQL digests that consumed the most RU.

### Trend charts

The trend chart shows how the selected metric changes over time for the dimension you are viewing. To keep the chart readable, only the top 10 values (by the selected metric) are shown as individual lines. All remaining values are aggregated into a single **Others** series.

## Limitations

- Statement Insight is intended for historical analysis and cost or performance baselining. The displayed RU might differ slightly from the RU usage reported on your TiDB Cloud invoice due to differences in collection and aggregation. Do not use Statement Insight data for billing reconciliation.
- Data freshness is up to **30 minutes**, matching the underlying collection cycle.
- The **DB User** filter currently supports selecting only one user at a time.
- Only the top 10 values per dimension are shown as individual trend lines. The rest are aggregated into **Others**.

## FAQ

### Why is there no data, or only a short time range of data, in Statement Insight?

Statement Insight does not backfill historical data. Data starts accumulating from the moment the feature is enabled on your instance, and the available time range grows over time. If you enabled the feature recently, this is expected behavior, not a sign of missing or broken data.

### What is the difference between Statement Insight and Top RU?

[Top RU](/tidb-cloud/top-ru.md) is a near-real-time tool for diagnosing an ongoing RU spike: it ranks SQL statements by cumulative RU consumption, including statements that are still executing, over a short, recent time window.

Statement Insight is a historical analysis tool. It helps you understand RU consumption, latency, and execution count trends over a longer time range, broken down by DB User, SQL Type, or SQL Digest, so that you can establish cost and performance baselines and identify sustained optimization opportunities.

### Is the RU shown in Statement Insight the same as the billed RU?

No. Statement Insight is intended for observability and optimization, not billing. For billing and cost management, refer to the RU usage in your TiDB Cloud billing console.
