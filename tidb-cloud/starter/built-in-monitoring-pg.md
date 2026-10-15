---
title: Built-in Metrics for PostgreSQL-Compatible TiDB Cloud Starter
summary: Learn about the built-in metrics available for PostgreSQL-compatible TiDB Cloud Starter instances.
---

# Built-in Metrics for PostgreSQL-Compatible TiDB Cloud Starter

TiDB Cloud collects and displays a full set of standard metrics of your TiDB resource on the Metrics page. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

## View the Metrics page

To view the metrics on the **Metrics** page, take the following steps:

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target resource to go to its overview page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the left navigation pane, click **Monitoring** > **Metrics**.

## Metrics retention policy

In TiDB Cloud, the metrics data is kept for 7 days.

## Metrics for PostgreSQL-compatible {{{ .starter }}} Instances

The following sections illustrate the metrics on the **Metrics** page for PostgreSQL-compatible {{{ .starter }}} instances.

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Used Storage Size | Row-based storage, Row-based standard storage, Columnar storage | The size of row-based storage, row-based standard storage, and columnar storage. TiDB Cloud displays this metric only when the size of each storage type is 50 MiB or larger. **Row-based standard storage** has the same meaning as **Row-based storage**. |
| Query Per Second | All, {SQL type} | The number of SQL statements executed per second, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Query Duration | Avg, P99, P99-{SQL type} | The duration from receiving a request from the client to the {{{ .starter }}} instance until the instance executes the request and returns the result to the client. |
| Total Connection | All | The number of connections to the {{{ .starter }}} instance. |

## FAQ

**1. Why are some panes empty on this page?**

Check that the selected time range includes activity on your instance. If the charts remain empty, contact [PingCAP Support](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.

**2. Why might metrics be discontinuous in rare cases?**

In some rare cases, metrics might be lost, such as when the metrics system experiences high pressure.

If you encounter this problem, you can contact [PingCAP Support](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.
