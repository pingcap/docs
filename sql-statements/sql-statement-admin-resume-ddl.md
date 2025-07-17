---
title: ADMIN RESUME DDL JOBS
summary: 关于 TiDB 数据库中 ADMIN RESUME DDL 的使用概述。
---

# ADMIN RESUME DDL JOBS

`ADMIN RESUME DDL` 允许你恢复已暂停的 DDL 任务。你可以通过运行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 来查找 `job_id`。

你可以使用此语句来恢复已暂停的 DDL 任务。恢复完成后，执行该 DDL 任务的 SQL 语句仍会显示为正在执行状态。如果你尝试恢复已完成的 DDL 任务，在 `RESULT` 列中会显示 `DDL Job:90 not found` 错误，表示该任务已从 DDL 等待队列中被移除。

## 语法概要

```ebnf+diagram
AdminResumeDDLStmt ::=
    'ADMIN' 'RESUME' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

`ADMIN RESUME DDL JOBS` 会恢复当前暂停的 DDL 任务，并返回任务是否成功恢复。

```sql
ADMIN RESUME DDL JOBS job_id [, job_id] ...;
```

如果恢复失败，会显示具体的失败原因。

<CustomContent platform="tidb">

> **注意：**
>
> + 在集群升级期间，正在进行的 DDL 任务会被暂停，升级过程中发起的 DDL 任务也会暂停。升级完成后，所有暂停的 DDL 任务将会恢复。升级期间的暂停和恢复操作由系统自动处理。详情请参见 [TiDB 平滑升级](/smooth-upgrade-tidb.md)。
> + 此语句可以恢复多个 DDL 任务。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 来获取 DDL 任务的 `job_id`。
> + 其他状态（非 `paused`）的 DDL 任务无法恢复，恢复操作会失败。
> + 如果你尝试多次恢复同一任务，TiDB 会报告错误 `Error Number: 8261`。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注意：**
>
> + 在集群升级期间，正在进行的 DDL 任务会被暂停，升级过程中发起的 DDL 任务也会暂停。升级完成后，所有暂停的 DDL 任务将会恢复。升级期间的暂停和恢复操作由系统自动处理。详情请参见 [TiDB 平滑升级](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)。
> + 此语句可以恢复多个 DDL 任务。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 来获取 DDL 任务的 `job_id`。
> + 其他状态（非 `paused`）的 DDL 任务无法恢复，恢复操作会失败。
> + 如果你尝试多次恢复同一任务，TiDB 会报告错误 `Error Number: 8261`。

</CustomContent>

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN ALTER DDL`](/sql-statements/sql-statement-admin-alter-ddl.md)