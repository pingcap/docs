---
title: PROCESSLIST
summary: Learn the `PROCESSLIST` information_schema table.
---

# PROCESSLIST

`PROCESSLIST`, just like [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md), is used to view the requests that are being handled.

The `PROCESSLIST` table has additional columns not present in `SHOW PROCESSLIST`:

<CustomContent platform="tidb">

* A `DIGEST` column to show the digest of the SQL statement.
* A `MEM` column to show the memory used by the request that is being processed, in bytes.
* A `DISK` column to show the disk usage in bytes.
* A `TxnStart` column to show the start time of the transaction.
* A `RESOURCE_GROUP` column to show the resource group name.
* A `SESSION_ALIAS` column to show the alias of the current session.
* A `ROWS_AFFECTED` column to show the number of rows currently affected by the statement.
* A `TIDB_CPU` column to show the amount of time in nanoseconds that the statement consumes the TiDB server CPU. This column shows meaningful value only when the [Top SQL](/dashboard/top-sql.md) feature is enabled. Otherwise the value will be `0`.
* A `TIKV_CPU` column to show the amount of time in nanoseconds that the statement consumes the TiKV server CPU.

</CustomContent>

<CustomContent platform="tidb-cloud">

* A `DIGEST` column to show the digest of the SQL statement.
* A `MEM` column to show the memory used by the request that is being processed, in bytes.
* A `DISK` column to show the disk usage in bytes.
* A `TxnStart` column to show the start time of the transaction.
* A `RESOURCE_GROUP` column to show the resource group name.
* A `SESSION_ALIAS` column to show the alias of the current session.
* A `ROWS_AFFECTED` column to show the number of rows currently affected by the statement.
* A `TIDB_CPU` column to show the amount of time in nanoseconds that the statement consumes the TiDB server CPU. This column shows meaningful value only when the [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) feature is enabled. Otherwise the value will be `0`.
* A `TIKV_CPU` column to show the amount of time in nanoseconds that the statement consumes the TiKV server CPU.

</CustomContent>

```sql
USE information_schema;
DESC processlist;
```

```sql
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| ID             | bigint(21) unsigned | NO   |      | 0       |       |
| USER           | varchar(16)         | NO   |      |         |       |
| HOST           | varchar(64)         | NO   |      |         |       |
| DB             | varchar(64)         | YES  |      | NULL    |       |
| COMMAND        | varchar(16)         | NO   |      |         |       |
| TIME           | int(7)              | NO   |      | 0       |       |
| STATE          | varchar(7)          | YES  |      | NULL    |       |
| INFO           | longtext            | YES  |      | NULL    |       |
| DIGEST         | varchar(64)         | YES  |      |         |       |
| MEM            | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK           | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart       | varchar(64)         | NO   |      |         |       |
| RESOURCE_GROUP | varchar(32)         | NO   |      |         |       |
| SESSION_ALIAS  | varchar(64)         | NO   |      |         |       |
| ROWS_AFFECTED  | bigint(21) unsigned | YES  |      | NULL    |       |
| TIDB_CPU       | bigint(21)          | NO   |      | 0       |       |
| TIKV_CPU       | bigint(21)          | NO   |      | 0       |       |
+----------------+---------------------+------+------+---------+-------+
```

```sql
SELECT * FROM information_schema.processlist\G
```

```sql
*************************** 1. row ***************************
            ID: 1268776964
          USER: root
          HOST: 127.0.0.1:59922
            DB: NULL
       COMMAND: Query
          TIME: 0
         STATE: autocommit
          INFO: SELECT * FROM information_schema.processlist
        DIGEST: 4b5e7cdd5d3ed84d6c1a6d56403a3d512554b534313caf296268abdec1c9ea99
           MEM: 0
          DISK: 0
      TxnStart:
RESOURCE_GROUP: default
 SESSION_ALIAS:
 ROWS_AFFECTED: 0
      TIDB_CPU: 0
      TIKV_CPU: 0
```

Fields in the `PROCESSLIST` table are described as follows:

<CustomContent platform="tidb">

* `ID`: The ID of the user connection.
* `USER`: The name of the user who is executing `PROCESS`.
* `HOST`: The address that the user is connecting to.
* `DB`: The name of the currently connected default database.
* `COMMAND`: The command type that `PROCESS` is executing.
* `TIME`: The current execution duration of `PROCESS`, in seconds.
* `STATE`: The current connection state.
* `INFO`: The requested statement that is being processed.
* `DIGEST`: The digest of the SQL statement.
* `MEM`: The memory used by the request that is being processed, in bytes.
* `DISK`: The disk usage in bytes.
* `TxnStart`: The start time of the transaction.
* `RESOURCE_GROUP`: The resource group name.
* `SESSION_ALIAS`: The alias of the current session.
* `ROWS_AFFECTED`: The number of rows currently affected by the statement.
* `TIDB_CPU`: The amount of time in nanoseconds that the statement consumes the TiDB server CPU. This column shows meaningful value only when the [Top SQL](/dashboard/top-sql.md) feature is enabled. Otherwise the value will be `0`.
* `TIKV_CPU`: The amount of time in nanoseconds that the statement consumes the TiKV server CPU.

</CustomContent>

<CustomContent platform="tidb-cloud">

* `ID`: The ID of the user connection.
* `USER`: The name of the user who is executing `PROCESS`.
* `HOST`: The address that the user is connecting to.
* `DB`: The name of the currently connected default database.
* `COMMAND`: The command type that `PROCESS` is executing.
* `TIME`: The current execution duration of `PROCESS`, in seconds.
* `STATE`: The current connection state.
* `INFO`: The requested statement that is being processed.
* `DIGEST`: The digest of the SQL statement.
* `MEM`: The memory used by the request that is being processed, in bytes.
* `DISK`: The disk usage in bytes.
* `TxnStart`: The start time of the transaction.
* `RESOURCE_GROUP`: The resource group name.
* `SESSION_ALIAS`: The alias of the current session.
* `ROWS_AFFECTED`: The number of rows currently affected by the statement.
* `TIDB_CPU`: The amount of time in nanoseconds that the statement consumes the TiDB server CPU. This column shows meaningful value only when the [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) feature is enabled. Otherwise the value will be `0`.
* `TIKV_CPU`: The amount of time in nanoseconds that the statement consumes the TiKV server CPU.

</CustomContent>

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` is the cluster system table corresponding to `PROCESSLIST`. It is used to query the `PROCESSLIST` information of all TiDB nodes in the cluster. The table schema of `CLUSTER_PROCESSLIST` has one more column than `PROCESSLIST`, the `INSTANCE` column, which stores the address of the TiDB node this row of data is from.

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
| INSTANCE        | ID         | USER | HOST            | DB   | COMMAND | TIME | STATE      | INFO                                                 | DIGEST                                                           | MEM  | DISK | TxnStart                               | RESOURCE_GROUP | SESSION_ALIAS | ROWS_AFFECTED | TIDB_CPU | TIKV_CPU |
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
| 127.0.0.1:10080 | 1268776964 | root | 127.0.0.1:59922 | NULL | Query   |    0 | autocommit | SELECT * FROM information_schema.cluster_processlist | b1e38e59fbbc3e2b35546db5c8053040db989a497ac6cd71ff8dd4394395701a |    0 |    0 | 07-29 12:39:24.282(451471727468740609) | default        |               |             0 |        0 |        0 |
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
```
