---
title: Top RU
summary: Learn how to use Top RU to identify the SQL statements and database users with the highest Request Unit (RU) consumption at one-minute granularity.
---

# Top RU

**Top RU** ranks SQL statements by their Request Unit (RU) consumption, helping you quickly identify which queries drive your RU usage. When you notice an unexpected RU spike in your {{{ .essential }}} or {{{ .premium }}} instance metrics, use Top RU to identify the responsible SQL statements and take targeted action.

> **Note:**
>
> - Top RU is available in public preview for {{{ .premium }}} instances.
> - Top RU is available for {{{ .essential }}} instances in selected regions during a phased rollout.

## Product plan comparison

Top RU capabilities vary by TiDB Cloud plan:

| Feature | {{{ .premium }}} | {{{ .essential }}} |
|---|---|---|
| **Overview** tab | Supported | Supported |
| **Sliced by Users** tab | Supported | Supported |
| **Top DB Users (RU)** panel | Supported | Supported |
| Top N options | 5, 10, 20, 100 | 5, 10, 20 |
| Data retention | 30 days | 7 days |

## Open Top RU

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to your {{{ .essential }}} or {{{ .premium }}} instance.
2. In the left navigation pane, click **Monitoring** > **Top RU**.

## Analyze RU consumption by SQL

The **Overview** tab shows the top RU-consuming SQL statements across all database users for the selected time range.

### Set filters

Use the filters at the top of the page to narrow down the data.

- **Time range**: select a preset interval or a custom range.

    Preset options: **Last 15 min**, **30 min**, **1 hour**, **2 hours**, **6 hours**, **12 hours**, and **1 day**.

    For custom time ranges:
    
    - The earliest available start date depends on your data retention: **30 days ago** for {{{ .premium }}} instances, and **7 days ago** for {{{ .essential }}} instances.
    - The maximum window for a single query is **24 hours**.

- **Top N**: select how many SQL statements to display.

    - {{{ .premium }}} instance: **10** by default. Options: **5**, **20**, and **100**.
    - {{{ .essential }}} instance: **10** by default. Options: **5** and **20**.

### Read the SQL list

The **Top N SQL list** shows the highest RU-consuming SQL statements for the selected filters:

| Column | Description |
|---|---|
| SQL Statement | Normalized SQL template |
| Total RU | Total RU consumed by this SQL statement in the selected time range |
| Mean RU | Mean RU consumed by this SQL statement in the selected time range. This value equals total RU divided by executions. |
| Share | Percentage of total RU consumed by this SQL statement in the selected {{{ .essential }}} or {{{ .premium }}} instance. The top N SQL statements might not add up to 100%. Include the **Others** row to account for the remaining RU consumption and reach 100%. |
| Executions | Number of times this SQL statement was executed in the selected time range |
| Plans | Number of execution plans for this SQL statement in the selected time range. |
| Total latency | Total execution time consumed by this SQL statement in the selected time range |
| Mean latency | Mean execution time consumed by this SQL statement in the selected time range. This value equals total latency divided by executions. |

> **Note:**
>
> Top RU ranks SQL statements by their **cumulative RU consumption**, including queries that are still executing. This lets you detect expensive queries before they complete. For queries that are still executing, the execution plan is not available.

### View the RU trend

Hover over a SQL statement in the list to highlight its **RU trend line** in the trend chart. The chart shows RU consumption over the selected time range at one-minute intervals, helping you identify when a spike started and whether the spike is still ongoing.

## Identify RU consumption by user

### Rank by Users panel

The **Overview** tab includes a **Top 3 DB Users (RU)** panel that shows a ranked list of database users by their total RU consumption for the selected time range. Use this panel to determine whether a specific database user drives the RU spike.

### Sliced by Users tab

To drill into a specific database user's SQL statements:

1. Click the **Sliced by Users** tab.
2. In the **User** filter, select the user you want to investigate. The filter displays up to 100 users and groups any additional users as **Other users**.
3. The **Top N SQL list** and trend chart show only the selected user's queries.

## Drill down into a SQL statement

Click a SQL statement in the **Top N SQL list** to open its detail panel.

### Execution summary

| Section | Content |
|---|---|
| SQL Digest | Normalized SQL template ID |
| Total RU | Total RU consumed by this SQL in the selected time range |
| Mean RU | Mean RU consumed by this SQL statement in the selected time range. This value equals total RU divided by executions. |
| Share | Percentage of total RU consumed by this SQL statement in the selected {{{ .essential }}} or {{{ .premium }}} instance. |
| Executions | Number of times this SQL statement was executed in the selected time range. |
| Plans | Number of execution plans for this SQL statement in the selected time range. |
| Total latency | Total execution time consumed by this SQL statement in the selected time range. |
| Mean latency | Mean execution time consumed by this SQL statement in the selected time range. This value equals total latency divided by executions. |

### Execution plans

Top RU displays information based on how many execution plans the SQL statement has and whether plan data is available.

#### Plans not available

When plan data is not available, Top RU does not show **Plan digest**, **SQL RU Trend by Plan**, or **Execution Plan**. The other fields remain visible.

#### Multiple plans

When the SQL has multiple execution plans, the panel displays a plan list first:

- Click an available plan to expand its full details.
- Click an unavailable plan to view its summary. Unavailable plans do not expand.

## Typical workflow

Use the following workflow to investigate an RU spike:

1. Notice an RU spike in your {{{ .essential }}} or {{{ .premium }}} instance metrics or a triggered alert.
2. Go to **Monitoring** > **Top RU**, click the **Overview** tab, and select a time range covering the spike.
3. Identify the SQL statements with the highest **Total RU**. Hover over each SQL statement to see its RU trend and identify when the spike started.
4. Check the **Rank by Users** panel to see whether a specific user is driving the spike.
5. If needed, go to the **Sliced by Users** tab, select the user, and focus on their top RU-consuming SQL statements.
6. Click a SQL statement to open its detail panel. Review the execution plan to find optimization opportunities such as missing indexes.
7. Use the **Query Template ID** to cross-reference Slow Query or SQL Statement for additional execution context.
8. Apply optimizations, such as adding indexes, rewriting the SQL, or adjusting business logic.
9. Return to the **Top RU** page and select a recent time range to confirm that RU consumption has decreased.

## Limitations

- **Not equivalent to billing RU**: Top RU data is intended for near-real-time observability and might differ from the RU usage reported on your TiDB Cloud invoice. Do not use Top RU data for billing reconciliation or auditing.
- **Top N aggregation**: Only the highest RU-consuming SQL statements are displayed individually. SQL statements with lower RU consumption are aggregated into the **Others** category.
- **Data freshness**: Data is updated at minute-level granularity.
- **Maximum query window**: You can query up to 24 hours of data at a time.

## FAQ

### What is the difference between Top RU and Top SQL?

[Top SQL](/tidb-cloud/tidb-cloud-clinic.md#monitor-top-sql) ranks SQL statements by CPU time on a specific TiDB or TiKV node. It applies to TiDB Cloud Dedicated clusters.

Top RU ranks SQL statements by Request Unit (RU) consumption at the instance level and supports user-level breakdown. It applies to {{{ .premium }}} instances and {{{ .essential }}} instances.

### Why is there no data in Top RU?

- Make sure the selected time range contains actual SQL workload.
- Refresh the page after running a workload for at least 1 minute.
- Check [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md) to confirm that Top RU is available for your {{{ .essential }}} or {{{ .premium }}} instance version and region.

If the issue persists, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

### Is Top RU the same as billing RU?

No. Top RU shows near-real-time RU statistics for diagnosing high-consumption SQL. For billing and cost management, refer to the billing RU in your TiDB Cloud billing console.

### What is the difference between the RU usage in metrics and Top RU?

- The RU/s metric shows the 1-minute average RU rate (RU/s) at overall instance level.
- Top RU shows cumulative RU per SQL statement (RU/s × duration) over the selected time range, helping you identify which SQL statements consum the most resources in total.
