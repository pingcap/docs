---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance in TiDB Cloud.
aliases: ['/tidbcloud/index-insight']
---

# Analyze and Tune Performance

<CustomContent plan="starter,essential,dedicated">

TiDB Cloud provides [Slow Query](#slow-query), [Statement Analysis](#statement-analysis), and [Key Visualizer](#key-visualizer) to analyze performance.

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud provides [Slow Query](#slow-query) and [SQL Statement](#sql-statement) to analyze performance.

</CustomContent>

- Slow Query lets you search and view all slow queries in your TiDB <CustomContent plan="starter,essential,dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>, and explore the bottlenecks of each slow query by viewing its execution plan, SQL execution information, and other details.

- <CustomContent plan="starter,essential,dedicated">Statement Analysis</CustomContent><CustomContent plan="premium">SQL Statement</CustomContent> enables you to directly observe the SQL execution on the page, and easily locate performance problems without querying the system tables.

<CustomContent plan="starter,essential,dedicated">

- Key Visualizer helps you observe TiDB's data access patterns and data hotspots.

> **Note:**
>
> Currently, **Key Visualizer** is only available on TiDB Cloud Dedicated clusters.

</CustomContent>

## View the Diagnosis page

<CustomContent plan="starter,essential,dedicated">

1. On the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. In the left navigation pane, click **Monitoring** > **Diagnosis**.

</CustomContent>

<CustomContent plan="premium">

1. On the [**TiDB Instances**](https://tidbcloud.com/tidbs) page of your organization, click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and instances.

2. In the left navigation pane, click **Monitoring**.

</CustomContent>

## Slow Query

By default, SQL queries that take more than 300 milliseconds are considered as slow queries.

To view slow queries in a TiDB <CustomContent plan="starter,essential,dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>, perform the following steps:

<CustomContent plan="starter,essential,dedicated">

1. Navigate to the [**Diagnosis**](#view-the-diagnosis-page) page of a cluster.

2. Click the **Slow Query** tab.

3. Click any slow query in the list to display its detailed execution information.

4. (Optional) You can filter slow queries based on the target time range, the related databases, and SQL keywords. You can also limit the number of slow queries to be displayed.

</CustomContent>

<CustomContent plan="premium">

1. Navigate to the overview page of the TiDB instance, and then click **Monitoring** > **Slow Query** in the left navigation pane.

2. Select a slow query from the list to view its detailed execution information.

3. (Optional) You can filter slow queries based on the target time range and SQL keywords. You can also limit the number of slow queries to be displayed.

</CustomContent>

The results are displayed in the form of a table, and you can sort the results by different columns.

<CustomContent plan="starter,essential,dedicated">

For more information, see [Slow Queries in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-slow-query).

</CustomContent>

<CustomContent plan="starter,essential,dedicated">

## Statement Analysis

To use the statement analysis, perform the following steps:

1. Navigate to the [**Diagnosis**](#view-the-diagnosis-page) page of a cluster.

2. Click the **SQL Statement** tab.

3. Select the time period to be analyzed in the time interval box. Then you can get the execution statistics of SQL statements of all databases in this period.

4. (Optional) If you only care about certain databases, you can select the corresponding schema(s) in the next box to filter the results.

</CustomContent>

<CustomContent plan="premium">

## SQL Statement

To use the **SQL Statement** page, perform the following steps:

1. Navigate to the overview page of the TiDB instance, and then click **Monitoring** > **SQL Statement** in the left navigation pane.

2. Click a SQL statement in the list to view its detailed execution information.

3. In the time interval box, select the time period to be analyzed. Then you can get the execution statistics for SQL statements across all databases in this period.

4. (Optional) If you only care about certain databases, you can select the corresponding schema(s) in the next box to filter the results.

</CustomContent>

The results are displayed in the form of a table, and you can sort the results by different columns.

<CustomContent plan="starter,essential,dedicated">

For more information, see [Statement Execution Details in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-statement-details).

## Key Visualizer

> **Note:**
>
> Key Visualizer is only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

To view the key analytics, perform the following steps:

1. Navigate to the [**Diagnosis**](#view-the-diagnosis-page) page of a cluster.

2. Click the **Key Visualizer** tab.

On the **Key Visualizer** page, a large heat map shows how access traffic changes over time. The average values along each axis of the heat map are shown below and on the right side. The left side displays the table name, index name, and other related information.

For more information, see [Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer).

</CustomContent>
