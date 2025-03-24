---
title: TiDB Cloud Built-in Metrics
summary: Learn how to view TiDB Cloud built-in metrics and understand the meanings of these metrics.
---

# TiDB Cloud Built-in Metrics

TiDB Cloud collects and displays a full set of standard metrics of your cluster on the Metrics page. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

## View the Metrics page

To view the metrics on the Metrics page, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of the target cluster. The cluster overview page is displayed.
3. Click **Metrics** in the left navigation pane.

## Metrics retention policy

For TiDB Cloud Serverless clusters, the metrics data is kept for 7 days.

## Metrics for TiDB Cloud Serverless clusters

The Metrics page provides two tabs for metrics of TiDB Cloud Serverless clusters:

- Cluster Status: displays the cluster-level main metrics.
- Database Status: displays the database-level main metrics.

### Cluster Status

The following table illustrates the cluster-level main metrics under the **Cluster Status** tab.

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Request Units | RU per second | The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. In addition to queries that you run, Request Units can be consumed by background activities, so when the QPS is 0, the Request Units per second might not be zero. |
| Used Storage Size | Row-based storage, Columnar storage | The size of the row store and the size of the column store. |
| Query Per Second | All, {SQL type} | The number of SQL statements executed per second, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Average Query Duration | All, {SQL type} | The duration from receiving a request from the client to the TiDB Cloud Serverless cluster until the cluster executes the request and returns the result to the client. |
| Failed Query | All | The number of SQL statement execution errors per second. |
| Transaction Per Second | All | The number of transactions executed per second. |
| Average Transaction Duration | All | The average execution duration of transactions. |
| Total Connection | All | The number of connections to the TiDB Cloud Serverless cluster. |

### Database Status

The following table illustrates the database-level main metrics under the **Database Status** tab.

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| QPS Per DB | All, {Database name} | The number of SQL statements executed per second on every database, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Average Query Duration Per DB | All, {Database name} | The duration from receiving a request from the client to a database until the database executes the request and returns the result to the client.|
| Failed Query Per DB | All, {Database name} | The statistics of error types according to the SQL statement execution errors per second on every database.|

## FAQ

**1. Why are some panes empty on this page?**

If a pane does not provide any metrics, the possible reasons are as follows:

- The workload of the corresponding cluster does not trigger this metric. For example, the failed query metric is always empty in the case of no failed queries.
- The cluster version is low. You need to upgrade it to the latest version of TiDB to see these metrics.

If all these reasons are excluded, you can contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.

**2. Why might metrics be discontinuous in rare cases?**

In some rare cases, metrics might be lost, such as when the metrics system experiences high pressure.

If you encounter this problem, you can contact [PingCAP Support](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.
