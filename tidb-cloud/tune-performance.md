---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# Analyze and Tune Performance

TiDB Cloud provides [Slow Query](#slow-query) and [Statement Analysis](#statement-analysis) to analyze performance.

- Slow Query lets you search and view all slow queries in your TiDB cluster, and explore the bottlenecks of each slow query by viewing its execution plan, SQL execution information, and other details.

- Statement Analysis enables you to directly observe the SQL execution on the page, and easily locate performance problems without querying the system tables.

## View the Diagnosis page

1. On the [**Clusters**](https://console.tidb.io/project/clusters) page, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. In the left navigation pane, click **Monitoring** > **Diagnosis**.

## Slow Query

By default, SQL queries that take more than 300 milliseconds are considered as slow queries.

To view slow queries in a cluster, perform the following steps:

1. Navigate to the [**Diagnosis**](#view-the-diagnosis-page) page of a cluster.

2. Click the **Slow Query** tab.

3. Click any slow query in the list to display its detailed execution information.

4. (Optional) You can filter slow queries based on the target time range, the related databases, and SQL keywords. You can also limit the number of slow queries to be displayed.

The results are displayed in the form of a table, and you can sort the results by different columns.

For more information, see [Slow Queries in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-slow-query).

## Statement Analysis

To use the statement analysis, perform the following steps:

1. Navigate to the [**Diagnosis**](#view-the-diagnosis-page) page of a cluster.

2. Click the **SQL Statement** tab.

3. Select the time period to be analyzed in the time interval box. Then you can get the execution statistics of SQL statements of all databases in this period.

4. (Optional) If you only care about certain databases, you can select the corresponding schema(s) in the next box to filter the results.

The results are displayed in the form of a table, and you can sort the results by different columns.

For more information, see [Statement Execution Details in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-statement-details).
