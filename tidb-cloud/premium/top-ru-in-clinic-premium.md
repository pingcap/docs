---
title: TopRU page in TiDB Cloud Clinic
summary: Learn how to use TopRU in TiDB Cloud Clinic to identify SQL statements and database users with high RU consumption.
---

# TopRU page in TiDB Cloud Clinic

TopRU is an SQL observability feature in TiDB Cloud Clinic. It ranks SQL workloads by request unit (RU) consumption to help you quickly identify SQL statements with high resource usage.

TopRU reuses the Top SQL collection and reporting pipeline, but extends the core metric from CPU to RU, and aggregates records by `(user, sql_digest, plan_digest)`. This means that TopRU helps you identify both high-cost SQL statements and the database users who continuously consume RU.

TopRU and Top SQL can coexist. Enabling TopRU does not change the existing CPU semantics of Top SQL.

## Feature overview

TopRU is designed to answer the following questions:

- Which SQL statements continuously consume high RU?
- Is an RU spike in a time range caused by a small set of users or SQL statements?
- Why is resource consumption high even when CPU usage is not high?

TopRU data comes from runtime RU statistics in SQL execution, so it can reflect near-real-time resource trends. To control overhead, TopRU applies TopN aggregation to users and SQL statements, and merges low-priority items instead of outputting a full per-statement stream.

## Recommended scenarios

TopRU is useful in the following scenarios:

- You need to locate high RU-consuming SQL in clusters with [Resource Control](/tidb-resource-control-ru-groups.md) enabled.
- CPU usage is not the main bottleneck, but overall resource consumption is still high.
- You need user-level visibility to answer "who is consuming RU" instead of only "which SQL consumes CPU".
- You need to quickly identify major RU hotspots under high load and prioritize SQL optimization, resource group governance, or workload throttling.

TopRU is not intended for the following scenarios:

- Billing, reconciliation, or precise auditing.
- Replacing slow query logs, `statements_summary`, or daily offline statistics from resource groups.

## Prerequisites

Before using TopRU, make sure that all of the following conditions are met:

- You can access [TiDB Cloud Clinic](https://clinic.pingcap.com/).
- Your cluster has [Resource Control](/tidb-resource-control-ru-groups.md) enabled.
- The subscription side supports Top SQL `PubSubService` and explicitly requests TopRU capability.
- Your cluster version supports TopRU. For exact version availability, see TiDB Cloud release notes or contact support.

> **Note:**
>
> TopRU is available in TiDB Cloud Clinic for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

> **Note:**
>
> TopRU currently has no independent SQL system variable and no dedicated `SET GLOBAL ...` switch. Whether TopRU is enabled is determined by Top SQL PubSub subscription negotiation, not by a standalone TiDB system variable.

## Page views

The TopRU page currently includes the following views:

- **Overview view (instance-level)**: inspect top RU-consuming SQL from the cluster instance perspective.
- **Sliced by Users view (DB user-level)**: inspect RU consumption grouped by database user.

![TopRU overview view](/media/tidb-cloud/top-ru-instance-view.png)

![TopRU overview detail](/media/tidb-cloud/top-ru-instance-detail.png)

![TopRU sliced by users view](/media/tidb-cloud/top-ru-db-user-view.png)

![TopRU sliced by users detail](/media/tidb-cloud/top-ru-db-user-detail.png)

A common diagnosis path is to locate RU hotspots in the overview view first, and then switch to the user view to identify whether specific users dominate RU consumption.

## Use TopRU

A common workflow for TopRU is as follows:

1. Open the TopRU page and select a time range.
2. In the **Overview** view, identify top RU-consuming SQL statements and hotspot periods.
3. Switch to the **Sliced by Users** view to verify whether RU is concentrated on a small set of users.
4. Open SQL details and combine SQL Digest / Plan Digest with execution count and execution duration to prioritize optimization.
5. Continue analysis with Top SQL, slow query data, and execution plans.

TopRU trends are usually correlated with RU and QPS trends, and can be used for cross-checking:

![TopRU vs RU trend](/media/tidb-cloud/top-ru-vs-ru-trend.png)

![TopRU vs QPS trend](/media/tidb-cloud/top-ru-vs-qps-trend.png)

## TopRU observation dimensions

TopRU uses `(user, sql_digest, plan_digest)` as the aggregation key. Each time point usually includes the following fields:

- `Total RU`: total RU consumption in the interval.
- `Exec Count`: number of executions in the interval.
- `Exec Duration`: aggregated execution duration in the interval.

TopRU supports output granularities of `15s`, `30s`, and `60s`. If no valid granularity is provided in the subscription request, it falls back to `60s`. Internally, RU data is summarized and reported in 60-second aligned windows, so the behavior is typically minute-level near-real-time refresh.

To limit memory and network overhead, TopRU applies TopN aggregation to users and SQL statements. High-priority items are kept as individual records, while low-priority items are merged.

## Limitations and considerations

- TopRU currently supports only `PubSubService` subscription mode.
- TopRU does not support exporting via `SingleTargetDataSink` fixed-target gRPC push mode.
- RU values shown in TopRU are runtime `RUDetails` observability values and are not equivalent to billing RU.
- If Resource Control is not enabled, TopRU cannot generate effective RU data.
- To control collection and reporting overhead, TopRU applies TopN compression and does not retain all low-RU items.

> **Note:**
>
> TopRU is designed for real-time hotspot diagnosis, not for billing settlement, precise reconciliation, or long-term offline auditing.

## FAQ

### What is the difference between TopRU and Top SQL?

Top SQL is CPU-focused. TopRU is RU-focused and adds user-level visibility. TopRU reuses the Top SQL pipeline but changes the observed metric from CPU to RU.

### Why is there no TopRU data after enabling it?

The most common reasons are that [Resource Control](/tidb-resource-control-ru-groups.md) is not enabled, or the subscription side builds a Top SQL subscription but does not explicitly request TopRU capability.

### Is TopRU equal to billing RU?

No. TopRU is based on runtime `RUDetails` observability values and is intended for diagnosing high resource-consumption SQL. For billing and reconciliation, use billing RU and related offline statistics.

### Does TopRU support fixed gRPC target export?

No. TopRU currently supports only `PubSubService` subscription mode, and does not support `SingleTargetDataSink` fixed-target gRPC push export.
