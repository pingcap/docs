---
title: The System Variables
summary: Learn how to use the system variables in TiDB.
aliases: ['/docs/v3.0/system-variables/','/docs/v3.0/reference/configuration/tidb-server/mysql-variables/','/docs/sql/variable/']
---

# The System Variables

The system variables in MySQL are the system parameters that modify the operation of the database runtime. These variables have two types of scope, Global Scope and Session Scope. TiDB supports all the system variables in MySQL 5.7. Most of the variables are only supported for compatibility and do not affect the runtime behaviors.

## Set the system variables

You can use the [`SET`](/sql-statements/sql-statement-set-variable.md) statement to change the value of the system variables. Before you change, consider the scope of the variable. For more information, see [MySQL Dynamic System Variables](https://dev.mysql.com/doc/refman/5.7/en/dynamic-system-variables.html).

### Set Global variables

Add the `GLOBAL` keyword before the variable or use `@@global.` as the modifier:

```sql
SET GLOBAL autocommit = 1;
SET @@global.autocommit = 1;
```

> **Note:**
>
<<<<<<< HEAD
> In a distributed TiDB database, a variable's `GLOBAL` setting is persisted to the storage layer. A single TiDB instance proactively gets the `GLOBAL` information and forms `gvc` (global variables cache) every 2 seconds. The cache information remains valid within 2 seconds. When you set the `GLOBAL` variable, to ensure the effectiveness of new sessions, make sure that the interval between two operations is larger than 2 seconds. For details, see [Issue #14531](https://github.com/pingcap/tidb/issues/14531).
=======
> Only the default value of `0` can be considered safe. Setting `tidb_enable_noop_functions=1` might lead to unexpected behaviors in your application, because it permits TiDB to ignore certain syntax without providing an error.

### tidb_enable_slow_log

- Scope: INSTANCE
- Default value: `1`
- This variable is used to control whether to enable the slow log feature. It is enabled by default.

### tidb_enable_stmt_summary <span class="version-mark">New in v3.0.4</span>

- Scope: SESSION | GLOBAL
- Default value: 1 (the value of the default configuration file)
- This variable is used to control whether to enable the statement summary feature. If enabled, SQL execution information like time consumption is recorded to the `information_schema.STATEMENTS_SUMMARY` system table to identify and troubleshoot SQL performance issues.

### tidb_enable_table_partition

- Scope: SESSION | GLOBAL
- Default value: "on"
- This variable is used to set whether to enable the `TABLE PARTITION` feature.
    - `off` indicates disabling the `TABLE PARTITION` feature. In this case, the syntax that creates a partition table can be executed, but the table created is not a partitioned one.
    - `on` indicates enabling the `TABLE PARTITION` feature for the supported partition types. Currently, it indicates enabling range partition, hash partition and range column partition with one single column.
    - `auto` functions the same way as `on` does.

- Currently, TiDB only supports range partition and hash partition.

### tidb_enable_telemetry <span class="version-mark">New in v4.0.2 version</span>

- Scope: GLOBAL
- Default value: 1
- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled. By setting the value to `0`, the telemetry collection is disabled. If the [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB configuration item is set to `false` on all TiDB instances, the telemetry collection is always disabled and this system variable will not take effect. See [Telemetry](/telemetry.md) for details.

### tidb_enable_vectorized_expression <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 1
- This variable is used to control whether to enable vectorized execution.

### tidb_enable_window_function

- Scope: SESSION | GLOBAL
- Default value: 1, indicating enabling the window function feature.
- This variable is used to control whether to enable the support for window functions. Note that window functions may use reserved keywords. This might cause SQL statements that could be executed normally cannot be parsed after upgrading TiDB. In this case, you can set `tidb_enable_window_function` to `0`.

### tidb_evolve_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: off
- This variable is used to control whether to enable the baseline evolution feature. For detailed introduction or usage , see [Baseline Evolution](/sql-plan-management.md#baseline-evolution).
- To reduce the impact of baseline evolution on the cluster, use the following configurations:
    - Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is 600s.
    - Set `tidb_evolve_plan_task_start_time` and `tidb_evolve_plan_task_end_time` to limit the time window. The default values are respectively `00:00 +0000` and `23:59 +0000`.

### tidb_evolve_plan_task_end_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Default value: 23:59 +0000
- This variable is used to set the end time of baseline evolution in a day.

### tidb_evolve_plan_task_max_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Default value: 600
- This variable is used to limit the maximum execution time of each execution plan in the baseline evolution feature. The unit is second.

### tidb_evolve_plan_task_start_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Default value: 00:00 +0000
- This variable is used to set the start time of baseline evolution in a day.

### tidb_expensive_query_time_threshold

- Scope: INSTANCE
- Default value: 60
- This variable is used to set the threshold value that determines whether to print expensive query logs. The unit is second. The difference between expensive query logs and slow query logs is:
    - Slow logs are printed after the statement is executed.
    - Expensive query logs print the statements that are being executed, with execution time exceeding the threshold value, and their related information.

### tidb_force_priority

- Scope: INSTANCE
- Default value: `NO_PRIORITY`
- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.
- You can set the value of this variable to `NO_PRIORITY`, `LOW_PRIORITY`, `DELAYED` or `HIGH_PRIORITY`.

### tidb_general_log

- Scope: INSTANCE
- Default value: 0
- This variable is used to set whether to record all the SQL statements in the log.

### tidb_hash_join_concurrency
>>>>>>> ba2fcf58... config: hide & deprecate enable-streaming (#4146)

### Set Session variables

Add the `SESSION` keyword before the variable, use `@@session.` as the modifier, or use no modifier:

```sql
SET SESSION autocommit = 1;
SET @@session.autocommit = 1;
SET @@autocommit = 1;
```

> **Note:**
>
> `LOCAL` and `@@local.` are the synonyms for `SESSION` and `@@session.`

### The working mechanism of system variables

* Session variables will only initialize their own values based on global variables when a session is created. Changing a global variable does not change the value of the system variable being used by the session that has already been created.

    ```sql
    mysql> SELECT @@GLOBAL.autocommit;
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | ON                  |
    +---------------------+
    1 row in set (0.00 sec)

    mysql> SELECT @@SESSION.autocommit;
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)

    mysql> SET GLOBAL autocommit = OFF;
    Query OK, 0 rows affected (0.01 sec)

    mysql> SELECT @@SESSION.autocommit; -- Session variables do not change, and the transactions in the session are executed in the form of autocommit.
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)

    mysql> SELECT @@GLOBAL.autocommit;
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | OFF                 |
    +---------------------+
    1 row in set (0.00 sec)

    mysql> exit
    Bye
    $ mysql -h127.0.0.1 -P4000 -uroot -D test
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 3
    Server version: 5.7.25-TiDB-None MySQL Community Server (Apache License 2.0)

    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> SELECT @@SESSION.autocommit; -- The newly created session uses a new global variable.
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | OFF                  |
    +----------------------+
    1 row in set (0.00 sec)
    ```

## The fully supported MySQL system variables in TiDB

The following MySQL system variables are fully supported in TiDB and have the same behaviors as in MySQL.

| Name | Scope | Description |
| ---------------- | -------- | -------------------------------------------------- |
| autocommit | GLOBAL \| SESSION | whether automatically commit a transaction|
| sql_mode | GLOBAL \| SESSION | support some of the MySQL SQL modes|
| time_zone | GLOBAL \| SESSION | the time zone of the database |
| tx_isolation | GLOBAL \| SESSION | the isolation level of a transaction |
| max\_execution\_time | GLOBAL \| SESSION | the execution timeout for a statement, in milliseconds |
| innodb\_lock\_wait\_timeout | GLOBAL \| SESSION | the lock wait time for pessimistic transactions, in seconds |
| interactive\_timeout | SESSION \| GLOBAL | the idle timeout of the interactive user session, in seconds   |

> **Note:**
>
> Unlike in MySQL, the `max_execution_time` system variable currently works on all kinds of statements in TiDB, not only restricted to the `SELECT` statement. The precision of the timeout value is roughly 100ms. This means the statement might not be terminated in accurate milliseconds as you specify.

## TiDB specific system variables

See [TiDB Specific System Variables](/tidb-specific-system-variables.md).
