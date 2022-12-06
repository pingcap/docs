---
title: TiFlash Query Result Materialization
summary: Learn how to save the query results of TiFlash in a transaction.
---

# TiFlash Query Result Materialization

> **Warning:**
>
> This is an experimental feature, which might be changed or removed without prior notice. The syntax and implementation might change before GA. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) in GitHub.

This document introduces how to save the TiFlash query result to a specified TiDB table in an `INSERT INTO SELECT` transaction.

Since v6.5.0, during the execution of the `INSERT INTO SELECT` statement, the query result of TiFlash can be saved to a specified TiDB table when TiDB pushes down the subquery in the `SELECT` clause to TiFlash, that is, the materialization of TiFlash query result. For TiDB versions earlier than v6.5.0, the query results of TiFlash are read-only, so if you want to save TiFlash query results, you have to obtain them from the application level, and then save them in a separate transaction or process.

> **Note:**
>
> - By default ([`tidb_allow_mpp = ON`](/system-variables#tidb_allow_mpp-new-in-v50)), the TiDB optimizer intelligently chooses to push down queries to TiKV or TiFlash based on the query cost. To enforce that the queries are pushed down to TiFlash, you can set the system variable [`tidb_enforce_mpp`](/system-variables#tidb_enforce_mpp-new-in-v51) to `ON`.
> - During the experimental phase, this feature is disabled by default. To enable this feature, you can set the system variable [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables#tidb_enable_tiflash_read_for_write_stmt) to `ON`.

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

For example, you can save the query result from table `t1` in the `SELECT` clause to table `t2` with the following `INSERT INTO SELECT` statement:

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## Typical and recommended usage scenarios

- Efficient BI solutions

    For many BI applications, the analysis query requests are very heavy. For example, when a lot of users access and refresh a report at the same time, a BI application needs to handle a lot of concurrent query requests. To deal with this situation effectively, you can use `INSERT INTO SELECT` to save the query results of the report in a TiDB table. Then, the end users can query data directly from the result table when the report is refreshed, which avoids multiple repeated computations and analyses. Similarly, by saving historical analysis results, you can further reduce the computation volume for long-time historical data analysis. For example, if you have a report `A` that is used to analyze daily sales profit, you can save the results of report `A` to a result table `T` using `INSERT INTO SELECT`. Then, when you need to generate a report `B` to analyze the sales profit of the past month, you can directly use the daily analysis results in table `T`. This way not only greatly reduces the computation volume but also improves the query response speed and reduces the system load.

- Serving online applications with TiFlash

    The number of concurrent requests supported by TiFlash depends on the volume of data and complexity of the queries, but it typically does not exceed 100 QPS. You can use `INSERT INTO SELECT` to save TiFlash query results, and then use the query result tables to support highly concurrent online requests. The data in result tables can be updated in the background at a low frequency (for example, at an interval of 0.5 second), which is well below the TiFlash concurrency limit, while still maintaining a high level of data freshness.

## Execution process

* During the execution of the `INSERT INTO SELECT` statement, TiFlash first returns the query results of the `SELECT` clause to a TiDB server node in the cluster, and then writes the results to the target table (which can have a TiFlash replica).
* The execution of the `INSERT INTO SELECT` statement guarantees ACID properties.

## Restrictions

* TiDB has a memory limit on the `INSERT INTO SELECT` statement. You can adjust the limit using the system variable [`tidb_mem_quota_query`](/system-variables#tidb_mem_quota_query).

    For more information, see [TiDB memory control](/configure-memory-usage.md).

* TiDB has no hard limit on the concurrency of the `INSERT INTO SELECT` statement, but it is recommended to consider the following practices:

    * When a "write transaction" is large, such as close to 1 GiB, it is recommended to control concurrency to no more than 10.
    * When a "write transaction" is small, such as less than 100 MiB, it is recommended to control concurrency to no more than 30.
    * Determine the concurrency based on testing results and specific circumstances.