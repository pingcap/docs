---
title: Top SQL
summary: This document describes how to use Top SQL to locate SQL queries that contribute to a high load.
---

# Top SQL

> **Warning:**
>
> Currently, Top SQL is an experimental feature. It is not recommended that you use it for production environments.

This document describes how to use Top SQL to locate SQL queries that contribute to a high load of a TiDB or TiKV node in a specified time range. For example, you can use Top SQL to locate an analytic query that contributes to 99% of the load and is executed on a low-load database.

For a specified TiDB or TiKV node, Top SQL can provide the following features:

* Show the top 5 SQL queries that contribute the most load in a specified time range.
* Show information such as CPU usage, requests per second, average latency, and query plan of a particular query, which can be used as a potential performance optimization way to improve your business.

## Enable Top SQL

The Top SQL feature is disabled by default. You can enable the feature for the entire cluster using either of the following method:

- Method 1: Log in to TiDB Dashboard, click **Top SQL** in the left panel, click the gear button in the upper-right corner of the page, and then enable the Top SQL feature.
- Method 2: Set the value of the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-introduced-from-v540-version) to `ON`.

> **Note:**
>
> Enabling Top SQL has a slight impact on cluster performance.

## Using Top SQL

Once Top SQL is enabled, you can use Top SQL by logging into TiDB Dashboard and then clicking **Top SQL** in the left pane.

![Top SQL](/media/dashboard/top-sql-overview.png)

Usage tips：

* You can select the target node and the time range in the drop-down list at the top of the page, or you can select the time range in the chart.
* If the data displayed in the chart is out of date, you can click **Refresh**, or you can select whether to refresh automatically and select the auto-refresh interval in the **Refresh** drop-down list.
* The chart shows the top 5 types of queries that contribute to the most load for the selected node in selected time range.
* You can click a query type in the list to view query details, including the execution plan for that query, and the Call/sec, Scan Rows/sec, Scan Indexes/sec, and Latency/call for each execution plan on this node.

![Top SQL Details](/media/dashboard/top-sql-details.png)