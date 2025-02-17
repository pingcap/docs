---
title: TiDB Cloud Clinic
summary: Learn how to use advanced monitoring and diagnostics of TiDB Cloud using TiDB Cloud Clinic.
---

# TiDB Cloud Clinic

TiDB Cloud Clinic offers advanced monitoring and diagnostic capabilities for TiDB Cloud.

> **Note:**
>
> Currently, TiDB Cloud Clinic is only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## Prerequisites

To use TiDB Cloud Clinic, you need to have an **Enterprise** support plan or higher for TiDB Cloud.

## View the **Cluster** page

To view the **Cluster** page, take the following steps:

1. Log in to the [TiDB Cloud Clinic console](https://clinic.pingcap.com/) and select **Continue with TiDB Account** to enter the TiDB Cloud login page.

2. From the organization list, select your target organization. The clusters in the selected project are displayed.

3. Click the name of your target cluster. The cluster overview page is displayed, where you can view detailed information about your cluster, including:

    - Advanced Metrics
    - Top Slow Queries
    - TopSQL
    - Benchmark Report

## Monitor advanced metrics

TiDB Cloud Clinic uses Grafana to provide a comprehensive set of metrics for TiDB clusters. These metrics include dashboards for TiDB, TiKV, TiFlash, BR, Lightning, TiCDC, TiDB resource control, and TiDB performance.

To view the metrics dashboard, take the following steps:

1. In the [TiDB Cloud Clinic console](https://clinic.pingcap.com/), navigate to the **Cluster** page of a cluster.

2. Click **Metrics**.

3. Click the name of the dashboard you want to view. The dashboard is displayed.

The retention policy for advanced metrics is 90 days.

## Analyze top slow queries

By default, SQL queries that take longer than 300 milliseconds are considered slow queries.

On the default **Slow Queries** page, it can be difficult to quickly identify performance-impacting SQL queries when a cluster has a large volume of slow queries. The **Top Slow Queries** feature provides aggregated analysis based on slow query logs. With this feature, you can easily pinpoint queries with performance issues, reducing overall performance tuning time by at least half.

Top Slow Queries displays the top 10 queries aggregated by SQL digest, sorted by the following dimensions:

- Total latency 
- Maximum latency
- Average latency
- Total memory
- Maximum memory
- Average memory
- Total count

To view slow queries in a cluster, take the following steps:

1. In the [TiDB Cloud Clinic console](https://clinic.pingcap.com/), navigate to the **Cluster** page of a cluster.

2. Click **Slow Query**.

3. The top slow queries are displayed in a table. You can sort the results by different columns.

4. (Optional) Click any slow query in the list to view its detailed execution information.

5. (Optional) Filter slow queries by time range, database, or statement type.

The retention policy for slow queries is 7 days.

For more information, see [Slow Queries in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-slow-query).

## Monitor TopSQL

TiDB Cloud Clinic provides TopSQL information, enabling you to monitor and visually explore the CPU overhead of each SQL statement in your database in real time. This helps you optimize and resolve database performance issues.

To view TopSQL, take the following steps:

1. In the [TiDB Cloud Clinic console](https://clinic.pingcap.com/), navigate to the **Cluster** page of a cluster.

2. Click **TopSQL**.

3. Select a specific TiDB or TiKV instance to observe its load. You can use the time picker or select a time range in the chart to refine your analysis.

4. Analyze the charts and tables displayed by TopSQL.

For more information, see [TopSQL in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/top-sql). 

## Generate benchmark reports

The **Benchmark Report** feature helps you identify performance issues in a TiDB cluster during performance testing. After completing a stress test, you can generate a benchmark report to analyze the cluster's performance. The report highlights identified bottlenecks and provides optimization suggestions. After applying these suggestions, you can run another round of stress testing and generate a new benchmark report to compare performance improvements.

To generate a benchmark report, take the following steps:

1. In the [TiDB Cloud Clinic console](https://clinic.pingcap.com/), navigate to the **Cluster** page of a cluster.

2. Click **Benchmark Report**.

3. Select the time range to be analyzed in the benchmark report.

4. Click **Create Report** to generate the benchmark report.

5. Wait for report generation to complete. When the report is ready, click **View** to open it.