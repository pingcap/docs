---
title: SHOW FIELDS
summary: 显示给定表中各列的信息。等同于 DESCRIBE TABLE。
---

# SHOW FIELDS

显示给定表中各列的信息。等同于 [DESCRIBE TABLE](/tidb-cloud-lake/sql/describe-table.md)。

> **Tip:**
>
> [SHOW COLUMNS](/tidb-cloud-lake/sql/show-columns.md) 提供与之类似但更详细的表列信息。

## 语法 {#syntax}

```sql
SHOW FIELDS FROM [ <database_name>. ]<table_name>
```

## 示例 {#examples}

```sql
CREATE TABLE books
  (
     price  FLOAT Default 0.00,
     pub_time DATETIME Default '1900-01-01',
     author VARCHAR
  );

SHOW FIELDS FROM books;

Field   |Type     |Null|Default                     |Extra|
--------+---------+----+----------------------------+-----+
price   |FLOAT    |YES |0                           |     |
pub_time|TIMESTAMP|YES |'1900-01-01 00:00:00.000000'|     |
author  |VARCHAR  |YES |NULL                        |     |
```