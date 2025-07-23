---
title: Metadata Lock
summary: 介绍 TiDB 中元数据锁的概念、原理及实现细节。
---

# Metadata Lock

本文档介绍了 TiDB 中的元数据锁。

## 概念

TiDB 采用在线异步模式的 schema 变更算法，支持对元数据对象的变更。当一个事务执行时，它会在事务开始时获取对应的元数据快照。如果在事务期间元数据发生变化，为了确保数据一致性，TiDB 会返回 `Information schema is changed` 错误，事务无法提交。

为了解决这个问题，TiDB 从 v6.3.0 版本开始在在线 DDL 算法中引入了元数据锁。为了避免大部分 DML 错误，TiDB 在表元数据变更期间协调 DML 和 DDL 的优先级，使得执行 DDL 时等待持有旧元数据的 DML 提交。

## 场景

TiDB 中的元数据锁适用于所有 DDL 语句，例如：

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- [`ADD COLUMN`](/sql-statements/sql-statement-add-column.md)
- [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
- [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
- [`DROP PARTITION`](/partitioned-table.md#partition-management)
- [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)
- [`EXCHANGE PARTITION`](/partitioned-table.md#partition-management)
- [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)
- [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)

启用元数据锁可能会对 TiDB 中 DDL 任务的执行性能产生一定影响。为减少影响，以下列出一些不需要元数据锁的场景：

+ 自动提交的 `SELECT` 查询
+ 启用 Stale Read
+ 访问临时表

## 使用方式

从 v6.5.0 版本开始，TiDB 默认启用元数据锁。当你将现有集群从 v6.4.0 或更早版本升级到 v6.5.0 或更高版本时，TiDB 会自动启用元数据锁。若要禁用元数据锁，可以将系统变量 [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) 设置为 `OFF`。

## 影响

- 对于 DML，元数据锁不会阻塞其执行，也不会引发死锁。
- 当启用元数据锁时，事务中某个元数据对象的信息在首次访问时被确定，此后不会发生变化。
- 对于 DDL，在变更元数据状态时，可能会被旧事务阻塞。以下为示例：

    | Session 1 | Session 2 |
    |:---------------------------|:----------|
    | `CREATE TABLE t (a INT);`  |           |
    | `INSERT INTO t VALUES(1);` |           |
    | `BEGIN;`                   |           |
    |                            | `ALTER TABLE t ADD COLUMN b INT;` |
    | `SELECT * FROM t;`<br/>(使用当前元数据版本的表 `t`，返回 `(a=1, b=NULL)` 并锁定表 `t`) |           |
    |                            | `ALTER TABLE t ADD COLUMN c INT;`（被 Session 1 阻塞） |

在可重复读隔离级别下，从事务开始到确定表的元数据的时间点，如果执行了需要数据变更的 DDL，例如添加索引或更改列类型，DDL 会返回如下错误：

    | Session 1                  | Session 2                                 |
    |:---------------------------|:------------------------------------------|
    | `CREATE TABLE t (a INT);`  |                                           |
    | `INSERT INTO t VALUES(1);` |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t ADD INDEX idx(a);`         |
    | `SELECT * FROM t;`（索引 `idx` 不可用） |                                |
    | `COMMIT;`                  |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
    | `SELECT * FROM t;`（返回 `ERROR 8028 (HY000): public column a has changed`） | |

## 可观察性

TiDB v6.3.0 引入了 `mysql.tidb_mdl_view` 视图，帮助你获取当前阻塞的 DDL 信息。

> **Note:**
>
> 要查询 `mysql.tidb_mdl_view` 视图，需具备 [`PROCESS` privilege](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)。

以下以为表 `t` 添加索引的场景为例，假设存在 DDL 语句 `ALTER TABLE t ADD INDEX idx(a)`：

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

从上述输出可以看到，`SESSION ID` 为 `1547698182` 的事务阻塞了 `ADD COLUMN` 的 DDL。`SQL_DIGEST` 展示了该事务执行的 SQL 语句，为 ``["begin","select * from `t`"]``。若要让阻塞的 DDL 继续执行，可以使用以下全局 `KILL` 语句杀死该事务：

```sql
mysql> KILL 1547698182;
Query OK, 0 rows affected (0.00 sec)
```

杀死事务后，再次查询 `mysql.tidb_mdl_view` 视图，此时前述事务不再显示，表示该 DDL 不再被阻塞。

```sql
TABLE mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

## 原理

### 问题描述

TiDB 中的 DDL 操作采用在线 DDL 模式。当执行某个 DDL 语句时，待修改对象的元数据版本可能会经历多次微版本变更。在线异步元数据变更算法只保证相邻两个微版本之间兼容，即两个版本之间的操作不会破坏 DDL 改变对象的数据一致性。

在给表添加索引时，DDL 语句的状态变化如下：None -> Delete Only -> Write Only -> Write Reorg -> Public。

以下事务提交过程违反了上述约束：

| 事务  | 使用的版本  | 集群中的最新版本 | 版本差异 |
|:-----|:-----------|:-----------|:----|
| txn1 | None       | None       | 0   |
| txn2 | DeleteOnly | DeleteOnly | 0   |
| txn3 | WriteOnly  | WriteOnly  | 0   |
| txn4 | None       | WriteOnly  | 2   |
| txn5 | WriteReorg | WriteReorg | 0   |
| txn6 | WriteOnly  | WriteReorg | 1   |
| txn7 | Public     | Public     | 0   |

在上述表中，`txn4` 提交时使用的元数据版本与集群中的最新版本相差两版，可能导致数据不一致。

### 实现细节

元数据锁可以确保集群中所有事务使用的元数据版本最多相差一版。为实现此目标，TiDB 实现了以下两条规则：

- 执行 DML 时，TiDB 会在事务上下文中记录 DML 访问的元数据对象（如表、视图及对应的元数据版本），事务提交时清理这些记录。
- 当 DDL 语句变更状态时，最新的元数据版本会被推送到所有 TiDB 节点。如果所有相关事务在某个 TiDB 节点上使用的元数据版本与当前最新版本的差异小于两版，则该 TiDB 节点视为已获取该元数据对象的元数据锁。下一次状态变更只有在集群中所有节点都已获取到该元数据对象的元数据锁后才能执行。
