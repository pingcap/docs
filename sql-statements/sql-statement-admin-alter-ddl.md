---
title: ADMIN ALTER DDL JOBS
summary: 关于在 TiDB 数据库中使用 `ADMIN ALTER DDL JOBS` 的概述。
---

# ADMIN ALTER DDL JOBS

> **Note:**
>
> 目前，该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

`ADMIN ALTER DDL JOBS` 语句允许你修改单个正在运行的 DDL 任务的参数。例如：

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
```

- `101`：表示 DDL 任务的 ID。你可以通过执行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 获取该 ID。
- `THREAD`：表示 DDL 任务的并发数。你可以使用系统变量 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) 配置其初始值。

`ADMIN ALTER DDL JOBS` 支持的 DDL 任务类型包括 `ADD INDEX`、`MODIFY COLUMN` 和 `REORGANIZE PARTITION`。对于其他 DDL 任务类型，执行 `ADMIN ALTER DDL JOBS` 会返回 `unsupported DDL operation` 错误。

目前，你只能通过执行 `ADMIN ALTER DDL JOBS` 来修改单个 DDL 任务的参数。不支持同时修改多个 DDL 任务 ID 的参数。

以下是不同 DDL 任务支持的参数及其对应的系统变量：

- `ADD INDEX`：
    - `THREAD`：DDL 任务的并发数。初始值由 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`：批处理大小。初始值由 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 设置。
    - `MAX_WRITE_SPEED`：导入索引记录到每个 TiKV 的最大带宽限制。初始值由 [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v6512-v755-and-v850) 设置。

  目前，以上参数仅对在 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 禁用后提交并运行的 `ADD INDEX` 任务生效。

- `MODIFY COLUMN`：
    - `THREAD`：DDL 任务的并发数。初始值由 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`：批处理大小。初始值由 `tidb_ddl_reorg_batch_size` 设置。

- `REORGANIZE PARTITION`：
    - `THREAD`：DDL 任务的并发数。初始值由 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`：批处理大小。初始值由 `tidb_ddl_reorg_batch_size` 设置。

以上参数的取值范围与对应的系统变量保持一致。

`ADMIN ALTER DDL JOBS` 仅对正在运行的 DDL 任务生效。如果 DDL 任务不存在或已完成，执行该语句会返回 `ddl job is not running` 错误。

以下是一些示例：

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
ADMIN ALTER DDL JOBS 101 BATCH_SIZE = 256;
ADMIN ALTER DDL JOBS 101 MAX_WRITE_SPEED = '200MiB';
ADMIN ALTER DDL JOBS 101 THREAD = 8, BATCH_SIZE = 256;
```

若要查看某个特定 DDL 任务的当前参数值，可以执行 `ADMIN SHOW DDL JOBS`。结果会显示在 `COMMENTS` 列中：

```sql
ADMIN SHOW DDL JOBS 1;
```

```
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE  | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE  | COMMENTS              |
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
|    124 | test    | t          | add index | public       |         2 |      122 |         3 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:08.363000 | synced | ingest, DXF, thread=8 |
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
```

## 概要

```ebnf+diagram
AdminAlterDDLStmt ::=
    'ADMIN' 'ALTER' 'DDL' 'JOBS' Int64Num AlterJobOptionList

AlterJobOptionList ::=
    AlterJobOption ( ',' AlterJobOption )*

AlterJobOption ::=
    identifier "=" SignedLiteral
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
