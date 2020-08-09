---
title: ADMIN SHOW DDL [JOBS|QUERIES] | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-admin/','/docs/dev/reference/sql/statements/admin/']
---

# ADMIN SHOW DDL [JOBS,QUERIES]

The `ADMIN SHOW DDL [JOBS,QUERIES]` statement shows information about running and recently completed DDL jobs.

## Synopsis

**AdminStmt:**

![AdminStmt](/media/sqlgram/AdminStmt.png)

**NumList:**

![NumList](/media/sqlgram/NumList.png)

**WhereClauseOptional:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

## Examples

### `ADMIN SHOW DDL`

Provide an overview of DDL in the cluster, including any running jobs:

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL;
```

```
mysql> ADMIN SHOW DDL;
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
1 row in set (0.00 sec)
```

### `ADMIN SHOW DDL JOBS`

To view all the results in the current DDL job queue (including tasks that are running and waiting to be run) and the last ten results in the completed DDL job queue, use `ADMIN SHOW DDL JOBS`:

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOBS;
```

```
mysql> ADMIN SHOW DDL JOBS;
+--------+---------+-------------------------+--------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+--------+
| JOB_ID | DB_NAME | TABLE_NAME              | JOB_TYPE                 | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME          | END_TIME            | STATE  |
+--------+---------+-------------------------+--------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+--------+
|     51 | test    | t1                      | create table             | public       |         1 |       50 |         0 | 2020-08-09 15:02:43 | 2020-08-09 15:02:43 | synced |
|     49 | ontime  | ontime                  | rebase auto_increment ID | public       |        45 |       47 |         0 | 2020-08-09 13:41:53 | 2020-08-09 13:41:53 | synced |
|     48 | ontime  | ontime                  | create table             | public       |        45 |       47 |         0 | 2020-08-09 13:28:23 | 2020-08-09 13:28:23 | synced |
|     46 | ontime  |                         | create schema            | public       |        45 |        0 |         0 | 2020-08-09 13:28:22 | 2020-08-09 13:28:22 | synced |
|     44 | mysql   | opt_rule_blacklist      | create table             | public       |         3 |       43 |         0 | 2020-08-09 10:17:18 | 2020-08-09 10:17:18 | synced |
|     42 | mysql   | expr_pushdown_blacklist | create table             | public       |         3 |       41 |         0 | 2020-08-09 10:17:17 | 2020-08-09 10:17:18 | synced |
|     40 | mysql   | stats_top_n             | create table             | public       |         3 |       39 |         0 | 2020-08-09 10:17:17 | 2020-08-09 10:17:17 | synced |
|     38 | mysql   | bind_info               | create table             | public       |         3 |       37 |         0 | 2020-08-09 10:17:17 | 2020-08-09 10:17:17 | synced |
|     36 | mysql   | default_roles           | create table             | public       |         3 |       35 |         0 | 2020-08-09 10:17:17 | 2020-08-09 10:17:17 | synced |
|     34 | mysql   | role_edges              | create table             | public       |         3 |       33 |         0 | 2020-08-09 10:17:17 | 2020-08-09 10:17:17 | synced |
+--------+---------+-------------------------+--------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+--------+
10 rows in set (0.01 sec)
```

You may limit the number of rows shown by specifying a number and where condition. i.e.

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

* `NUM`: to view the last `NUM` results in the completed DDL job queue. If not specified, `NUM` is by default 10.
* `WHERE`: to add filter conditions.

### `ADMIN SHOW DDL JOB QUERIES`

To view the original SQL statements of the DDL job corresponding to `job_id`, use `ADMIN SHOW DDL JOB QUERIES`:

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOBS;
ADMIN SHOW DDL JOB QUERIES 51;
```

```
mysql> ADMIN SHOW DDL JOB QUERIES 51;
+--------------------------------------------------------------+
| QUERY                                                        |
+--------------------------------------------------------------+
| CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------------------------------------------------------------+
1 row in set (0.02 sec)
```

You can only searches the running DDL job corresponding to `job_id` and the last ten results in the DDL history job queue.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [ADMIN CANCEL DDL](/sql-statements/sql-statement-admin-cancel-ddl.md)