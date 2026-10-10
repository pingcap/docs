---
title: DESCRIBE TABLE
summary: 指定したテーブルのカラムに関する情報を表示します。SHOW FIELDS と同等です。
---

# DESCRIBE TABLE

指定したテーブルのカラムに関する情報を表示します。[SHOW FIELDS](/tidb-cloud-lake/sql/show-fields.md) と同等です。

> **Tip:**
>
> [SHOW COLUMNS](/tidb-cloud-lake/sql/show-columns.md) は、テーブルのカラムについて同様の情報を提供しますが、より多くの情報を表示します。

## 構文 {#syntax}

```sql
DESC|DESCRIBE [TABLE] [ <database_name>. ]<table_name>
```

## 例 {#examples}

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