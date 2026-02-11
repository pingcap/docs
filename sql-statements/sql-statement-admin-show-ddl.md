---
title: ADMIN SHOW DDL [JOBS|JOB QUERIES] | TiDB SQL Statement Reference
summary: TiDB 数据库中 ADMIN 用法概述。
---

# ADMIN SHOW DDL [JOBS|JOB QUERIES]

`ADMIN SHOW DDL [JOBS|JOB QUERIES]` 语句用于显示正在运行和最近完成的 DDL 任务的信息。

## 语法

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

## 示例

### `ADMIN SHOW DDL`

要查看当前正在运行的 DDL 任务状态，可使用 `ADMIN SHOW DDL`。输出内容包括当前 schema 版本、owner 的 DDL ID 和地址、正在运行的 DDL 任务及 SQL 语句，以及当前 TiDB 实例的 DDL ID。返回结果字段说明如下：

- `SCHEMA_VER`：表示 schema 版本的数字。
- `OWNER_ID`：DDL owner 的 UUID。参见 [`TIDB_IS_DDL_OWNER()`](/functions-and-operators/tidb-functions.md)。
- `OWNER_ADDRESS`：DDL owner 的 IP 地址。
- `RUNNING_JOBS`：正在运行的 DDL 任务的详细信息。
- `SELF_ID`：你当前连接的 TiDB 节点的 UUID。如果 `SELF_ID` 与 `OWNER_ID` 相同，说明你连接的是 DDL owner。
- `QUERY`：查询的语句内容。

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

`ADMIN SHOW DDL JOBS` 语句用于查看当前 DDL 任务队列中的 10 个任务（包括正在运行和等待中的任务，如有），以及已执行 DDL 任务队列中的最近 10 个任务（如有）。返回结果字段说明如下：

<CustomContent platform="tidb">

- `JOB_ID`：每个 DDL 操作对应一个 DDL 任务。`JOB_ID` 在全局范围内唯一。
- `DB_NAME`：执行 DDL 操作的数据库名称。
- `TABLE_NAME`：执行 DDL 操作的表名称。
- `JOB_TYPE`：DDL 操作类型。常见类型包括：
    - `create schema`：对应 [`CREATE SCHEMA`](/sql-statements/sql-statement-create-database.md) 操作。
    - `create table`：对应 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 操作。
    - `create view`：对应 [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md) 操作。
    - `add index`：对应 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 操作。
- `SCHEMA_STATE`：DDL 操作对象的当前状态。如果 `JOB_TYPE` 为 `ADD INDEX`，则为索引的状态；如果为 `ADD COLUMN`，则为列的状态；如果为 `CREATE TABLE`，则为表的状态。常见状态包括：
    - `none`：表示不存在。通常在 `DROP` 操作后或 `CREATE` 操作失败回滚后会变为 `none` 状态。
    - `delete only`、`write only`、`delete reorganization`、`write reorganization`：这四种为中间状态。具体含义参见 [TiDB 在线 DDL 异步变更原理](/best-practices/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb)。由于中间状态转换较快，通常操作过程中不会看到这些状态。只有在执行 `ADD INDEX` 操作时，可能会看到 `write reorganization`，表示正在添加索引数据。
    - `public`：表示存在且可被用户访问。通常在 `CREATE TABLE` 和 `ADD INDEX`（或 `ADD COLUMN`）操作完成后会变为 `public`，表示新建的表、列、索引可正常读写。
- `SCHEMA_ID`：执行 DDL 操作的数据库 ID。
- `TABLE_ID`：执行 DDL 操作的表 ID。
- `ROW_COUNT`：执行 `ADD INDEX` 操作时，表示已添加的数据行数。
- `CREATE_TIME`：DDL 操作的创建时间。
- `START_TIME`：DDL 操作的开始时间。
- `END_TIME`：DDL 操作的结束时间。
- `STATE`：DDL 操作的状态。常见状态包括：
    - `none`：表示操作尚未开始。
    - `queueing`：表示操作任务已进入 DDL 任务队列，但因等待前序 DDL 任务完成尚未执行。另一种情况是执行 `DROP` 操作后，`queueing` 状态会变为 `done`，但很快会更新为 `synced`，表示所有 TiDB 实例已同步到该状态。
    - `running`：表示操作正在执行。
    - `synced`：表示操作已成功执行，且所有 TiDB 实例已同步到该状态。
    - `rollback done`：表示操作失败且回滚已完成。
    - `rollingback`：表示操作失败，正在回滚。
    - `cancelling`：表示操作正在被取消。该状态仅在使用 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 任务时出现。
    - `cancelled`：表示操作已被取消。
    - `pausing`：表示操作正在被暂停。
    - `paused`：表示操作已被暂停。该状态仅在使用 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 命令暂停 DDL 任务时出现。你可以使用 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 命令恢复 DDL 任务。
    - `done`：表示操作已在 TiDB owner 节点成功执行，但其他 TiDB 节点尚未同步该 DDL 任务的变更。
- `COMMENTS`：包含用于诊断的附加信息。
    - `ingest`：通过 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 配置的加速添加索引回填的 ingest 任务。
    - `txn`：在禁用 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 后的基于事务的索引回填。
    - `txn-merge`：带有临时索引的事务性回填，回填完成后与原索引合并。
    - `DXF`：通过 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 配置的分布式执行框架（DXF）任务。
    - `service_scope`：通过 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 配置的 TiDB 节点服务作用域。
    - `thread`：回填任务的并发数。可通过 `tidb_ddl_reorg_worker_cnt` 设置初始值，支持通过 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md) 动态修改。
    - `batch_size`：回填任务的批量大小。可通过 `tidb_ddl_reorg_batch_size` 设置初始值，支持通过 `ADMIN ALTER DDL JOBS` 动态修改。
    - `max_write_speed`：ingest 任务导入时的流控。初始值可通过 `tidb_ddl_reorg_max_write_speed` 设置，支持通过 `ADMIN ALTER DDL JOBS` 动态修改。

</CustomContent>

<CustomContent platform="tidb-cloud">

- `JOB_ID`：每个 DDL 操作对应一个 DDL 任务。`JOB_ID` 在全局范围内唯一。
- `DB_NAME`：执行 DDL 操作的数据库名称。
- `TABLE_NAME`：执行 DDL 操作的表名称。
- `JOB_TYPE`：DDL 操作类型。
- `SCHEMA_STATE`：DDL 操作对象的当前状态。如果 `JOB_TYPE` 为 `ADD INDEX`，则为索引的状态；如果为 `ADD COLUMN`，则为列的状态；如果为 `CREATE TABLE`，则为表的状态。常见状态包括：
    - `none`：表示不存在。通常在 `DROP` 操作后或 `CREATE` 操作失败回滚后会变为 `none` 状态。
    - `delete only`、`write only`、`delete reorganization`、`write reorganization`：这四种为中间状态。具体含义参见 [TiDB 在线 DDL 异步变更原理](https://docs.pingcap.com/tidb/stable/ddl-introduction#how-the-online-ddl-asynchronous-change-works-in-tidb)。由于中间状态转换较快，通常操作过程中不会看到这些状态。只有在执行 `ADD INDEX` 操作时，可能会看到 `write reorganization`，表示正在添加索引数据。
    - `public`：表示存在且可被用户访问。通常在 `CREATE TABLE` 和 `ADD INDEX`（或 `ADD COLUMN`）操作完成后会变为 `public`，表示新建的表、列、索引可正常读写。
- `SCHEMA_ID`：执行 DDL 操作的数据库 ID。
- `TABLE_ID`：执行 DDL 操作的表 ID。
- `ROW_COUNT`：执行 `ADD INDEX` 操作时，表示已添加的数据行数。
- `START_TIME`：DDL 操作的开始时间。
- `STATE`：DDL 操作的状态。常见状态包括：
    - `queueing`：表示操作任务已进入 DDL 任务队列，但因等待前序 DDL 任务完成尚未执行。另一种情况是执行 `DROP` 操作后，会变为 `none` 状态，但很快会更新为 `synced`，表示所有 TiDB 实例已同步到该状态。
    - `running`：表示操作正在执行。
    - `synced`：表示操作已成功执行，且所有 TiDB 实例已同步到该状态。
    - `rollback done`：表示操作失败且回滚已完成。
    - `rollingback`：表示操作失败，正在回滚。
    - `cancelling`：表示操作正在被取消。该状态仅在使用 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 任务时出现。
    - `paused`：表示操作已被暂停。该状态仅在使用 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 命令暂停 DDL 任务时出现。你可以使用 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 命令恢复 DDL 任务。

</CustomContent>

以下示例展示了 `ADMIN SHOW DDL JOBS` 的结果：

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

从上述输出可以看出：

- 任务 565 当前正在进行中（`STATE` 为 `running`）。schema 状态当前为 `write reorganization`，任务完成后会切换为 `public`，表示该变更对用户会话可见。`end_time` 列为 `NULL`，说明任务的完成时间尚未知晓。

- `job_id` 为 566 的 `STATE` 显示为 `queueing`，表示正在排队。待 565 任务完成并开始执行 566 时，566 的 `STATE` 会变为 `running`。

- 对于如删除索引、删除表等破坏性变更，任务完成后 `SCHEMA_STATE` 会变为 `none`。对于新增变更，`SCHEMA_STATE` 会变为 `public`。

如需限制显示的行数，可指定数量和 where 条件：

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

* `NUM`：查看已完成 DDL 任务队列中最近 `NUM` 条结果。未指定时，默认 `NUM` 为 10。
* `WHERE`：添加过滤条件。

### `ADMIN SHOW DDL JOB QUERIES`

要查看指定 `job_id` 对应 DDL 任务的原始 SQL 语句，可使用 `ADMIN SHOW DDL JOB QUERIES`：

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

你只能在 DDL 历史任务队列的最近十条结果中，查询指定 `job_id` 对应的正在运行的 DDL 任务。

### `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`

要在指定范围 `[n+1, n+m]` 内，查看 DDL 任务对应的原始 SQL 语句，可使用 `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`：

```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT m;  # 获取前 m 行
 ADMIN SHOW DDL JOB QUERIES LIMIT n, m;  # 获取第 n+1 行到 n+m 行
 ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n;  # 获取第 n+1 行到 n+m 行
 ```

 其中 `n` 和 `m` 为大于等于 0 的整数。

 ```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT 3;  # 获取前 3 行
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
 ADMIN SHOW DDL JOB QUERIES LIMIT 6, 2;  # 获取第 7-8 行
 +--------+----------------------------------------------------------------------------+
 | JOB_ID | QUERY                                                                      |
 +--------+----------------------------------------------------------------------------+
 |     52 | ALTER TABLE t1 ADD INDEX index1 (col1)                                     |
 |     51 | CREATE TABLE IF NOT EXISTS t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
 +--------+----------------------------------------------------------------------------+
 3 rows in set (0.00 sec)
 ```

 ```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT 3 OFFSET 4;  # 获取第 5-7 行
 +--------+----------------------------------------+
 | JOB_ID | QUERY                                  |
 +--------+----------------------------------------+
 |     54 | DROP TABLE IF EXISTS t3                |
 |     53 | ALTER TABLE t1 DROP INDEX index1       |
 |     52 | ALTER TABLE t1 ADD INDEX index1 (col1) |
 +--------+----------------------------------------+
 3 rows in set (0.00 sec)
 ```

 你可以在 DDL 历史任务队列的任意指定范围内，查询指定 `job_id` 对应的正在运行的 DDL 任务。该语法不受 `ADMIN SHOW DDL JOB QUERIES` 最近十条结果的限制。

## MySQL 兼容性

该语句为 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [DDL 简介](/best-practices/ddl-introduction.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
* [`ADMIN ALTER DDL`](/sql-statements/sql-statement-admin-alter-ddl.md)
* [INFORMATION_SCHEMA.DDL_JOBS](/information-schema/information-schema-ddl-jobs.md)
