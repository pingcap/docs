---
title: ADMIN ALTER DDL JOBS
summary: An overview of the usage of `ADMIN ALTER DDL JOBS` for the TiDB database.
---

# ADMIN ALTER DDL JOBS

The `ADMIN ALTER DDL JOBS` statement allows you to modify the parameter of a single running DDL job. For example:

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
```

- `101`: indicates the ID of the DDL job. You can obtain the ID by executing [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md).
- `THREAD`: indicates the concurrency of the DDL job. You can configure its initial value using the system variable [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt).

The DDL job types supported by the `ADMIN ALTER DDL JOBS` statement include `ADD INDEX`, `MODIFY COLUMN`, and `REORGANIZE PARTITION`. For other DDL job types, executing `ADMIN ALTER DDL JOBS` returns the `unsupported DDL operation` error.

Currently, you can only modify the parameters of a single DDL job by executing `ADMIN ALTER DDL JOBS`. Modifying the parameters of multiple DDL job IDs at the same time is not supported.

The following are the supported parameters for different DDL jobs and their corresponding system variables:

- `ADD INDEX`:
    - `THREAD`: the concurrency of the DDL job. The initial value is set by `tidb_ddl_reorg_worker_cnt`.
    - `BATCH_SIZE`: the batch size. The initial value is set by [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size).
    - `MAX_WRITE_SPEED`: the maximum bandwidth limit for importing index records into each TiKV. The initial value is set by [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v6512-v755-and-v850).

  Currently, the preceding parameters only work for `ADD INDEX` jobs that are submitted and running after [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) is disabled.

- `MODIFY COLUMN`:
    - `THREAD`: the concurrency of the DDL job. The initial value is set by `tidb_ddl_reorg_worker_cnt`.
    - `BATCH_SIZE`: the batch size. The initial value is set by `tidb_ddl_reorg_batch_size`.

- `REORGANIZE PARTITION`:
    - `THREAD`: the concurrency of the DDL job. The initial value is set by `tidb_ddl_reorg_worker_cnt`.
    - `BATCH_SIZE`: the batch size. The initial value is set by `tidb_ddl_reorg_batch_size`.

The value ranges of the preceding parameters are consistent with those of the corresponding system variables.

`ADMIN ALTER DDL JOBS` takes effect only on running DDL jobs. If the DDL job does not exist or has already completed, executing this statement returns the `ddl job is not running` error.

The following are some examples of this statement:

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
ADMIN ALTER DDL JOBS 101 BATCH_SIZE = 256;
ADMIN ALTER DDL JOBS 101 MAX_WRITE_SPEED = '200MiB';
ADMIN ALTER DDL JOBS 101 THREAD = 8, BATCH_SIZE = 256;
```

To view the current parameter values for a specific DDL job, you can execute `ADMIN SHOW DDL JOBS`. The results are displayed in the `COMMENTS` column:

```sql
ADMIN SHOW DDL JOBS 1;
```

```
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE  | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE  | COMMENTS              |
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
|    124 | test    | t          | add index | public       |         2 |      122 |         3 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:08.363000 | synced | ingest, DXF, thread=8 |
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
1 row in set (0.01 sec)
```

## Synopsis

```ebnf+diagram
AdminAlterDDLStmt ::=
    'ADMIN' 'ALTER' 'DDL' 'JOBS' Int64Num AlterJobOptionList

AlterJobOptionList ::=
    AlterJobOption ( ',' AlterJobOption )*

AlterJobOption ::=
    identifier "=" SignedLiteral
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
