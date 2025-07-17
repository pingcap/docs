---
title: SHOW CREATE SEQUENCE
summary: 关于 TiDB 数据库中使用 SHOW CREATE SEQUENCE 的概述。
---

# SHOW CREATE SEQUENCE

`SHOW CREATE SEQUENCE` 显示序列的详细信息，类似于 `SHOW CREATE TABLE`。

## 概述

```ebnf+diagram
ShowCreateSequenceStmt ::=
    "SHOW" "CREATE" "SEQUENCE" ( SchemaName "." )? TableName
```

## 示例

```sql
CREATE SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.03 sec)
```

```sql
SHOW CREATE SEQUENCE seq;
```

```
+-------+----------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------+
| seq   | CREATE SEQUENCE `seq` start with 1 minvalue 1 maxvalue 9223372036854775806 increment by 1 cache 1000 nocycle ENGINE=InnoDB |
+-------+----------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 的扩展功能。其实现借鉴了 MariaDB 中的序列机制。

## 相关链接

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [ALTER SEQUENCE](/sql-statements/sql-statement-alter-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)