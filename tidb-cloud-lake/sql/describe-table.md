---
title: DESCRIBE TABLE
summary: 显示给定表中列的信息。等同于 SHOW FIELDS。
---

# DESCRIBE TABLE

显示给定表中列的信息。等同于 [SHOW FIELDS](/tidb-cloud-lake/sql/show-fields.md)。

> **Tip:**
>
> [SHOW COLUMNS](/tidb-cloud-lake/sql/show-columns.md) 提供类似功能，但会返回关于表列的更多信息。

## 语法 {#syntax}

```sql
DESC|DESCRIBE [TABLE] [ <database_name>. ]<table_name>
```

## 示例 {#examples}

```sql
CREATE TABLE books
  (
     price  FLOAT Default 0.00,
     pub_time DATETIME Default '1900-01-01',
     author VARCHAR
  );

DESC books;

Field   |Type     |Null|Default                     |Extra|
--------+---------+----+----------------------------+-----+
price   |FLOAT    |YES |0                           |     |
pub_time|TIMESTAMP|YES |'1900-01-01 00:00:00.000000'|     |
author  |VARCHAR  |YES |NULL                        |     |
```