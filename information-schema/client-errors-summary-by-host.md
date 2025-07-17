---
title: CLIENT_ERRORS_SUMMARY_BY_HOST
summary: Learn about the `CLIENT_ERRORS_SUMMARY_BY_HOST` INFORMATION_SCHEMA table.
---

# CLIENT_ERRORS_SUMMARY_BY_HOST

The table `CLIENT_ERRORS_SUMMARY_BY_HOST` provides a summary of SQL errors and warnings that have been returned to clients that connect to a TiDB server. These include:

* Malformed SQL statements.
* Division by zero errors.
* The attempt to insert out-of-range or duplicate key values.
* Permission errors.
* A table that does not exist.

These errors are returned to the client via the MySQL server protocol, where applications are expected to take appropriate action. The `INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST` table provides a useful method to inspect errors in the scenario where applications are not correctly handling (or logging) errors returned by the TiDB server.

Because `CLIENT_ERRORS_SUMMARY_BY_HOST` summarizes the errors on a per-remote-host basis, it can be useful to diagnose scenarios where one application server is generating more errors than other servers. Possible scenarios include:

* An outdated MySQL client library.
* An outdated application (possibly this server was missed when rolling out a new deployment).
* Incorrect usage of the "host" portion of user permissions.
* Unreliable network connectivity generating more timeouts or disconnected connections.

The summarized counts can be reset using the statement `FLUSH CLIENT_ERRORS_SUMMARY`. The summary is local to each TiDB server and is only retained in memory. Summaries will be lost if the TiDB server restarts.

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_HOST;
```

The output is as follows:

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| HOST          | varchar(255)  | NO   |      | NULL    |       |
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

Field description:

* `HOST`: The remote host of the client.
* `ERROR_NUMBER`: The MySQL-compatible error number that was returned.
* `ERROR_MESSAGE`: The error message which matches the error number (in prepared statement form).
* `ERROR_COUNT`: The number of times this error was returned to the client host.
* `WARNING_COUNT`: The number of times this warning was returned to the client host.
* `FIRST_SEEN`: The first time this error (or warning) was seen from the client host.
* `LAST_SEEN`: The most recent time this error (or warning) was seen from the client host.

The following example shows a warning being generated when the client connects to a local TiDB server. The summary is reset after executing `FLUSH CLIENT_ERRORS_SUMMARY`:

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
```

The output is as follows:

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| HOST      | ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| 127.0.0.1 |         1365 | Division by 0 |           0 |             1 | 2021-03-18 12:51:54 | 2021-03-18 12:51:54 |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```
