---
title: BATCH
summary: 关于在 TiDB 数据库中使用 BATCH 的概述。
---

# BATCH

`BATCH` 语法在 TiDB 中将一个 DML 语句拆分成多个语句以供执行。这意味着 **没有保证**事务的原子性和隔离性。因此，它是一个“非事务性”语句。

目前，`INSERT`、`REPLACE`、`UPDATE` 和 `DELETE` 支持在 `BATCH` 中使用。

基于某一列，`BATCH` 语法将一个 DML 语句划分为多个范围进行执行。在每个范围内，执行单个 SQL 语句。

有关用法和限制的详细信息，请参见 [Non-transactional DML statements](/non-transactional-dml.md)。

当你在 `BATCH` 语句中使用多表连接时，需要指定列的完整路径以避免歧义：

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

上述语句将要拆分的列指定为 `test.t2.id`，这是明确的。如果你使用如下的 `id`，则会报错：

```sql
BATCH ON id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;

Non-transactional DML, shard column must be fully specified
```

## 概要

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

`BATCH` 语法是 TiDB 特有的，不兼容 MySQL。

## 另请参见

* [Non-transactional DML statements](/non-transactional-dml.md)