---
title: SHOW COLUMNS
summary: 显示给定表中列的信息。
---

# SHOW COLUMNS

显示给定表中列的信息。

> **Tip:**
>
> [DESCRIBE TABLE](/tidb-cloud-lake/sql/describe-table.md) 也可以提供表中列的类似信息，但信息较少。

## 语法 {#syntax}

```sql
SHOW  [ FULL ] COLUMNS
    {FROM | IN} tbl_name
    [ {FROM | IN} db_name ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

当包含可选关键字 FULL 时，{{{ .lake }}} 会在结果中为表中的每一列额外返回排序规则、权限和注释信息。

## 示例 {#examples}

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