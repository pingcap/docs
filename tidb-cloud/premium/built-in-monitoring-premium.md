---
title: "{{{ .premium }}} Built-in Metrics"
summary: Learn how to view {{{ .premium }}} built-in metrics and understand the meanings of these metrics.
---

# {{{ .premium }}} Built-in Metrics

TiDB Cloud collects and displays a full set of standard metrics of your cluster on the Metrics page. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

## View the Metrics page

To view the metrics on the **Metrics** page, take the following steps:

1. On the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and TiDB instances.

2. In the left navigation pane, click **Monitoring** > **Metrics**.

## Metrics retention policy

For TiDB Cloud instances, the metrics data is kept for 7 days.

## Metrics for {{{ .premium }}} Instances

The following sections illustrate the metrics on the **Metrics** page for {{{ .premium }}} instances.

### Overview

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Request Units per Second | Total RU per second | The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. In addition to queries that you run, request units can be consumed by background activities, so when the QPS is 0, the request units per second may not be zero. |
| Used Storage Size | {type} | The size of the row store and the size of the column store. |
| Query Per Second | All, {SQL type} | The number of SQL statements executed per second in all TiDB instances, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Query Duration | avg, avg-{SQL type}, 99, 99-{SQL type} | The duration from receiving a request from the client to TiDB until TiDB executes the request and returns the result to the client. |
| Database Time by SQL Types | All, {SQL type} | All: total database time per second. <br/> {SQL type}: database time consumed by SQL statements per second, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Failed Queries | All | The statistics of error types (such as syntax errors and primary key conflicts) according to the SQL statement execution errors per minute. |
| Command Per Second | {type} | The number of commands processed by all TiDB instances per second based on command types. |
| Queries Using Plan Cache OPS | hit, miss | hit: the number of queries using plan cache per second in all TiDB instances. <br/> miss: the number of queries missing plan cache per second in all TiDB instances. |
| Transaction Per Second | {types}-{transaction model} | The number of transactions executed per second. |
| Transaction Duration | avg-{transaction model}, 99-{transaction model} | The average or the 99th percentile duration of transactions. |
| Connection Count | All, active connection | All: the number of connections to all TiDB instances. <br/> Active connections: the number of active connections to all TiDB instances. |
| Disconnection Count | {result} | The number of clients disconnected to all TiDB instances. |

### Database

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| QPS Per DB | All, {database} | The number of SQL statements executed per second on every database, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Query Duration Per DB | avg, avg-{database}, 99, 99-{database} | The duration from receiving a request from the client to a database until the database executes the request and returns the result to the client. |
| Failed Query Per DB | All, {database} | The statistics of error types according to the SQL statement execution errors per second on every database. |

### Advanced

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Average Idle Connection Duration | avg-in-txn, avg-not-in-txn | The connection idle duration indicates the duration of a connection being idle.<br/> avg-in-txn: The average connection idle duration when a connection is within a transaction. <br/>avg-not-in-txn: The average connection idle duration when a connection is not within a transaction. |
| Get Token Duration | avg, 99 | The average or the 99th percentile duration consumed in getting tokens of SQL statements. |
| Parse Duration | avg, 99 | The average or the 99th percentile duration consumed in parsing SQL statements. |
| Compile Duration | avg, 99 | The average or the 99th percentile duration consumed in compiling the parsed SQL AST to execution plans. |
| Execute Duration | avg, 99 | The average or the 99th percentile duration consumed in executing execution plans of SQL statements. |
| Average TiDB KV Request Duration | {Request Type} | The average time consumed in executing KV requests in all TiDB instances based on request types, such as `Get`, `Prewrite`, and `Commit`. |
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99, rpc-avg/99 | Wait: the average or the 99th percentile duration in waiting for PD to return TSO in all TiDB instances. <br/> RPC: the average time or the 99th percentile of duration from sending TSO requests to PD to receiving TSO in all TiDB instances. |

## FAQ

**1. Why are some panes empty on this page?**

If a pane does not provide any metrics, the possible reasons are as follows:

- The workload of the corresponding cluster does not trigger this metric. For example, the failed query metric is always empty in the case of no failed queries.
- The cluster version is low. You need to upgrade it to the latest version of TiDB to see these metrics.

If all these reasons are excluded, you can contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.

**2. Why might metrics be discontinuous in rare cases?**

In some rare cases, metrics might be lost, such as when the metrics system experiences high pressure.

If you encounter this problem, you can contact [PingCAP Support](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.
