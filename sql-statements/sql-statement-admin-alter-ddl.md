---
title: ADMIN ALTER DDL JOBS
summary: 关于在 TiDB 数据库中使用 `ADMIN ALTER DDL JOBS` 的用法概述。
---

# ADMIN ALTER DDL JOBS

> **注意：**
>
> 目前，该功能不适用于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

`ADMIN ALTER DDL JOBS` 语句允许你修改单个正在运行的 DDL job 的参数。例如：

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
```

- `101`：表示 DDL job 的 ID。你可以通过执行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 获取该 ID。
- `THREAD`：表示 DDL job 的并发度。你可以通过系统变量 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) 配置其初始值。

`ADMIN ALTER DDL JOBS` 语句支持的 DDL job 类型包括 `ADD INDEX`、`MODIFY COLUMN` 和 `REORGANIZE PARTITION`。对于其他 DDL job 类型，执行 `ADMIN ALTER DDL JOBS` 会返回 `unsupported DDL operation` 错误。

目前，你只能通过执行 `ADMIN ALTER DDL JOBS` 修改单个 DDL job 的参数，不支持同时修改多个 DDL job ID 的参数。

以下是不同 DDL job 支持的参数及其对应的系统变量：

- `ADD INDEX`：
    - `THREAD`：DDL job 的并发度。初始值由 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`：批处理大小。初始值由 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 设置。
    - `MAX_WRITE_SPEED`：向每个 TiKV 导入索引记录的最大带宽限制。初始值由 [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v6512-v755-and-v850) 设置。

  在 TiDB v8.5.5 之前的版本中，注意上述参数仅对在禁用 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 后提交并运行的 `ADD INDEX` job 生效。

<CustomContent platform="tidb-cloud" plan="premium">

> **注意：**
>
> 对于 TiDB Cloud Premium，`THREAD` 和 `MAX_WRITE_SPEED` 都会自动调整为合适的值，用户无法修改。如果你需要调整这些设置，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

- `MODIFY COLUMN`：
    - `THREAD`：DDL job 的并发度。初始值由 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`：批处理大小。初始值由 `tidb_ddl_reorg_batch_size` 设置。

- `REORGANIZE PARTITION`：
    - `THREAD`：DDL job 的并发度。初始值由 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`：批处理大小。初始值由 `tidb_ddl_reorg_batch_size` 设置。

上述参数的取值范围与对应系统变量的取值范围一致。

`ADMIN ALTER DDL JOBS` 仅对正在运行的 DDL job 生效。如果 DDL job 不存在或已完成，执行该语句会返回 `ddl job is not running` 错误。

以下是该语句的一些示例：

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
ADMIN ALTER DDL JOBS 101 BATCH_SIZE = 256;
ADMIN ALTER DDL JOBS 101 MAX_WRITE_SPEED = '200MiB';
ADMIN ALTER DDL JOBS 101 THREAD = 8, BATCH_SIZE = 256;
```

要查看指定 DDL job 当前的参数值，你可以执行 `ADMIN SHOW DDL JOBS`。结果会显示在 `COMMENTS` 列中：

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

## 语法

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

## 另请参阅

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
