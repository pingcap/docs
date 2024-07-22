---
title: mysql Schema
summary: Learn about the TiDB system tables.
aliases: ['/docs/dev/system-tables/system-table-overview/','/docs/dev/reference/system-databases/mysql/','/tidb/dev/system-table-overview/']
---

# `mysql` Schema

The `mysql` schema contains TiDB system tables. The design is similar to the `mysql` schema in MySQL, where tables such as `mysql.user` can be edited directly. It also contains a number of tables which are extensions to MySQL.

## Grant system tables

These system tables contain grant information about user accounts and their privileges:

- `user`: user accounts, global privileges, and other non-privilege columns
- `db`: database-level privileges
- `tables_priv`: table-level privileges
- `columns_priv`: column-level privileges
- `password_history`: password change history
- `default_roles`: the default roles for a user
- `global_grants`: dynamic privileges
- `global_priv`: the authentication information based on certificates
- `role_edges`: the relationship between roles

### `mysql.user`

`mysql.user` is a frequently used system table. You can display the columns of `mysql.user` by:

```sql
desc mysql.user;
```

```
+------------------------+----------------------+------+-----+-------------------+-------+
| Field                  | Type                 | Null | Key | Default           | Extra |
+------------------------+----------------------+------+-----+-------------------+-------+
| Host                   | char(255)            | NO   | PRI | <null>            |       |
| User                   | char(32)             | NO   | PRI | <null>            |       |
| authentication_string  | text                 | YES  |     | <null>            |       |
| plugin                 | char(64)             | YES  |     | <null>            |       |
| Select_priv            | enum('N','Y')        | NO   |     | N                 |       |
| Insert_priv            | enum('N','Y')        | NO   |     | N                 |       |
| Update_priv            | enum('N','Y')        | NO   |     | N                 |       |
| Delete_priv            | enum('N','Y')        | NO   |     | N                 |       |
| Create_priv            | enum('N','Y')        | NO   |     | N                 |       |
| Drop_priv              | enum('N','Y')        | NO   |     | N                 |       |
| Process_priv           | enum('N','Y')        | NO   |     | N                 |       |
| Grant_priv             | enum('N','Y')        | NO   |     | N                 |       |
| References_priv        | enum('N','Y')        | NO   |     | N                 |       |
| Alter_priv             | enum('N','Y')        | NO   |     | N                 |       |
| Show_db_priv           | enum('N','Y')        | NO   |     | N                 |       |
| Super_priv             | enum('N','Y')        | NO   |     | N                 |       |
| Create_tmp_table_priv  | enum('N','Y')        | NO   |     | N                 |       |
| Lock_tables_priv       | enum('N','Y')        | NO   |     | N                 |       |
| Execute_priv           | enum('N','Y')        | NO   |     | N                 |       |
| Create_view_priv       | enum('N','Y')        | NO   |     | N                 |       |
| Show_view_priv         | enum('N','Y')        | NO   |     | N                 |       |
| Create_routine_priv    | enum('N','Y')        | NO   |     | N                 |       |
| Alter_routine_priv     | enum('N','Y')        | NO   |     | N                 |       |
| Index_priv             | enum('N','Y')        | NO   |     | N                 |       |
| Create_user_priv       | enum('N','Y')        | NO   |     | N                 |       |
| Event_priv             | enum('N','Y')        | NO   |     | N                 |       |
| Repl_slave_priv        | enum('N','Y')        | NO   |     | N                 |       |
| Repl_client_priv       | enum('N','Y')        | NO   |     | N                 |       |
| Trigger_priv           | enum('N','Y')        | NO   |     | N                 |       |
| Create_role_priv       | enum('N','Y')        | NO   |     | N                 |       |
| Drop_role_priv         | enum('N','Y')        | NO   |     | N                 |       |
| Account_locked         | enum('N','Y')        | NO   |     | N                 |       |
| Shutdown_priv          | enum('N','Y')        | NO   |     | N                 |       |
| Reload_priv            | enum('N','Y')        | NO   |     | N                 |       |
| FILE_priv              | enum('N','Y')        | NO   |     | N                 |       |
| Config_priv            | enum('N','Y')        | NO   |     | N                 |       |
| Create_Tablespace_Priv | enum('N','Y')        | NO   |     | N                 |       |
| Password_reuse_history | smallint(5) unsigned | YES  |     | <null>            |       |
| Password_reuse_time    | smallint(5) unsigned | YES  |     | <null>            |       |
| User_attributes        | json                 | YES  |     | <null>            |       |
| Token_issuer           | varchar(255)         | YES  |     | <null>            |       |
| Password_expired       | enum('N','Y')        | NO   |     | N                 |       |
| Password_last_changed  | timestamp            | YES  |     | CURRENT_TIMESTAMP |       |
| Password_lifetime      | smallint(5) unsigned | YES  |     | <null>            |       |
+------------------------+----------------------+------+-----+-------------------+-------+
44 rows in set
```

There are several types of columns in `mysql.user`:

* Scope:
  * `Host` and `User` are used to specify a TiDB account
* Privilege:
  * From `Select_priv` to `Drop_role_priv`, and from `Shutdown_priv` to `Create_Tablespace_Priv`: see [privileges required for TiDB operations](/privilege-management.md#privileges-required-for-tidb-operations)
* Security
  * `authentication_string` and `plugin`: `authentication_string` records credentials for the accounts. Credentials are interpreted using the authentication plugin named in the `plugin` column.
  * `Account_locked` records the account locking state.
  * `Password_reuse_history` and `Password_reuse_time` are used for [password reuse policy](/password-management.md#password-reuse-policy)
  * `User_attributes` provides information about user comments and user attributes
  * `Token_issuer` is used for [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token)
  * `Password_expired`, `Password_last_changed` and `Password_lifetime` are used for [password expiration policy](/password-management.md#password-expiration-policy)

## Cluster status system tables

* The `tidb` table contains some global information about TiDB:

    * `bootstrapped`: whether the TiDB cluster has been initialized. Note that this value is read-only and cannot be modified.
    * `tidb_server_version`: the version information of TiDB when it is initialized. Note that this value is read-only and cannot be modified.
    * `system_tz`: the system time zone of TiDB.
    * `new_collation_enabled`: whether TiDB has enabled the [new framework for collations](/character-set-and-collation.md#new-framework-for-collations). Note that this value is read-only and cannot be modified.

## Server-side help system tables

Currently, the `help_topic` is NULL.

## Statistics system tables

- `stats_buckets`: the buckets of statistics
- `stats_histograms`: the histograms of statistics
- `stats_top_n`: the TopN of statistics
- `stats_meta`: the meta information of tables, such as the total number of rows and updated rows
- `stats_extended`: extended statistics, such as the order correlation between columns
- `stats_feedback`: the query feedback of statistics
- `stats_fm_sketch`: the FMSketch distribution of the histogram of the statistics column
- `analyze_options`: the default `analyze` options for each table
- `column_stats_usage`: the usage of column statistics
- `schema_index_usage`: the usage of indexes
- `analyze_jobs`: the ongoing statistics collection tasks and the history task records within the last 7 days

## Execution plan-related system tables

- `bind_info`: the binding information of execution plans
- `capture_plan_baselines_blacklist`: the blocklist for the automatic binding of the execution plan

## GC worker system tables

> **Note:**
>
> The GC worker system tables are only applicable to TiDB Self-Hosted and not available on [TiDB Cloud](https://docs.pingcap.com/tidbcloud/).

- `gc_delete_range`: the KV range to be deleted
- `gc_delete_range_done`: the deleted KV range

## System tables related to cached tables

- `table_cache_meta` stores the metadata of cached tables.

## TTL related system tables

* `tidb_ttl_table_status`: the previously executed TTL job and ongoing TTL job for all TTL tables
* `tidb_ttl_task`: the current ongoing TTL subtasks
* `tidb_ttl_job_history`: the execution history of TTL tasks in the last 90 days

## System tables related to runaway queries

* `tidb_runaway_queries`: the history records of all identified runaway queries in the past 7 days
* `tidb_runaway_watch`: the watch list of runaway queries
* `tidb_runaway_watch_done`: a watch list of deleted or expired runaway queries

## System tables related to metadata locks

* `tidb_mdl_view`: a view of metadata locks. You can use it to view information about the currently blocked DDL statements
* `tidb_mdl_info`: used internally by TiDB to synchronize metadata locks across nodes

## System tables related to DDL statements

* `tidb_ddl_history`: the history records of DDL statements
* `tidb_ddl_jobs`: the metadata of DDL statements that are currently being executed by TiDB
* `tidb_ddl_reorg`: the metadata of physical DDL statements (such as adding indexes) that are currently being executed by TiDB

## System tables related to TiDB Distributed eXecution Framework (DXF)

* `dist_framework_meta`: the metadata of the Distributed eXecution Framework (DXF) task scheduler
* `tidb_global_task`: the metadata of the current DXF task
* `tidb_global_task_history`: the metadata of the historical DXF tasks, including both succeeded and failed tasks
* `tidb_background_subtask`: the metadata of the current DXF subtask
* `tidb_background_subtask_history`: the metadata of the historical DXF subtasks

## System tables related to Resource Control

* `request_unit_by_group`: the history records of consumed resource units (RUs) of all resource groups

## Miscellaneous system tables

<CustomContent platform="tidb">

> **Note:**
>
> The `tidb`, `expr_pushdown_blacklist`, `opt_rule_blacklist`, `table_cache_meta`, `tidb_import_jobs`, and `tidb_timers` system tables are only applicable to TiDB Self-Hosted and not available on [TiDB Cloud](https://docs.pingcap.com/tidbcloud/).

- `GLOBAL_VARIABLES`: global system variable table
- `expr_pushdown_blacklist`: the blocklist for expression pushdown
- `opt_rule_blacklist`: the blocklist for logical optimization rules
- `tidb_import_jobs`: the job information of [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
- `tidb_timers`: the metadata of internal timers

</CustomContent>

<CustomContent platform="tidb-cloud">

- `GLOBAL_VARIABLES`: global system variable table

</CustomContent>