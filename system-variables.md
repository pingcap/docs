---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
aliases: ['/tidb/stable/tidb-specific-system-variables','/docs/stable/system-variables/','/docs/v4.0/system-variables/','/docs/stable/reference/configuration/tidb-server/mysql-variables/','/docs/stable/tidb-specific-system-variables/','/docs/v4.0/tidb-specific-system-variables/','/docs/stable/reference/configuration/tidb-server/tidb-specific-variables/','/tidb/v4.0/tidb-specific-system-variables']
---

# System Variables

TiDB system variables behave similar to MySQL with some differences, in that settings might apply on a `SESSION`, `INSTANCE`, or `GLOBAL` scope, or on a scope that combines `SESSION`, `INSTANCE`, or `GLOBAL`.

- Changes to `GLOBAL` scoped variables **only apply to new connection sessions with TiDB**. Currently active connection sessions are not affected. These changes are persisted and valid after restarts.
- Changes to `INSTANCE` scoped variables apply to all active or new connection sessions with the current TiDB instance immediately after the changes are made. Other TiDB instances are not affected. These changes are not persisted and become invalid after TiDB restarts.

Variables can be set with the [`SET` statement](/sql-statements/sql-statement-set-variable.md) on a per-session, instance or global basis:

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
> TiDB differs from MySQL in that `GLOBAL` scoped variables **persist** through TiDB server restarts. Changes to `GLOBAL` variables might take up to 2 seconds to be effective, including on the TiDB server where the changes are made. See [TiDB #14531](https://github.com/pingcap/tidb/issues/14531) for details.
> Additionally, TiDB presents several MySQL variables from MySQL 5.7 as both readable and settable. This is required for compatibility, since it is common for both applications and connectors to read MySQL variables. For example: JDBC connectors both read and set query cache settings, despite not relying on the behavior.

## Variable Reference

### autocommit

- Scope: SESSION | GLOBAL
- Default value: ON
- Controls whether statements should automatically commit when not in an explicit transaction. See [Transaction Overview](/transaction-overview.md#autocommit) for more information.

### allow_auto_random_explicit_insert <span class="version-mark">New in v4.0.3</span>

- Scope: SESSION (since v4.0.5: SESSION | GLOBAL)
- Default value: 0
- Determines whether to allow explicitly specifying the values of the column with the `AUTO_RANDOM` attribute in the `INSERT` statement. `1` means to allow and `0` means to disallow.

### datadir

- Scope: NONE
- Default value: /tmp/tidb
- This variable indicates the location where data is stored. This location can be a local path or point to a PD server if the data is stored on TiKV.
- A value in the format of `ip_address:port` indicates the PD server that TiDB connects to on startup.

### ddl_slow_threshold

- Scope: INSTANCE
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

### last_plan_from_binding <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 0
- This variable is used to show whether the execution plan used in the previous statement was influenced by a [plan binding](/sql-plan-management.md)

### license

- Scope: NONE
- Default value: Apache License 2.0
- This variable indicates the license of your TiDB server installation.

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

### tidb_allow_remove_auto_inc <span class="version-mark">New in v2.1.18 and v3.0.4</span>

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the `AUTO_INCREMENT` property of a column is allowed to be removed by executing `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default.

### tidb_auto_analyze_end_time

- Scope: GLOBAL
- Default value: 23:59 +0000
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_auto_analyze_ratio

- Scope: GLOBAL
- Default value: 0.5
- This variable is used to set the threshold when TiDB automatically executes [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) in a background thread to update table statistics. For example, a value of 0.5 means that auto-analyze is triggered when greater than 50% of the rows in a table have been modified. Auto-analyze can be restricted to only execute during certain hours of the day by specifying `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.

> **Note:**
>
> Only when the `run-auto-analyze` option is enabled in the starting configuration file of TiDB, the `auto_analyze` feature can be triggered.

### tidb_auto_analyze_start_time

- Scope: GLOBAL
- Default value: 00:00 +0000
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_backoff_lock_fast

- Scope: SESSION | GLOBAL
- Default value: 100
- This variable is used to set the `backoff` time when the read request meets a lock.

### tidb_backoff_weight

- Scope: SESSION | GLOBAL
- Default value: 2
- This variable is used to increase the weight of the maximum time of TiDB `backoff`, that is, the maximum retry time for sending a retry request when an internal network or other component (TiKV, PD) failure is encountered. This variable can be used to adjust the maximum retry time and the minimum value is 1.

    For example, the base timeout for TiDB to take TSO from PD is 15 seconds. When `tidb_backoff_weight = 2`, the maximum timeout for taking TSO is: *base time \* 2 = 30 seconds*.

    In the case of a poor network environment, appropriately increasing the value of this variable can effectively alleviate error reporting to the application end caused by timeout. If the application end wants to receive the error information more quickly, minimize the value of this variable.

### tidb_capture_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: off
- This variable is used to control whether to enable the [baseline capturing](/sql-plan-management.md#baseline-capturing) feature. This feature depends on the statement summary, so you need to enable the statement summary before you use baseline capturing.
- After this feature is enabled, the historical SQL statements in the statement summary are traversed periodically, and bindings are automatically created for SQL statements that appear at least twice.

### tidb_check_mb4_value_in_utf8

- Scope: INSTANCE
- Default value: 1, indicating check the validity of UTF-8 data. This default behavior is compatible with MySQL.
- This variable is used to set whether to check the validity of UTF-8 data.
- To upgrade an earlier version (TiDB v2.1.1 or earlier), you may need to disable this option. Otherwise, you can successfully write invalid strings in an earlier version but fail to do this in a later version, because there is no data validity check in the earlier version. For details, see [FAQs After Upgrade](/faq/upgrade-faq.md).

### tidb_config

- Scope: SESSION
- Default value: ""
- This variable is read-only. It is used to obtain the configuration information of the current TiDB server.

### tidb_constraint_check_in_place

- Scope: SESSION | GLOBAL
- Default value: 0
- This setting only applies to optimistic transactions. When this variable is set to zero, checking for duplicate values in UNIQUE indexes is deferred until the transaction commits. This helps improve performance, but might be an unexpected behavior for some applications. See [Constraints](/constraints.md) for details.

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
- Default value: 0
- This variable is read-only. It is used to obtain the timestamp of the current transaction.

### tidb_ddl_error_count_limit

- Scope: GLOBAL
- Default value: 512
- This variable is used to set the number of retries when the DDL operation fails. When the number of retries exceeds the parameter value, the wrong DDL operation is canceled.

### tidb_ddl_reorg_batch_size

- Scope: GLOBAL
- Default value: 256
- This variable is used to set the batch size during the `re-organize` phase of the DDL operation. For example, when TiDB executes the `ADD INDEX` operation, the index data needs to backfilled by `tidb_ddl_reorg_worker_cnt` (the number) concurrent workers. Each worker backfills the index data in batches.
    - If many updating operations such as `UPDATE` and `REPLACE` exist during the `ADD INDEX` operation, a larger batch size indicates a larger probability of transaction conflicts. In this case, you need to adjust the batch size to a smaller value. The minimum value is 32.
    - If the transaction conflict does not exist, you can set the batch size to a large value. The maximum value is 10240. This can increase the speed of the backfilling data, but the write pressure on TiKV also becomes higher.

### tidb_ddl_reorg_priority

- Scope: SESSION
- Default value: `PRIORITY_LOW`
- This variable is used to set the priority of executing the `ADD INDEX` operation in the `re-organize` phase.
- You can set the value of this variable to `PRIORITY_LOW`, `PRIORITY_NORMAL` or `PRIORITY_HIGH`.

### tidb_ddl_reorg_worker_cnt

- Scope: GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the DDL operation in the `re-organize` phase.

### tidb_disable_txn_auto_retry

- Scope: SESSION | GLOBAL
- Default: on
- This variable is used to set whether to disable the automatic retry of explicit optimistic transactions. The default value of `on` means that transactions will not automatically retry in TiDB and `COMMIT` statements might return errors that need to be handled in the application layer.

    Setting the value to `off` means that TiDB will automatically retry transactions, resulting in fewer errors from `COMMIT` statements. Be careful when making this change, because it might result in lost updates.

    This variable does not affect automatically committed implicit transactions and internally executed transactions in TiDB. The maximum retry count of these transactions is determined by the value of `tidb_retry_limit`.

    For more details, see [limits of retry](/optimistic-transaction.md#limits-of-retry).

    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is controlled by [`max_retry_count`](/tidb-configuration-file.md#max-retry-count).

### `tidb_enable_amend_pessimistic_txn` <span class="version-mark">New in v4.0.7</span>

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to control whether to enable the `AMEND TRANSACTION` feature. If you enable the `AMEND TRANSACTION` feature in a pessimistic transaction, when concurrent DDL operations and SCHEMA VERSION changes exist on tables associated with this transaction, TiDB attempts to amend the transaction. TiDB corrects the transaction commit to make the commit consistent with the latest valid SCHEMA VERSION so that the transaction can be successfully committed without getting the `Information schema is changed` error. This feature is effective on the following concurrent DDL operations:

    - `ADD COLUMN` or `DROP COLUMN` operations.
    - `MODIFY COLUMN` or `CHANGE COLUMN` operations which increase the length of a field.
    - `ADD INDEX` or `DROP INDEX` operations in which the index column is created before the transaction is opened.

> **Note:**
>
> Currently, this feature is incompatible with TiDB Binlog in some scenarios and might cause semantic changes on a transaction. For more usage precautions of this feature, refer to [Incompatibility issues about transaction semantic](https://github.com/pingcap/tidb/issues/21069) and [Incompatibility issues about TiDB Binlog](https://github.com/pingcap/tidb/issues/20996).

### tidb_enable_cascades_planner

> **Warning:**
>
> Currently, cascades planner is an experimental feature. It is not recommended that you use it in the production environment.

- Scope: SESSION | GLOBAL
- Default value: `OFF`
- This variable is used to control whether to enable the cascades planner.

### tidb_enable_chunk_rpc <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 1
- This variable is used to control whether to enable the `Chunk` data encoding format in Coprocessor.

### tidb_enable_fast_analyze

> **Warning:**
>
> Currently, `Fast Analyze` is an experimental feature. It is not recommended that you use it in the production environment.

- Scope: SESSION | GLOBAL
- Default value: 0, indicating not enabling the statistics fast `Analyze` feature.
- This variable is used to set whether to enable the statistics `Fast Analyze` feature.
- If the statistics `Fast Analyze` feature is enabled, TiDB randomly samples about 10,000 rows of data as statistics. When the data is distributed unevenly or the data size is small, the statistics accuracy is low. This might lead to a non-optimal execution plan, for example, selecting a wrong index. If the execution time of the regular `Analyze` statement is acceptable, it is recommended to disable the `Fast Analyze` feature.

### tidb_enable_index_merge <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to control whether to enable the index merge feature.

### tidb_enable_noop_functions <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to control whether to enable `get_lock` and `release_lock` functions. These two functions are not implemented, and always return 1 in the current version of TiDB.

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

<<<<<<< HEAD
### tidb_evolve_plan_task_start_time <span class="version-mark">New in v4.0</span>
=======
- Scope: NONE
- Default value: ""
- The location of the certificate authority file (if there is one). The value of this variable is defined by the TiDB configuration item [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca).
   
</CustomContent>

### ssl_cert

<CustomContent platform="tidb">

- Scope: NONE
- Default value: ""
- The location of the certificate file (if there is a file) that is used for SSL/TLS connections. The value of this variable is defined by the TiDB configuration item [`ssl-cert`](/tidb-configuration-file.md#ssl-cert).
   
</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: NONE
- Default value: ""
- The location of the certificate file (if there is a file) that is used for SSL/TLS connections. The value of this variable is defined by the TiDB configuration item [`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert).
   
</CustomContent>

### ssl_key

<CustomContent platform="tidb">

- Scope: NONE
- Default value: ""
- The location of the private key file (if there is one) that is used for SSL/TLS connections. The value of this variable is defined by TiDB configuration item [`ssl-key`](/tidb-configuration-file.md#ssl-cert).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: NONE
- Default value: ""
- The location of the private key file (if there is one) that is used for SSL/TLS connections. The value of this variable is defined by TiDB configuration item [`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key).

</CustomContent>

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
- Default value: `lower`, `md5`, `reverse`, `tidb_shard`, `upper`, `vitess_hash`
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

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether the `AUTO_INCREMENT` property of a column is allowed to be removed by executing `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default.

### tidb_analyze_version <span class="version-mark">New in v5.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer

<CustomContent platform="tidb">

- Default value: `2`

</CustomContent>

<CustomContent platform="tidb-cloud">

- Default value: `1`

</CustomContent>

- Range: `[1, 2]`
- Controls how TiDB collects statistics.

<CustomContent platform="tidb">

- In v5.3.0 and later versions, the default value of this variable is `2`. If your cluster is upgraded from a version earlier than v5.3.0 to v5.3.0 or later, the default value of `tidb_analyze_version` does not change. For detailed introduction, see [Introduction to Statistics](/statistics.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

- For detailed introduction of this variable, see [Introduction to Statistics](/statistics.md).

</CustomContent>

### tidb_auth_signing_cert

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: String
- Default value: ""
- This variable is associated with an unreleased feature. **DO NOT** set this variable.

### tidb_auth_signing_key

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: String
- Default value: ""
- This variable is associated with an unreleased feature. **DO NOT** set this variable.

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

### tidb_batch_commit

> **Warning:**
>
> It is **NOT** recommended to enable this variable.

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- The variable is used to control whether to enable the deprecated batch-commit feature. When this variable is enabled, a transaction might be split into multiple transactions by grouping a few statements and committed non-atomically, which is not recommended.

### tidb_batch_delete

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the batch-delete feature, which is a part of the deprecated batch-dml feature. When this variable is enabled, `DELETE` statements might be split into multiple transactions and committed non-atomically. To make it work, you also need to enable `tidb_enable_batch_dml` and set a positive value for `tidb_dml_batch_size`, which is not recommended.

### tidb_batch_insert

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the batch-insert feature, which is a part of the deprecated batch-dml feature. When this variable is enabled, `INSERT` statements might be split into multiple transactions and committed non-atomically. To make it work, you also need to enable `tidb_enable_batch_dml` and set a positive value for `tidb_dml_batch_size`, which is not recommended.

### tidb_batch_pending_tiflash_count <span class="version-mark">New in v6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `4000`
- Range: `[0, 2147483647]`
- Specifies the maximum number of permitted unavailable tables when you use `ALTER DATABASE SET TIFLASH REPLICA` to add TiFlash replicas. If the number of unavailable tables exceeds this limit, the operation will be stopped or setting TiFlash replicas for the remaining tables will be very slow.

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

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Type: Boolean
- Default value: `ON`
- This variable is used to enforce that the `utf8` character set only stores values from the [Basic Multilingual Plane (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane). To store characters outside the BMP, it is recommended to use the `utf8mb4` character set.
- You might need to disable this option when upgrading your cluster from an earlier version of TiDB where the `utf8` checking was more relaxed. For details, see [FAQs After Upgrade](https://docs.pingcap.com/tidb/stable/upgrade-faq).

### tidb_checksum_table_concurrency

- Scope: SESSION
- Default value: `4`
- Unit: Threads
- This variable is used to set the scan index concurrency of executing the [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) statement.
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

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
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

### tidb_cost_model_version <span class="version-mark">New in v6.2.0</span>

> **Warning:**
>
> - Cost Model Version 2 is currently an experimental feature. It is not recommended that you use it for production environments.
> - Switching the version of the cost model might cause changes to query plans.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `1`
- Value options: `1`, `2`
- TiDB v6.2.0 introduces the [Cost Model Version 2](/cost-model.md#cost-model-version-2), which is more accurate than the previous version in internal tests.
- To enable the Cost Model Version 2, you can set the `tidb_cost_model_version` to `2`. If you set this variable to `1`, the Cost Model Version 1 will be used.
- The version of cost model affects the plan decision of optimizer. For more details, see [Cost Model](/cost-model.md).

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
    - If the transaction conflict does not exist, you can set the batch size to a large value (consider the worker count. See [Interaction Test on Online Workloads and `ADD INDEX` Operations](https://docs.pingcap.com/tidb/stable/online-workloads-and-add-index-operations) for reference). This can increase the speed of the backfilling data, but the write pressure on TiKV also becomes higher.

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

### tidb_default_string_match_selectivity <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `0.8`
- Range: `[0, 1]`
- This variable is used to set the default selectivity of `like`, `rlike`, and `regexp` functions in the filter condition when estimating the number of rows. This variable also controls whether to enable TopN to help estimate these functions.
- TiDB tries to estimate `like` in the filter condition using statistics. But when `like` matches a complex string, or when using `rlike` or `regexp`, TiDB often fails to fully use statistics, and the default value `0.8` is set as the selectivity rate instead, resulting in inaccurate estimation.
- This variable is used to change the preceding behavior. If the variable is set to a value other than `0`, the selectivity rate is the specified variable value instead of `0.8`.
- If the variable is set to `0`, TiDB tries to evaluate using TopN in statistics to improve the accuracy and consider the NULL number in statistics when estimating the preceding three functions. The prerequisite is that statistics are collected when [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) is set to `2`. Such evaluation might slightly affect the performance.
- If the variable is set to a value other than the `0.8`, TiDB adjusts the estimation for `not like`, `not rlike`, and `not regexp` accordingly.

### tidb_disable_txn_auto_retry

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to disable the automatic retry of explicit optimistic transactions. The default value of `ON` means that transactions will not automatically retry in TiDB and `COMMIT` statements might return errors that need to be handled in the application layer.

    Setting the value to `OFF` means that TiDB will automatically retry transactions, resulting in fewer errors from `COMMIT` statements. Be careful when making this change, because it might result in lost updates.

    This variable does not affect automatically committed implicit transactions and internally executed transactions in TiDB. The maximum retry count of these transactions is determined by the value of `tidb_retry_limit`.

    For more details, see [limits of retry](/optimistic-transaction.md#limits-of-retry).

    <CustomContent platform="tidb">

    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is controlled by [`max_retry_count`](/tidb-configuration-file.md#max-retry-count).

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is 256.

    </CustomContent>

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

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- Unit: Rows
- When this value is greater than `0`, TiDB will batch commit statements such as `INSERT` or `LOAD DATA` into smaller transactions. This reduces memory usage and helps ensure that the `txn-total-size-limit` is not reached by bulk modifications.
- Only the value `0` provides ACID compliance. Setting this to any other value will break the atomicity and isolation guarantees of TiDB.
- To make this variable work, you also need to enable `tidb_enable_batch_dml` and at least one of `tidb_batch_insert` and `tidb_batch_delete`.

### tidb_enable_1pc <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to specify whether to enable the one-phase commit feature for transactions that only affect one Region. Compared with the often-used two-phase commit, one-phase commit can greatly reduce the latency of transaction commit and increase the throughput.

> **Note:**
>
> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.
> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) instead.
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

### tidb_enable_analyze_snapshot <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to read historical data or the latest data when performing `ANALYZE`. If this variable is set to `ON`, `ANALYZE` reads the historical data available at the time of `ANALYZE`. If this variable is set to `OFF`, `ANALYZE` reads the latest data.
- Before v5.2, `ANALYZE` reads the latest data. From v5.2 to v6.1, `ANALYZE` reads the historical data available at the time of `ANALYZE`.

> **Warning:**
>
> If `ANALYZE` reads the historical data available at the time of `ANALYZE`, the long duration of `AUTO ANALYZE` might cause the `GC life time is shorter than transaction duration` error because the historical data is garbage-collected.

### tidb_enable_async_commit <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the async commit feature for the second phase of the two-phase transaction commit to perform asynchronously in the background. Enabling this feature can reduce the latency of transaction commit.

> **Note:**
>
> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.
> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) instead.
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

### tidb_enable_batch_dml

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the deprecated batch-dml feature. When it is enabled, certain statements might be split into multiple transactions, which is non-atomic and should be used with care. When using batch-dml, you must ensure that there are no concurrent operations on the data you are operating on. To make it work, you must also specify a positive value for `tidb_batch_dml_size` and enable at least one of `tidb_batch_insert` and `tidb_batch_delete`.

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

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
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

### tidb_enable_concurrent_ddl <span class="version-mark">New in v6.2.0</span>

> **Warning:**
>
> **DO NOT modify this variable**. The risk of disabling this variable is unknown and might corrupt the metadata of the cluster.

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `ON`
- This variable controls whether to allow TiDB to use concurrent DDL statements. When concurrent DDL statements are used, the DDL execution flow is changed, and DDL statements are not easily blocked by other DDL statements. In addition, multiple indexes can be added at the same time.

### tidb_enable_enhanced_security

- Scope: NONE
- Type: Boolean

<CustomContent platform="tidb">

- Default value: `OFF`
- This variable indicates whether the TiDB server you are connected to has the Security Enhanced Mode (SEM) enabled. To change its value, you need to modify the value of `enable-sem` in your TiDB server configuration file and restart the TiDB server.

</CustomContent>

<CustomContent platform="tidb-cloud">

- Default value: `ON`
- This variable is read-only. For TiDB Cloud, the Security Enhanced Mode (SEM) is enabled by default.

</CustomContent>

- SEM is inspired by the design of systems such as [Security-Enhanced Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux). It reduces the abilities of users with the MySQL `SUPER` privilege and instead requires `RESTRICTED` fine-grained privileges to be granted as a replacement. These fine-grained privileges include:
    - `RESTRICTED_TABLES_ADMIN`: The ability to write data to system tables in the `mysql` schema and to see sensitive columns on `information_schema` tables.
    - `RESTRICTED_STATUS_ADMIN`: The ability to see sensitive variables in the command `SHOW STATUS`.
    - `RESTRICTED_VARIABLES_ADMIN`: The ability to see and set sensitive variables in `SHOW [GLOBAL] VARIABLES` and `SET`.
    - `RESTRICTED_USER_ADMIN`: The ability to prevent other users from making changes or dropping a user account.

### tidb_enable_exchange_partition

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the [`exchange partitions with tables`](/partitioned-table.md#partition-management) feature. The default value is `OFF`, that is, `exchange partitions with tables` is disabled by default.

### tidb_enable_extended_stats

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

<CustomContent platform="tidb">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable indicates whether TiDB can collect the extended statistic to guide the optimizer. See [Introduction to Extended Statistics](/extended-statistics.md) for more information.

</CustomContent>

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

### tidb_enable_gc_aware_memory_track

> **Warning:**
>
> This variable is an internal variable for debugging in TiDB. It might be removed in a future release. **Do not** set this variable.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable GC-Aware memory track.

### tidb_enable_historical_stats

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used for an unreleased feature. **Do not change the variable value**.

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

### tidb_enable_index_merge_join

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- Specifies whether to enable the `IndexMergeJoin` operator.
- This variable is used only for the internal operation of TiDB. It is **NOT recommended** to adjust it. Otherwise, data correctness might be affected.

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

### tidb_enable_local_txn

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used for an unreleased feature. **Do not change the variable value**.

### tidb_enable_mutation_checker <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable TiDB mutation checker, which is a tool used to check consistency between data and indexes during the execution of DML statements. If the checker returns an error for a statement, TiDB rolls back the execution of the statement. Enabling this variable causes a slight increase in CPU usage. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md).
- For new clusters of v6.0.0 or later versions, the default value is `ON`. For existing clusters that upgrade from versions earlier than v6.0.0, the default value is `OFF`.

### tidb_enable_new_cost_interface <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- Value options: `OFF` and `ON`
- TiDB v6.2.0 refactors the implementation of previous cost model. This variable controls whether to enable the refactored Cost Model implementation.
- This variable is enabled by default because the refactored Cost Model uses the same cost formula as before, which does not change the plan decision.
- If your cluster is upgraded from v6.1 to v6.2, this variable remains `OFF`, and it is recommended to enable it manually. If your cluster is upgraded from a version earlier than v6.1, this variable sets to `ON` by default.

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

### tidb_enable_noop_variables <span class="version-mark">New in v6.2.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `ON`
- If you set the variable value to `OFF`, TiDB behaves as follows:
    * When you use `SET` to set a `noop` variable, TiDB returns the `"setting *variable_name* has no effect in TiDB"` warning.
    * The result of `SHOW [SESSION | GLOBAL] VARIABLES` does not include `noop` variables.
    * When you use `SELECT` to read a `noop` variable, TiDB returns the `"variable *variable_name* has no effect in TiDB"` warning.
- To check whether a TiDB instance has set and read the `noop` variable, you can use the `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;` statement.

### tidb_enable_outer_join_reorder <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: In v6.1.0, the default value is `ON`. After v6.1.0, the default value is `OFF`.
- Since v6.1.0, the [Join Reorder](/join-reorder.md) algorithm of TiDB supports Outer Join. This variable controls the support behavior. The default value is `OFF`, which means the Join Reorder's support for Outer Join is disabled by default.
- For a cluster upgraded from a version earlier than v6.1.0, the default value is `OFF`. For a cluster upgraded from v6.1.0, the default value is `ON`.

### tidb_enable_ordered_result_mode

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `OFF`
- Specifies whether to sort the final output result automatically.
- For example, with this variable enabled, TiDB processes `SELECT a, MAX(b) FROM t GROUP BY a` as `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`.

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

### tidb_enable_pipelined_window_function

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variables specifies whether to use the pipeline execution algorithm for window functions.

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

<CustomContent platform="tidb">

- The optimizer determines whether the statistics of a table is outdated in this way: since the last time `ANALYZE` is executed on a table to get the statistics, if 80% of the table rows are modified (the modified row count divided by the total row count), the optimizer determines that the statistics of this table is outdated. You can change this ratio using the [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) configuration.

</CustomContent>

<CustomContent platform="tidb-cloud">

- The optimizer determines whether the statistics of a table is outdated in this way: since the last time `ANALYZE` is executed on a table to get the statistics, if 80% of the table rows are modified (the modified row count divided by the total row count), the optimizer determines that the statistics of this table is outdated.

</CustomContent>

- By default (with the variable value `ON`), when the statistics of a table is outdated, the optimizer determines that the statistics of the table is no longer reliable except for the total row count. Then, the optimizer uses the pseudo statistics. If you set the variable value to `OFF`, even if the statistics of a table are outdated, the optimizer still keeps using the statistics.
- If the data on a table is frequently modified without executing `ANALYZE` on this table in time, to keep the execution plan stable, you can set the variable value to `OFF`.

### tidb_enable_rate_limit_action

> **Note:**
>
> This variable is enabled by default, which makes the memory usage not under the control of [`tidb_mem_quota_query`](#tidb_mem_quota_query) in some cases. Therefore, it is recommended to set the value of `tidb_enable_rate_limit_action` to `OFF`.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the dynamic memory control feature for the operator that reads data. By default, this operator enables the maximum number of threads that [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) allows to read data. When the memory usage of a single SQL statement exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) each time, the operator that reads data stops one thread.

<CustomContent platform="tidb">

- When the operator that reads data has only one thread left and the memory usage of a single SQL statement continues to exceed [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors, such as [spilling data to disk](/tidb-configuration-file.md#oom-use-tmp-storage).

</CustomContent>

<CustomContent platform="tidb-cloud">

- When the operator that reads data has only one thread left and the memory usage of a single SQL statement continues to exceed [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors, such as spilling data to disk.

</CustomContent>

### tidb_enable_slow_log

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
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

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`

<CustomContent platform="tidb">

- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled. By setting the value to `OFF`, the telemetry collection is disabled. If the [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB configuration item is set to `false` on all TiDB instances, the telemetry collection is always disabled and this system variable will not take effect. See [Telemetry](/telemetry.md) for details.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled.

</CustomContent>

### tidb_enable_top_sql <span class="version-mark">New in v5.4.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Currently, Top SQL is an experimental feature. It is not recommended that you use it for production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `OFF`

<CustomContent platform="tidb">

- This variable is used to control whether to enable the [Top SQL](/dashboard/top-sql.md) feature.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to control whether to enable the [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) feature.

</CustomContent>

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

<CustomContent platform="tidb">

- To change this default value, modify the [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) configuration value.

</CustomContent>

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

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Type: Integer
- Default value: `60`
- Range: `[10, 2147483647]`
- Unit: Seconds
- This variable is used to set the threshold value that determines whether to print expensive query logs. The difference between expensive query logs and slow query logs is:
    - Slow logs are printed after the statement is executed.
    - Expensive query logs print the statements that are being executed, with execution time exceeding the threshold value, and their related information.

### tidb_force_priority

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Default value: `NO_PRIORITY`
- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.
- The default value `NO_PRIORITY` means that the priority for statements is not forced to change. Other options are `LOW_PRIORITY`, `DELAYED`, and `HIGH_PRIORITY` in ascending order.

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

<CustomContent platform="tidb">

- This variable specifies the way of scanning locks in the Resolve Locks step of GC. When the variable value is set to `LEGACY`, TiDB scans locks by Regions. When the value `PHYSICAL` is used, it enables each TiKV node to bypass the Raft layer and directly scan data, which can effectively mitigate the impact of GC wakening up all Regions when the [Hibernate Region](/tikv-configuration-file.md#hibernate-regions) feature is enabled, thus improving the execution speed in the Resolve Locks step.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable specifies the way of scanning locks in the Resolve Locks step of GC. When the variable value is set to `LEGACY`, TiDB scans locks by Regions. When the value `PHYSICAL` is used, it enables each TiKV node to bypass the Raft layer and directly scan data, which can effectively mitigate the impact of GC wakening up all Regions, thus improving the execution speed in the Resolve Locks step.

</CustomContent>

### tidb_general_log

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Type: Boolean
- Default value: `OFF`

<CustomContent platform="tidb-cloud">

- This variable is used to set whether to record all SQL statements in the log. This feature is disabled by default. If you need to trace all SQL statements when locating issues, enable this feature.

</CustomContent>

<CustomContent platform="tidb">

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

</CustomContent>

### tidb_generate_binary_plan <span class="version-mark">New in v6.2.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `ON`
- This variable controls whether to generate binary-encoded execution plans in slow logs and statement summaries.
- When this variable is set to `ON`, you can view visual execution plans in TiDB Dashboard. Note that TiDB Dashboard only provides visual display for execution plans generated after this variable is enabled.
- You can execute the `SELECT tidb_decode_binary_plan('xxx...')` statement to parse the specific plan from a binary plan.

### tidb_guarantee_linearizability <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls the way commit TS is calculated for async commit. By default (with the `ON` value), the two-phase commit requests a new TS from the PD server and uses the TS to calculate the final commit TS. In this situation, linearizability is guaranteed for all the concurrent transactions.
- If you set this variable to `OFF`, the process of fetching TS from the PD server is skipped, with the cost that only causal consistency is guaranteed but not linearizability. For more details, see the blog post [Async Commit, the Accelerator for Transaction Commit in TiDB 5.0](https://en.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/).
- For scenarios that require only causal consistency, you can set this variable to `OFF` to improve performance.

### tidb_hash_exchange_with_new_collation

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether the MPP hash partition exchange operator is generated in a cluster with new collation enabled. `true` means to generate the operator, and `false` means not to generate it.
- This variable is used for the internal operation of TiDB. It is **NOT recommended** to set this variable.

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

### tidb_last_ddl_info <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION
- Default value: ""
- Type: String
- This is a read-only variable. It is internally used in TiDB to get the information of the last DDL operation within the current session.
    - "query": The last DDL query string.
    - "seq_num": The sequence number for each DDL operation. It is used to identify the order of DDL operations. 

### tidb_last_query_info <span class="version-mark">New in v4.0.14</span>

- Scope: SESSION
- Default value: ""
- This is a read-only variable. It is internally used in TiDB to query the transaction information of the last DML statement. The information includes:
    - `txn_scope`: The scope of the transaction, which can be `global` or `local`.
    - `start_ts`: The start timestamp of the transaction.
    - `for_update_ts`: The `for_update_ts` of the previously executed DML statement. This is an internal term of TiDB used for tests. Usually, you can ignore this information.
    - `error`: The error message, if any.

### tidb_last_txn_info <span class="version-mark">New in v4.0.9</span>

- Scope: SESSION
- Type: String
- This variable is used to get the last transaction information within the current session. It is a read-only variable. The transaction information includes:
    - The transaction scope.
    - The start and commit TS.
    - The transaction commit mode, which might be a two-phase, one-phase, or async commit.
    - The information of transaction fallback from async commit or one-phase commit to two-phase commit.
    - The error encountered.

### tidb_log_file_max_days <span class="version-mark">New in v5.3.0</span>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`

<CustomContent platform="tidb">

- This variable is used to set the maximum days that the log is retained on the current TiDB instance. Its value defaults to the value of the [`max-days`](/tidb-configuration-file.md#max-days) configuration in the configuration file. Changing the variable value only affects the current TiDB instance. After TiDB is restarted, the variable value is reset and the configuration value is not affected.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to set the maximum days that the log is retained on the current TiDB instance.

</CustomContent>

### tidb_low_resolution_tso

- Scope: SESSION
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to enable the low precision TSO feature. After this feature is enabled, new transactions use a timestamp updated every 2 seconds to read data.
- The main applicable scenario is to reduce the overhead of acquiring TSO for small read-only transactions when reading old data is acceptable.

### tidb_max_auto_analyze_time <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `43200`
- Range: `[0, 2147483647]`
- Unit: seconds
- This variable is used to specify the maximum execution time of automatic `ANALYZE` tasks. When the execution time of an automatic `ANALYZE` task exceeds the specified time, the task will be terminated. When the value of this variable is `0`, there is no limit to the maximum execution time of automatic `ANALYZE` tasks.

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

### tidb_max_tiflash_threads <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `-1`
- Range: `[-1, 256]`
- This variable is used to set the maximum concurrency for TiFlash to execute a request. The default value is `-1`, indicating that this system variable is invalid. When the value is `0`, the maximum number of threads is automatically configured by TiFlash.

### tidb_mem_oom_action <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Type: Enumeration
- Default value: `CANCEL`
- Possible values: `CANCEL`, `LOG`

<CustomContent platform="tidb">

- Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by `tidb_mem_quota_query` and cannot be spilled over to disk. See [TiDB Memory Control](/configure-memory-usage.md) for details.

</CustomContent>

<CustomContent platform="tidb-cloud">

- Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by [`tidb_mem_quota_query`](#tidb_mem_quota_query) and cannot be spilled over to disk.

</CustomContent>

- The default value is `CANCEL`, but in TiDB v4.0.2 and earlier versions, the default value is `LOG`.
- This setting was previously a `tidb.toml` option (`oom-action`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_mem_quota_analyze <span class="version-mark">New in v6.1.0</span>

> **Warning:**
>
> Currently, the `ANALYZE` memory quota is an experimental feature, and the memory statistics might be inaccurate in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Default value: `-1`
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

<CustomContent platform="tidb">

- For versions earlier than TiDB v6.1.0, this is a session scope variable and uses the value of `mem-quota-query` from `tidb.toml` as an initial value. Starting from v6.1.0, `tidb_mem_quota_query` is a `SESSION | GLOBAL` scope variable.

</CustomContent>

<CustomContent platform="tidb-cloud">

- For versions earlier than TiDB v6.1.0, this is a session scope variable. Starting from v6.1.0, `tidb_mem_quota_query` is a `SESSION | GLOBAL` scope variable.

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio

- Scope: SESSION
- Type: Float
- Default value: `0`
- This variable represents the memory statistics error value allowed in the TiDB memory debug mode.
- This variable is used for the internal testing of TiDB. It is **NOT recommended** to set this variable. 

### tidb_memory_debug_mode_min_heap_inuse

- Scope: SESSION
- Type: INT64
- Default value: `0`
- This variable is used for the internal testing of TiDB. It is **NOT recommended** to set this variable. Enabling this variable will affect the performance of TiDB.
- After configuring this parameter, TiDB will enter the memory debug mode to analyze the accuracy of memory tracking. TiDB will frequently trigger GC during the execution of subsequent SQL statements, and compare the actual memory usage and memory statistics. If the current memory usage is greater than `tidb_memory_debug_mode_min_heap_inuse` and the memory statistics error exceeds `tidb_memory_debug_mode_alarm_ratio`, TiDB will output the relevant memory information to the log and file.

### tidb_memory_usage_alarm_ratio

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Type: Float
- Default value: `0.8`
- Range: `[0, 1]`

<CustomContent platform="tidb">

- TiDB triggers an alarm when the percentage of the memory it takes exceeds a certain threshold. For the detailed usage description of this feature, see [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).
- You can set the initial value of this variable by configuring [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).

</CustomContent>

<CustomContent platform="tidb-cloud">

- TiDB triggers an alarm when the percentage of the memory it takes exceeds a certain threshold. For the detailed usage description of this feature, see [`memory-usage-alarm-ratio`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#memory-usage-alarm-ratio-new-in-v409).

</CustomContent>

### tidb_merge_join_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Default value: `1`
- This variable sets the concurrency of the `MergeJoin` operator when a query is executed.
- It is **NOT recommended** to set this variable. Modifying the value of this variable might cause data correctness issues.

### tidb_metric_query_range_duration <span class="version-mark">New in v4.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: SESSION
- Type: Integer
- Default value: `60`
- Range: `[10, 216000]`
- Unit: Seconds
- This variable is used to set the range duration of the Prometheus statement generated when querying `METRICS_SCHEMA`.

### tidb_metric_query_step <span class="version-mark">New in v4.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: SESSION
- Type: Integer
- Default value: `60`
- Range: `[10, 216000]`
- Unit: Seconds
- This variable is used to set the step of the Prometheus statement generated when querying `METRICS_SCHEMA`.

### tidb_min_paging_size <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Integer
- Default value: `128`
- Range: `[1, 9223372036854775807]`
- Unit: Rows
- This variable is used to set the minimum number of rows during the coprocessor paging request process. Setting it to too small a value increases the RPC request count between TiDB and TiKV, while setting it to too large a value might cause performance decrease when executing queries using IndexLookup with Limit.

### tidb_mpp_store_fail_ttl

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Type: Duration
- Default value: `60s`
- The newly started TiFlash node does not provide services. To prevent queries from failing, TiDB limits the tidb-server sending queries to the newly started TiFlash node. This variable indicates the time range in which the newly started TiFlash node is not sent requests.

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

### tidb_opt_broadcast_cartesian_join

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Type: Integer
- Default value: `1`
- Range: `[0, 2]`
- Indicates whether to allow the Broadcast Cartesian Join. 
- `0` means that the Broadcast Cartesian Join is not allowed. `1` means that it is allowed based on [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50). `2` means that it is always allowed even if the table size exceeds the threshold.
- This variable is internally used in TiDB, and it is **NOT** recommended to modify its value.

### tidb_opt_concurrency_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `3.0`
- Indicates the CPU cost of starting a Golang goroutine in TiDB. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_concurrency_factor_v2

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Type: Float
- Range: `[0, 18446744073709551615]`
- Default value: `3.0`
- Indicates the CPU cost of starting a Golang goroutine in TiDB. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_copcpu_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Type: Float
- Range: `[0, 18446744073709551615]`
- Default value: `3.0`
- Indicates the CPU cost for TiKV Coprocessor to process one row. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_copcpu_factor_v2

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `30.0`
- Indicates the CPU cost for TiKV Coprocessor to process one row. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

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

### tidb_opt_cpu_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `3.0`
- Indicates the CPU cost for TiDB to process one row. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_cpu_factor_v2

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `30.0`
- Indicates the CPU cost for TiDB to process one row. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_desc_factor
>>>>>>> 5135daa32 (sysvar: add a note to disable tidb_enable_rate_limit_action (#11444))

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
- Default value: NO_PRIORITY
- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.
- You can set the value of this variable to `NO_PRIORITY`, `LOW_PRIORITY`, `DELAYED` or `HIGH_PRIORITY`.

### tidb_general_log

- Scope: INSTANCE
- Default value: 0
- This variable is used to set whether to record all SQL statements in the [log](/tidb-configuration-file.md#logfile). This feature is disabled by default. If maintenance personnel needs to trace all SQL statements when locating issues, they can enable this feature.
- To see all records of this feature in the log, query the `"GENERAL_LOG"` string. The following information is recorded:
    - `conn`: The ID of the current session.
    - `user`: The current session user.
    - `schemaVersion`: The current schema version.
    - `txnStartTS`: The timestamp at which the current transaction starts.
    - `forUpdateTS`: In the pessimistic transactional model, `forUpdateTS` is the current timestamp of the SQL statement. When a write conflict occurs in the pessimistic transaction, TiDB retries the SQL statement currently being executed and updates this timestamp. You can configure the number of retries via [`max-retry-count`](/tidb-configuration-file.md#max-retry-count). In the optimistic transactional model, `forUpdateTS` is equivalent to `txnStartTS`.
    - `isReadConsistency`: Indicates whether the current transactional isolation level is Read Committed (RC).
    - `current_db`: The name of the current database.
    - `txn_mode`: The transactional mode. Value options are `OPTIMISTIC` and `PESSIMISTIC`.
    - `sql`: The SQL statement corresponding to the current query.

### tidb_build_stats_concurrency

- Scope: SESSION
- Default value: 4
- This variable is used to set the concurrency of executing the `ANALYZE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_checksum_table_concurrency

- Scope: SESSION
- Default value: 4
- This variable is used to set the scan index concurrency of executing the `ADMIN CHECKSUM TABLE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_distsql_scan_concurrency

- Scope: SESSION | GLOBAL
- Default value: 15
- This variable is used to set the concurrency of the `scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.
- For OLAP scenarios, the maximum value cannot exceed the number of CPU cores of all the TiKV nodes.
- If a table has a lot of partitions, you can reduce the variable value appropriately to avoid TiKV becoming out of memory (OOM).

### tidb_hash_join_concurrency

- Scope: SESSION | GLOBAL
- Default value: 5
- This variable is used to set the concurrency of the `hash join` algorithm.

### tidb_hashagg_final_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `final` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.

### tidb_hashagg_partial_concurrency

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

### tidb_projection_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `Projection` operator.

### tidb_window_concurrency <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency degree of the `window` operator.

### tidb_union_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency degree of the `union` operator.

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

### tidb_memory_usage_alarm_ratio

- Scope: INSTANCE
- Default value: `0.8`
- TiDB triggers an alarm when the percentage of the memory it takes exceeds a certain threshold. For the detailed usage description of this feature, see [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).
- You can set the initial value of this variable by configuring [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409).

### tidb_metric_query_range_duration <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 60
- This variable is used to set the range duration of the Prometheus statement generated when querying METRIC_SCHEMA. The unit is second.

### tidb_metric_query_step <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: 60
- This variable is used to set the step of the Prometheus statement generated when querying `METRIC_SCHEMA`. The unit is second.

### tidb_multi_statement_mode <span class="version-mark">New in v4.0.11</span>

- Scope: SESSION | GLOBAL
- Default value: For v4.0.14 or a later v4.0 version, the default value is OFF. For v4.0 versions earlier than v4.0.14, the default value is WARN.
- Permitted values: OFF, ON, WARN
- This variable controls whether to allow multiple queries to be executed in the same `COM_QUERY` call.
- To reduce the impact of SQL injection attacks, TiDB now prevents multiple queries from being executed in the same `COM_QUERY` call by default. This variable is intended to be used as part of an upgrade path from earlier versions of TiDB. The following behaviors apply:

| Client setting         | `tidb_multi_statement_mode` value | Multiple statements permitted? |
|------------------------|-----------------------------------|--------------------------------|
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

### tidb_opt_agg_push_down

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join, Projection, and UnionAll.
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

In the following example, before `tidb_opt_distinct_agg_push_down` is enabled, TiDB needs to read all data from TiKV and execute `disctinct` on the TiDB side. After `tidb_opt_distinct_agg_push_down` is enabled, `distinct a` is pushed down to Coprocessor, and a `group by` column `test.t.a` is added to `HashAgg_5`.

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

### tidb_opt_insubq_to_join_and_agg

- Scope: SESSION | GLOBAL
- Default value: 1
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

### tidb_opt_write_row_id

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to allow `insert`, `replace` and `update` statements to operate on the column `_tidb_rowid`. It is not allowed by default. This variable can be used only when importing data with TiDB tools.

### tidb_query_log_max_len

- Scope: INSTANCE
- Default value: 4096 (bytes)
- The maximum length of the SQL statement output. When the output length of a statement is larger than the `tidb_query-log-max-len` value, the statement is truncated to output.

Usage example:

```sql
set tidb_query_log_max_len = 20
```

### tidb_pprof_sql_cpu <span class="version-mark">New in v4.0</span>

- Scope: INSTANCE
- Default value: 0
- This variable is used to control whether to mark the corresponding SQL statement in the profile output to identify and troubleshoot performance issues.

### tidb_record_plan_in_slow_log

- Scope: INSTANCE
- Default value: `1`
- This variable is used to control whether to include the execution plan of slow queries in the slow log.

### tidb_replica_read <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Default value: leader
- This variable is used to control where TiDB reads data. Here are three options:
    - leader: Read only from leader node
    - follower: Read only from follower node
    - leader-and-follower: Read from leader or follower node
- See [follower reads](/follower-read.md) for additional details.

### tidb_retry_limit

- Scope: SESSION | GLOBAL
- Default value: 10
- This variable is used to set the maximum number of the retries. When a transaction encounters retryable errors (such as transaction conflicts, very slow transaction commit, or table schema changes), this transaction is re-executed according to this variable. Note that setting `tidb_retry_limit` to `0` disables the automatic retry. This variable only applies to optimistic transactions, not to pessimistic transactions.

### tidb_row_format_version

- Scope: GLOBAL
- Default value: `2`
- Controls the format version of the newly saved data in the table. In TiDB v4.0, the [new storage row format](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md) version `2` is used by default to save new data.
- If you upgrade from a TiDB version earlier than 4.0.0 to 4.0.0, the format version is not changed, and TiDB continues to use the old format of version `1` to write data to the table, which means that **only newly created clusters use the new data format by default**.
- Note that modifying this variable does not affect the old data that has been saved, but applies the corresponding version format only to the newly written data after modifying this variable.

### tidb_scatter_region

- Scope: GLOBAL
- Default value: 0
- By default, Regions are split for a new table when it is being created in TiDB. After this variable is enabled, the newly split Regions are scattered immediately during the execution of the `CREATE TABLE` statement. This applies to the scenario where data need to be written in batches right after the tables are created in batches, because the newly split Regions can be scattered in TiKV beforehand and do not have to wait to be scheduled by PD. To ensure the continuous stability of writing data in batches, the `CREATE TABLE` statement returns success only after the Regions are successfully scattered. This makes the statement's execution time multiple times longer than that when you disable this variable.
- Note that if `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` have been set when a table is created, the specified number of Regions are evenly split after the table creation.

### tidb_skip_isolation_level_check

- Scope: SESSION | GLOBAL
- Default value: 0
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
- Default value: 0
- This variable is used to set whether to skip UTF-8 validation.
- Validating UTF-8 characters affects the performance. When you are sure that the input characters are valid UTF-8 characters, you can set the variable value to 1.

### tidb_slow_log_threshold

- Scope: INSTANCE
- Default value: 300ms
- This variable is used to output the threshold value of the time consumed by the slow log. When the time consumed by a query is larger than this value, this query is considered as a slow log and its log is output to the slow query log.

Usage example:

```sql
SET tidb_slow_log_threshold = 200;
```

### tidb_enable_collect_execution_info

- Scope: INSTANCE
- Default value: 1
- This variable controls whether to record the execution information of each operator in the slow query log.

### tidb_redact_log

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable controls whether to hide user information in the SQL statement being recorded into the TiDB log and slow log.
- When you set the variable to `1`, user information is hidden. For example, if the executed SQL statement is `insert into t values (1,2)`, the statement is recorded as `insert into t values (?,?)` in the log.

### tidb_slow_query_file

- Scope: SESSION
- Default value: ""
- When `INFORMATION_SCHEMA.SLOW_QUERY` is queried, only the slow query log name set by `slow-query-file` in the configuration file is parsed. The default slow query log name is "tidb-slow.log". To parse other logs, set the `tidb_slow_query_file` session variable to a specific file path, and then query `INFORMATION_SCHEMA.SLOW_QUERY` to parse the slow query log based on the set file path. For details, see [Identify Slow Queries](/identify-slow-queries.md).

### tidb_snapshot

- Scope: SESSION
- Default value: ""
- This variable is used to set the time point at which the data is read by the session. For example, when you set the variable to "2017-11-11 20:20:20" or a TSO number like "400036290571534337", the current session reads the data of this moment.

### tidb_stmt_summary_history_size <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 24 (the value of the default configuration file)
- This variable is used to set the history capacity of [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_internal_query <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 0 (the value of the default configuration file)
- This variable is used to control whether to include the SQL information of TiDB in [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_max_sql_length <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 4096 (the value of the default configuration file)
- This variable is used to control the length of the SQL string in [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_max_stmt_count <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: Before v4.0.14, the default value is 200. Since v4.0.14, the default value is 3000 (the value of the default configuration file).
- This variable is used to set the maximum number of statements that [statement summary tables](/statement-summary-tables.md) store in memory.

### tidb_stmt_summary_refresh_interval <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: 1800 (the value of the default configuration file)
- This variable is used to set the refresh time of [statement summary tables](/statement-summary-tables.md). The unit is second.

### tidb_store_limit <span class="version-mark">New in v3.0.4 and v4.0</span>

- Scope: INSTANCE | GLOBAL
- Default value: 0
- This variable is used to limit the maximum number of requests TiDB can send to TiKV at the same time. 0 means no limit.

### tidb_txn_mode

- Scope: SESSION | GLOBAL
- Default value: "pessimistic"
- This variable is used to set the transaction mode. TiDB 3.0 supports the pessimistic transactions. Since TiDB 3.0.8, the [pessimistic transaction mode](/pessimistic-transaction.md) is enabled by default.
- If you upgrade TiDB from v3.0.7 or earlier versions to v3.0.8 or later versions, the default transaction mode does not change. **Only the newly created clusters use the pessimistic transaction mode by default**.
- If this variable is set to "optimistic" or "", TiDB uses the [optimistic transaction mode](/optimistic-transaction.md).

### tidb_use_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Default value: on
- This variable is used to control whether to enable the execution plan binding feature. It is enabled by default, and can be disabled by assigning the `off` value. For the use of the execution plan binding, see [Execution Plan Binding](/sql-plan-management.md#create-a-binding).

### tidb_wait_split_region_finish

- Scope: SESSION
- Default value: 1, indicating returning the result after all Regions are scattered.
- It usually takes a long time to scatter Regions, which is determined by PD scheduling and TiKV loads. This variable is used to set whether to return the result to the client after all Regions are scattered completely when the `SPLIT REGION` statement is being executed. Value `0` indicates returning the value before finishing scattering all Regions.
- Note that when scattering Regions, the write and read performances for the Region that is being scattered might be affected. In batch-write or data importing scenarios, it is recommended to import data after Regions scattering is finished.

### tidb_wait_split_region_timeout

- Scope: SESSION
- Default value: 300
- This variable is used to set the timeout for executing the `SPLIT REGION` statement. The unit is second. If a statement is not executed completely within the specified time value, a timeout error is returned.

### time_zone

- Scope: SESSION | GLOBAL
- Default value: SYSTEM
- This variable sets the sytem time zone. Values can be specified as either an offset such as '-8:00' or a named zone 'America/Los_Angeles'.

### transaction_isolation

- Scope: SESSION | GLOBAL
- Default value: REPEATABLE-READ
- This variable sets the transaction isolation. TiDB advertises `REPEATABLE-READ` for compatibility with MySQL, but the actual isolation level is Snapshot Isolation. See [transaction isolation levels](/transaction-isolation-levels.md) for further details.

### tx_isolation

This variable is an alias for _transaction_isolation_.

### version

- Scope: NONE
- Default value: 5.7.25-TiDB-(tidb version)
- This variable returns the MySQL version, followed by the TiDB version. For example '5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253'.

### version_comment

- Scope: NONE
- Default value: (string)
- This variable returns additional details about the TiDB version. For example, 'TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible'.

### wait_timeout

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable controls the idle timeout of user sessions in seconds. A zero-value means unlimited.

### warning_count

- Scope: SESSION
- Default value: 0
- This read-only variable indicates the number of warnings that occurred in the statement that was previously executed.

### windowing_use_high_precision

- Scope: SESSION | GLOBAL
- Default value: ON
- This variable controls whether to use the high precision mode when computing the window functions.

### `tidb_enable_rate_limit_action`

- Scope: SESSION | GLOBAL
- Default value: ON
- This variable controls whether to enable the dynamic memory control feature for the operator that reads data. By default, this operator enables the maximum number of threads that [`tidb_disql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) allows to read data. When the memory usage of a single SQL statement exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) each time, the operator that reads data stops one thread.
- When the operator that reads data has only one thread left and the memory usage of a single SQL statement continues to exceed [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors.
