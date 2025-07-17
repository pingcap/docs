---
title: FLUSH TABLES | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 FLUSH TABLES 的概述。
---

# FLUSH TABLES

此语句是为了与 MySQL 兼容而存在。在 TiDB 中没有实际的使用场景。

## 概要

```ebnf+diagram
FlushStmt ::=
    'FLUSH' NoWriteToBinLogAliasOpt FlushOption

NoWriteToBinLogAliasOpt ::=
    ( 'NO_WRITE_TO_BINLOG' | 'LOCAL' )?

FlushOption ::=
    'PRIVILEGES'
|   'STATUS'
|    'TIDB' 'PLUGINS' PluginNameList
|    'HOSTS'
|    LogTypeOpt 'LOGS'
|    TableOrTables TableNameListOpt WithReadLockOpt

LogTypeOpt ::=
    ( 'BINARY' | 'ENGINE' | 'ERROR' | 'GENERAL' | 'SLOW' )?

TableOrTables ::=
    'TABLE'
|   'TABLES'

TableNameListOpt ::=
    TableNameList?

WithReadLockOpt ::=
    ( 'WITH' 'READ' 'LOCK' )?
```

## 示例

```sql
mysql> FLUSH TABLES;
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH TABLES WITH READ LOCK;
ERROR 1105 (HY000): FLUSH TABLES WITH READ LOCK is not supported.  Please use @@tidb_snapshot
```

## MySQL 兼容性

* TiDB 没有像 MySQL 那样的表缓存概念。因此，`FLUSH TABLES` 在 TiDB 中会被解析但忽略，以保持兼容性。
* 语句 `FLUSH TABLES WITH READ LOCK` 会产生错误，因为 TiDB 目前不支持锁定表。建议使用 [Historical reads](/read-historical-data.md) 来实现类似功能。