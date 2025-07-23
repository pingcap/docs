---
title: ALTER DATABASE | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 ALTER DATABASE 的用法概述。
---

# ALTER DATABASE

`ALTER DATABASE` 用于指定或修改当前数据库的默认字符集和排序规则。`ALTER SCHEMA` 与 `ALTER DATABASE` 具有相同的效果。

## 概要

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' 'DATABASE' DBName? DatabaseOptionList

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## 示例

将测试数据库的字符集修改为 utf8mb4 ：


```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

目前，TiDB 仅支持部分字符集和排序规则。详细信息请参见 [Character Set and Collation Support](/character-set-and-collation.md)。

## MySQL 兼容性

TiDB 中的 `ALTER DATABASE` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，请 [report a bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW DATABASES](/sql-statements/sql-statement-show-databases.md)