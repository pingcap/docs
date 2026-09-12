---
title: SHOW DROP TABLES
summary: 列出当前或指定数据库中已删除的表。
---

# SHOW DROP TABLES

列出当前或指定数据库中已删除的表。

另请参阅：[system.tables_with_history](/tidb-cloud-lake/sql/system-tables-with-history.md)

## 语法 {#syntax}

```sql
SHOW DROP TABLES [ FROM <database_name> ] [ LIKE '<pattern>' | WHERE <expr> ]
```

## 示例 {#examples}

```sql
USE database1;

-- List dropped tables in the current database
SHOW DROP TABLES;

-- List dropped tables in the "default" database
SHOW DROP TABLES FROM default;

Name                |Value                        |
--------------------+-----------------------------+
tables              |t1                           |
table_type          |BASE TABLE                   |
database            |default                      |
catalog             |default                      |
engine              |FUSE                         |
create_time         |2023-06-13 08:43:36.556 +0000|
drop_time           |2023-07-19 04:39:18.536 +0000|
num_rows            |2                            |
data_size           |34                           |
data_compressed_size|330                          |
index_size          |464                          |
```