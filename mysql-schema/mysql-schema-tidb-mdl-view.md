---
title: mysql.tidb_mdl_view
summary: Learn about the `tidb_mdl_view` table in the `mysql` schema.
---

# `mysql.tidb_mdl_view`

This table shows the information about the [metadata lock](/metadata-lock.md) views.

```sql
DESC mysql.tidb_mdl_view;
```

The output is as follows:

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

## Fields

* `job_id`: The identifier of the job.
* `db_name`: The database name.
* `table_name`: The table name.
* `query`: The query.
* `session_id`: The identifier of the session.
* `start_time`: The start time. This column was called `TxnStart` in earlier versions.
* `SQL_DIGESTS`: The digests of the SQL statements.