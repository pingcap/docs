---
title: SHOW FIELDS
summary: 指定したテーブルのカラムに関する情報を表示します。DESCRIBE TABLE と同等です。
---

# SHOW FIELDS

指定したテーブルのカラムに関する情報を表示します。[DESCRIBE TABLE](/tidb-cloud-lake/sql/describe-table.md) と同等です。

> **Tip:**
>
> [SHOW COLUMNS](/tidb-cloud-lake/sql/show-columns.md) は、テーブルのカラムに関して同様ですが、より多くの情報を提供します。

## 構文 {#syntax}

```sql
SHOW FIELDS FROM [ <database_name>. ]<table_name>
```

## 例 {#examples}

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