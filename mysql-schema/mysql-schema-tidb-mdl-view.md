---
title: mysql.tidb_mdl_view
summary: 了解 `tidb_mdl_view` 表在 `mysql` 架构中的信息。
---

# `mysql.tidb_mdl_view`

该表显示关于 [metadata lock](/metadata-lock.md) 视图的信息。

```sql
DESC mysql.tidb_mdl_view;
```

输出结果如下：

```
+-------------+-----------------+------+------+---------+-------+
| Field       | Type            | Null | Key  | Default | Extra |
+-------------+-----------------+------+------+---------+-------+
| job_id      | bigint          | NO   | PRI  | NULL    |       |
| db_name     | longtext        | YES  |      | NULL    |       |
| table_name  | longtext        | YES  |      | NULL    |       |
| query       | longtext        | YES  |      | NULL    |       |
| session_id  | bigint unsigned | YES  |      | NULL    |       |
| start_time  | timestamp(6)    | YES  |      | NULL    |       |
| SQL_DIGESTS | varchar(5)      | YES  |      | NULL    |       |
+-------------+-----------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

## 字段

* `job_id`: 任务的标识符。
* `db_name`: 数据库名称。
* `table_name`: 表名称。
* `query`: 查询语句。
* `session_id`: 会话的标识符。
* `start_time`: 开始时间。在早期版本中，该列被称为 `TxnStart`。
* `SQL_DIGESTS`: SQL 语句的摘要。