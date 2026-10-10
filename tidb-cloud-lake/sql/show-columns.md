---
title: SHOW COLUMNS
summary: 指定したテーブルのカラムに関する情報を表示します。
---

# SHOW COLUMNS

指定したテーブルのカラムに関する情報を表示します。

> **Tip:**
>
> [DESCRIBE TABLE](/tidb-cloud-lake/sql/describe-table.md) でもテーブルのカラムに関する類似の情報を確認できますが、表示される情報はこれより少なくなります。

## 構文 {#syntax}

```sql
SHOW  [ FULL ] COLUMNS
    {FROM | IN} tbl_name
    [ {FROM | IN} db_name ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

省略可能なキーワード `FULL` を含めると、{{{ .lake }}} は結果にテーブル内の各カラムの照合順序、権限、およびコメント情報を追加します。

## 例 {#examples}

```sql
CREATE TABLE books
  (
     price  FLOAT Default 0.00,
     pub_time DATETIME Default '1900-01-01',
     author VARCHAR
  );

SHOW COLUMNS FROM books FROM default;

Field   |Type     |Null|Default     |Extra|Key|
--------+---------+----+------------+-----+---+
author  |VARCHAR  |NO  |            |     |   |
price   |FLOAT    |NO  |0.00        |     |   |
pub_time|TIMESTAMP|NO  |'1900-01-01'|     |   |

SHOW FULL COLUMNS FROM books;

Field   |Type     |Null|Default     |Extra|Key|Collation|Privileges|Comment|
--------+---------+----+------------+-----+---+---------+----------+-------+
author  |VARCHAR  |NO  |            |     |   |         |          |       |
price   |FLOAT    |NO  |0.00        |     |   |         |          |       |
pub_time|TIMESTAMP|NO  |'1900-01-01'|     |   |         |          |       |

SHOW FULL COLUMNS FROM books LIKE 'a%'

Field |Type   |Null|Default|Extra|Key|Collation|Privileges|Comment|
------+-------+----+-------+-----+---+---------+----------+-------+
author|VARCHAR|NO  |       |     |   |         |          |       |
```