---
title: 元信息锁
summary: 介绍 TiDB 中元信息锁的概念、原理及实现细节。
---

# 元信息锁

本文档介绍 TiDB 中的元信息锁。

## 概念

TiDB 使用在线异步 schema 变更算法以支持更改元数据对象。当一个事务被执行时，会在事务开始时获取对应的元信息快照。如果在事务期间元信息发生了变更，为了保证数据一致性，TiDB 会返回 `Information schema is changed` 错误，事务提交失败。

为了解决该问题，TiDB v6.3.0 在在线 DDL 算法中引入了元信息锁。为避免大多数 DML 报错，TiDB 在表元信息变更期间协调 DML 和 DDL 的优先级，使 DDL 的执行等待持有旧元信息的 DML 提交。

## 场景

TiDB 中的元信息锁适用于所有 DDL 语句，例如：

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- [`ADD COLUMN`](/sql-statements/sql-statement-add-column.md)
- [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
- [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
- [`DROP PARTITION`](/partitioned-table.md#partition-management)
- [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)
- [`EXCHANGE PARTITION`](/partitioned-table.md#partition-management)
- [`REORGANIZE PARTITION`](/partitioned-table.md#partition-management)
- [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)
- [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)

启用元信息锁可能会对 TiDB 中 DDL 任务的执行产生一定的性能影响。为减少影响，以下场景不需要元信息锁：

+ 开启自动提交的 `SELECT` 查询
+ 启用 Stale Read
+ 访问临时表

## 使用方法

自 v6.5.0 起，TiDB 默认启用元信息锁。当你将现有集群从 v6.4.0 或更早版本升级到 v6.5.0 或更高版本时，TiDB 会自动启用元信息锁。若需关闭元信息锁，可以将系统变量 [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) 设置为 `OFF`。

## 影响

- 对于 DML，元信息锁不会阻塞其执行，也不会导致任何死锁。
- 启用元信息锁后，事务中某个元信息对象的信息在首次访问时确定，之后不会再发生变化。
- 对于 DDL，在变更元信息状态时，DDL 可能会被旧事务阻塞。如下所示：

    | Session 1 | Session 2 |
    |:---------------------------|:----------|
    | `CREATE TABLE t (a INT);`  |           |
    | `INSERT INTO t VALUES(1);` |           |
    | `BEGIN;`                   |           |
    |                            | `ALTER TABLE t ADD COLUMN b INT;` |
    | `SELECT * FROM t;`<br/>(使用表 `t` 当前元信息版本。返回 `(a=1, b=NULL)` 并锁定表 `t`。)         |           |
    |                            | `ALTER TABLE t ADD COLUMN c INT;` (被 Session 1 阻塞) |

    在可重复读隔离级别下，从事务开始到确定表元信息的时间点，如果执行了需要数据变更的 DDL（如添加索引、修改列类型等），DDL 会返回如下错误：

    | Session 1                  | Session 2                                 |
    |:---------------------------|:------------------------------------------|
    | `CREATE TABLE t (a INT);`  |                                           |
    | `INSERT INTO t VALUES(1);` |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t ADD INDEX idx(a);`         |
    | `SELECT * FROM t;` (索引 `idx` 不可用) |                    |
    | `COMMIT;`                  |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
    | `SELECT * FROM t;` (返回 `ERROR 8028 (HY000): public column a has changed`) | |

## 可观测性

TiDB v6.3.0 引入了 `mysql.tidb_mdl_view` 视图，帮助你获取当前被阻塞的 DDL 信息。

> **注意：**
>
> 查询 `mysql.tidb_mdl_view` 视图需要 [`PROCESS` privilege](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)。

以下以为表 `t` 添加索引为例。假设有 DDL 语句 `ALTER TABLE t ADD INDEX idx(a)`：

```sql
TABLE mysql.tidb_mdl_view\G
```

```
*************************** 1. row ***************************
     job_id: 118
    db_name: test
 table_name: t
      query: ALTER TABLE t ADD COLUMN c INT
 session_id: 1547698182
 start_time: 2025-03-19 09:52:36.509000
SQL_DIGESTS: ["begin","select * from `t`"]
1 row in set (0.00 sec)

```

从上述输出可以看到，`SESSION ID` 为 `1547698182` 的事务阻塞了 `ADD COLUMN` DDL。`SQL_DIGEST` 显示了该事务执行的 SQL 语句，即 ``["begin","select * from `t`"]``。若需让被阻塞的 DDL 继续执行，可以使用如下全局 `KILL` 语句终止 `1547698182` 事务：

```sql
mysql> KILL 1547698182;
Query OK, 0 rows affected (0.00 sec)
```

终止事务后，可以再次查询 `mysql.tidb_mdl_view` 视图。此时输出中不再显示上述事务，说明 DDL 已不再被阻塞。

```sql
TABLE mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

## 原理

### 问题描述

TiDB 中的 DDL 操作为在线 DDL 模式。当 DDL 语句执行时，被修改对象的元信息版本可能会经历多次小版本变更。在线异步元信息变更算法只保证相邻两个小版本之间是兼容的，即两个版本之间的操作不会破坏 DDL 变更对象的数据一致性。

以为表添加索引为例，DDL 语句的状态变更如下：None -> Delete Only，Delete Only -> Write Only，Write Only -> Write Reorg，Write Reorg -> Public。

以下事务的提交过程违反了上述约束：

| 事务  | 事务使用的版本  | 集群中的最新版本 | 版本差异 |
|:-----|:-----------|:-----------|:----|
| txn1 | None       | None       | 0   |
| txn2 | DeleteOnly | DeleteOnly | 0   |
| txn3 | WriteOnly  | WriteOnly  | 0   |
| txn4 | None       | WriteOnly  | 2   |
| txn5 | WriteReorg | WriteReorg | 0   |
| txn6 | WriteOnly  | WriteReorg | 1   |
| txn7 | Public     | Public     | 0   |

在上表中，`txn4` 提交时使用的元信息版本与集群中的最新版本相差 2 个版本，这可能导致数据不一致。

### 实现细节

元信息锁可以保证 TiDB 集群中所有事务使用的元信息版本最多只相差 1 个版本。为实现该目标，TiDB 实现了以下两条规则：

- 执行 DML 时，TiDB 会在事务上下文中记录 DML 访问过的元信息对象（如表、视图）及其对应的元信息版本。这些记录会在事务提交时清理。
- 当 DDL 语句变更状态时，最新的元信息会被推送到所有 TiDB 节点。如果与该状态变更相关的所有事务在某个 TiDB 节点上使用的元信息版本与当前元信息版本的差异小于 2，则认为该 TiDB 节点已获取该元信息对象的元信息锁。只有当集群中所有 TiDB 节点都获取到该元信息对象的元信息锁后，才能执行下一次状态变更。