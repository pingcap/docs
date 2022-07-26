---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
---

# System Variables

TiDB system variables behave similar to MySQL, in that settings apply on a `SESSION` or `GLOBAL` scope:

- Changes on a `SESSION` scope will only affect the current session.
- Changes on a `GLOBAL` scope apply immediately. If this variable is also`SESSION` scoped, all sessions (including your session) will continue to use their current session value.
- Changes are made using the [`SET` statement](/sql-statements/sql-statement-set-variable.md):

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
> Several `GLOBAL` variables persist to the TiDB cluster. Some variables in this document have a `Persists to cluster` setting, which can be configured to `Yes` or `No`.
>
> - For variables with the `Persists to cluster: Yes` setting, when a global variable is changed, a notification is sent to all TiDB servers to refresh their system variable cache. When you add additional TiDB servers or restart existing TiDB servers, the persisted configuration value is automatically used.
> - For variables with the `Persists to cluster: No` setting, changes only apply to the local TiDB instance that you are connected to. To retain any values set, you need to specify the variables in your `tidb.toml` configuration file.
>
> Additionally, TiDB presents several MySQL variables as both readable and settable. This is required for compatibility, because it is common for both applications and connectors to read MySQL variables. For example, JDBC connectors both read and set query cache settings, despite not relying on the behavior.

> **Note:**
>
> Larger values do not always yield better performance. It is also important to consider the number of concurrent connections that are executing statements, because most settings apply to each connection.
>
> Consider the unit of a variable when you determine safe values:
>
> * For threads, safe values are typically up to the number of CPU cores.
> * For bytes, safe values are typically less than the amount of system memory.
> * For time, pay attention that the unit might be seconds or milliseconds.
>
> Variables using the same unit might compete for the same set of resources.

## Variable Reference

### allow_auto_random_explicit_insert <span class="version-mark">New in v4.0.3</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- Determines whether to allow explicitly specifying the values of the column with the `AUTO_RANDOM` attribute in the `INSERT` statement.

### auto_increment_increment

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1`
- Range: `[1, 65535]`
- Controls the step size of `AUTO_INCREMENT` values to be allocated to a column. It is often used in combination with `auto_increment_offset`.

### auto_increment_offset

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1`
- Range: `[1, 65535]`
- Controls the initial offset of `AUTO_INCREMENT` values to be allocated to a column. This setting is often used in combination with `auto_increment_increment`. For example:

```sql
mysql> CREATE TABLE t1 (a int not null primary key auto_increment);
Query OK, 0 rows affected (0.10 sec)

mysql> set auto_increment_offset=1;
Query OK, 0 rows affected (0.00 sec)

mysql> set auto_increment_increment=3;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (),(),(),();
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+
| a  |
+----+
|  1 |
|  4 |
|  7 |
| 10 |
+----+
4 rows in set (0.00 sec)
```

### autocommit

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- Controls whether statements should automatically commit when not in an explicit transaction. See [Transaction Overview](/transaction-overview.md#autocommit) for more information.

### block_encryption_mode

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `aes-128-ecb`
- Defines the encryption mode for the `AES_ENCRYPT()` and `AES_DECRYPT()` functions.

### character_set_client

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4`
- The character set for data sent from the client. See [Character Set and Collation](/character-set-and-collation.md) for details on the use of character sets and collations in TiDB. It is recommended to use [`SET NAMES`](/sql-statements/sql-statement-set-names.md) to change the character set when needed.

### character_set_connection

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4`
- The character set for string literals that do not have a specified character set.

### character_set_database

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4`
- This variable indicates the character set of the default database in use. **It is NOT recommended to set this variable**. When a new default database is selected, the server changes the variable value.

### character_set_results

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4`
- The character set that is used when data is sent to the client.

### character_set_server

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4`
- The default character set for the server.

### collation_connection

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4_bin`
- This variable indicates the collation for string literals that do not have a specified collation.

### collation_database

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4_bin`
- This variable indicates the collation of the default database in use. **It is NOT recommended to set this variable**. When a new default database is selected, the server changes the variable value.

### collation_server

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `utf8mb4_bin`
- The default collation for the server.

### cte_max_recursion_depth

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1000`
- Range: `[0, 4294967295]`
- Controls the maximum recursion depth in Common Table Expressions.

### datadir

- Scope: NONE
- Default value: /tmp/tidb
- This variable indicates the location where data is stored. This location can be a local path or point to a PD server if the data is stored on TiKV.
- A value in the format of `ip_address:port` indicates the PD server that TiDB connects to on startup.

### ddl_slow_threshold

- Scope: GLOBAL
- Persists to cluster: No
- Default value: `300`
- Unit: Milliseconds
- Log DDL operations whose execution time exceeds the threshold value.

### default_authentication_plugin

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `mysql_native_password`
- Possible values: `mysql_native_password`, `caching_sha2_password`
- This variable sets the authentication method that the server advertises when the server-client connection is being established. Possible values for this variable are documented in [Authentication plugin status](/security-compatibility-with-mysql.md#authentication-plugin-status).
- Value options: `mysql_native_password` and `caching_sha2_password`. For more details, see [Authentication plugin status](/security-compatibility-with-mysql.md#authentication-plugin-status).

### default_week_format

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 7]`
- Sets the week format used by the `WEEK()` function.

### foreign_key_checks

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- For compatibility, TiDB returns foreign key checks as `OFF`.

### group_concat_max_len

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1024`
- Range: `[4, 18446744073709551615]`
- The maximum buffer size for items in the `GROUP_CONCAT()` function.

### have_openssl

- Scope: NONE
- Default value: `DISABLED`
- A read-only variable for MySQL compatibility. Set to `YES` by the server when the server has TLS enabled.

### have_ssl

- Scope: NONE
- Default value: `DISABLED`
- A read-only variable for MySQL compatibility. Set to `YES` by the server when the server has TLS enabled.

### hostname

- Scope: NONE
- Default value: (system hostname)
- The hostname of the TiDB server as a read-only variable.

### identity

This variable is an alias for `last_insert_id`.

### init_connect

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: ""
- The `init_connect` feature permits a SQL statement to be automatically executed when you first connect to a TiDB server. If you have the `CONNECTION_ADMIN` or `SUPER` privileges, this `init_connect` statement will not be executed. If the `init_connect` statement results in an error, your user connection will be terminated.

### innodb_lock_wait_timeout

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `50`
- Range: `[1, 3600]`
- Unit: Seconds
- The lock wait timeout for pessimistic transactions (default).

### interactive_timeout

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `28800`
- Range: `[1, 31536000]`
- Unit: Seconds
- This variable represents the idle timeout of the interactive user session. Interactive user session refers to the session established by calling [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API using the `CLIENT_INTERACTIVE` option (for example, MySQL Shell and MySQL Client). This variable is fully compatible with MySQL.

### last_insert_id

- Scope: SESSION
- Default value: `0`
- This variable returns the last `AUTO_INCREMENT` or `AUTO_RANDOM` value generated by an insert statement.
- The value of `last_insert_id` is the same as the value returned by the function `LAST_INSERT_ID()`.

### last_plan_from_binding <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to show whether the execution plan used in the previous statement was influenced by a [plan binding](/sql-plan-management.md)

### last_plan_from_cache <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to show whether the execution plan used in the previous `execute` statement is taken directly from the plan cache.

### license

- Scope: NONE
- Default value: `Apache License 2.0`
- This variable indicates the license of your TiDB server installation.

### log_bin

- Scope: NONE
- Type: Boolean
- Default value: `OFF`
- This variable indicates whether [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is used.

### max_allowed_packet

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `67108864`
- Range: `[1024, 1073741824]`
- Unit: Bytes
- The maximum size of a packet for the MySQL protocol.

### max_execution_time

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- Unit: Milliseconds
- The maximum execution time of a statement. The default value is unlimited (zero).

> **Note:**
>
> Unlike in MySQL, the `max_execution_time` system variable currently works on all kinds of statements in TiDB, not only restricted to the `SELECT` statement. The precision of the timeout value is roughly 100ms. This means the statement might not be terminated in accurate milliseconds as you specify.

### plugin_dir

- Scope: GLOBAL
- Persists to cluster: No
- Default value: ""
- Indicates the directory to load plugins as specified by a command-line flag.

### plugin_load

- Scope: GLOBAL
- Persists to cluster: No
- Default value: ""
- Indicates the plugins to load when TiDB is started. These plugins are specified by a command-line flag and separated by commas.

### port

- Scope: NONE
- Type: Integer
- Default value: `4000`
- Range: `[0, 65535]`
- The port that the `tidb-server` is listening on when speaking the MySQL protocol.

### rand_seed1

- Scope: SESSION
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- This variable is used to seed the random value generator used in the `RAND()` SQL function.
- The behavior of this variable is MySQL compatible.

### rand_seed2

- Scope: SESSION
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- This variable is used to seed the random value generator used in the `RAND()` SQL function.
- The behavior of this variable is MySQL compatible.

### require_secure_transport <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable ensures that all connections to TiDB are either on a local socket, or using TLS. See [Enable TLS between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md) for additional details.
- Setting this variable to `ON` requires you to connect to TiDB from a session that has TLS enabled. This helps prevent lock-out scenarios when TLS is not configured correctly.
- This setting was previously a `tidb.toml` option (`security.require-secure-transport`), but changed to a system variable starting from TiDB v6.1.0.

### skip_name_resolve <span class="version-mark">New in v5.2.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether the `tidb-server` instance resolves hostnames as a part of the connection handshake.
- When the DNS is unreliable, you can enable this option to improve network performance.

> **Note:**
>
> When `skip_name_resolve=ON`, users with a hostname in their identity will no longer be able to log into the server. For example:
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> In this example, it is recommended to replace `apphost` with an IP address or the wildcard (`%`).

### socket

- Scope: NONE
- Default value: ""
- The local unix socket file that the `tidb-server` is listening on when speaking the MySQL protocol.

### sql_log_bin

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- Indicates whether to write changes to [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) or not.

> **Note:**
>
> It is not recommended to set `sql_log_bin` as a global variable because the future versions of TiDB might only allow setting this as a session variable.

### sql_mode

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- This variable controls a number of MySQL compatibility behaviors. See [SQL Mode](/sql-mode.md) for more information.

### sql_select_limit <span class="version-mark">New in v4.0.2</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `18446744073709551615`
- Range: `[0, 18446744073709551615]`
- Unit: Rows
- The maximum number of rows returned by the `SELECT` statements.

### ssl_ca

- Scope: NONE
- Default value: ""
- The location of the certificate authority file (if there is one).

### ssl_cert

- Scope: NONE
- Default value: ""
- The location of the certificate file (if there is a file) that is used for SSL/TLS connections.

### ssl_key

- Scope: NONE
- Default value: ""
- The location of the private key file (if there is one) that is used for SSL/TLS connections.

### system_time_zone

- Scope: NONE
- Default value: (system dependent)
- This variable shows the system time zone from when TiDB was first bootstrapped. See also [`time_zone`](#time_zone).

### tidb_allow_batch_cop <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1`
- Range: `[0, 2]`
- This variable is used to control how TiDB sends a coprocessor request to TiFlash. It has the following values:

    * `0`: Never send requests in batches
    * `1`: Aggregation and join requests are sent in batches
    * `2`: All coprocessor requests are sent in batches

### tidb_allow_fallback_to_tikv <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: ""
- This variable is used to specify a list of storage engines that might fall back to TiKV. If the execution of a SQL statement fails due to a failure of the specified storage engine in the list, TiDB retries executing this SQL statement with TiKV. This variable can be set to "" or "tiflash". When this variable is set to "tiflash", if TiFlash returns a timeout error (error code: ErrTiFlashServerTimeout), TiDB retries executing this SQL statement with TiKV.

### tidb_allow_function_for_expression_index <span class="version-mark">New in v5.2.0</span>

- Scope: NONE
- Default value: `lower, md5, reverse, tidb_shard, upper, vitess_hash`
- This variable is used to show the functions that are allowed to be used for creating expression indexes.

### tidb_allow_mpp <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- Controls whether to use the MPP mode of TiFlash to execute queries. The value options are as follows:
    - `0` or `OFF`, which means that the MPP mode will not be used.
    - `1` or `ON`, which means that the optimizer determines whether to use the MPP mode based on the cost estimation (by default).

MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [Control whether to select the MPP mode](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode).

### tidb_allow_remove_auto_inc <span class="version-mark">New in v2.1.18 and v3.0.4</span>

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether the `AUTO_INCREMENT` property of a column is allowed to be removed by executing `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default.

### tidb_analyze_version <span class="version-mark">New in v5.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `2`
- Range: `[1, 2]`
- Controls how TiDB collects statistics.
- In v5.3.0 and later versions, the default value of this variable is `2`, which serves as an experimental feature. If your cluster is upgraded from a version earlier than v5.3.0 to v5.3.0 or later, the default value of `tidb_analyze_version` does not change. For detailed introduction, see [Introduction to Statistics](/statistics.md).

### tidb_auto_analyze_end_time

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Time
- Default value: `23:59 +0000`
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_auto_analyze_ratio

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Float
- Default value: `0.5`
- Range: `[0, 18446744073709551615]`
- This variable is used to set the threshold when TiDB automatically executes [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) in a background thread to update table statistics. For example, a value of 0.5 means that auto-analyze is triggered when greater than 50% of the rows in a table have been modified. Auto-analyze can be restricted to only execute during certain hours of the day by specifying `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.

> **Note:**
>
> This feature requires the system variable `tidb_enable_auto_analyze` set to `ON`.

### tidb_auto_analyze_start_time

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Time
- Default value: `00:00 +0000`
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1 AM and 3 AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### `tidb_max_auto_analyze_time` <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `43200`
- Range: `[0, 2147483647]`
- Unit: seconds
- This variable is used to specify the maximum execution time of automatic `ANALYZE` tasks. When the execution time of an automatic `ANALYZE` task exceeds the specified time, the task will be terminated. When the value of this variable is `0`, there is no limit to the maximum execution time of automatic `ANALYZE` tasks.

### tidb_backoff_lock_fast

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `10`
- Range: `[1, 2147483647]`
- This variable is used to set the `backoff` time when the read request meets a lock.

### tidb_backoff_weight

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `2`
- Range: `[0, 2147483647]`
- This variable is used to increase the weight of the maximum time of TiDB `backoff`, that is, the maximum retry time for sending a retry request when an internal network or other component (TiKV, PD) failure is encountered. This variable can be used to adjust the maximum retry time and the minimum value is 1.

    For example, the base timeout for TiDB to take TSO from PD is 15 seconds. When `tidb_backoff_weight = 2`, the maximum timeout for taking TSO is: *base time \* 2 = 30 seconds*.

    In the case of a poor network environment, appropriately increasing the value of this variable can effectively alleviate error reporting to the application end caused by timeout. If the application end wants to receive the error information more quickly, minimize the value of this variable.

### tidb_broadcast_join_threshold_count <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `10240`
- Range: `[0, 9223372036854775807]`
- Unit: Rows
- If the objects of the join operation belong to a subquery, the optimizer cannot estimate the size of the subquery result set. In this situation, the size is determined by the number of rows in the result set. If the estimated number of rows in the subquery is less than the value of this variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.

### tidb_broadcast_join_threshold_size <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `104857600` (100 MiB)
- Range: `[0, 9223372036854775807]`
- Unit: Bytes
- If the table size is less than the value of the variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.

### tidb_build_stats_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `4`
- Unit: Threads
- This variable is used to set the concurrency of executing the `ANALYZE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_capture_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the [baseline capturing](/sql-plan-management.md#baseline-capturing) feature. This feature depends on the statement summary, so you need to enable the statement summary before you use baseline capturing.
- After this feature is enabled, the historical SQL statements in the statement summary are traversed periodically, and bindings are automatically created for SQL statements that appear at least twice.

### tidb_check_mb4_value_in_utf8

- Scope: GLOBAL
- Persists to cluster: No
- Type: Boolean
- Default value: `ON`
- This variable is used to enforce that the `utf8` character set only stores values from the [Basic Multilingual Plane (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane). To store characters outside the BMP, it is recommended to use the `utf8mb4` character set.
- You might need to disable this option when upgrading your cluster from an earlier version of TiDB where the `utf8` checking was more relaxed. For details, see [FAQs After Upgrade](/faq/upgrade-faq.md).

### tidb_checksum_table_concurrency

- Scope: SESSION
- Default value: `4`
- Unit: Threads
- This variable is used to set the scan index concurrency of executing the `ADMIN CHECKSUM TABLE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_committer_concurrency <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `128`
- Range: `[1, 10000]`
- The number of goroutines for requests related to executing commit in the commit phase of the single transaction.
- If the transaction to commit is too large, the waiting time for the flow control queue when the transaction is committed might be too long. In this situation, you can increase the configuration value to speed up the commit.
- This setting was previously a `tidb.toml` option (`performance.committer-concurrency`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_config

- Scope: SESSION
- Default value: ""
- This variable is read-only. It is used to obtain the configuration information of the current TiDB server.

### tidb_constraint_check_in_place

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This setting only applies to optimistic transactions. When this variable is set to `OFF`, checking for duplicate values in UNIQUE indexes is deferred until the transaction commits. This helps improve performance, but might be an unexpected behavior for some applications. See [Constraints](/constraints.md) for details.

    - When set to zero and using optimistic transactions:

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- Check only when a transaction is committed.
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

    - When set to 1 and using optimistic transactions:

        ```sql
        tidb> set @@tidb_constraint_check_in_place=1;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

Constraint checking is always performed in place for pessimistic transactions (default).

### tidb_current_ts

- Scope: SESSION
- Default value: `0`
- This variable is read-only. It is used to obtain the timestamp of the current transaction.

### tidb_ddl_error_count_limit

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `512`
- Range: `[0, 9223372036854775807]`
- This variable is used to set the number of retries when the DDL operation fails. When the number of retries exceeds the parameter value, the wrong DDL operation is canceled.

### tidb_ddl_reorg_batch_size

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `256`
- Range: `[32, 10240]`
- Unit: Rows
- This variable is used to set the batch size during the `re-organize` phase of the DDL operation. For example, when TiDB executes the `ADD INDEX` operation, the index data needs to backfilled by `tidb_ddl_reorg_worker_cnt` (the number) concurrent workers. Each worker backfills the index data in batches.
    - If many updating operations such as `UPDATE` and `REPLACE` exist during the `ADD INDEX` operation, a larger batch size indicates a larger probability of transaction conflicts. In this case, you need to adjust the batch size to a smaller value. The minimum value is 32.
    - If the transaction conflict does not exist, you can set the batch size to a large value (consider the worker count. See [Interaction Test on Online Workloads and `ADD INDEX` Operations](/benchmark/online-workloads-and-add-index-operations.md) for reference). This can increase the speed of the backfilling data, but the write pressure on TiKV also becomes higher.

### tidb_ddl_reorg_priority

- Scope: SESSION
- Default value: `PRIORITY_LOW`
- This variable is used to set the priority of executing the `ADD INDEX` operation in the `re-organize` phase.
- You can set the value of this variable to `PRIORITY_LOW`, `PRIORITY_NORMAL` or `PRIORITY_HIGH`.

### tidb_ddl_reorg_worker_cnt

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `4`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the DDL operation in the `re-organize` phase.

### tidb_disable_txn_auto_retry

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to disable the automatic retry of explicit optimistic transactions. The default value of `ON` means that transactions will not automatically retry in TiDB and `COMMIT` statements might return errors that need to be handled in the application layer.

    Setting the value to `OFF` means that TiDB will automatically retry transactions, resulting in fewer errors from `COMMIT` statements. Be careful when making this change, because it might result in lost updates.

    This variable does not affect automatically committed implicit transactions and internally executed transactions in TiDB. The maximum retry count of these transactions is determined by the value of `tidb_retry_limit`.

    For more details, see [limits of retry](/optimistic-transaction.md#limits-of-retry).

    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is controlled by [`max_retry_count`](/tidb-configuration-file.md#max-retry-count).

### tidb_distsql_scan_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `15`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.
- For OLAP scenarios, the maximum value should not exceed the number of CPU cores of all the TiKV nodes.
- If a table has a lot of partitions, you can reduce the variable value appropriately (determined by the size of the data to be scanned and the frequency of the scan) to avoid TiKV becoming out of memory (OOM).

### tidb_dml_batch_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- Unit: Rows
- When this value is greater than `0`, TiDB will batch commit statements such as `INSERT` or `LOAD DATA` into smaller transactions. This reduces memory usage and helps ensure that the `txn-total-size-limit` is not reached by bulk modifications.
- Only the value `0` provides ACID compliance. Setting this to any other value will break the atomicity and isolation guarantees of TiDB.

### tidb_enable_1pc <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to specify whether to enable the one-phase commit feature for transactions that only affect one Region. Compared with the often-used two-phase commit, one-phase commit can greatly reduce the latency of transaction commit and increase the throughput.

> **Note:**
>
> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.
> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead.
> - Enabling this parameter only means that one-phase commit becomes an optional mode of transaction commit. In fact, the most suitable mode of transaction commit is determined by TiDB.

### tidb_enable_amend_pessimistic_txn <span class="version-mark">New in v4.0.7</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the `AMEND TRANSACTION` feature. If you enable the `AMEND TRANSACTION` feature in a pessimistic transaction, when concurrent DDL operations and SCHEMA VERSION changes exist on tables associated with this transaction, TiDB attempts to amend the transaction. TiDB corrects the transaction commit to make the commit consistent with the latest valid SCHEMA VERSION so that the transaction can be successfully committed without getting the `Information schema is changed` error. This feature is effective on the following concurrent DDL operations:

    - `ADD COLUMN` or `DROP COLUMN` operations.
    - `MODIFY COLUMN` or `CHANGE COLUMN` operations which increase the length of a field.
    - `ADD INDEX` or `DROP INDEX` operations in which the index column is created before the transaction is opened.

> **Note:**
>
> Currently, this feature is incompatible with TiDB Binlog in some scenarios and might cause semantic changes on a transaction. For more usage precautions of this feature, refer to [Incompatibility issues about transaction semantic](https://github.com/pingcap/tidb/issues/21069) and [Incompatibility issues about TiDB Binlog](https://github.com/pingcap/tidb/issues/20996).

### tidb_enable_async_commit <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the async commit feature for the second phase of the two-phase transaction commit to perform asynchronously in the background. Enabling this feature can reduce the latency of transaction commit.

> **Note:**
>
> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.
> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead.
> - Enabling this parameter only means that Async Commit becomes an optional mode of transaction commit. In fact, the most suitable mode of transaction commit is determined by TiDB.

### tidb_enable_auto_analyze <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- Determines whether TiDB automatically updates table statistics as a background operation.
- This setting was previously a `tidb.toml` option (`performance.run-auto-analyze`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_enable_auto_increment_in_generated

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to determine whether to include the `AUTO_INCREMENT` columns when creating a generated column or an expression index.

### tidb_enable_change_multi_schema

> **Warning:**
>
> TiDB will support more types of multi-schema changes in the future. This system variable will be deleted in a future release of TiDB.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether multiple columns or indexes can be altered in one `ALTER TABLE` statement. When the value of this variable is `ON`, only the following multi-schema changes are supported:
    - Add multiple columns. For example, `ATLER TABLE t ADD COLUMN c1 INT, ADD COLUMN c2 INT;`.
    - Drop multiple columns. For example, `ATLER TABLE t DROP COLUMN c1, DROP COLUMN c2;`.
    - Drop multiple indexes. For example, `ATLER TABLE t DROP INDEX i1, DROP INDEX i2;`.
    - Drop a column covered by a single-column index. For example, `ALTER TABLE t DROP COLUMN c1`, in which the schema contains `INDEX idx(c1)`.

### tidb_enable_cascades_planner

> **Warning:**
>
> Currently, cascades planner is an experimental feature. It is not recommended that you use it in production environments.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the cascades planner.

### tidb_enable_chunk_rpc <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the `Chunk` data encoding format in Coprocessor.

### tidb_enable_clustered_index <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `INT_ONLY`
- Possible values: `OFF`, `ON`, `INT_ONLY`
- This variable is used to control whether to create the primary key as a [clustered index](/clustered-indexes.md) by default. "By default" here means that the statement does not explicitly specify the keyword `CLUSTERED`/`NONCLUSTERED`. Supported values are `OFF`, `ON`, and `INT_ONLY`:
    - `OFF` indicates that primary keys are created as non-clustered indexes by default.
    - `ON` indicates that primary keys are created as clustered indexes by default.
    - `INT_ONLY` indicates that the behavior is controlled by the configuration item `alter-primary-key`. If `alter-primary-key` is set to `true`, all primary keys are created as non-clustered indexes by default. If it is set to `false`, only the primary keys which consist of an integer column are created as clustered indexes.

### tidb_enable_collect_execution_info

- Scope: GLOBAL
- Persists to cluster: No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to record the execution information of each operator in the slow query log.

### tidb_enable_column_tracking <span class="version-mark">New in v5.4.0</span>

> **Warning:**
>
> Currently, collecting statistics on `PREDICATE COLUMNS` is an experimental feature. It is not recommended that you use it in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable TiDB to collect `PREDICATE COLUMNS`. After enabling the collection, if you disable it, the information of previously collected `PREDICATE COLUMNS` is cleared. For details, see [Collect statistics on some columns](/statistics.md#collect-statistics-on-some-columns).

### tidb_enable_enhanced_security

- Scope: NONE
- Type: Boolean
- Default value: `OFF`
- This variable indicates whether the TiDB server you are connected to has the Security Enhanced Mode (SEM) enabled. To change its value, you need to modify the value of `enable-sem` in your TiDB server configuration file and restart the TiDB server.
- SEM is inspired by the design of systems such as [Security-Enhanced Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux). It reduces the abilities of users with the MySQL `SUPER` privilege and instead requires `RESTRICTED` fine-grained privileges to be granted as a replacement. These fine-grained privileges include:
    - `RESTRICTED_TABLES_ADMIN`: The ability to write data to system tables in the `mysql` schema and to see sensitive columns on `information_schema` tables.
    - `RESTRICTED_STATUS_ADMIN`: The ability to see sensitive variables in the command `SHOW STATUS`.
    - `RESTRICTED_VARIABLES_ADMIN`: The ability to see and set sensitive variables in `SHOW [GLOBAL] VARIABLES` and `SET`.
    - `RESTRICTED_USER_ADMIN`: The ability to prevent other users from making changes or dropping a user account.

### tidb_enable_fast_analyze

> **Warning:**
>
> Currently, `Fast Analyze` is an experimental feature. It is not recommended that you use it in production environments.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to enable the statistics `Fast Analyze` feature.
- If the statistics `Fast Analyze` feature is enabled, TiDB randomly samples about 10,000 rows of data as statistics. When the data is distributed unevenly or the data size is small, the statistics accuracy is low. This might lead to a non-optimal execution plan, for example, selecting a wrong index. If the execution time of the regular `Analyze` statement is acceptable, it is recommended to disable the `Fast Analyze` feature.

### tidb_enable_index_merge <span class="version-mark">New in v4.0</span>

> **Note:**
>
> - After upgrading a TiDB cluster from versions earlier than v4.0.0 to v5.4.0 or later, this variable is disabled by default to prevent performance regression due to changes of execution plans.
>
> - After upgrading a TiDB cluster from v4.0.0 or later to v5.4.0 or later, this variable remains the setting before the upgrade.
>
> - Since v5.4.0, for a newly deployed TiDB cluster, this variable is enabled by default.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the index merge feature.

### tidb_enable_legacy_instance_scope <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable permits `INSTANCE` scoped variables to be set using the `SET SESSION` as well as `SET GLOBAL` syntax.
- This option is enabled by default for compatibility with earlier versions of TiDB.

### tidb_enable_list_partition <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to enable the `LIST (COLUMNS) TABLE PARTITION` feature.

### tidb_enable_mutation_checker <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable TiDB mutation checker, which is a tool used to check consistency between data and indexes during the execution of DML statements. If the checker returns an error for a statement, TiDB rolls back the execution of the statement. Enabling this variable causes a slight increase in CPU usage. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md ).
- For new clusters of v6.0.0 or later versions, the default value is `ON`. For existing clusters that upgrade from versions earlier than v6.0.0, the default value is `OFF`.

### tidb_enable_new_only_full_group_by_check <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `OFF`
- Value options: `OFF` and `ON`
- This variable controls the behavior when TiDB performs the `ONLY_FULL_GOUP_BY` check. For detailed information about `ONLY_FULL_GROUP_BY`, see the [MySQL documentation](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by). In v6.1.0, TiDB handles this check more strictly and correctly.
- To avoid potential compatibility issues caused by version upgrades, the default value of this variable is `OFF` in v6.1.0.

### tidb_enable_noop_functions <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `OFF`
- Possible values: `OFF`, `ON`, `WARN`
- By default, TiDB returns an error when you attempt to use the syntax for functionality that is not yet implemented. When the variable value is set to `ON`, TiDB silently ignores such cases of unavailable functionality, which is helpful if you cannot make changes to the SQL code.
- Enabling `noop` functions controls the following behaviors:
    * `LOCK IN SHARE MODE` syntax
    * `SQL_CALC_FOUND_ROWS` syntax
    * `START TRANSACTION READ ONLY` and `SET TRANSACTION READ ONLY` syntax
    * The `tx_read_only`, `transaction_read_only`, `offline_mode`, `super_read_only`, `read_only` and `sql_auto_is_null` system variables
    * `GROUP BY <expr> ASC|DESC` syntax

> **Warning:**
>
> Only the default value of `OFF` can be considered safe. Setting `tidb_enable_noop_functions=1` might lead to unexpected behaviors in your application, because it permits TiDB to ignore certain syntax without providing an error. For example, the syntax `START TRANSACTION READ ONLY` is permitted, but the transaction remains in read-write mode.

### tidb_enable_outer_join_reorder <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `ON`
- Since v6.1.0, the [Join Reorder](/join-reorder.md) algorithm of TiDB supports Outer Join. This variable controls the support behavior, and the default value is `ON`.
- For a cluster upgraded from a version earlier than v6.1.0, the default value is still `TRUE`.

### tidb_enable_paging <span class="version-mark">New in v5.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to use the method of paging to send coprocessor requests in `IndexLookUp` operator.
- User scenarios: For read queries that use `IndexLookup` and `Limit` and that `Limit` cannot be pushed down to `IndexScan`, there might be high latency for the read queries and high CPU usage for TiKV's `unified read pool`. In such cases, because the `Limit` operator only requires a small set of data, if you set `tidb_enable_paging` to `ON`, TiDB processes less data, which reduces query latency and resource consumption.
- When `tidb_enable_paging` is enabled, for the `IndexLookUp` requests with `Limit` that cannot be pushed down and are fewer than `960`, TiDB uses the method of paging to send coprocessor requests. The fewer `Limit`, the more obvious the optimization.

### tidb_enable_parallel_apply <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable concurrency for the `Apply` operator. The number of concurrencies is controlled by the `tidb_executor_concurrency` variable. The `Apply` operator processes correlated subqueries and has no concurrency by default, so the execution speed is slow. Setting this variable value to `1` can increase concurrency and speed up execution. Currently, concurrency for `Apply` is disabled by default.

### tidb_enable_prepared_plan_cache <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- Determines whether to enable [Prepared Plan Cache](/sql-prepared-plan-cache.md). When it is enabled, the execution plans of `Prepare` and `Execute` are cached so that the subsequent executions skip optimizing the execution plans, which brings performance improvement.
- This setting was previously a `tidb.toml` option (`prepared-plan-cache.enabled`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">New in v5.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls the behavior of the optimizer on using statistics of a table when the statistics are outdated.
- The optimizer determines whether the statistics of a table is outdated in this way: since the last time `ANALYZE` is executed on a table to get the statistics, if 80% of the table rows are modified (the modified row count divided by the total row count), the optimizer determines that the statistics of this table is outdated. You can change this ratio using the [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) configuration.
- By default (with the variable value `ON`), when the statistics of a table is outdated, the optimizer determines that the statistics of the table is no longer reliable except for the total row count. Then, the optimizer uses the pseudo statistics. If you set the variable value to `OFF`, even if the statistics of a table are outdated, the optimizer still keeps using the statistics.
- If the data on a table is frequently modified without executing `ANALYZE` on this table in time, to keep the execution plan stable, you can set the variable value to `OFF`.

### tidb_enable_rate_limit_action

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the dynamic memory control feature for the operator that reads data. By default, this operator enables the maximum number of threads that [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) allows to read data. When the memory usage of a single SQL statement exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) each time, the operator that reads data stops one thread.
- When the operator that reads data has only one thread left and the memory usage of a single SQL statement continues to exceed [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors, such as [spilling data to disk](/tidb-configuration-file.md#oom-use-tmp-storage).

### tidb_enable_slow_log

- Scope: GLOBAL
- Persists to cluster: No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the slow log feature.

### tidb_enable_stmt_summary <span class="version-mark">New in v3.0.4</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the statement summary feature. If enabled, SQL execution information like time consumption is recorded to the `information_schema.STATEMENTS_SUMMARY` system table to identify and troubleshoot SQL performance issues.

### tidb_enable_strict_double_type_check <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control if tables can be created with invalid definitions of type `DOUBLE`. This setting is intended to provide an upgrade path from earlier versions of TiDB, which were less strict in validating types.
- The default value of `ON` is compatible with MySQL.

For example, the type `DOUBLE(10)` is now considered invalid because the precision of floating point types is not guaranteed. After changing `tidb_enable_strict_double_type_check` to `OFF`, the table is created:

```sql
mysql> CREATE TABLE t1 (id int, c double(10));
ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use

mysql> SET tidb_enable_strict_double_type_check = 'OFF';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t1 (id int, c double(10));
Query OK, 0 rows affected (0.09 sec)
```

> **Note:**
>
> This setting only applies to the type `DOUBLE` since MySQL permits precision for `FLOAT` types. This behavior is deprecated starting with MySQL 8.0.17, and it is not recommended to specify precision for either `FLOAT` or `DOUBLE` types.

### tidb_enable_table_partition

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `ON`
- Possible values: `OFF`, `ON`, `AUTO`
- This variable is used to set whether to enable the `TABLE PARTITION` feature:
    - `ON` indicates enabling Range partitioning, Hash partitioning, and Range column partitioning with one single column.
    - `AUTO` functions the same way as `ON` does.
    - `OFF` indicates disabling the `TABLE PARTITION` feature. In this case, the syntax that creates a partition table can be executed, but the table created is not a partitioned one.

### tidb_enable_telemetry <span class="version-mark">New in v4.0.2</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled. By setting the value to `OFF`, the telemetry collection is disabled. If the [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB configuration item is set to `false` on all TiDB instances, the telemetry collection is always disabled and this system variable will not take effect. See [Telemetry](/telemetry.md) for details.

### tidb_enable_top_sql <span class="version-mark">New in v5.4.0</span>

> **Warning:**
>
> Currently, Top SQL is an experimental feature. It is not recommended that you use it for production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the [Top SQL](/dashboard/top-sql.md) feature.

### tidb_enable_tso_follower_proxy <span class="version-mark">New in v5.3.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to enable the TSO Follower Proxy feature. When the value is `OFF`, TiDB only gets TSO from the PD leader. After this feature is enabled, TiDB gets TSO by evenly sending requests to all PD nodes and forwarding TSO requests through PD followers. This helps reduce the CPU pressure of PD leader.
- Scenarios for enabling TSO Follower Proxy:
    * Due to the high pressure of TSO requests, the CPU of the PD leader reaches a bottleneck, which causes high latency of TSO RPC requests.
    * The TiDB cluster has many TiDB instances, and increasing the value of [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530) cannot alleviate the high latency issue of TSO RPC requests.

> **Note:**
>
> Suppose that the TSO RPC latency increases for reasons other than a CPU usage bottleneck of the PD leader (such as network issues). In this case, enabling the TSO Follower Proxy might increase the execution latency in TiDB and affect the QPS performance of the cluster.

### tidb_enable_vectorized_expression <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable vectorized execution.

### tidb_enable_window_function

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the support for window functions. Note that window functions may use reserved keywords. This might cause SQL statements that could be executed normally cannot be parsed after upgrading TiDB. In this case, you can set `tidb_enable_window_function` to `OFF`.

### tidb_enforce_mpp <span class="version-mark">New in v5.1</span>

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- To change this default value, modify the [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) configuration value.
- Controls whether to ignore the optimizer's cost estimation and to forcibly use TiFlash's MPP mode for query execution. The value options are as follows:
    - `0` or `OFF`, which means that the MPP mode is not forcibly used (by default).
    - `1` or `ON`, which means that the cost estimation is ignored and the MPP mode is forcibly used. Note that this setting only takes effect when `tidb_allow_mpp=true`.

MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [Control whether to select the MPP mode](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode).

### tidb_evolve_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the baseline evolution feature. For detailed introduction or usage , see [Baseline Evolution](/sql-plan-management.md#baseline-evolution).
- To reduce the impact of baseline evolution on the cluster, use the following configurations:
    - Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is 600s.
    - Set `tidb_evolve_plan_task_start_time` and `tidb_evolve_plan_task_end_time` to limit the time window. The default values are respectively `00:00 +0000` and `23:59 +0000`.

### tidb_evolve_plan_task_end_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Time
- Default value: `23:59 +0000`
- This variable is used to set the end time of baseline evolution in a day.

### tidb_evolve_plan_task_max_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `600`
- Range: `[-1, 9223372036854775807]`
- Unit: Seconds
- This variable is used to limit the maximum execution time of each execution plan in the baseline evolution feature.

### tidb_evolve_plan_task_start_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Time
- Default value: `00:00 +0000`
- This variable is used to set the start time of baseline evolution in a day.

### tidb_executor_concurrency <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `5`
- Range: `[1, 256]`
- Unit: Threads

This variable is used to set the concurrency of the following SQL operators (to one value):

- `index lookup`
- `index lookup join`
- `hash join`
- `hash aggregation` (the `partial` and `final` phases)
- `window`
- `projection`

`tidb_executor_concurrency` incorporates the following existing system variables as a whole for easier management:

+ `tidb_index_lookup_concurrency`
+ `tidb_index_lookup_join_concurrency`
+ `tidb_hash_join_concurrency`
+ `tidb_hashagg_partial_concurrency`
+ `tidb_hashagg_final_concurrency`
+ `tidb_projection_concurrency`
+ `tidb_window_concurrency`

Since v5.0, you can still separately modify the system variables listed above (with a deprecation warning returned) and your modification only affects the corresponding single operators. After that, if you use `tidb_executor_concurrency` to modify the operator concurrency, the separately modified operators will not be affected. If you want to use `tidb_executor_concurrency` to modify the concurrency of all operators, you can set the values of all variables listed above to `-1`.

For a system upgraded to v5.0 from an earlier version, if you have not modified any value of the variables listed above (which means that the `tidb_hash_join_concurrency` value is `5` and the values of the rest are `4`), the operator concurrency previously managed by these variables will automatically be managed by `tidb_executor_concurrency`. If you have modified any of these variables, the concurrency of the corresponding operators will still be controlled by the modified variables.

### tidb_expensive_query_time_threshold

- Scope: GLOBAL
- Persists to cluster: No
- Type: Integer
- Default value: `60`
- Range: `[10, 2147483647]`
- Unit: Seconds
- This variable is used to set the threshold value that determines whether to print expensive query logs. The difference between expensive query logs and slow query logs is:
    - Slow logs are printed after the statement is executed.
    - Expensive query logs print the statements that are being executed, with execution time exceeding the threshold value, and their related information.

### tidb_force_priority

- Scope: GLOBAL
- Persists to cluster: No
- Default value: `NO_PRIORITY`
- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.
- You can set the value of this variable to `NO_PRIORITY`, `LOW_PRIORITY`, `DELAYED` or `HIGH_PRIORITY`.

### tidb_gc_concurrency <span class="version-mark">New in v5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- Specifies the number of threads in the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) step of GC. A value of `-1` means that TiDB will automatically decide the number of garbage collection threads to use.

### tidb_gc_enable <span class="version-mark">New in v5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- Enables garbage collection for TiKV. Disabling garbage collection will reduce system performance, as old versions of rows will no longer be purged.

### tidb_gc_life_time <span class="version-mark">New in v5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Duration
- Default value: `10m0s`
- Range: `[10m0s, 8760h0m0s]`
- The time limit during which data is retained for each GC, in the format of Go Duration. When a GC happens, the current time minus this value is the safe point.

> **Note:**
>
> - In scenarios of frequent updates, a large value (days or even months) for `tidb_gc_life_time` may cause potential issues, such as:
>     - Larger storage use
>     - A large amount of history data may affect performance to a certain degree, especially for range queries such as `select count(*) from t`
> - If there is any transaction that has been running longer than `tidb_gc_life_time`, during GC, the data since `start_ts` is retained for this transaction to continue execution. For example, if `tidb_gc_life_time` is configured to 10 minutes, among all transactions being executed, the transaction that starts earliest has been running for 15 minutes, GC will retain data of the recent 15 minutes.

### tidb_gc_max_wait_time <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `86400`
- Range: `[600, 31536000]`
- Unit: Seconds
- This variable is used to set the maximum time that active transactions block the GC safe point. During each time of GC, the safe point does not exceed the start time of the ongoing transactions by default. If the runtime of active transactions does not exceed this variable value, the GC safe point will be blocked until the runtime exceeds this value. This variable value is an integer type.

### tidb_gc_run_interval <span class="version-mark">New in v5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Duration
- Default value: `10m0s`
- Range: `[10m0s, 8760h0m0s]`
- Specifies the GC interval, in the format of Go Duration, for example, `"1h30m"`, and `"15m"`

### tidb_gc_scan_lock_mode <span class="version-mark">New in v5.0</span>

> **Warning:**
>
> Currently, Green GC is an experimental feature. It is not recommended that you use it in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `LEGACY`
- Possible values: `PHYSICAL`, `LEGACY`
    - `LEGACY`: Uses the old way of scanning, that is, disable Green GC.
    - `PHYSICAL`: Uses the physical scanning method, that is, enable Green GC.
- This variable specifies the way of scanning locks in the Resolve Locks step of GC. When the variable value is set to `LEGACY`, TiDB scans locks by Regions. When the value `PHYSICAL` is used, it enables each TiKV node to bypass the Raft layer and directly scan data, which can effectively mitigate the impact of GC wakening up all Regions when the [Hibernate Region](/tikv-configuration-file.md#hibernate-regions) feature is enabled, thus improving the execution speed in the Resolve Locks step.

### tidb_general_log

- Scope: GLOBAL
- Persists to cluster: No
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to record all SQL statements in the [log](/tidb-configuration-file.md#logfile). This feature is disabled by default. If maintenance personnel needs to trace all SQL statements when locating issues, they can enable this feature.
- To see all records of this feature in the log, query the `"GENERAL_LOG"` string. The following information is recorded:
    - `conn`: The ID of the current session.
    - `user`: The current session user.
    - `schemaVersion`: The current schema version.
    - `txnStartTS`: The timestamp at which the current transaction starts.
    - `forUpdateTS`: In the pessimistic transactional mode, `forUpdateTS` is the current timestamp of the SQL statement. When a write conflict occurs in the pessimistic transaction, TiDB retries the SQL statement currently being executed and updates this timestamp. You can configure the number of retries via [`max-retry-count`](/tidb-configuration-file.md#max-retry-count). In the optimistic transactional model, `forUpdateTS` is equivalent to `txnStartTS`.
    - `isReadConsistency`: Indicates whether the current transactional isolation level is Read Committed (RC).
    - `current_db`: The name of the current database.
    - `txn_mode`: The transactional mode. Value options are `OPTIMISTIC` and `PESSIMISTIC`.
    - `sql`: The SQL statement corresponding to the current query.

### tidb_hash_join_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `hash join` algorithm.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_hashagg_final_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `final` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_hashagg_partial_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `partial` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to ignore the commands for closing prepared statement cache.
- When this variable is set to `ON`, the `COM_STMT_CLOSE` command of the Binary protocol and the [`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md) statement of the text protocol are ignored. For details, see [Ignore the `COM_STMT_CLOSE` command and the `DEALLOCATE PREPARE` statement](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement).

### tidb_index_join_batch_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `25000`
- Range: `[1, 2147483647]`
- Unit: Rows
- This variable is used to set the batch size of the `index lookup join` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_index_lookup_join_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `index lookup join` algorithm.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_index_lookup_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `20000`
- Range: `[1, 2147483647]`
- Unit: Rows
- This variable is used to set the batch size of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_serial_scan_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `serial scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_init_chunk_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `32`
- Range: `[1, 32]`
- Unit: Rows
- This variable is used to set the number of rows for the initial chunk during the execution process.

### tidb_isolation_read_engines <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: `tikv,tiflash,tidb`
- This variable is used to set the storage engine list that TiDB can use when reading data.

### tidb_log_file_max_days <span class="version-mark">New in v5.3.0</span>

- Scope: SESSION
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- This variable is used to adjust the maximum days of logger on the current TiDB instance. Its value defaults to the value of the [`max-days`](/tidb-configuration-file.md#max-days) configuration in the configuration file. Changing the variable value only affects the current TiDB instance. After TiDB is restarted, the variable value is reset and the configuration value is not affected.

### tidb_low_resolution_tso

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to enable the low precision TSO feature. After this feature is enabled, new transactions use a timestamp updated every 2 seconds to read data.
- The main applicable scenario is to reduce the overhead of acquiring TSO for small read-only transactions when reading old data is acceptable.

### tidb_max_chunk_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1024`
- Range: `[32, 2147483647]`
- Unit: Rows
- This variable is used to set the maximum number of rows in a chunk during the execution process. Setting to too large of a value may cause cache locality issues.

### tidb_max_delta_schema_count <span class="version-mark">New in v2.1.18 and v3.0.5</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1024`
- Range: `[100, 16384]`
- This variable is used to set the maximum number of schema versions (the table IDs modified for corresponding versions) allowed to be cached. The value range is 100 ~ 16384.

### tidb_mem_oom_action <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `CANCEL`
- Possible values: `CANCEL`, `LOG`
- Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by `tidb_mem_quota_query` and cannot be spilled over to disk. See [TiDB Memory Control](/configure-memory-usage.md) for details.
- The default value is `CANCEL`, but in TiDB v4.0.2 and earlier versions, the default value is `LOG`.
- This setting was previously a `tidb.toml` option (`oom-action`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_mem_quota_analyze <span class="version-mark">New in v6.1.0</span>

> **Warning:**
>
> Currently, the `ANALYZE` memory quota is an experimental feature, and the memory statistics might be inaccurate in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `0`
- Unit: Bytes
- This variable controls the maximum memory usage of TiDB updating statistics. Such a memory usage occurs when you manually execute [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) and when TiDB automatically analyzes tasks in the background. When the total memory usage exceeds this threshold, user-executed `ANALYZE` will exit, and an error message is reported that reminds you to try a lower sampling rate or retry later. If the automatic task in the TiDB background exits because the memory threshold is exceeded, and the sampling rate used is higher than the default value, TiDB will retry the update using the default sampling rate. When this variable value is negative or zero, TiDB does not limit the memory usage of both the manual and automatic update tasks.

> **Note:**
>
> `auto_analyze` will be triggered in a TiDB cluster only when `run-auto-analyze` is enabled in the TiDB startup configuration file.

### tidb_mem_quota_apply_cache <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `33554432` (32 MiB)
- Range: `[0, 9223372036854775807]`
- Unit: Bytes
- This variable is used to set the memory usage threshold of the local cache in the `Apply` operator.
- The local cache in the `Apply` operator is used to speed up the computation of the `Apply` operator. You can set the variable to `0` to disable the `Apply` cache feature.

### tidb_mem_quota_binding_cache <span class="version-mark">New in v6.0.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `67108864`
- Range: `[0, 2147483647]`
- Unit: Bytes
- This variable is used to set the threshold of the memory used for caching bindings.
- If a system creates or captures excessive bindings, resulting in overuse of memory space, TiDB returns a warning in the log. In this case, the cache cannot hold all available bindings or determine which bindings to store. For this reason, some queries might miss their bindings. To address this problem, you can increase the value of this variable, which increases the memory used for caching bindings. After modifying this parameter, you need to run `admin reload bindings` to reload bindings and validate the modification.

### tidb_mem_quota_query

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1073741824` (1 GiB)
- Range: `[-1, 9223372036854775807]`
- Unit: Bytes
- This variable is used to set the threshold value of memory quota for a query.
- If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation designated by `tidb_mem_oom_action`.
- This setting was previously session scoped and used the value of `mem-quota-query` from `tidb.toml` as an initial value. Starting from v6.1.0 `tidb_mem_quota_query` is now a `SESSION | GLOBAL` scoped variable.

### tidb_memory_usage_alarm_ratio

- Scope: GLOBAL
- Persists to cluster: No
- Type: Float
- Default value: `0.8`
- Range: `[0, 1]`
- TiDB triggers an alarm when the percentage of the memory it takes exceeds a certain threshold. For the detailed usage description of this feature, see [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).
- You can set the initial value of this variable by configuring [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).

### tidb_metric_query_range_duration <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Type: Integer
- Default value: `60`
- Range: `[10, 216000]`
- Unit: Seconds
- This variable is used to set the range duration of the Prometheus statement generated when querying `METRICS_SCHEMA`.

### tidb_metric_query_step <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Type: Integer
- Default value: `60`
- Range: `[10, 216000]`
- Unit: Seconds
- This variable is used to set the step of the Prometheus statement generated when querying `METRICS_SCHEMA`.

### tidb_multi_statement_mode <span class="version-mark">New in v4.0.11</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `OFF`
- Possible values: `OFF`, `ON`, `WARN`
- This variable controls whether to allow multiple queries to be executed in the same `COM_QUERY` call.
- To reduce the impact of SQL injection attacks, TiDB now prevents multiple queries from being executed in the same `COM_QUERY` call by default. This variable is intended to be used as part of an upgrade path from earlier versions of TiDB. The following behaviors apply:

| Client setting            | `tidb_multi_statement_mode` value | Multiple statements permitted? |
| ------------------------- | --------------------------------- | ------------------------------ |
| Multiple Statements = ON  | OFF                               | Yes                            |
| Multiple Statements = ON  | ON                                | Yes                            |
| Multiple Statements = ON  | WARN                              | Yes                            |
| Multiple Statements = OFF | OFF                               | No                             |
| Multiple Statements = OFF | ON                                | Yes                            |
| Multiple Statements = OFF | WARN                              | Yes (+warning returned)        |

> **Note:**
>
> Only the default value of `OFF` can be considered safe. Setting `tidb_multi_statement_mode=ON` might be required if your application was specifically designed for an earlier version of TiDB. If your application requires multiple statement support, it is recommended to use the setting provided by your client library instead of the `tidb_multi_statement_mode` option. For example:
>
> * [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) (`multiStatements`)
> * [Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html) (`allowMultiQueries`)
> * PHP [mysqli](https://dev.mysql.com/doc/apis-php/en/apis-php-mysqli.quickstart.multiple-statement.html) (`mysqli_multi_query`)

### tidb_nontransactional_ignore_error <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `OFF`
- This variable specifies whether to return an error immediately when the error occurs in a non-transactional DML statement.
- When the value is set to `OFF`, the non-transactional DML statement stops immediately at the first error and returns the error. All the following batches are canceled.
- When the value is set to `ON` and an error occurs in a batch, the following batches will continue to be executed until all batches are executed. All errors occurred during the execution process are returned together in the result.

### tidb_opt_agg_push_down

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join, Projection, and UnionAll.
- When the aggregate operation is slow in query, you can set the variable value to ON.

### tidb_opt_correlation_exp_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1`
- Range: `[0, 2147483647]`
- When the method that estimates the number of rows based on column order correlation is not available, the heuristic estimation method is used. This variable is used to control the behavior of the heuristic method.
    - When the value is 0, the heuristic method is not used.
    - When the value is greater than 0:
        - A larger value indicates that an index scan will probably be used in the heuristic method.
        - A smaller value indicates that a table scan will probably be used in the heuristic method.

### tidb_opt_correlation_threshold

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Float
- Default value: `0.9`
- Range: `[0, 1]`
- This variable is used to set the threshold value that determines whether to enable estimating the row count by using column order correlation. If the order correlation between the current column and the `handle` column exceeds the threshold value, this method is enabled.

### tidb_opt_distinct_agg_push_down

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function with `distinct` (such as `select count(distinct a) from t`) to Coprocessor.
- When the aggregate function with the `distinct` operation is slow in the query, you can set the variable value to `1`.

In the following example, before `tidb_opt_distinct_agg_push_down` is enabled, TiDB needs to read all data from TiKV and execute `distinct` on the TiDB side. After `tidb_opt_distinct_agg_push_down` is enabled, `distinct a` is pushed down to Coprocessor, and a `group by` column `test.t.a` is added to `HashAgg_5`.

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```

### tidb_opt_enable_correlation_adjustment

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether the optimizer estimates the number of rows based on column order correlation

### tidb_opt_insubq_to_join_and_agg

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to enable the optimization rule that converts a subquery to join and aggregation.
- For example, after you enable this optimization rule, the subquery is converted as follows:

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    The subquery is converted to join as follows:

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    If `t1` is limited to be `unique` and `not null` in the `aa` column. You can use the following statement, without aggregation.

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_limit_push_down_threshold

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `100`
- Range: `[0, 2147483647]`
- This variable is used to set the threshold that determines whether to push the Limit or TopN operator down to TiKV.
- If the value of the Limit or TopN operator is smaller than or equal to this threshold, these operators are forcibly pushed down to TiKV. This variable resolves the issue that the Limit or TopN operator cannot be pushed down to TiKV partly due to wrong estimation.

### tidb_opt_prefer_range_scan <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- After you set the value of this variable to `ON`, the optimizer always prefers range scans over full table scans.
- In the following example, before you enable `tidb_opt_prefer_range_scan`, the TiDB optimizer performs a full table scan. After you enable `tidb_opt_prefer_range_scan`, the optimizer selects an index range scan.

```sql
explain select * from t where age=5;
+-------------------------+------------+-----------+---------------+-------------------+
| id                      | estRows    | task      | access object | operator info     |
+-------------------------+------------+-----------+---------------+-------------------+
| TableReader_7           | 1048576.00 | root      |               | data:Selection_6  |
| └─Selection_6           | 1048576.00 | cop[tikv] |               | eq(test.t.age, 5) |
|   └─TableFullScan_5     | 1048576.00 | cop[tikv] | table:t       | keep order:false  |
+-------------------------+------------+-----------+---------------+-------------------+
3 rows in set (0.00 sec)

set session tidb_opt_prefer_range_scan = 1;

explain select * from t where age=5;
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| id                            | estRows    | task      | access object               | operator info                 |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| IndexLookUp_7                 | 1048576.00 | root      |                             |                               |
| ├─IndexRangeScan_5(Build)     | 1048576.00 | cop[tikv] | table:t, index:idx_age(age) | range:[5,5], keep order:false |
| └─TableRowIDScan_6(Probe)     | 1048576.00 | cop[tikv] | table:t                     | keep order:false              |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
3 rows in set (0.00 sec)
```

### tidb_opt_write_row_id

- Scope: SESSION
- Default value: `OFF`
- This variable is used to control whether to allow `INSERT`, `REPLACE`, and `UPDATE` statements to operate on the `_tidb_rowid` column. This variable can be used only when you import data using TiDB tools.

### tidb_partition_prune_mode <span class="version-mark">New in v5.1</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `static`
- Specifies whether to enable `dynamic` mode for partitioned tables. For details about the dynamic pruning mode, see [Dynamic Pruning Mode for Partitioned Tables](/partitioned-table.md#dynamic-pruning-mode).

### tidb_persist_analyze_options <span class="version-mark">New in v5.4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the [ANALYZE configuration persistence](/statistics.md#persist-analyze-configurations) feature.

### tidb_placement_mode <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `STRICT`
- Possible values: `STRICT`, `IGNORE`
- This variable controls whether DDL statements ignore the [placement rules specified in SQL](/placement-rules-in-sql.md). When the variable value is `IGNORE`, all placement rule options are ignored.
- It is intended to be used by logical dump/restore tools to ensure that tables can always be created even if invalid placement rules are assigned. This is similar to how mysqldump writes `SET FOREIGN_KEY_CHECKS=0;` to the start of every dump file.

### tidb_pprof_sql_cpu <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: No
- Type: Integer
- Default value: `0`
- Range: `[0, 1]`
- This variable is used to control whether to mark the corresponding SQL statement in the profile output to identify and troubleshoot performance issues.

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Float
- Default value: `0.1`
- Range: `[0, 1]`
- The threshold at which the prepared plan cache triggers a memory protection mechanism. For details, see [Memory management of Prepared Plan Cache](/sql-prepared-plan-cache.md).
- This setting was previously a `tidb.toml` option (`prepared-plan-cache.memory-guard-ratio`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_prepared_plan_cache_size <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `100`
- Range: `[1, 100000]`
- The maximum number of plans that can be cached in a session. For details, see [Memory management of Prepared Plan Cache](/sql-prepared-plan-cache.md).
- This setting was previously a `tidb.toml` option (`prepared-plan-cache.capacity`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_projection_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[-1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `Projection` operator.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_query_log_max_len

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `4096` (4 KiB)
- Range: `[0, 1073741824]`
- Unit: Bytes
- The maximum length of the SQL statement output. When the output length of a statement is larger than the `tidb_query_log_max_len` value, the statement is truncated to output.
- This setting was previously also available as a `tidb.toml` option (`log.query-log-max-len`), but is only a system variable starting from TiDB v6.1.0.

### tidb_rc_read_check_ts <span class="version-mark">New in v6.0.0</span>

> **Warning:**
>
> - This feature is incompatible with [`replica-read`](#tidb_replica_read-new-in-v40). Do not enable `tidb_rc_read_check_ts` and `replica-read` at the same time.
> - If your client uses a cursor, it is not recommended to enable `tidb_rc_read_check_ts` in case that the previous batch of returned data has already been used by the client and the statement eventually fails.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to optimize the timestamp acquisition, which is suitable for scenarios with read-committed isolation level where read-write conflicts are rare. Enabling this variable can avoid the latency and cost of getting the global timestamp, and can optimize the transaction-level read latency.
- If read-write conflicts are severe, enabling this feature will increase the cost and latency of getting the global timestamp, and might cause performance regression. For details, see [Read Committed isolation level](/transaction-isolation-levels.md#read-committed-isolation-level).

### tidb_read_staleness <span class="version-mark">New in v5.4.0</span>

- Scope: SESSION
- Type: Integer
- Default value: `0`
- Range: `[-2147483648, 0]`
- This variable is used to set the time range of historical data that TiDB can read in the current session. After setting the value, TiDB selects a timestamp as new as possible from the range allowed by this variable, and all subsequent read operations are performed against this timestamp. For example, if the value of this variable is set to `-5`, on the condition that TiKV has the corresponding historical version's data, TiDB selects a timestamp as new as possible within a 5-second time range.

### tidb_record_plan_in_slow_log

- Scope: GLOBAL
- Persists to cluster: No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to include the execution plan of slow queries in the slow log.

### tidb_redact_log

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to hide user information in the SQL statement being recorded into the TiDB log and slow log.
- When you set the variable to `1`, user information is hidden. For example, if the executed SQL statement is `insert into t values (1,2)`, the statement is recorded as `insert into t values (?,?)` in the log.

### tidb_regard_null_as_point <span class="version-mark">New in v5.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether the optimizer can use a query condition including null equivalence as a prefix condition for index access.
- This variable is enabled by default. When it is enabled, the optimizer can reduce the volume of index data to be accessed, which accelerates query execution. For example, if a query involves multiple-column indexes `index(a, b)` and the query condition contains `a<=>null and b=1`, the optimizer can use both `a<=>null` and `b=1` in the query condition for index access. If the variable is disabled, because `a<=>null and b=1` includes the null equivalence condition, the optimizer does not use `b=1` for index access.

### tidb_replica_read <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `leader`
- Possible values: `leader`, `follower`, `leader-and-follower`, `closest-replicas`
- This variable is used to control where TiDB reads data. Here are three options:
    - leader: Read only from leader node
    - follower: Read only from follower node
    - leader-and-follower: Read from leader or follower node
- See [follower reads](/follower-read.md) for additional details.

### tidb_restricted_read_only <span class="version-mark">New in v5.2.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls the read-only status of the entire cluster. When the variable is `ON`, all TiDB servers in the entire cluster are in the read-only mode. In this case, TiDB only executes the statements that do not modify data, such as `SELECT`, `USE`, and `SHOW`. For other statements such as `INSERT` and `UPDATE`, TiDB rejects executing those statements in the read-only mode.
- Enabling the read-only mode using this variable only ensures that the entire cluster finally enters the read-only status. If you have changed the value of this variable in a TiDB cluster but the change has not yet propagated to other TiDB servers, the un-updated TiDB servers are still **not** in the read-only mode.
- When this variable is enabled, the SQL statements being executed are not affected. TiDB only performs the read-only check for the SQL statements **to be** executed.
- When this variable is enabled, TiDB handles the uncommitted transactions in the following ways:
    - For uncommitted read-only transactions, you can commit the transactions normally.
    - For uncommitted transactions that are not read-only, SQL statements that perform write operations in these transactions are rejected.
    - For uncommitted read-only transactions with modified data, the commit of these transactions is rejected.
- After the read-only mode is enabled, all users (including the users with the `SUPER` privilege) cannot execute the SQL statements that might write data unless the user is explicitly granted the `RESTRICTED_REPLICA_WRITER_ADMIN` privilege.
- Users with `RESTRICTED_VARIABLES_ADMIN` or `SUPER` privileges can modify this variable. However, if the [security enhanced mode](#tidb_enable_enhanced_security) is enabled, only the users with the `RESTRICTED_VARIABLES_ADMIN` privilege can modify this variable.

### tidb_retry_limit

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `10`
- Range: `[-1, 9223372036854775807]`
- This variable is used to set the maximum number of the retries for optimistic transactions. When a transaction encounters retryable errors (such as transaction conflicts, very slow transaction commit, or table schema changes), this transaction is re-executed according to this variable. Note that setting `tidb_retry_limit` to `0` disables the automatic retry. This variable only applies to optimistic transactions, not to pessimistic transactions.

### tidb_row_format_version

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `2`
- Range: `[1, 2]`
- Controls the format version of the newly saved data in the table. In TiDB v4.0, the [new storage row format](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md) version `2` is used by default to save new data.
- If you upgrade from a TiDB version earlier than 4.0.0 to 4.0.0, the format version is not changed, and TiDB continues to use the old format of version `1` to write data to the table, which means that **only newly created clusters use the new data format by default**.
- Note that modifying this variable does not affect the old data that has been saved, but applies the corresponding version format only to the newly written data after modifying this variable.

### tidb_scatter_region

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- By default, Regions are split for a new table when it is being created in TiDB. After this variable is enabled, the newly split Regions are scattered immediately during the execution of the `CREATE TABLE` statement. This applies to the scenario where data need to be written in batches right after the tables are created in batches, because the newly split Regions can be scattered in TiKV beforehand and do not have to wait to be scheduled by PD. To ensure the continuous stability of writing data in batches, the `CREATE TABLE` statement returns success only after the Regions are successfully scattered. This makes the statement's execution time multiple times longer than that when you disable this variable.
- Note that if `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` have been set when a table is created, the specified number of Regions are evenly split after the table creation.

### tidb_skip_ascii_check <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to skip ASCII validation.
- Validating ASCII characters affects the performance. When you are sure that the input characters are valid ASCII characters, you can set the variable value to `ON`.

### tidb_skip_isolation_level_check

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- After this switch is enabled, if an isolation level unsupported by TiDB is assigned to `tx_isolation`, no error is reported. This helps improve compatibility with applications that set (but do not depend on) a different isolation level.

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_utf8_check

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to skip UTF-8 validation.
- Validating UTF-8 characters affects the performance. When you are sure that the input characters are valid UTF-8 characters, you can set the variable value to `ON`.

> **Note:**
>
> If the character check is skipped, TiDB might fail to detect illegal UTF-8 characters written by the application, cause decoding errors when `ANALYZE` is executed, and introduce other unknown encoding issues. If your application cannot guarantee the validity of the written string, it is not recommended to skip the character check.

### tidb_slow_log_threshold

- Scope: GLOBAL
- Persists to cluster: No
- Type: Integer
- Default value: `300`
- Range: `[-1, 9223372036854775807]`
- Unit: Milliseconds
- This variable is used to output the threshold value of the time consumed by the slow log. When the time consumed by a query is larger than this value, this query is considered as a slow log and its log is output to the slow query log.

Usage example:

```sql
SET tidb_slow_log_threshold = 200;
```

### tidb_max_tiflash_threads <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `-1`
- Range: `[-1, 256]`
- This variable is used to set the maximum concurrency for TiFlash to execute a request. The default value is `-1`, indicating that this system variable is invalid. When the value is `0`, the maximum number of threads is automatically configured by TiFlash.

### tidb_slow_query_file

- Scope: SESSION
- Default value: ""
- When `INFORMATION_SCHEMA.SLOW_QUERY` is queried, only the slow query log name set by `slow-query-file` in the configuration file is parsed. The default slow query log name is "tidb-slow.log". To parse other logs, set the `tidb_slow_query_file` session variable to a specific file path, and then query `INFORMATION_SCHEMA.SLOW_QUERY` to parse the slow query log based on the set file path. For details, see [Identify Slow Queries](/identify-slow-queries.md).

### tidb_snapshot

- Scope: SESSION
- Default value: ""
- This variable is used to set the time point at which the data is read by the session. For example, when you set the variable to "2017-11-11 20:20:20" or a TSO number like "400036290571534337", the current session reads the data of this moment.

### tidb_stats_cache_mem_quota <span class="version-mark">New in v6.1.0</span>

> **Warning:**
>
> This variable is an experimental feature. It is not recommended to use it in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 1099511627776]`
- This variable sets the memory quota for the TiDB statistics cache.

### tidb_stats_load_pseudo_timeout <span class="version-mark">New in v5.4.0</span>

> **Warning:**
>
> Currently, synchronously loading statistics is an experimental feature. It is not recommended that you use it in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls how TiDB behaves when the waiting time of SQL optimization reaches the timeout to synchronously load complete column statistics. The default value `OFF` means that SQL execution fails after the timeout. If you set this variable to `ON`, the SQL optimization gets back to using pseudo statistics after the timeout.

### tidb_stats_load_sync_wait <span class="version-mark">New in v5.4.0</span>

> **Warning:**
>
> Currently, synchronously loading statistics is an experimental feature. It is not recommended that you use it in production environments.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- Unit: Milliseconds
- This variable controls whether to enable the synchronously loading statistics feature. The default value `0` means that the feature is disabled. To enable the feature, you can set this variable to a timeout (in milliseconds) that SQL optimization can wait for at most to synchronously load complete column statistics. For details, see [Load statistics](/statistics.md#load-statistics).

### tidb_stmt_summary_history_size <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `24`
- Range: `[0, 255]`
- This variable is used to set the history capacity of [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_internal_query <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to include the SQL information of TiDB in [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_max_sql_length <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `4096`
- Range: `[0, 2147483647]`
- This variable is used to control the length of the SQL string in [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_max_stmt_count <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `3000`
- Range: `[1, 32767]`
- This variable is used to set the maximum number of statements that [statement summary tables](/statement-summary-tables.md) store in memory.

### tidb_stmt_summary_refresh_interval <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `1800`
- Range: `[1, 2147483647]`
- Unit: Seconds
- This variable is used to set the refresh time of [statement summary tables](/statement-summary-tables.md).

### tidb_store_limit <span class="version-mark">New in v3.0.4 and v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 9223372036854775807]`
- This variable is used to limit the maximum number of requests TiDB can send to TiKV at the same time. 0 means no limit.

### tidb_sysdate_is_now <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether the `SYSDATE` function can be replaced by the `NOW` function. This configuration item has the same effect as the MySQL option [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now).

### tidb_table_cache_lease <span class="version-mark">New in v6.0.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `3`
- Range: `[1, 10]`
- Unit: Seconds
- This variable is used to control the lease time of [cached tables](/cached-tables.md) with a default value of `3`. The value of this variable affects the modification to cached tables. After a modification is made to cached tables, the longest waiting time might be `tidb_table_cache_lease` seconds. If the table is read-only or can accept a high write latency, you can increase the value of this variable to increase the valid time for caching tables and to reduce the frequency of lease renewal.

### tidb_tmp_table_max_size <span class="version-mark">New in v5.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `67108864`
- Range: `[1048576, 137438953472]`
- Unit: Bytes
- This variable is used to set the maximum size of a single [temporary table](/temporary-tables.md). Any temporary table with a size larger than this variable value causes error.

### tidb_top_sql_max_meta_count <span class="version-mark">New in v6.0.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `5000`
- Range: `[1, 10000]`
- This variable is used to control the maximum number of SQL statement types collected by [Top SQL](/dashboard/top-sql.md) per minute.

### tidb_top_sql_max_time_series_count <span class="version-mark">New in v6.0.0</span>

> **Note:**
>
> Currently, the Top SQL page in TiDB Dashboard only displays the top 5 types of SQL queries that contribute the most to the load, which is irrelevant with the configuration of `tidb_top_sql_max_time_series_count`.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `100`
- Range: `[1, 5000]`
- This variable is used to control how many SQL statements that contribute the most to the load (that is, top N) can be recorded by [Top SQL](/dashboard/top-sql.md) per minute.

### tidb_tso_client_batch_max_wait_time <span class="version-mark">New in v5.3.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Float
- Default value: `0`
- Range: `[0, 10]`
- Range: `[0, 10]`
- Unit: Milliseconds
- This variable is used to set the maximum waiting time for a batch operation when TiDB requests TSO from PD. The default value is `0`, which means no extra waiting time.
- When obtaining TSO requests from PD each time, PD Client, used by TiDB, collects as many TSO requests received at the same time as possible. Then, PD Client merges the collected requests in batch into one RPC request and sends the request to PD. This helps reduce the pressure on PD.
- After setting this variable to a value greater than `0`, TiDB waits for the maximum duration of this value before the end of each batch merge. This is to collect more TSO requests and improve the effect of batch operations.
- Scenarios for increasing the value of this variable:
    * Due to the high pressure of TSO requests, the CPU of the PD leader reaches a bottleneck, which causes high latency of TSO RPC requests.
    * There are not many TiDB instances in the cluster, but every TiDB instance is in high concurrency.
- It is recommended to set this variable to a value as small as possible.

> **Notes:**
>
> Suppose that the TSO RPC latency increases for reasons other than a CPU usage bottleneck of the PD leader (such as network issues). In this case, increasing the value of `tidb_tso_client_batch_max_wait_time` might increase the execution latency in TiDB and affect the QPS performance of the cluster.

### tidb_txn_assertion_level <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `FAST`
- Possible values: `OFF`, `FAST`, `STRICT`
- This variable is used to control the assertion level. Assertion is a consistency check between data and indexes, which checks whether a key being written exists in the transaction commit process. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md ).

    - `OFF`: Disable this check.
    - `FAST`: Enable most of the check items, with almost no impact on performance.
    - `STRICT`: Enable all check items, with a minor impact on pessimistic transaction performance when the system workload is high.

- For new clusters of v6.0.0 or later versions, the default value is `FAST`. For existing clusters that upgrade from versions earlier than v6.0.0, the default value is `OFF`.

### tidb_txn_mode

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `pessimistic`
- Possible values: `pessimistic`, `optimistic`
- This variable is used to set the transaction mode. TiDB 3.0 supports the pessimistic transactions. Since TiDB 3.0.8, the [pessimistic transaction mode](/pessimistic-transaction.md) is enabled by default.
- If you upgrade TiDB from v3.0.7 or earlier versions to v3.0.8 or later versions, the default transaction mode does not change. **Only the newly created clusters use the pessimistic transaction mode by default**.
- If this variable is set to "optimistic" or "", TiDB uses the [optimistic transaction mode](/optimistic-transaction.md).

### tidb_use_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the execution plan binding feature. It is enabled by default, and can be disabled by assigning the `OFF` value. For the use of the execution plan binding, see [Execution Plan Binding](/sql-plan-management.md#create-a-binding).

### tidb_wait_split_region_finish

- Scope: SESSION
- Type: Boolean
- Default value: `ON`
- It usually takes a long time to scatter Regions, which is determined by PD scheduling and TiKV loads. This variable is used to set whether to return the result to the client after all Regions are scattered completely when the `SPLIT REGION` statement is being executed:
    - `ON` requires that the `SPLIT REGIONS` statement waits until all Regions are scattered.
    - `OFF` permits the `SPLIT REGIONS` statement to return before finishing scattering all Regions.
- Note that when scattering Regions, the write and read performances for the Region that is being scattered might be affected. In batch-write or data importing scenarios, it is recommended to import data after Regions scattering is finished.

### tidb_wait_split_region_timeout

- Scope: SESSION
- Type: Integer
- Default value: `300`
- Range: `[1, 2147483647]`
- Unit: Seconds
- This variable is used to set the timeout for executing the `SPLIT REGION` statement. If a statement is not executed completely within the specified time value, a timeout error is returned.

### tidb_window_concurrency <span class="version-mark">New in v4.0</span>

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency degree of the window operator.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### time_zone

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `SYSTEM`
- This variable returns the current time zone. Values can be specified as either an offset such as '-8:00' or a named zone 'America/Los_Angeles'.
- The value `SYSTEM` means that the time zone should be the same as the system host, which is available via the [`system_time_zone`](#system_time_zone) variable.

### timestamp

- Scope: SESSION
- Type: Float
- Default value: `0`
- Range: `[0, 2147483647]`
- A non-empty value of this variable indicates the UNIX epoch that is used as the timestamp for `CURRENT_TIMESTAMP()`, `NOW()`, and other functions. This variable might be used in data restore or replication.

### transaction_isolation

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `REPEATABLE-READ`
- Possible values: `READ-UNCOMMITTED`, `READ-COMMITTED`, `REPEATABLE-READ`, `SERIALIZABLE`
- This variable sets the transaction isolation. TiDB advertises `REPEATABLE-READ` for compatibility with MySQL, but the actual isolation level is Snapshot Isolation. See [transaction isolation levels](/transaction-isolation-levels.md) for further details.

### tx_isolation

This variable is an alias for `transaction_isolation`.

### version

- Scope: NONE
- Default value: `5.7.25-TiDB-`(tidb version)
- This variable returns the MySQL version, followed by the TiDB version. For example '5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253'.

### version_comment

- Scope: NONE
- Default value: (string)
- This variable returns additional details about the TiDB version. For example, 'TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible'.

### version_compile_machine

- Scope: NONE
- Default value: (string)
- This variable returns the name of the CPU architecture on which TiDB is running.

### version_compile_os

- Scope: NONE
- Default value: (string)
- This variable returns the name of the OS on which TiDB is running.

### wait_timeout

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `28800`
- Range: `[0, 31536000]`
- Unit: Seconds
- This variable controls the idle timeout of user sessions. A zero-value means unlimited.

### warning_count

- Scope: SESSION
- Default value: `0`
- This read-only variable indicates the number of warnings that occurred in the statement that was previously executed.

### windowing_use_high_precision

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to use the high precision mode when computing the window functions.
