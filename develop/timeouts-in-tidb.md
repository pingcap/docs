---
title: Timeouts in TiDB
summary: A brief introduction to the timeouts in TiDB to provide a basis for troubleshooting errors.
---

# Timeouts in TiDB

This chapter will describe the timeouts in TiDB to provide a basis for troubleshooting errors.

## GC Timeout

TiDB's transaction implementation uses MVCC (Multiple Version Concurrency Control) mechanism, when the newly written data overwrites the old data, the old data will not be replaced, but will be kept at the same time with the newly written data, and the version will be distinguished by the time stamp. TiDB cleans up the old data that is no longer needed by the mechanism of periodic GC.

By default, TiDB guarantees that each MVCC version (consistency snapshot) is kept for `10` minutes, and transactions that take longer than `10` minutes to read will receive an error that `GC life time is shorter than transaction duration`.

When you are sure you need longer read time, for example, in a scenario where you are using **Mydumper** for full backups (**Mydumper** backs up consistent snapshots), you can adjust the value of `tikv_gc_life_time` in the `mysql.tidb` table in TiDB to increase the MVCC version retention time, and note that `tikv_gc_life_time` is configured to have an immediate global impact; turning it up will increase the life time of all currently existing snapshots, and turning it down will immediately shorten the life time of all snapshots. Too many MVCC versions will slow down TiKV's processing efficiency, so you need to adjust `tikv_gc_life_time` back to the previous setting in time after doing a full volume backup with **Mydumper**.

For more information about GC, please refer to the [GC Overview](https://docs.pingcap.com/tidb/stable/garbage-collection-overview) document.

## Transaction Timeout

**Garbage Collection (GC)** does not affect ongoing transactions. However, there is still an upper limit to the number of pessimistic transactions that can run, with a limit based on transaction timeout (modified by `max-txn-ttl` under the `[performance]` category of the TiDB profile, which defaults to `60` minutes) and a limit based on the memory used by the transaction.

SQL statements such as `INSERT INTO t10 SELECT * FROM t1` are not affected by GC, but will be rolled back due to timeout after exceeding `max-txn-ttl`.

## SQL Execution Timeout

TiDB also provides a system variable to limit the execution time of a single SQL statement: max_execution_time, which defaults to `0`, indicating no limit. `max_execution_time` currently takes effect for all types of statements, not just `SELECT` statements. The unit is `ms`, but the actual precision is at the `100ms` level, not the more accurate millisecond level.

## JDBC Query Timeout

MySQL JDBC's query timeout setting `setQueryTimeout()` does **_NOT_** work for TiDB. This is because real clients send a `KILL` command to the database when they sense the timeout. But since the tidb-server is load balanced, the tidb-server will not execute this `KILL` to prevent termination of the connection on the wrong tidb-server, so you have to use `MAX_EXECUTION_TIME` to achieve the query timeout effect.

TiDB provides 3 MySQL-compatible timeout control parameters.

- **wait_timeout**, which controls the non-interactive idle timeout for connections to Java applications, defaults to `0`, which allows connections to be idle indefinitely.
- **interactive_timeout**, controls the interactive idle timeout for connections to Java applications, the default value is `8 hours`.
- **max_execution_time**, controls the timeout for SQL execution in the connection, the default value is `0`, i.e. the connection is allowed to be infinitely busy (an SQL statement is executed for an infinitely long time).

However, in a real production environment, idle connections and SQL that keeps executing indefinitely have a bad effect on both the database and the application. You can avoid idle connections and SQL statements that take too long to execute by configuring these two session-level variables in your application's connection string. For example, set `sessionVariables=wait_timeout=3600` (1 hour) and `sessionVariables=max_execution_time=300000` (5 minutes).
