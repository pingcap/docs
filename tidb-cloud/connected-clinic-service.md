---
title: Connected: Clinic Service
summary: Introduces detailed information about the Clinic Service
---

# Connected: Clinic Service

TiDB Cloud Clinic offers advanced monitoring and diagnostic capabilities on the TiDB Cloud, designed to help you quickly identify performance issues, optimize your database, and enhance overall performance with detailed analysis and actionable insights.

> **Note**
>
> Currently, the TiDB Cloud Clinic feature is only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

TiDB Cloud Clinic is only available for organizations that subscribe to the **Enterprise** or **Premium** support plan.

## View the Cluster page

To view the Cluster page, take the following steps:

1. Log in to the [TiDB Cloud Clinic console](https://clinic.pingcap.com/).

2. Click the name of the target organization. The clusters in one of the projects are displayed.

3. Click the name of the target cluster. The cluster overview page is displayed with the following sections:

   * Advanced Metrics

   * Top Slow Queries

   * TopSQL

   * Benchmark Report


## Advanced Metrics

TiDB Cloud Clinic uses Grafana to provide a wider range of TiDB cluster metrics, including dashboards for TiDB, TiKV, TiFlash, BR, Lightning, TiCDC, TiDB resource control, and TiDB performance.

To view the metrics dashboard, take the following steps:

1. Navigate to the **Cluster** page of a cluster.

2. Click the **Metrics** button. 

3. Click the name of the target dashboard. The dashboard is displayed.

The retention policy for advanced metrics is 90 days.

## Top Slow Queries

By default, SQL queries that take more than 300 milliseconds are considered slow queries.

On the default Slow Queries page, identifying performance-impacting queries can be difficult, especially in clusters with a large number of slow queries. The Top Slow Queries feature provides an aggregated analysis of slow query logs, allowing you to quickly identify queries that affect performance. This can significantly reduce performance tuning time by at least half.

Top Slow Queries displays the top 10 queries, aggregated by SQL digest, and can be sorted by the following dimensions:

* Total Latency

* Max Latency

* Avg Latency

* Total Memory

* Max Memory

* Avg Memory

* Total Count

To view slow queries in a cluster, take the following steps:

Navigate to the **Cluster** page of a cluster.

1. Click the **Slow Query** button.

2. The top slow queries are displayed in the form of a table, where you can sort the results by different columns.

3. (Optional) Click any slow query in the list to display its detailed execution information.

4. (Optional) Filter slow queries based on the target time range, the related databases, and statement kinds.

5. The retention policy for slow queries is 7 days.

For more information, see [Slow Queries in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-slow-query).

## TopSQL

With Top SQL, you can monitor and visually explore the CPU overhead of each SQL statement in your database in real-time, which helps you optimize and resolve database performance issues.

To view TopSQL, take the following steps:

1. Navigate to the **Cluster** page of a cluster.

2. Click the **TopSQL** button.

3. Select a TiDB or TiKV instance that you want to observe the workload. You can adjust the time range in the time picker or select a specific time range in the chart for a more precise and detailed view.

4. Observe the charts and tables presented by Top SQL.

For more information, see [TopSQL in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/top-sql).

## Benchmark Report

The Benchmark Report helps identify performance issues in a TiDB cluster during performance testing. After completing a stress test, you can generate a benchmark report to analyze the cluster's performance. The report highlights identified bottlenecks and provides suggestions for optimization. After applying these suggestions, you can run another round of stress testing and generate a new benchmark report to compare performance improvements.

To generate a benchmark report, take the following steps:

1. Navigate to the **Cluster** page of a cluster.

2. Click the **Benchmark Report** button.

3. Select the time range to be analyzed in the benchmark report.

4. Click **Create Report** to generate the benchmark report.

5. Wait until the benchmark report is successfully generated. Then, click **View** to check the report.
