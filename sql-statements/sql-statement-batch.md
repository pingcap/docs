---
title: BATCH
summary: TiDB 数据库中 BATCH 的用法概述。
---

# BATCH

`BATCH` 语法会将一个 DML 语句在 TiDB 中切分为多个语句进行执行。这意味着 **不保证** 事务的原子性和隔离性。因此，它是一个“非事务型”语句。

目前，`BATCH` 支持 `INSERT`、`REPLACE`、`UPDATE` 和 `DELETE`。

基于某一列，`BATCH` 语法将 DML 语句切分为多个作用域范围进行执行。在每个范围内，会执行一条 SQL 语句。

关于用法和限制的详细信息，参见 [非事务型 DML 语句](/non-transactional-dml.md)。

当你在 `BATCH` 语句中使用多表 join 时，需要指定列的完整路径以避免歧义：

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

上述语句指定了切分的列为 `test.t2.id`，这样不会产生歧义。如果你像下面这样仅使用 `id`，则会报错：

```sql
BATCH ON id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;

Non-transactional DML, shard column must be fully specified
```

> **注意：**
>
> `BATCH` 语句在内部会被重写并切分为多个 DML 语句进行执行。在当前版本中，表别名可能不会被保留，这可能导致如 `Unknown column '<alias>.<column>' in 'where clause'` 的报错。为避免此问题，请不要使用表别名。在执行前，可以使用 `DRY RUN QUERY` 或 `DRY RUN` 预览切分后的语句。更多信息参见 [非事务型 DML 语句](/non-transactional-dml.md)。

## 语法

```ebnf+diagram
NonTransactionalDMLStmt ::=
    'BATCH' ( 'ON' ColumnName )? 'LIMIT' NUM DryRunOptions? ShardableStmt

DryRunOptions ::=
    'DRY' 'RUN' 'QUERY'?

ShardableStmt ::=
    DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
```

## MySQL 兼容性

`BATCH` 语法是 TiDB 特有的，并不兼容 MySQL。

## 另请参阅

* [非事务型 DML 语句](/non-transactional-dml.md)