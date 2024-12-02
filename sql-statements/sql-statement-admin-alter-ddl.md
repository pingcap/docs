---
title: ADMIN ALTER DDL JOBS
summary: An overview of the usage of `ADMIN ALTER DDL JOBS` for the TiDB database.
---

# ADMIN ALTER DDL JOBS

`ADMIN ALTER DDL JOBS` can be used to change the parameter of a running DDL job. For example:

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
```

- `101`: indicates the ID of the DDL job. You can obtain the ID by executing [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md). 
- `THREAD`: indicates the concurrency of the DDL job. You can configure the initial value of the thread by the system variable [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt).

The following DDL job types support `ADMIN ALTER DDL JOBS`: `ADD INDEX`, `MODIFY COLUMN`, and `REORGANIZE PARTITION`. For other DDL job types, executing `ADMIN ALTER DDL JOBS` reports an error `unsupported DDL operation`.

Currently, you can only modiy the parameters of a single DDL job by executing `ADMIN ALTER DDL JOBS`. Modifying the parameters of multiple IDs at the same time is not supported.

The following are the supported parameters for different DDL jobs and their corresponding system variables:

- `ADD INDEX`:
    - `THREAD`: the concurrency of the DDL job. The initial value is set by `tidb_ddl_reorg_worker_cnt`.
    - `BATCH_SIZE`: the batch size. You can set the initial value by [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size).
    - `MAX_WRITE_SPEED`: the maximum bandwidth limit for importing index records into each TiKV. The initial value is set by [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v850). 
  Currently this parameter only works for jobs with `ADD INDEX` submitted and running after disabling [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710).  

- `MODIFY COLUMN`:
    - `THREAD`: the concurrency of the DDL job. The initial value is set by `tidb_ddl_reorg_worker_cnt`.
    - `BATCH_SIZE`: the batch size. The initial value is set by `tidb_ddl_reorg_batch_size`.

- `REORGANIZE PARTITION`:
    - `THREAD`: the concurrency of the DDL job. The initial value is set by `tidb_ddl_reorg_worker_cnt`.
    - `BATCH_SIZE`: the batch size. The initial value is set by `tidb_ddl_reorg_batch_size`.

The value range of the parameter is consistent with that of the system variable.

`ADMIN ALTER DDL JOBS` takes effect only for running DDL jobs. If the DDL job does not exist or has ended, execution of this statement results in a `ddl job is not running` error.

The following are examples of this statement:

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
ADMIN ALTER DDL JOBS 101 BATCH_SIZE = 256;
ADMIN ALTER DDL JOBS 101 MAX_WRITE_SPEED = '200MiB';
ADMIN ALTER DDL JOBS 101 THREAD = 8, BATCH_SIZE = 256;
```

To view the current parameter values for a specific DDL job, you can execute `ADMIN SHOW DDL JOBS` and the results are displayed in the `COMMENTS` column:

```sql
mysql> ADMIN SHOW DDL JOBS 1;
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

`ADMIN ALTER DDL JOBS` statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
