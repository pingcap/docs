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
> In a distributed TiDB database, a variable's `GLOBAL` setting is persisted to the storage layer. A single TiDB instance proactively gets the `GLOBAL` information and forms `gvc` (global variables cache) every 2 seconds. The cache information remains valid within 2 seconds. When you set the `GLOBAL` variable, to ensure the effectiveness of new sessions, make sure that the interval between two operations is larger than 2 seconds. For details, see [Issue #14531](https://github.com/pingcap/tidb/issues/14531).

### Set Session variables

<<<<<<< HEAD
Add the `SESSION` keyword before the variable, use `@@session.` as the modifier, or use no modifier:
=======
- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `partial` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.

### tidb_index_join_batch_size

- Scope: SESSION | GLOBAL
- Default value: 25000
- This variable is used to set the batch size of the `index lookup join` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_join_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `index lookup join` algorithm.

### tidb_index_lookup_size

- Scope: SESSION | GLOBAL
- Default value: 20000
- This variable is used to set the batch size of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_serial_scan_concurrency

- Scope: SESSION | GLOBAL
- Default value: 1
- This variable is used to set the concurrency of the `serial scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_init_chunk_size

- Scope: SESSION | GLOBAL
- Default value: 32
- Range: 1 - 32
- This variable is used to set the number of rows for the initial chunk during the execution process.

### tidb_isolation_read_engines <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: tikv, tiflash, tidb
- This variable is used to set the storage engine list that TiDB can use when reading data.

### tidb_low_resolution_tso

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to enable the low precision TSO feature. After this feature is enabled, new transactions use a timestamp updated every 2 seconds to read data.
- The main applicable scenario is to reduce the overhead of acquiring TSO for small read-only transactions when reading old data is acceptable.

### tidb_max_chunk_size

- Scope: SESSION | GLOBAL
- Default value: 1024
- Minimum value: 32
- This variable is used to set the maximum number of rows in a chunk during the execution process. Setting to too large of a value may cause cache locality issues.

### tidb_max_delta_schema_count <span class="version-mark">New in v2.1.18 and v3.0.5</span>

- Scope: GLOBAL
- Default value: 1024
- This variable is used to set the maximum number of schema versions (the table IDs modified for corresponding versions) allowed to be cached. The value range is 100 ~ 16384.

### tidb_mem_quota_query

- Scope: SESSION
- Default value: 1 GB
- This variable is used to set the threshold value of memory quota for a query.
- If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file. The initial value of this variable is configured by [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query).

### tidb_metric_query_range_duration <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 60
- This variable is used to set the range duration of the Prometheus statement generated when querying METRIC_SCHEMA. The unit is second.

### tidb_metric_query_step <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 60
- This variable is used to set the step of the Prometheus statement generated when querying `METRIC_SCHEMA`. The unit is second.

### tidb_opt_agg_push_down

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join.
- When the aggregate operation is slow in query, you can set the variable value to 1.

### tidb_opt_correlation_exp_factor

- Scope: SESSION | GLOBAL
- Default value: 1
- When the method that estimates the number of rows based on column order correlation is not available, the heuristic estimation method is used. This variable is used to control the behavior of the heuristic method.
    - When the value is 0, the heuristic method is not used.
    - When the value is greater than 0:
        - A larger value indicates that an index scan will probably be used in the heuristic method.
        - A smaller value indicates that a table scan will probably be used in the heuristic method.

### tidb_opt_correlation_threshold

- Scope: SESSION | GLOBAL
- Default value: 0.9
- This variable is used to set the threshold value that determines whether to enable estimating the row count by using column order correlation. If the order correlation between the current column and the `handle` column exceeds the threshold value, this method is enabled.

### tidb_opt_distinct_agg_push_down

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function with `distinct` (such as `select count(distinct a) from t`) to Coprocessor.
- When the aggregate function with the `distinct` operation is slow in the query, you can set the variable value to `1`.

In the following example, before `tidb_opt_distinct_agg_push_down` is enabled, TiDB needs to read all data from TiKV and execute `distinct` on the TiDB side. After `tidb_opt_distinct_agg_push_down` is enabled, `distinct a` is pushed down to Coprocessor, and a `group by` column `test.t.a` is added to `HashAgg_5`.
>>>>>>> 55ecb13... system-variables: remove the useless memory quota variables (#3947)

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
