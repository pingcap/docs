---
title: DROP DATABASE
summary: 删除一个数据库。
---

# DROP DATABASE

删除一个数据库。

另请参阅：[UNDROP DATABASE](/tidb-cloud-lake/sql/undrop-database.md)

## 语法 {#syntax}

```sql
DROP { DATABASE | SCHEMA } [ IF EXISTS ] <database_name>
```

`DROP SCHEMA` 是 `DROP DATABASE` 的同义词。

## 示例 {#examples}

以下示例先创建一个名为 "orders_2024" 的数据库，然后将其删除：

```sql
root@localhost:8000/default> CREATE DATABASE orders_2024;

CREATE DATABASE orders_2024

0 row written in 0.014 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)

root@localhost:8000/default> DROP DATABASE orders_2024;

DROP DATABASE orders_2024

0 row written in 0.012 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)
```