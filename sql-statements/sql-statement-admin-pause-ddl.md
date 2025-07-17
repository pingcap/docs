---
title: ADMIN PAUSE DDL JOBS
summary: 关于在 TiDB 数据库中使用 ADMIN PAUSE DDL JOBS 的概述。
---

# ADMIN PAUSE DDL JOBS

`ADMIN PAUSE DDL` 允许你暂停正在运行的 DDL 任务。可以通过运行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 来获取 `job_id`。

你可以使用此语句暂停已发出但尚未完成执行的 DDL 任务。暂停后，执行 DDL 任务的 SQL 语句不会立即返回，而是看起来仍在运行。如果你尝试暂停已经完成的 DDL 任务，在 `RESULT` 列中会看到 `DDL Job:90 not found` 错误，表示该任务已从 DDL 等待队列中被移除。

## 语法概要

```ebnf+diagram
AdminPauseDDLStmt ::=
    'ADMIN' 'PAUSE' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

`ADMIN PAUSE DDL JOBS` 会暂停当前正在运行的 DDL 任务，并返回任务是否成功暂停。可以通过 `ADMIN RESUME DDL JOBS` 恢复该任务。

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

如果暂停失败，会显示具体的失败原因。

<CustomContent platform="tidb">

> **Note:**
>
> + 这个语句可以暂停一个 DDL 任务，但其他操作和环境变更（如机器重启和集群重启）除集群升级外，不会暂停 DDL 任务。
> + 在集群升级期间，正在进行的 DDL 任务会被暂停，升级期间发起的 DDL 任务也会被暂停。升级完成后，所有暂停的 DDL 任务将会恢复。升级期间的暂停和恢复操作是自动进行的。详情请参见 [TiDB Smooth Upgrade](/smooth-upgrade-tidb.md)。
> + 这个语句可以暂停多个 DDL 任务。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 任务的 `job_id`。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **Note:**
>
> + 这个语句可以暂停一个 DDL 任务，但其他操作和环境变更（如机器重启和集群重启）除集群升级外，不会暂停 DDL 任务。
> + 在集群升级期间，正在进行的 DDL 任务会被暂停，升级期间发起的 DDL 任务也会被暂停。升级完成后，所有暂停的 DDL 任务将会恢复。升级期间的暂停和恢复操作是自动进行的。详情请参见 [TiDB Smooth Upgrade](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)。
> + 这个语句可以暂停多个 DDL 任务。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 任务的 `job_id`。

</CustomContent>

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
* [`ADMIN ALTER DDL`](/sql-statements/sql-statement-admin-alter-ddl.md)