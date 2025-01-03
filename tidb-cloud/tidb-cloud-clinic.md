---
title: TiDB Cloud Clinic
summary: Learn how to advanced monitoring and diagnostics of TiDB Cloud.
---

# TiDB Cloud Clinic

TiDB Cloud Clinic offers advanced monitoring and diagnostic capabilities on the TiDB Cloud.

> **Note:**
>
> Currently, the TiDB Cloud Clinic feature is only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

To use TiDB Cloud Clinic, you need to have an Enterprise support plan or higher on TiDB Cloud.

## View the Cluster page

To view the Cluster page, take the following steps:

1. Log in to the [TiDB Cloud Clinic console](https://clinic.pingcap.com/)

2. Click the name of the target orgnization. The clusters in one project are displayed.

3. Click the name of the target cluster. The cluster overview page is displayed.


- Advanced Metrics
- Top Slow Queries
- TopSQL
- Benchmark Report

### Advanced Metrics

TiDB Cloud Clinic uses Grafana to provide a wider range of TiDB cluster metrics. These include dashboards for TiDB, TiKV, TiFlash, BR, Lightning, TiCDC, TiDB resource control, and TiDB performance.

To view the metrics dashboard, take the following steps:

1. Navigate to the **Cluseter** page of a cluster.

2. Click the **Metrics** button.

3. Click the name of target dashboard. The dashboard is displayed.

The retention policy for advanced metrics is 90 days.

### Top Slow Queries

By default, SQL queries that take more than 300 milliseconds are considered slow queries.

On the default Slow Queries page, it can be challenging to quickly identify performance-impacting SQL queries when a cluster has a large volume of slow queries. Top Slow Queries provides aggregated analysis based on slow query logs. With this feature, you can easily pinpoint queries with performance issues, reducing overall performance tuning time by at least half.

Top Slow Queries will show the Top 10 Queries aggregated by SQL digest, can order by the following dimentions:
- Total Latency 
- Max Latency
- Avg Latency
- Total Memory
- Max Memory
- Avg Memory
- Total Count

To view slow queries in a cluster, take the following steps:

1. Navigate to the **Cluster** page of a cluster.

2. Click the **Slow Query** button.

3. The top slow queries are displayed in the form of a table, and you can sort the results by different columns.

4. (Optional) Click any slow query in the list to display its detailed execution information.

5. (Optional) You can filter slow queries based on the target time range, the related databases, and statement kinds.

The retention policy for slow queries is 7 days.

For more information, see [Slow Queries in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-slow-query).

### TopSQL

With Top SQL, you can monitor and visually explore the CPU overhead of each SQL statement in your database in real-time, which helps you optimize and resolve database performance issues.

To view the TopSQL, take the following steps:

1. Navigate to the **Cluster** page of a cluster.

2. Click the **TopSQL** button.

3. Select a particular TiDB or TiKV instance that you want to observe the load. You can adjust the time range in the time picker or select a time range in the chart to get a more precise and detailed look at the problem.

4. Observe the charts and tables presented by Top SQL.

For more information, see [TopSQL in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/top-sql). 

### Benchmark Report

The Benchmark Report helps identify performance issues in a TiDB cluster during performance testing. After completing a stress test, you can generate a benchmark report to analyze the cluster's performance. The report highlights identified bottlenecks and provides suggestions for optimization. After applying these suggestions, you can run another round of stress testing and generate a new benchmark report to compare performance improvements.

To use the benchmark report, take the following steps:

1. Navigate to the **Cluster** page of a cluster.

2. Click the **Benchmark Report** button.

3. Select the time range to be analyzed in the benchmark report.

4. Click **Create Report** to generate the benchmark report.

4. Wait until the benchmark report is successfully generated. Click the **View** button to view the report.