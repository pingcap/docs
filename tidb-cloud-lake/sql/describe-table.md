---
title: DESCRIBE TABLE
sidebar_position: 2
---

Shows information about the columns in a given table. Equivalent to [SHOW FIELDS](show-fields.md).

:::tip
[SHOW COLUMNS](show-full-columns.md) provides similar but more information about the columns of a table. 
:::

## Syntax

```sql
DESC|DESCRIBE [TABLE] [ <database_name>. ]<table_name>
```

## Examples

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
