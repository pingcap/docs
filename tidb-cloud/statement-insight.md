---
title: Statement Insight
summary: Learn how to use Statement Insight to analyze historical RU consumption, latency, and execution counts by DB User, SQL Type, or SQL Digest, and to build RU and performance baselines for your TiDB Cloud Premium instances.
---

# Statement Insight

**Statement Insight** provides multi-dimensional analysis of SQL resource consumption for your {{{ .premium }}}, {{{ .byoc }}}, {{{ .essential }}} instance. It breaks down Request Unit (RU) consumption, latency, and execution counts by **DB User**, **DB**, **Table**, **SQL Type**, or **SQL Digest**, with leaderboards and trend charts that surface your top contributors at a glance. Use Statement Insight to establish RU and performance baselines from historical data and pinpoint what is driving RU consumptions or slowdowns.

Statement Insight is a historical, baseline-oriented view. 

> **Note:**
>
> Statement Insight is in public preview and available only for a limited number of {{{ .premium }}}, {{{ .byoc }}}, {{{ .essential }}} instances, with broader rollout planned in a subsequent release. To request early access, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Before you begin

Because Statement Insight only starts collecting data after it is enabled for your instance, keep the following in mind when you first open the page:

- No historical data is backfilled. You only see data from the time the feature was activated on your instance.
- The available time range grows day by day. For example, you see about one day of data after the feature has been running for a day.

## Open Statement Insight

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to your {{{ .premium }}}, {{{ .byoc }}}, {{{ .essential }}} instance.
2. In the left navigation pane, click **Monitoring** > **Diagnosis**.
3. On the **Diagnosis** page, click the **Statement Insight** tab.

## Set filters

Use the filters at the top of the page to narrow down the data:

- **Time range**: select a preset interval or a custom range.
- **DB User**: filter by the database user that executed the SQL statements. 
- **SQL Type**: filter by SQL statement type, such as `SELECT`, `INSERT`, or `UPDATE`.
- **Database**: filter by the database that the SQL statements ran against.
- **Table**: filter by the table that the SQL statements ran against.
- **SQL Digest**: filter by a specific SQL digest.

All filters can be combined to narrow the analysis to the SQL statements you care about.

## Analyze RU consumption, latency, and execution counts

The **Top Contributors** panel summarizes the SQL statements that match your filters, sliced by multiple dimensions. For each dimension, you can switch the **Measured by** control to change which metric drives both the leaderboard and the trend chart:

- **Total RU**: the sum of RU consumed.
- **Mean RU**: total RU divided by execution count.
- **Total latency**: the sum of execution latency.
- **Mean latency**: total latency divided by execution count.
- **Execution count**: the number of times the SQL statements were executed.

### Top Contributors of DB Users, SQL Types, SQL Digests, DBs and Tables

For each dimension (DB User, SQL Type, SQL Digest, DB or Table), the panel shows:

- **Total count**: the total number of distinct values for the dimension among the selected SQL statements. For example, the total number of distinct DB users that ran the selected SQL statements.
- **Top values**: the top values ranked by the metric selected in **Measured by**. For example, if **Measured by** is set to **Total RU**, the panel shows the top DB users, SQL types, SQL digests, DBs or Tables that consumed the most RU.

### Trend charts

The trend chart shows how the selected metric changes over time for the dimension you are viewing.

## Limitations

- Statement Insight is intended for historical analysis and RU or performance baselining. The displayed RU might differ slightly from the RU usage reported on your TiDB Cloud invoice due to differences in collection and aggregation. Do not use Statement Insight data for billing reconciliation.
- Data freshness is up to **10 minutes**, matching the underlying collection cycle.

## FAQ

### Why is there no data, or only a short time range of data, in Statement Insight?

Statement Insight does not backfill historical data. Data starts accumulating from the moment the feature is enabled on your instance, and the available time range grows over time. If you enabled the feature recently, this is expected behavior, not a sign of missing or broken data.

### What is the difference between Statement Insight and Top RU?

[Top RU](/tidb-cloud/top-ru.md) is a near-real-time tool for diagnosing an ongoing RU spike: it ranks SQL statements by cumulative RU consumption, including statements that are still executing, over a short, recent time window.

Statement Insight is a historical analysis tool. It helps you understand RU consumption, latency, and execution count trends over a longer time range and brings more detailed fields, broken down by DB User, SQL Type, SQL Digest, DB or Table, so that you can establish RU and performance baselines and identify sustained optimization opportunities.

### Is the RU shown in Statement Insight the same as the billed RU?

No. Statement Insight is intended for observability and optimization, not billing. For billing and cost management, refer to your TiDB Cloud billing console.
