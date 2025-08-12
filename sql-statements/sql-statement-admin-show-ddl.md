---
title: ADMIN SHOW DDL [JOBS|JOB QUERIES] | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
---

# ADMIN SHOW DDL [JOBS|JOB QUERIES]

The `ADMIN SHOW DDL [JOBS|JOB QUERIES]` statement shows information about running and recently completed DDL jobs.

## Synopsis

```ebnf+diagram
AdminShowDDLStmt ::=
    'ADMIN' 'SHOW' 'DDL'
    (
        'JOBS' Int64Num? WhereClauseOptional
    |   'JOB' 'QUERIES' NumList
    |   'JOB' 'QUERIES' 'LIMIT' m ( ('OFFSET' | ',') n )?
    )?

NumList ::=
    Int64Num ( ',' Int64Num )*

WhereClauseOptional ::=
    WhereClause?
```

## Examples

### `ADMIN SHOW DDL`

To view the status of the currently running DDL jobs, use `ADMIN SHOW DDL`. The output includes the current schema version, the DDL ID and address of the owner, the running DDL jobs and SQL statements, and the DDL ID of the current TiDB instance. The returned result fields are described as follows:

- `SCHEMA_VER`: a number indicating the version of the schema.
- `OWNER_ID`: the UUID of the DDL owner. See also [`TIDB_IS_DDL_OWNER()`](/functions-and-operators/tidb-functions.md).
- `OWNER_ADDRESS`: the IP address of the DDL owner.
- `RUNNING_JOBS`: details about the running DDL job.
- `SELF_ID`: the UUID of the TiDB node to which you are currently connected. If `SELF_ID` is the same as the `OWNER_ID`, it means that you are connected to the DDL owner.
- `QUERY`: the statements of the queries.

```sql
ADMIN SHOW DDL\G;
```

```sql
*************************** 1. row ***************************
   SCHEMA_VER: 26
     OWNER_ID: 2d1982af-fa63-43ad-a3d5-73710683cc63
OWNER_ADDRESS: 0.0.0.0:4000
 RUNNING_JOBS:
      SELF_ID: 2d1982af-fa63-43ad-a3d5-73710683cc63
        QUERY:
1 row in set (0.00 sec)
```

### `ADMIN SHOW DDL JOBS`

The `ADMIN SHOW DDL JOBS` statement is used to view the 10 jobs in the current DDL job queue, including running and pending jobs (if any), and the last 10 jobs in the executed DDL job queue (if any). The returned result fields are described as follows:

<CustomContent platform="tidb">

- `JOB_ID`: each DDL operation corresponds to a DDL job. `JOB_ID` is globally unique.
- `DB_NAME`: the name of the database where the DDL operation is performed.
- `TABLE_NAME`: the name of the table where the DDL operation is performed.
- `JOB_TYPE`: the type of DDL operation. Common job types include the following:
    - `create schema`: for [`CREATE SCHEMA`](/sql-statements/sql-statement-create-database.md) operations.
    - `create table`: for [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) operations.
    - `create view`: for [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md) operations.
    - `add index`: for [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) operations.
- `SCHEMA_STATE`: the current state of the schema object that the DDL operates on. If `JOB_TYPE` is `ADD INDEX`, it is the state of the index; if `JOB_TYPE` is `ADD COLUMN`, it is the state of the column; if `JOB_TYPE` is `CREATE TABLE`, it is the state of the table. Common states include the following:
    - `none`: indicates that it does not exist. Generally, after the `DROP` operation or after the `CREATE` operation fails and rolls back, it will become the `none` state.
    - `delete only`, `write only`, `delete reorganization`, `write reorganization`: these four states are intermediate states. For their specific meanings, see [How the Online DDL Asynchronous Change Works in TiDB](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb). As the intermediate state conversion is fast, these states are generally not visible during operation. Only when performing `ADD INDEX` operation can the `write reorganization` state be seen, indicating that index data is being added.
    - `public`: indicates that it exists and is available to users. Generally, after `CREATE TABLE` and `ADD INDEX` (or `ADD COLUMN`) operations are completed, it will become the `public` state, indicating that the newly created table, column, and index can be read and written normally.
- `SCHEMA_ID`: the ID of the database where the DDL operation is performed.
- `TABLE_ID`: the ID of the table where the DDL operation is performed.
- `ROW_COUNT`: when performing the `ADD INDEX` operation, it is the number of data rows that have been added.
- `CREATE_TIME`: the creation time of the DDL operation.
- `START_TIME`: the start time of the DDL operation.
- `END_TIME`: the end time of the DDL operation.
- `STATE`: the state of the DDL operation. Common states include the following:
    - `none`: indicates that the operation has not started yet.
    - `queueing`: indicates that the operation job has entered the DDL job queue but has not been executed because it is still waiting for an earlier DDL job to complete. Another reason might be that after executing the `DROP` operation, the `queueing` state will become the `done` state, but it will soon be updated to the `synced` state, indicating that all TiDB instances have been synchronized to that state.
    - `running`: indicates that the operation is being executed.
    - `synced`: indicates that the operation has been executed successfully and all TiDB instances have been synchronized to this state.
    - `rollback done`: indicates that the operation has failed and the rollback has been completed.
    - `rollingback`: indicates that the operation has failed and is rolling back.
    - `cancelling`: indicates that the operation is being canceled. This state only appears when you use the [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) command to cancel the DDL job.
    - `cancelled`: indicates that the operation has been canceled.
    - `pausing`: indicates that the operation is being paused.
    - `paused`: indicates that the operation has been paused. This state only appears when you use the [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) command to pause the DDL job. You can use the [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) command to resume the DDL job.
    - `done`: indicates that the operation has been successfully executed on the TiDB owner node, but other TiDB nodes have not yet synchronized the changes performed by this DDL job.
- `COMMENTS`: contains additional information for diagnostic purposes.
    - `ingest`: ingest tasks for accelerated adding index backfill configured via [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630).
    - `txn`: transaction-based index backfill after [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) is disabled.
    - `txn-merge`: transactional backfilling with a temporary index that gets merged with the original index when the backfilling is finished.
    - `DXF`: tasks executed with Distributed eXecution Framework (DXF) configured via [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710).
    - `service_scope`: the service scope of the TiDB node configured via [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740).
    - `thread`: the concurrency of backfill tasks. You can set the initial value by `tidb_ddl_reorg_worker_cnt`. It supports dynamic modification via [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md).
    - `batch_size`: the batch size of backfill tasks. You can set the initial value by `tidb_ddl_reorg_batch_size`. It supports dynamic modification via `ADMIN ALTER DDL JOBS`.
    - `max_write_speed`: flow control during ingest task import. The initial value can be set with `tidb_ddl_reorg_max_write_speed`. It supports dynamic modification via `ADMIN ALTER DDL JOBS`.

</CustomContent>

<CustomContent platform="tidb-cloud">

- `JOB_ID`: each DDL operation corresponds to a DDL job. `JOB_ID` is globally unique.
- `DB_NAME`: the name of the database where the DDL operation is performed.
- `TABLE_NAME`: the name of the table where the DDL operation is performed.
- `JOB_TYPE`: the type of DDL operation.
- `SCHEMA_STATE`: the current state of the schema object that the DDL operates on. If `JOB_TYPE` is `ADD INDEX`, it is the state of the index; if `JOB_TYPE` is `ADD COLUMN`, it is the state of the column; if `JOB_TYPE` is `CREATE TABLE`, it is the state of the table. Common states include the following:
    - `none`: indicates that it does not exist. Generally, after the `DROP` operation or after the `CREATE` operation fails and rolls back, it will become the `none` state.
    - `delete only`, `write only`, `delete reorganization`, `write reorganization`: these four states are intermediate states. For their specific meanings, see [How the Online DDL Asynchronous Change Works in TiDB](https://docs.pingcap.com/tidb/stable/ddl-introduction#how-the-online-ddl-asynchronous-change-works-in-tidb). As the intermediate state conversion is fast, these states are generally not visible during operation. Only when performing `ADD INDEX` operation can the `write reorganization` state be seen, indicating that index data is being added.
    - `public`: indicates that it exists and is available to users. Generally, after `CREATE TABLE` and `ADD INDEX` (or `ADD COLUMN`) operations are completed, it will become the `public` state, indicating that the newly created table, column, and index can be read and written normally.
- `SCHEMA_ID`: the ID of the database where the DDL operation is performed.
- `TABLE_ID`: the ID of the table where the DDL operation is performed.
- `ROW_COUNT`: when performing the `ADD INDEX` operation, it is the number of data rows that have been added.
- `START_TIME`: the start time of the DDL operation.
- `STATE`: the state of the DDL operation. Common states include the following:
    - `queueing`: indicates that the operation job has entered the DDL job queue but has not been executed because it is still waiting for an earlier DDL job to complete. Another reason might be that after executing the `DROP` operation, it will become the `none` state, but it will soon be updated to the `synced` state, indicating that all TiDB instances have been synchronized to that state.
    - `running`: indicates that the operation is being executed.
    - `synced`: indicates that the operation has been executed successfully and all TiDB instances have been synchronized to this state.
    - `rollback done`: indicates that the operation has failed and the rollback has been completed.
    - `rollingback`: indicates that the operation has failed and is rolling back.
    - `cancelling`: indicates that the operation is being canceled. This state only appears when you use the [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) command to cancel the DDL job.
    - `paused`: indicates that the operation has been paused. This state only appears when you use the [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) command to pause the DDL job. You can use the [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) command to resume the DDL job.

</CustomContent>

The following example shows the results of `ADMIN SHOW DDL JOBS`:

```sql
ADMIN SHOW DDL JOBS;
```

```sql
+--------+---------+------------+---------------------------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+----------+-------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE                        | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE    | COMMENTS    |
+--------+---------+------------+---------------------------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+----------+-------------+
|    565 | test    | sbtest1    | add index                       | write reorganization |       554 |      556 |         0 | 2024-11-22 12:39:25.475000 | 2024-11-22 12:39:25.524000 | NULL                       | running  | ingest, DXF |
|    566 | test    | sbtest1    | add index                       | none                 |       554 |      556 |         0 | 2024-11-22 12:39:26.425000 | NULL                       | NULL                       | queueing |             |
|    564 | test    | sbtest1    | alter table multi-schema change | none                 |       554 |      556 |         0 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:03.275000 | synced   |             |
|    564 | test    | sbtest1    | drop index /* subjob */         | none                 |       554 |      556 |         0 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:03.275000 | done     |             |
|    564 | test    | sbtest1    | drop index /* subjob */         | none                 |       554 |      556 |         0 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:02.975000 | 2024-11-22 12:39:03.275000 | done     |             |
|    563 | test    | sbtest1    | modify column                   | public               |       554 |      556 |         0 | 2024-11-22 12:38:35.624000 | 2024-11-22 12:38:35.624000 | 2024-11-22 12:38:35.674000 | synced   |             |
|    562 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:36:58.471000 | 2024-11-22 12:37:05.271000 | 2024-11-22 12:37:13.374000 | synced   | ingest, DXF |
|    561 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:36:57.771000 | 2024-11-22 12:36:57.771000 | 2024-11-22 12:37:04.671000 | synced   | ingest, DXF |
|    560 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:34:53.314000 | 2024-11-22 12:34:53.314000 | 2024-11-22 12:34:57.114000 | synced   | ingest      |
|    559 | test    | sbtest1    | drop index                      | none                 |       554 |      556 |         0 | 2024-11-22 12:34:43.565000 | 2024-11-22 12:34:43.565000 | 2024-11-22 12:34:43.764000 | synced   |             |
|    558 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:34:06.215000 | 2024-11-22 12:34:06.215000 | 2024-11-22 12:34:14.314000 | synced   | ingest, DXF |
|    557 | test    | sbtest1    | create table                    | public               |       554 |      556 |         0 | 2024-11-22 12:32:09.515000 | 2024-11-22 12:32:09.915000 | 2024-11-22 12:32:10.015000 | synced   |             |
|    555 | test    |            | create schema                   | public               |       554 |        0 |         0 | 2024-11-22 12:31:51.215000 | 2024-11-22 12:31:51.264000 | 2024-11-22 12:31:51.264000 | synced   |             |
|    553 | test    |            | drop schema                     | none                 |         2 |        0 |         0 | 2024-11-22 12:31:48.615000 | 2024-11-22 12:31:48.615000 | 2024-11-22 12:31:48.865000 | synced   |             |
+--------+---------+------------+---------------------------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+----------+-------------+
14 rows in set (0.00 sec)
```

From the output above:

- Job 565 is currently in progress (`STATE` of `running`). The schema state is currently in `write reorganization`, but will switch to `public` once the job is completed to note that the change can be observed publicly by user sessions. The `end_time` column is also `NULL` indicating that the completion time for the job is currently not known.

- The `STATE` for `job_id` 566 is shown as `queueing`, indicating that it is queuing. When job 565 completes and job 566 begins execution, the `STATE` for job 566 will change to `running`.

- For destructive changes such as dropping an index or dropping a table, the `SCHEMA_STATE` will change to `none` when the job is complete. For additive changes, the `SCHEMA_STATE` will change to `public`.

To limit the number of rows shown, specify a number and a where condition:

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

* `NUM`: to view the last `NUM` results in the completed DDL job queue. If not specified, `NUM` is by default 10.
* `WHERE`: to add filter conditions.

### `ADMIN SHOW DDL JOB QUERIES`

To view the original SQL statements of the DDL job corresponding to `job_id`, use `ADMIN SHOW DDL JOB QUERIES`:

```sql
ADMIN SHOW DDL JOBS;
ADMIN SHOW DDL JOB QUERIES 51;
```

```sql
mysql> ADMIN SHOW DDL JOB QUERIES 51;
+--------------------------------------------------------------+
| QUERY                                                        |
+--------------------------------------------------------------+
| CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------------------------------------------------------------+
1 row in set (0.02 sec)
```

You can only search the running DDL job corresponding to `job_id` within the last ten results in the DDL history job queue.

### `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`

 To view the original SQL statements of the DDL job within a specified range `[n+1, n+m]` corresponding to `job_id`, use `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`:

```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT m;  # Retrieve first m rows
 ADMIN SHOW DDL JOB QUERIES LIMIT n, m;  # Retrieve rows [n+1, n+m]
 ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n;  # Retrieve rows [n+1, n+m]
 ```

 where `n` and `m` are integers greater or equal to 0.

 ```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT 3;  # Retrieve first 3 rows
 +--------+--------------------------------------------------------------+
 | JOB_ID | QUERY                                                        |
 +--------+--------------------------------------------------------------+
 |     59 | ALTER TABLE t1 ADD INDEX index2 (col2)                       |
 |     60 | ALTER TABLE t2 ADD INDEX index1 (col1)                       |
 |     58 | CREATE TABLE t2 (id INT NOT NULL PRIMARY KEY auto_increment) |
 +--------+--------------------------------------------------------------+
 3 rows in set (0.00 sec)
 ```

 ```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT 6, 2;  # Retrieve rows 7-8
 +--------+----------------------------------------------------------------------------+
 | JOB_ID | QUERY                                                                      |
 +--------+----------------------------------------------------------------------------+
 |     52 | ALTER TABLE t1 ADD INDEX index1 (col1)                                     |
 |     51 | CREATE TABLE IF NOT EXISTS t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
 +--------+----------------------------------------------------------------------------+
 3 rows in set (0.00 sec)
 ```

 ```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT 3 OFFSET 4;  # Retrieve rows 5-7
 +--------+----------------------------------------+
 | JOB_ID | QUERY                                  |
 +--------+----------------------------------------+
 |     54 | DROP TABLE IF EXISTS t3                |
 |     53 | ALTER TABLE t1 DROP INDEX index1       |
 |     52 | ALTER TABLE t1 ADD INDEX index1 (col1) |
 +--------+----------------------------------------+
 3 rows in set (0.00 sec)
 ```

 You can search the running DDL job corresponding to `job_id` within an arbitrarily specified range of results in the DDL history job queue. This syntax does not have the limitation of the last ten results of `ADMIN SHOW DDL JOB QUERIES`.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [DDL introduction](/ddl-introduction.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
* [`ADMIN ALTER DDL`](/sql-statements/sql-statement-admin-alter-ddl.md)
* [INFORMATION_SCHEMA.DDL_JOBS](/information-schema/information-schema-ddl-jobs.md)
