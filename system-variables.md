---
title: The System Variables
summary: Learn how to use the system variables in TiDB.
aliases: ['/docs/v3.0/system-variables/','/docs/v3.0/reference/configuration/tidb-server/mysql-variables/','/docs/sql/variable/']
---

# The System Variables

The system variables in MySQL are the system parameters that modify the operation of the database runtime. These variables have two types of scope, Global Scope and Session Scope. TiDB supports all the system variables in MySQL 5.7. Most of the variables are only supported for compatibility and do not affect the runtime behaviors.

<<<<<<< HEAD
## Set the system variables
=======
```sql
# These two identical statements change a session variable
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# These two identical statements change a global variable
SET @@global.tidb_distsql_scan_concurrency = 10;
SET  GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **Note:**
>
> TiDB differs from MySQL in that `GLOBAL` scoped variables **persist** through TiDB server restarts. Changes are also propagated to other TiDB servers every 2 seconds [TiDB #14531](https://github.com/pingcap/tidb/issues/14531).
> Additionally, TiDB presents several MySQL variables from MySQL 5.7 as both readable and settable. This is required for compatibility, since it is common for both applications and connectors to read MySQL variables. For example: JDBC connectors both read and set query cache settings, despite not relying on the behavior.

## Variable Reference

### autocommit

- Scope: SESSION | GLOBAL
- Default value: ON
- Whether automatically commit a transaction.

### ddl_slow_threshold

- Scope: SESSION
- Default value: 300
- DDL operations whose execution time exceeds the threshold value are output to the log. The unit is millisecond.

### foreign_key_checks

- Scope: NONE
- Default value: OFF
- For compatibility, TiDB returns foreign key checks as OFF.

### hostname

- Scope: NONE
- Default value: (system hostname)
- The hostname of the TiDB server as a read-only variable.

### innodb_lock_wait_timeout

- Scope: SESSION | GLOBAL
- Default value: 50
- The lock wait timeout for pessimistic transactions (default) in seconds.

### last_plan_from_cache <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 0
- This variable is used to show whether the execution plan used in the previous `execute` statement is taken directly from the plan cache.

### max_execution_time

- Scope: SESSION | GLOBAL
- Default value: 0
- The maximum execution time of a statement in milliseconds. The default value is unlimited (zero).

> **Note:**
>
> Unlike in MySQL, the `max_execution_time` system variable currently works on all kinds of statements in TiDB, not only restricted to the `SELECT` statement. The precision of the timeout value is roughly 100ms. This means the statement might not be terminated in accurate milliseconds as you specify.

### `interactive_timeout`

- Scope: SESSION | GLOBAL
- Default value: 28800
- This variable represents the idle timeout of the interactive user session, which is measured in seconds. Interactive user session refers to the session established by calling [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API using the `CLIENT_INTERACTIVE` option (for example, MySQL shell client). This variable is fully compatible with MySQL.

### sql_mode

- Scope: SESSION | GLOBAL
- Default value: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- This variable controls a number of MySQL compatibility behaviors. See [SQL Mode](/sql-mode.md) for more information.

### sql_select_limit <span class="version-mark">New in v4.0.2 version</span>

- Scope: SESSION | GLOBAL
- Default value: `2^64 - 1` (18446744073709551615)
- The maximum number of rows returned by the `SELECT` statements.

### tidb_allow_batch_cop <span class="version-mark">New in v4.0 version</span>

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to control how TiDB sends a coprocessor request to TiFlash. It has the following values:

    * `0`: Never send requests in batches
    * `1`: Aggregation and join requests are sent in batches
    * `2`: All coprocessor requests are sent in batches
>>>>>>> ffaf67f... system-variables: add variable description (#3672)

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

> **Note:**
>
> Unlike in MySQL, the `max_execution_time` system variable currently works on all kinds of statements in TiDB, not only restricted to the `SELECT` statement. The precision of the timeout value is roughly 100ms. This means the statement might not be terminated in accurate milliseconds as you specify.

## TiDB specific system variables

See [TiDB Specific System Variables](/tidb-specific-system-variables.md).
