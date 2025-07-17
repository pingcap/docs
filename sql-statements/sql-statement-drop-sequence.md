---
title: DROP SEQUENCE
summary: 关于在 TiDB 数据库中使用 DROP SEQUENCE 的概述。
---

# DROP SEQUENCE

`DROP SEQUENCE` 语句用于删除 TiDB 中的序列对象。

## 概述

```ebnf+diagram
DropSequenceStmt ::=
    'DROP' 'SEQUENCE' IfExists TableNameList

IfExists ::= ( 'IF' 'EXISTS' )?

TableNameList ::=
    TableName ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## 示例


```sql
DROP SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.10 sec)
```


```sql
DROP SEQUENCE seq, seq2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

## MySQL 兼容性

该语句是 TiDB 的扩展功能。其实现借鉴了 MariaDB 中的序列机制。

## 相关链接

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [ALTER SEQUENCE](/sql-statements/sql-statement-alter-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)