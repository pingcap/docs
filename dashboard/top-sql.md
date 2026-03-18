---
title: TiDB Dashboard TopSQL page
summary: Use TopSQL to identify queries that consume high CPU, network, and logical IO resources
---

# TiDB Dashboard TopSQL Page

TiDB Dashboard TopSQL helps you visually analyze the most resource-intensive queries on a specific TiDB or TiKV instance over a period of time. By default, TopSQL continuously collects CPU load data from each TiDB and TiKV instance and retains the data for up to 30 days. For TiKV instances, you can also enable **TiKV Network IO collection (multi-dimensional)** in the settings panel to view metrics such as `Network Bytes` and `Logical IO Bytes`, and analyze the results by `Query`, `Table`, `DB`, or `Region`.

TopSQL provides the following features:

* Show the top `5`, `20`, or `100` records with the highest load in the selected time range, and automatically aggregate the rest into `Others`.
* Sort hotspots by `CPU Time` or `Network Bytes`, and when a TiKV instance is selected, by `Logical IO Bytes` as well.
* Analyze load by `Query` and view SQL and execution plan details. When a TiKV instance is selected, you can also aggregate and analyze data by `Table`, `DB`, or `Region`.
* Zoom in on a selected time range in the chart, manually refresh data, enable auto refresh, and export table data to CSV.
* Collect all SQL statements that are running, including unfinished statements.
* View data for a specific TiDB or TiKV instance in the cluster.

## Recommended scenarios

TopSQL is suitable for analyzing performance issues in scenarios such as the following:

* You find that one TiDB or TiKV instance has very high CPU usage and want to quickly identify which queries are consuming the most CPU resources.
* The overall cluster becomes slower and you want to identify the queries that currently consume the most resources, or compare the major query changes before and after a workload shift.
* You want to locate hotspots at a higher level and analyze TiKV-side resource usage by `Table`, `DB`, or `Region`.
* You want to troubleshoot TiKV hotspots from the perspective of network traffic or logical IO instead of CPU alone.

TopSQL is not suitable for the following scenarios:

- It cannot answer non-performance questions such as data correctness issues or abnormal crashes.
- It is not designed to directly analyze issues such as lock conflicts or transaction semantic errors that are not caused by resource consumption.

## Access the page

You can access the TopSQL page using either of the following methods:

* After logging in to TiDB Dashboard, click **Top SQL** in the left navigation menu.

  ![TopSQL](/media/dashboard/top-sql-access.png)

* Visit <http://127.0.0.1:2379/dashboard/#/topsql> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Enable TopSQL

> **Note:**
>
> To use TopSQL, your cluster should be deployed or upgraded with a recent version of TiUP (v1.9.0 or above) or TiDB Operator (v1.3.0 or above). If your cluster was upgraded using an earlier version of TiUP or TiDB Operator, see [FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown) for instructions.

TopSQL is disabled by default because it has a slight impact on cluster performance, usually less than 3%. You can enable TopSQL as follows:

1. Visit the [TopSQL page](#access-the-page).
2. Click **Open Settings**. In the **Settings** panel on the right, turn on **Enable Feature**.
3. Click **Save**.

After TopSQL is enabled, only data collected from that point forward is available. Historical fine-grained data before enabling TopSQL is not backfilled. New data is usually visible after about 1 minute. After TopSQL is disabled, existing historical data remains queryable until it expires, but no new TopSQL data is collected.

In addition to the UI, you can also enable the TopSQL feature by setting the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540):

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

### Enable TiKV Network IO collection (optional)

If you want to use `Order By Network`, `Order By Logical IO`, or `By Region` on a TiKV instance, continue in the same settings panel and turn on **Enable TiKV Network IO collection (multi-dimensional)**, and then save the setting.

As shown in the following screenshot, the **Settings** panel contains both **Enable Feature** and **Enable TiKV Network IO collection (multi-dimensional)**:

![Enable TiKV network IO collection](/media/dashboard/top-sql-settings-enable-tikv-network-io.png)

This setting increases storage and query overhead. After it is enabled, the configuration is applied to all current TiKV nodes. The new data might still take about 1 minute to appear. If some TiKV nodes fail to enable the setting, the page displays a warning, and newly collected data might be incomplete.

For TiKV nodes that are added later by scaling out, this switch does not automatically take effect. You need to manually turn it on again so that the configuration is applied to all TiKV nodes. If you want newly added TiKV nodes to automatically enable this capability, add the following configuration under `server_configs.tikv` in the TiUP cluster topology file and re-apply the TiKV configuration using TiUP:

```yaml
server_configs:
  tikv:
    resource-metering.enable-network-io-collection: true
```

For more information about TiUP topology configuration, see [TiDB Cluster Topology Reference](/tiup/tiup-cluster-topology-reference.md).

## Use TopSQL {#use-top-sql}

The following are the common steps to use TopSQL:

1. Visit the [TopSQL page](#access-the-page).

2. Select the TiDB or TiKV instance that you want to observe.

    ![Select Instance](/media/dashboard/top-sql-usage-select-instance.png)

    If you are not sure which instance to inspect, you can first identify the busy node from Grafana or the Overview page, and then return to TopSQL for deeper analysis.

3. Set the time range, and use **Refresh** or auto refresh when needed.

    You can adjust the time range in the time picker, or drag over a range in the chart to zoom in. A smaller time range provides more fine-grained data, with precision down to 1 second.

    ![Change time range](/media/dashboard/top-sql-usage-change-timerange.png)

    If the chart is out of date, click **Refresh**, or select an auto refresh interval from the **Refresh** drop-down list.

    ![Refresh](/media/dashboard/top-sql-usage-refresh.png)

4. Choose the observation mode.

    - Use `Limit` to display the top `5`, `20`, or `100` records.
    - Use `Order By` to sort by `CPU Time` or `Network Bytes`. When a TiKV instance is selected, you can also sort by `Logical IO Bytes`.
    - Use `By Query`, `By Table`, `By DB`, or `By Region` to switch the aggregation dimension. The last three options are available only for TiKV instances.

    When a TiKV instance is selected and **TiKV Network IO collection (multi-dimensional)** is enabled, the `Order By` drop-down list shows `Order By CPU`, `Order By Network`, and `Order By Logical IO`.

    ![Select order by](/media/dashboard/top-sql-usage-select-order-by.png)

    ![Select aggregation dimension](/media/dashboard/top-sql-usage-select-agg-by.png)

    `By Region`, `Order By Network`, and `Order By Logical IO` depend on **TiKV Network IO collection (multi-dimensional)**. If the feature is disabled but historical data is still retained, the page can continue to display historical data and warns that newly collected data might be incomplete.

5. Observe hotspot records in the chart and table.

    ![Chart and Table](/media/dashboard/top-sql-usage-chart.png)

    Each block in the chart represents resource consumption under the current sort dimension, and different colors represent different records. The table is sorted by the current metric and includes an extra `Others` row that summarizes all non-Top N records.

6. In the `By Query` view, click a row in the table to expand query details by execution plan.

    ![Details](/media/dashboard/top-sql-details.png)

    In the detail panel, you can view the query template, query template ID, plan template ID, and execution plan text. The detail table shows different metrics depending on the selected instance type:

    - For TiDB instances, the detail table typically shows `Call/sec` and `Latency/call`.
    - For TiKV instances, the detail table typically shows `Call/sec`, `Scan Rows/sec`, and `Scan Indexes/sec`.

    In the `By Table`, `By DB`, or `By Region` views, the page shows aggregated results rather than per-plan SQL details.

7. On a TiKV instance, if you need to analyze hotspots at a higher level, switch to `By Table`, `By DB`, or `By Region` to view aggregated results.

    ![Aggregated results at DB level](/media/dashboard/top-sql-usage-agg-by-db-detail.png)

8. Based on these clues, continue with the [SQL Statements](/dashboard/dashboard-statement-list.md) page or the [Slow Queries](/dashboard/dashboard-slow-query.md) page to investigate the root cause.

    In the `By Query` view, you can also click **Search in SQL Statements** in the table to jump to the corresponding SQL Statements page. If you need to analyze the current table data offline, use `Download to CSV`.

## Disable TopSQL

You can disable TopSQL by following these steps:

1. Visit the [TopSQL page](#access-the-page).
2. Click the settings icon in the upper-right corner, and turn off **Enable Feature**.
3. Click **Save**.
4. In the confirmation dialog, click **Disable**.

After TopSQL is disabled, no new TopSQL data is collected. Existing historical data remains available until it expires.

In addition to the UI, you can also disable the TopSQL feature by setting the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540):

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

### Disable TiKV Network IO collection

If you want to stop collecting TiKV `Network Bytes`, `Logical IO Bytes`, and related multi-dimensional data while keeping TopSQL CPU analysis enabled, turn off **Enable TiKV Network IO collection (multi-dimensional)** in the settings panel.

After this setting is disabled:

- Historical network IO and logical IO data remains viewable until it expires.
- New `Network Bytes`, `Logical IO Bytes`, and `By Region` data is no longer collected.

## Frequently asked questions

**1. TopSQL cannot be enabled and the UI displays "required component NgMonitoring is not started".**

See [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown).

**2. Will performance be affected after enabling TopSQL?**

TopSQL itself has a slight impact on cluster performance. According to our benchmark, the average performance impact is usually less than 3%. If you also enable **TiKV Network IO collection (multi-dimensional)**, there is additional storage and query overhead.

**3. What is the status of this feature?**

It is now a generally available (GA) feature and can be used in production environments.

**4. What does `Others` mean in the UI?**

`Others` represents the aggregated result of all non-Top N records under the current sort dimension. You can use it to understand how much of the total load comes from the Top N records.

**5. What is the relationship between the CPU overhead displayed by TopSQL and the actual CPU usage of the process?**

Their correlation is strong but they are not exactly the same thing. For example, the cost of writing multiple replicas is not counted in the TiKV CPU overhead displayed by TopSQL. In general, SQL statements with higher CPU usage result in higher CPU overhead displayed in TopSQL.

**6. What does the Y-axis of the TopSQL chart mean?**

The Y-axis represents resource consumption under the currently selected sort dimension. When `Order By CPU` is selected, it represents CPU time. When `Order By Network` is selected, it represents network bytes. When `Order By Logical IO` is selected, it represents logical IO bytes.

**7. Does TopSQL collect running (unfinished) SQL statements?**

Yes. At each point in time, the TopSQL chart shows the load of all currently running SQL statements under the selected dimension, so unfinished SQL statements are included as well.

**8. Why can't I see new `Order By Network`, `Order By Logical IO`, or `By Region` data?**

These views depend on **TiKV Network IO collection (multi-dimensional)**. Check the following items:

- Make sure that you have selected a TiKV instance.
- Make sure that **Enable TiKV Network IO collection (multi-dimensional)** is turned on in the settings panel.
- Make sure that the relevant TiKV nodes have successfully enabled the configuration. If only some nodes are enabled, the page warns that newly collected data might be incomplete.
- If you recently scaled out new TiKV nodes, enable `resource-metering.enable-network-io-collection` in the TiKV default configuration managed by TiUP. Otherwise, newly added nodes do not automatically inherit the setting.
