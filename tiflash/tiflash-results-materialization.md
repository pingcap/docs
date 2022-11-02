---
title: TiFlash Query Result Materialization
summary: Introduce how to save the query results of TiFlash in the same transaction.
---

# TiFlash Query Result Materialization

> **Warning:**
>
> Currently, this feature is experimental and its form and usage may change in future releases.

This document introduces how to save TiFlash query results to a specified TiDB table in the same `INSERT INTO SELECT` transaction.

Since v6.4.0, during the execution of the `INSERT INTO SELECT` statement, the query result of TiFlash can be saved to a specified TiDB table when TiDB pushes down the subquery in the `SELECT` clause to TiFlash, that is, the materialization of TiFlash query result. For TiDB versions earlier than v6.4.0, the query results of TiFlash are read-only, so if you want to save TiFlash query results, you have to obtain them at the application level, and then save them in a separate transaction or process.

> **Note:**
>
> By default ([`tidb_allow_mpp = ON`](/system-variables#tidb_allow_mpp-new-in-v50)), the TiDB optimizer will intelligently choose to push down queries to TiKV or to TiFlash based on the query cost. To enforce that the queries are pushed down to TiFlash, you can set the system variable [`tidb_enforce_mpp = ON`](/system-variables#tidb_enforce_mpp-new-in-v51).

The syntax of `INSERT INTO SELECT` is as follows.

```sql
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    SELECT ...
    [ON DUPLICATE KEY UPDATE assignment_list]value:
    {expr | DEFAULT}

assignment:
    col_name = valueassignment_list:
    assignment [, assignment] ...
```

For example, you can save the query results from table `t1` in the `SELECT` clause to table `t2` with the following `INSERT INTO SELECT` statement:

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## Typical and recommended usage scenarios

- Efficient BI solutions

    For many reporting applications, the analysis query requests are usually very heavy. If a lot of users access and refresh reports at the same time, the query requests are getting even heavier. To address this issue effectively, you can use `INSERT INTO SELECT` to save report query results in TiDB tables. Then, you can query data direclty from the result tables when the reports are refreshed, which avoids multiple repeated computation and analysis. Similarly, by saving the historical analysis results, you can further reduce the computation volume for long-time historical data analysis. For example, if report `A` is used to analyze daily sales profit, you can use `INSERT INTO SELECT` to save the daily analysis results of report `A` to a result table `T`. Then, when generating report `B` to analyze the sales profit of the last month, you can directly use the daily analysis results data in table `T`. This way not only greatly reduces the computation volume but also improves the query response speed and reduces the system load.

- Serving online applications with TiFlash

    The number of concurrent requests supported by TiFlash depends on the volume of data and complexity of the queries, but it typically does not exceed 100 QPS. You can use `INSERT INTO SELECT` to save TiFlash query results and then use the query result tables to support highly concurrent online requests. The data in result tables can be updated in the background at a low frequency, for example at the 0.5 second interval, which is well below TiFlash concurrency limit, while still maintaining a high level of data freshness.

## Execution Process

* During the execution of the `INSERT INTO SELECT` statement, TiFlash first returns the query results of the `SELECT` clause to a TiDB server node in the cluster, and then writes the resutls to the target table (which can have a TiFlash replica).
* The execution of the `INSERT INTO SELECT` statement guarantees ACID properties.

## Restrictions

* TiDB has a hard limit of 1 GiB on the size of the results returned by the `SELECT` clause (that is, the size of the write transaction `INSERT`). The recommended usage scenario is under 100 MiB.

    If the size of results returned by `SELECT` exceeds 1 GiB, the statement is forced to terminated and TiDB returns the `The query produced a too large intermediate result and thus failed` error.

* TiDB has no hard limit on the concurrency of the `INSERT INTO SELECT` statement, but it is recommended to consider the following practices.

    * When a "write transaction" is large, such as close to 1 GiB, it is recommended to control concurrency to no more than 10.
    * When a "write transaction" is small, such as less than 100 MiB, it is recommended to control concurrency to no more than 30.
    * Determine the concurrency based on testing results and specific circumstances.