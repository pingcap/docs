---
title: TopRU page in TiDB Cloud Clinic
summary: Learn how to use TopRU in TiDB Cloud Clinic to identify SQL statements and database users with high RU consumption.
---

# TopRU page in TiDB Cloud Clinic

TopRU is an SQL observability feature in TiDB Cloud Clinic. It ranks SQL workloads by request unit (RU) consumption to help you quickly identify SQL statements with high resource usage.

TopRU reuses the Top SQL collection and reporting pipeline, but extends the core metric from CPU to RU, and aggregates records by `(user, sql_digest, plan_digest)`. This helps you identify both high-cost SQL statements and the database users who continuously consume RU.

TopRU and Top SQL can coexist. Enabling TopRU does not change the existing CPU semantics of Top SQL.

## Feature overview

TopRU answers the following questions:

- Which SQL statements continuously consume high RU?
- Is an RU spike in a time range caused by a small set of users or SQL statements?
- Why is resource consumption high even when CPU usage is not high?

TopRU data comes from runtime RU statistics in SQL execution, so it can reflect near-real-time resource trends. To control overhead, TopRU applies `TopN` aggregation to users and SQL statements, and merges low-priority items instead of outputting a full per-statement stream.

## Recommended scenarios

TopRU is useful in the following scenarios:

- You need to locate high RU-consuming SQL in clusters with [Resource Control](/tidb-resource-control-ru-groups.md) enabled.
- CPU usage is not the main bottleneck, but overall resource consumption is still high.
- You need user-level visibility to answer "who is consuming RU" instead of only "which SQL consumes CPU".
- You need to quickly identify major RU hotspots under high load and prioritize SQL optimization, resource group governance, or workload throttling.

TopRU is not for the following scenarios:

- Billing, reconciliation, or precise auditing.
- Replacing slow query logs, `statements_summary`, or daily offline statistics from resource groups.

## Prerequisites

Before using TopRU, make sure that all of the following conditions are met:

- You can access [TiDB Cloud Clinic](https://clinic.pingcap.com/).
- Your cluster has [Resource Control](/tidb-resource-control-ru-groups.md) enabled.
- Your cluster version supports TopRU in TiDB Cloud Clinic. For rollout updates, see [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md). If TopRU is still unavailable in your cluster, contact support.

> **Note:**
>
> TopRU is available in TiDB Cloud Clinic for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Page views

The TopRU page currently includes the following views:

- **Overview (instance-level)**: inspect top RU-consuming SQL from the cluster instance perspective.
- **Sliced by Users (DB user-level)**: inspect RU consumption grouped by database user.

![TopRU overview view](/media/tidb-cloud/top-ru-instance-view.png)

![TopRU overview detail](/media/tidb-cloud/top-ru-instance-detail.png)

![TopRU sliced by users view](/media/tidb-cloud/top-ru-db-user-view.png)

![TopRU sliced by users detail](/media/tidb-cloud/top-ru-db-user-detail.png)

A common diagnosis path is to locate RU hotspots in the **Overview** view first, and then switch to the **Sliced by Users** view to identify whether specific users dominate RU consumption.

## Use TopRU

A common workflow for TopRU is as follows:

1. Open the TopRU page and select a time range.
2. In the **Overview** view, identify top RU-consuming SQL statements and hotspot periods.
3. Switch to the **Sliced by Users** view to verify whether RU is concentrated on a small set of users.
4. Open SQL details and combine `sql_digest` / `plan_digest` with execution count and execution duration to prioritize optimization.
5. Continue analysis with Top SQL, slow query data, and execution plans.

TopRU trends usually correlate with RU and QPS trends, which you can use for cross-checking:

![TopRU vs RU trend](/media/tidb-cloud/top-ru-vs-ru-trend.png)

![TopRU vs QPS trend](/media/tidb-cloud/top-ru-vs-qps-trend.png)

## TopRU observation dimensions

TopRU uses `(user, sql_digest, plan_digest)` as the aggregation key. Each time point usually includes the following fields:

- `Total RU`: total RU consumption in the interval.
- `Exec Count`: number of executions in the interval.
- `Exec Duration`: aggregated execution duration in the interval.

TopRU shows time-series data in the selected time range. The TiDB Cloud Clinic UI automatically adjusts the displayed time buckets based on the selected range.

To limit memory and network overhead, TopRU applies `TopN` aggregation to users and SQL statements. High-priority items are kept as individual records, while low-priority items are merged.

## Limitations and considerations

- RU values in TopRU are runtime `RUDetails` observability values and are not equivalent to billing RU.
- If Resource Control is not enabled, TopRU cannot generate effective RU data.
- To control collection and reporting overhead, TopRU applies `TopN` compression and does not retain all low-RU items.

> **Note:**
>
> TopRU is for real-time hotspot diagnosis, not for billing settlement, precise reconciliation, or long-term offline auditing.

## FAQ

### What is the difference between TopRU and Top SQL?

Top SQL is CPU-focused. TopRU is RU-focused and adds user-level visibility. TopRU reuses the Top SQL pipeline but changes the observed metric from CPU to RU.

### Why is there no TopRU data after enabling it?

Check the following items:

- Confirm that [Resource Control](/tidb-resource-control-ru-groups.md) is enabled.
- Confirm that your cluster supports TopRU in TiDB Cloud Clinic.
- Select a recent time range that contains actual SQL workload.
- Refresh the page after running workload for a short period.

If the issue persists, contact TiDB Cloud support.

### Is TopRU equal to billing RU?

No. TopRU uses runtime `RUDetails` observability values to help you diagnose high resource-consumption SQL. For billing and reconciliation, use billing RU and related offline statistics.
