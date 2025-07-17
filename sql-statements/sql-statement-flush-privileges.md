---
title: FLUSH PRIVILEGES | TiDB SQL Statement Reference
summary: 关于在 TiDB 数据库中使用 FLUSH PRIVILEGES 的概述。
---

# FLUSH PRIVILEGES

语句 `FLUSH PRIVILEGES` 指示 TiDB 重新加载权限表中的权限到内存副本中。你必须在手动编辑诸如 `mysql.user` 之类的表后执行此语句。然而，在使用 `GRANT` 或 `REVOKE` 等权限语句后，执行此语句不是必需的。要执行此语句，需具备 `RELOAD` 权限。

## 语法简介

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
|   LogTypeOpt 'LOGS'
|   TableOrTables TableNameListOpt WithReadLockOpt
```

## 示例

```sql
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

TiDB 中的 `FLUSH PRIVILEGES` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

* [Privilege Management](/privilege-management.md)

</CustomContent>