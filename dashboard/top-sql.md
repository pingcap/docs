---
title: TiDB Dashboard Top SQL page
summary: Using Top SQL to find SQL statements with high CPU overhead
---

# TiDB Dashboard Top SQL page

With Top SQL, you can monitor and visually explore the CPU overhead of each SQL statement in your database in real-time, which helps you optimize and resolve database performance issues. Top SQL continuously collects and stores CPU load data summarized by SQL statements for any seconds from all TiDB and TiKV instances. The data can be stored stored for up to 30 days. Top SQL presents you visual charts and tables to quickly pinpoint which SQL statements are contributing the high CPU load of a TiDB or TiKV instance over a certain period of time.

Top SQL provides following features:

* Visualize the top 5 types of SQL statements with the highest CPU overhead through charts and tables.
* Display detailed execution information such as queries per second, average latency, query plan, etc.
* All running SQL statements are counted in.
* Allow to view data of a specific TiDB and TiKV instance.

## Recommended Scenarios

Top SQL is suitable for analyzing performance issues. The following are some typical Top SQL scenarios:

* You discovered that an individual TiKV instance in the cluster has a very high CPU usage through the Grafana charts. You want to know which SQL statements cause the CPU hotspots, so that you can optimize them and better leverage all of your distributed resources.
* You discovered that the cluster has a very high CPU usage overall and queries are slow. You want to quickly figure out which SQL statements are currently consuming the most CPU resources so that you can optimize them.
* The CPU usage of the cluster has drastically changed and you want to know the major cause.
* Analyze the most resource-intensive SQL statements in the cluster and optimize them to reduce hardware costs.

> **Note:**
>
> Top SQL currently does not count the CPU overhead of the SQL statements that were running before the Top SQL feature was enabled. Therefore, it is recommended to [enable the Top SQL feature](#enable-top-sql) as soon as possible instead of enabling it until you have already encountered performance problems.

Top SQL cannot be used to pinpoint non-performance issues, such as incorrect data or abnormal crashes.

Top SQL is still in its early stages and is being enhanced. Here are some scenarios that are **not supported** at the moment:

* Analyzing the overhead of SQL statements outside of Top 5 (for example, when multiple business workloads are mixed).
* Analyzing the overhead of Top N SQL statements by various dimensions such as User and Database.
* Analyzing database performance issues that are not caused by high CPU load, such as transaction lock conflicts.

## Access the page

You can access the Top SQL page using either of the following methods:

- After logging into TiDB Dashboard, click **Top SQL** on the left navigation bar.

  ![Top SQL](/media/dashboard/top-sql-access.png)

- Visit <http://127.0.0.1:2379/dashboard/#/topsql> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Enable Top SQL

> **Note:**
>
> To use Top SQL, your cluster should be deployed or upgraded with a recent version of TiUP (v1.9.0 and above) or TiDB Operator (v1.3.0 and above). If your cluster was upgraded with an older version, see [FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown) for instructions.

Top SQL is not enabled by default as there is a slight impact on cluster performance (within 3% on average) when enabled. You can enable Top SQL by the following methods.

1. Visit the [Top SQL page](#access-the-page).
2. Click **Open Settings**. On the right side of the **Settings** area, switch on **Enable Feature**.
3. Click **Save**.

The CPU load details after enabling the feature will be displayed. The data can be delayed for up to 1 minute.

In addition to the UI, you can also enable the Top SQL feature by setting the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540):

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

## Use Top SQL

The following are the common steps to use Top SQL.

1. Visit the [Top SQL page](#access-the-page).

2. Select a particular TiDB or TiKV instance that you want to observe the load.

   ![Select Instance](/media/dashboard/top-sql-usage-select-instance.png)

   If you are unsure of which TiDB or TiKV instance to observe, you can select arbitrary instances. Also, when the cluster CPU load is extremely unbalanced, you can first use Grafana charts to determine the specific instance you want to observe.

3. Observe the charts and tables presented by Top SQL.

   ![Chart and Table](/media/dashboard/top-sql-usage-chart.png)

   The size of the bars in the bar chart represents the amount of CPU resources consumed by the SQL statement at that moment. Different colors distinguish different types of SQL statements. In most cases, you should focus on the SQL statements that have a higher CPU resource overhead in the corresponding time range in the chart.

4. Click on a SQL statement in the table to expand. You can see detailed execution metrics of different plans of that statement, such as Call/sec (average queries per second), Scan Indexes/sec (average number of index rows scanned per second), etc.

   ![Details](/media/dashboard/top-sql-details.png)

5. Based on these initial clues, you can further explore the [SQL Statement](/dashboard/dashboard-statement-list.md) or [Slow Queries](/dashboard/dashboard-slow-query.md) page to find the root cause of high CPU consumption or large data scans of the SQL statement.

Additionally,

* You can adjust the time range in the time picker, or box a time range in the chart to get a more precise and detailed look at the problem. A smaller time range will provide more detailed data, with up to 1 second precision.

  ![Change time range](/media/dashboard/top-sql-usage-change-timerange.png)

* If the chart is out of date, you can click the **Refresh** button, or select Auto Refresh options from the **Refresh** drop-down list.

  ![Refresh](/media/dashboard/top-sql-usage-refresh.png)

## Disable Top SQL

You can disable this feature by following these steps.

1. Visit [Top SQL page](#access-the-page).
2. Click the **Gear icon** in the upper right corner to open the settings screen and switch off **Enable Feature**.
3. Click **Save**.
4. In the popped-up dialog box, click **Disable**.

In addition to the UI, you can also disable the Top SQL feature by setting the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540):

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

## Frequently Asked Questions

**1. Feature cannot be enabled as the UI displays "required component NgMonitoring is not started"**.

See [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown).

**2. Is there any performance impact when enabled?**

This feature has a slight impact on cluster performance. According to our benchmark, the average performance impact is usually less than 3% when the feature is enabled.

**3. What is the status of this feature?**

This is a generally available feature and can be used in production environments.

**4. What is the meaning of "Other Statements"?**

"Other Statement" counts the total CPU overhead of all non-Top 5 statements. With this information, you can learn how much CPU overhead Top 5 statements contribute compared to the overall.

**5. What is the relationship between the CPU overhead displayed by Top SQL and the actual CPU usage of the process?**

Their correlation is strong but they are not exactly the same thing. As an example, the cost of writing multiple replicas are not counted in TiKV's CPU overhead displayed by Top SQL. In general, SQL statements with higher CPU usage will result in higher CPU overhead displayed in Top SQL.

**6. What is the meaning of the Y-axis of the Top SQL chart?**

It represents the amount of CPU resources consumed. The more resources consumed by the SQL statement, the higher the value will be. In most cases, you don't need to care about the meaning or unit of the specific value.

**7. Does Top SQL count running (unfinished) SQL statements?**

Yes. The bars displayed in the Top SQL chart at each moment is the CPU overhead of all running SQL statements at that moment.
