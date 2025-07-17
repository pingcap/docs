---
title: ADMIN CANCEL DDL | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中使用 ADMIN CANCEL DDL 的概述。
category: reference
---

# ADMIN CANCEL DDL

`ADMIN CANCEL DDL` 语句允许你取消正在执行的 DDL 任务。可以通过运行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 获取 `job_id`。

`ADMIN CANCEL DDL` 语句还允许你取消已提交但尚未完成执行的 DDL 任务。取消后，执行该 DDL 任务的 SQL 语句会返回 `ERROR 8214 (HY000): Cancelled DDL job` 错误。如果你取消的 DDL 任务已经完成，则在 `RESULT` 列中会显示 `DDL Job:90 not found` 错误，表示该任务已从 DDL 等待队列中移除。

## 语法概要

```ebnf+diagram
AdminCancelDDLStmt ::=
    'ADMIN' 'CANCEL' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

若要取消当前正在运行的 DDL 任务，并返回对应任务是否成功取消的结果，可以使用 `ADMIN CANCEL DDL JOBS`：

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

如果操作未能成功取消任务，会显示具体原因。

> **注意：**
>
> - 在 v6.2.0 之前，只有此操作可以取消 DDL 任务，所有其他操作和环境变更（如机器重启和集群重启）都不能取消这些任务。从 v6.2.0 开始，可以通过 [`KILL`](/sql-statements/sql-statement-kill.md) 语句杀死正在进行的 DDL 任务以实现取消。
> - 此操作可以同时取消多个 DDL 任务。你可以通过 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 获取 DDL 任务的 ID。
> - 如果你要取消的任务已经完成，取消操作会失败。

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
