---
title: Top RU
summary: Learn how to use Top RU to identify the SQL statements and database users with the highest Request Unit (RU) consumption in minute-level.
---

# Top RU

**Top RU** ranks SQL statements by their Request Unit (RU) consumption, helping you quickly identify which queries are the primary drivers of your RU usage. When you notice an unexpected RU spike in your instances monitoring, use Top RU to pinpoint the responsible SQL statements and take targeted action.

> **Note:**
>
> Top RU is currently available for TiDB Cloud Premium and partial TiDB Cloud Essential instances for Public Preview, in gradual rollout.

## Product tier comparison

Different product tiers support different Top RU capabilities:

| Feature | Premium | Essential |
|---|---|---|
| **Overview** tab | ✓ | ✓ |
| **Sliced by Users** tab | ✓ | ✓ |
| **Top DB Users (RU)** panel | ✓ | ✓ |
| Top N options | 5, 10, 20, 100 | 5, 10, 20 |
| Data retention | 30 days | 7 days |

## Open Top RU

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to your instance.
2. In the left navigation pane, click **Monitoring** > **Top RU**.

## Analyze RU consumption by SQL

The **Overview** tab shows the top RU-consuming SQL statements across all database users for the selected time range.

### Set filters

Use the filters at the top of the page to narrow down the data:

- **Time range**: Select a preset interval or a custom range.

    Preset options: **Last 15 min**, **30 min**, **1 hour**, **2 hours**, **6 hours**, **12 hours**, **1 day**.

    For custom time ranges:
    - The earliest available start date depends on your data retention: **30 days ago** for Premium instances, **7 days ago** for Essential instances.
    - The maximum window for a single query is **24 hours**.

- **Top N**: Select how many SQL statements to display.
    - Premium: default **10**, options: **5**, **20**, **100**.
    - Essential: default **10**, options: **5**, **20**.

### Read the SQL list

The **Top N SQL list** shows the highest RU-consuming SQL statements for the selected filters:

| Column | Description |
|---|---|
| SQL Statement | Normalized SQL template |
| Total RU | Total RU consumed by this SQL in the selected time range |
| Mean RU | Mean RU consumed by this SQL in the selected time range, total ru/excecutions |
| Share | Percentage of total instance RU consumed by this SQL. The top N SQLs together account for less than 100%; adding the **Others** row gives 100%. |
| Executions | Number of times this SQL was executed in the selected time range |
| Plans | Number of plans this SQL was executed in the selected time range |
| Total latency | Total execution time cost by this SQL in the selected time range |
| Mean latency | Mean execution time cost by this SQL in the selected time range, total latency/excecutions |

> **Note:**
>
> Top RU ranks SQL statements by their **cumulative RU consumption**, including queries that are still executing. This lets you catch ongoing expensive queries before they complete. But for queries that are still executing, the plan is not available.

### View the RU trend

Hover over any SQL statement in the list to highlight its **RU trend line** in the trend chart. The chart shows RU consumption over the selected time range at minute-level intervals, helping you identify when a spike started and whether it is still ongoing.

## Identify RU consumption by user

### Rank by Users panel

The **Overview** tab includes a **Top 3 DB Users (RU)** panel that shows a ranked list of database users by their total RU consumption for the selected time range. Use this to quickly determine whether the RU spike is driven by a specific db user.

### Sliced by Users tab

To drill into a specific db user's SQL statements:

1. Click the **Sliced by Users** tab.
2. In the **User** filter, select the user you want to investigate. Up to 100 users are shown; users beyond 100 are grouped as **Other users**.
3. The **Top N SQL list** and trend chart now reflect only the selected user's queries.

## Drill down into a SQL statement

Click any SQL statement in the **Top N SQL list** to open its detail panel. 

### Execution Summary

| Section | Content |
|---|---|
| SQL Digest | Normalized SQL template id |
| Total RU | Total RU consumed by this SQL in the selected time range |
| Mean RU | Mean RU consumed by this SQL in the selected time range, total ru/excecutions |
| Share | Percentage of total instance RU consumed by this SQL |
| Executions | Number of times this SQL was executed in the selected time range |
| Plans | Number of plans this SQL was executed in the selected time range |
| Total latency | Total execution time cost by this SQL in the selected time range |
| Mean latency | Mean execution time cost by this SQL in the selected time range, total latency/excecutions |

### Execution Plans

The information displayed depends on how many execution plans the SQL has and whether plan data is available.

#### Plans not available

When plan data is not available, the following are not shown: Plan digest, SQL RU Trend by Plan, and Execution Plan. The other fields remain visible.

#### Multiple plans

When the SQL has multiple execution plans, a plan list is shown first:

- Click an **available plan** to expand its full details (same as the single available plan case).
- Clicking an **unavailable plan** does not expand further.

## Typical workflow

The following is a typical workflow for investigating an RU spike:

1. Notice an RU spike in your instance metrics or a triggered alert.
2. Open **Monitoring** > **Top RU** > **Overview** tab and select a time range covering the spike.
3. Identify the SQL statements with the highest Total RU. Hover over each to see its RU trend and identify when the spike started.
4. Check the **Rank by Users** panel to see whether a specific user is driving the spike.
5. If needed, go to the **Sliced by Users** tab, select the user, and focus on their top RU-consuming SQL statements.
6. Click a SQL statement to open its detail panel. Review the execution plan to find optimization opportunities such as missing indexes.
7. Use the **Query Template ID** to cross-reference Slow Query/SQL Statement for additional execution context.
8. Apply optimizations: add indexes, rewrite the SQL, or adjust business logic.
9. Return to Top RU and select a recent time range to confirm that RU consumption has decreased after the optimization.

## Limitations

- **Not equivalent to billing RU**: Top RU values are near-real-time observability data and do not match the billing RU in your TiDB Cloud invoice. Do not use Top RU for billing reconciliation or auditing.
- **TopN grouping**: SQL statements with lower RU may be grouped into **Others** rather than shown individually.
- **Data freshness**: minute-level.
- **Maximum query window**: 24 hours per time range selection.

## FAQ

### What is the difference between Top RU and Top SQL?

[Top SQL](/tidb-cloud/tidb-cloud-clinic.md#monitor-top-sql) ranks SQL statements by CPU time on a specific TiDB or TiKV node and is for Dedicated Tiers. Top RU ranks SQL statements by Request Unit (RU) consumption at the instance level, and supports user-level breakdown.

### Why is there no data in Top RU?

- Make sure the selected time range contains actual SQL workload.
- Refresh the page after running workload for at least 1 min.
- Check [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md) to confirm Top RU is available for your instance version/region.

If the issue persists, contact [TiDB Cloud support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

### Is Top RU the same as billing RU?

No. Top RU shows near-real-time RU statistics for diagnosing high-consumption SQL. For billing and cost management, refer to the billing RU in your TiDB Cloud billing console.
