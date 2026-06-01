---
title: Top RU
summary: Learn how to use Top RU to identify the SQL statements and database users with the highest Request Unit (RU) consumption in real time.
---

# Top RU

**Top RU** ranks SQL statements by their Request Unit (RU) consumption, helping you quickly identify which queries are the primary drivers of your RU usage. When you notice an unexpected RU spike in your cluster monitoring or billing, use Top RU to pinpoint the responsible SQL statements and take targeted action.

> **Note:**
>
> Top RU is currently available for TiDB Cloud Premium and TiDB Cloud Essential clusters.

## Product tier comparison

Different product tiers support different Top RU capabilities:

| Feature | Premium | Essential |
|---|---|---|
| **Overview** tab | ✓ | ✓ |
| **Sliced by Users** tab | ✓ | ✗ |
| **Rank by Users** panel | ✓ | ✗ |
| **User** column in SQL list | ✓ | ✗ |
| Top N (default) | 10 | 5 |
| Top N options | 20, 50, 100 | 10, 20 |
| Data retention | 30 days | 7 days |

## Open Top RU

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to your cluster.
2. In the left navigation, click **Monitoring** > **Top RU**.

## Analyze RU consumption by SQL

The **Overview** tab shows the top RU-consuming SQL statements across all database users for the selected time range.

### Set filters

Use the filters at the top of the page to narrow down the data:

- **Time range**: Select a preset interval or a custom range.

    Preset options: **Last 5 min**, **15 min**, **30 min**, **1 hour**, **6 hours**, **12 hours**, **1 day**.

    For custom time ranges:
    - The earliest available start date depends on your data retention: **30 days ago** for Premium clusters, **7 days ago** for Essential clusters.
    - The maximum window for a single query is **24 hours**.

- **Top N**: Select how many SQL statements to display.
    - Premium: default **10**, options: **20**, **50**, **100**.
    - Essential: default **5**, options: **10**, **20**.

### Read the SQL list

The **Top N SQL list** shows the highest RU-consuming SQL statements for the selected filters:

| Column | Description |
|---|---|
| SQL Statement | Normalized SQL template |
| Total RU | Total RU consumed by this SQL in the selected time range |
| RU Share % | Percentage of total cluster RU consumed by this SQL. The top N SQLs together account for less than 100%; adding the **Others** row gives 100%. |
| Execution Count | Number of times this SQL was executed in the selected time range |
| User | Database user(s) that ran this SQL (Premium only). A single SQL digest may be executed by multiple users. |

> **Note:**
>
> Top RU ranks SQL statements by their **cumulative RU consumption**, including queries that are still executing. This lets you catch ongoing expensive queries before they complete.

### View the RU trend

Hover over any SQL statement in the list to highlight its **RU trend line** in the trend chart. The chart shows RU consumption over the selected time range at 15-second intervals, helping you identify when a spike started and whether it is still ongoing.

## Identify RU consumption by user (Premium only)

### Rank by Users panel

The **Overview** tab includes a **Rank by Users** panel that shows a ranked list of database users by their total RU consumption for the selected time range. Use this to quickly determine whether the RU spike is driven by a specific user or application.

### Sliced by Users tab

To drill into a specific user's SQL statements:

1. Click the **Sliced by Users** tab.
2. In the **User** filter, select the user you want to investigate. Up to 100 users are shown; users beyond 100 are grouped as **Other users**.
3. The **Top N SQL list** and trend chart now reflect only the selected user's queries.

## Drill down into a SQL statement

Click any SQL statement in the **Top N SQL list** to open its detail panel. The information displayed depends on how many execution plans the SQL has and whether plan data is available.

### Single plan (plan available)

| Section | Content |
|---|---|
| SQL Statement Details | RU, Plan code, Call/sec, Latency/call, Execution count |
| SQL RU Trend by Plan | RU consumption trend for this execution plan |
| Statement Template | The SQL template text |
| Query Template ID | Use this to locate corresponding entries in [Slow Query logs](/tidb-cloud/tune-performance.md) |
| Plan Template ID | Use this to locate execution plan records |
| Execution Plan | The full execution plan, useful for identifying full table scans caused by missing indexes |

### Single plan (plan not available)

When plan data is not available, the following are not shown: Plan code, SQL RU Trend by Plan, Plan Template ID, and Execution Plan. The other fields remain visible.

### Multiple plans

When the SQL has multiple execution plans, a plan list is shown first:

- Click an **available plan** to expand its full details (same as the single available plan case).
- Clicking an **unavailable plan** does not expand further.

## Typical workflow

The following is a typical workflow for investigating an RU spike:

1. Notice an RU spike in your cluster metrics or a triggered alert.
2. Open **Monitoring** > **Top RU** > **Overview** tab and select a time range covering the spike.
3. Identify the SQL statements with the highest Total RU. Hover over each to see its RU trend and identify when the spike started.
4. **(Premium)** Check the **Rank by Users** panel to see whether a specific user is driving the spike.
5. **(Premium)** If needed, go to the **Sliced by Users** tab, select the user, and focus on their top RU-consuming SQL statements.
6. Click a SQL statement to open its detail panel. Review the execution plan to find optimization opportunities such as missing indexes.
7. Use the **Query Template ID** to cross-reference slow query logs for additional execution context.
8. Apply optimizations: add indexes, rewrite the SQL, or adjust business logic.
9. Return to Top RU and select a recent time range to confirm that RU consumption has decreased after the optimization.

## Limitations

- **Not equivalent to billing RU**: Top RU values are near-real-time observability data and do not match the billing RU in your TiDB Cloud invoice. Do not use Top RU for billing reconciliation or auditing.
- **TopN grouping**: SQL statements with lower RU may be grouped into **Others** rather than shown individually.
- **Data freshness**: 15 seconds.
- **Maximum query window**: 24 hours per time range selection.
- **Essential limitations**: The Sliced by Users tab and Rank by Users panel are not available for Essential clusters.

## FAQ

### What is the difference between Top RU and Top SQL?

[Top SQL](/tidb-cloud/tidb-cloud-clinic.md#monitor-top-sql) ranks SQL statements by CPU time on a specific TiDB or TiKV node. Top RU ranks SQL statements by Request Unit (RU) consumption at the cluster level, and supports user-level breakdown (Premium only).

### Why is there no data in Top RU?

- Make sure the selected time range contains actual SQL workload.
- Refresh the page after running workload for at least 15 seconds.
- Check [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md) to confirm Top RU is available for your cluster version.

If the issue persists, contact [TiDB Cloud support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

### Is Top RU the same as billing RU?

No. Top RU shows near-real-time RU statistics for diagnosing high-consumption SQL. For billing and cost management, refer to the billing RU metrics in your TiDB Cloud billing console.
