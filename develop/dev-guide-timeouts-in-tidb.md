---
title: Timeouts in TiDB
summary: Learn about timeouts in TiDB, and solutions for troubleshooting errors.
---

# Timeouts in TiDB

This document describes various timeouts in TiDB to help you troubleshoot errors.

## GC timeout

TiDB's transaction implementation uses the MVCC (Multiple Version Concurrency Control) mechanism. When the newly written data overwrites the old data, the old data will not be replaced, but kept together with the newly written data. The versions are distinguished by the timestamp. TiDB uses the mechanism of periodic Garbage Collection (GC) to clean up the old data that is no longer needed.

- For TiDB versions earlier than v4.0:

    By default, each MVCC version (consistency snapshots) is kept for 10 minutes. Transactions that take longer than 10 minutes to read will receive an error `GC life time is shorter than transaction duration`.

- For TiDB v4.0 and later versions:

    For running transactions that do not exceed a duration of 24 hours, garbage collection (GC) are blocked during the transaction execution. The error `GC life time is shorter than transaction duration` does not occur.

If you need longer read time temporarily in some cases, you can increase the retention time of MVCC versions:

- For TiDB versions earlier than v5.0: adjust `tikv_gc_life_time` in the `mysql.tidb` table in TiDB.
- For TiDB v5.0 and later versions: adjust the system variable [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50).

Note that the system variable configuration takes effect globally and immediately. Increasing its value will increase the life time of all existing snapshots, and decreasing it will immediately shorten the life time of all snapshots. Too many MVCC versions will impact the performance of the TiDB cluster. So you need to change this variable back to the previous setting in time.

<CustomContent platform="tidb">

> **Tip:**
>
> Specifically, when Dumpling is exporting data from TiDB (less than 1 TB), if the TiDB version is later than or equal to v4.0.0 and Dumpling can access the PD address of the TiDB cluster, Dumpling automatically extends the GC time without affecting the original cluster.
>
> However, in either of the following scenarios, Dumpling cannot automatically adjust the GC time:
>
> - The data size is very large (more than 1 TB).
> - Dumpling cannot connect directly to PD, for example, the TiDB cluster is on TiDB Cloud or on Kubernetes that is separated from Dumpling.
>
> In such scenarios, you must manually extend the GC time in advance to avoid export failure due to GC during the export process.
>
> For more details, see [Manually set the TiDB GC time](/dumpling-overview.md#manually-set-the-tidb-gc-time).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Tip:**
>
> Specifically, when Dumpling is exporting data from TiDB (less than 1 TB), if the TiDB version is later than or equal to v4.0.0 and Dumpling can access the PD address of the TiDB cluster, Dumpling automatically extends the GC time without affecting the original cluster.
>
> However, in either of the following scenarios, Dumpling cannot automatically adjust the GC time:
>
> - The data size is very large (more than 1 TB).
> - Dumpling cannot connect directly to PD, for example, the TiDB cluster is on TiDB Cloud or on Kubernetes that is separated from Dumpling.
>
> In such scenarios, you must manually extend the GC time in advance to avoid export failure due to GC during the export process.
>
> For more details, see [Manually set the TiDB GC time](https://docs.pingcap.com/tidb/stable/dumpling-overview#manually-set-the-tidb-gc-time).

</CustomContent>

For more information about GC, see [GC Overview](/garbage-collection-overview.md).

## Transaction timeout

GC does not affect ongoing transactions. However, there is still an upper limit to the number of pessimistic transactions that can run, with a limit on the transaction timeout and a limit on the memory used by the transaction. You can modify the transaction timeout by `max-txn-ttl` under the `[performance]` category of the TiDB profile, `60` minutes by default.

SQL statements such as `INSERT INTO t10 SELECT * FROM t1` are not affected by GC, but will be rolled back due to timeout after exceeding `max-txn-ttl`.

## SQL execution timeout

TiDB also provides a system variable (`max_execution_time`, `0` by default, indicating no limit) to limit the execution time of a single SQL statement. `max_execution_time` currently takes effect for all types of statements, not just the `SELECT` statements. The unit is `ms`, but the actual precision is at the `100ms` level instead of the millisecond level.

## JDBC query timeout

MySQL JDBC's query timeout setting for `setQueryTimeout()` does **_NOT_** work for TiDB, because the client sends a `KILL` command to the database when it detects the timeout. However, the tidb-server is load balanced, and it will not execute this `KILL` command to avoid termination of the connection on a wrong tidb-server. You need to use `MAX_EXECUTION_TIME` to check the query timeout effect.

TiDB provides the following MySQL-compatible timeout control parameters.

- **wait_timeout**, controls the non-interactive idle timeout for the connection to Java applications. Since TiDB v5.4, the default value of `wait_timeout` is `28800` seconds, which is 8 hours. For TiDB versions earlier than v5.4, the default value is `0`, which means the timeout is unlimited.
- **interactive_timeout**, controls the interactive idle timeout for the connection to Java applications. The value is `8 hours` by default.
- **max_execution_time**, controls the timeout for SQL execution in the connection. The value is `0` by default, which allows the connection to be infinitely busy, that is, an SQL statement is executed for an infinitely long time.

However, in a real production environment, idle connections and indefinitely executing SQL statements have a negative effect on both the database and the application. You can avoid idle connections and indefinitely executing SQL statements by configuring these two session-level variables in your application's connection string. For example, set the following:

- `sessionVariables=wait_timeout=3600` (1 hour)
- `sessionVariables=max_execution_time=300000` (5 minutes)
