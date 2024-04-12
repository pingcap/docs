---
title: Timeouts in TiDB
summary: Learn about timeouts in TiDB, and solutions for troubleshooting errors.
---

# Timeouts in TiDB

This document describes various timeouts in TiDB to help you troubleshoot errors.

## Transaction timeout

GC does not affect ongoing transactions. However, there is still an upper limit to the number of pessimistic transactions that can run, with a limit on the transaction timeout and a limit on the memory used by the transaction. You can modify the transaction timeout by `max-txn-ttl` under the `[performance]` category of the TiDB profile, `60` minutes by default.

SQL statements such as `INSERT INTO t10 SELECT * FROM t1` are not affected by GC, but will be rolled back due to timeout after exceeding `max-txn-ttl`.

## SQL execution timeout

TiDB also provides a system variable (`max_execution_time`, `0` by default, indicating no limit) to limit the execution time of a single SQL statement. Currently, the system variable only takes effect for read-only SQL statements. The unit of `max_execution_time` is `ms`, but the actual precision is at the `100ms` level instead of the millisecond level.

## JDBC query timeout

MySQL JDBC's query timeout setting for `setQueryTimeout()` does **_NOT_** work for TiDB, because the client sends a `KILL` command to the database when it detects the timeout. However, the tidb-server is load balanced, and it will not execute this `KILL` command to avoid termination of the connection on a wrong tidb-server. You need to use `MAX_EXECUTION_TIME` to check the query timeout effect.

TiDB provides the following MySQL-compatible timeout control parameters.

- **wait_timeout**, controls the non-interactive idle timeout for the connection to Java applications. Since TiDB v5.4, the default value of `wait_timeout` is `28800` seconds, which is 8 hours. For TiDB versions earlier than v5.4, the default value is `0`, which means the timeout is unlimited.
- **interactive_timeout**, controls the interactive idle timeout for the connection to Java applications. The value is `8 hours` by default.
- **max_execution_time**, controls the timeout for SQL execution in the connection, only effective for read-only SQL statements. The value is `0` by default, which allows the connection to be infinitely busy, that is, an SQL statement is executed for an infinitely long time.

However, in a real production environment, idle connections and indefinitely executing SQL statements have a negative effect on both the database and the application. You can avoid idle connections and indefinitely executing SQL statements by configuring these two session-level variables in your application's connection string. For example, set the following:

- `sessionVariables=wait_timeout=3600` (1 hour)
- `sessionVariables=max_execution_time=300000` (5 minutes)
