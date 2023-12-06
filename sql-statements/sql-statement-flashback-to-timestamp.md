---
title: FLASHBACK CLUSTER
summary: Learn the usage of FLASHBACK CLUSTER in TiDB databases.
aliases: ['/tidb/v6.5/sql-statement-flashback-to-timestamp']
---

# FLASHBACK CLUSTER

TiDB v6.4.0 introduces the `FLASHBACK CLUSTER TO TIMESTAMP` syntax. You can use it to restore a cluster to a specific point in time. When specifying the timestamp, you can either set a datetime value or use a time function. The format of datetime is like "2016-10-08 16:45:26.999", with millisecond as the minimum time unit, but in most cases, specifying the timestamp with second as the time unit is sufficient, such as "2016-10-08 16:45:26".

Starting from v6.5.6, TiDB introduces the `FLASHBACK CLUSTER TO TSO` syntax. This syntax enables you to use [TSO](/tso.md) to specify a more precise recovery point in time, thereby enhancing flexibility in data recovery.

<CustomContent platform="tidb-cloud">

> **Warning:**
>
> The `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` syntax is not applicable to [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters. Do not execute this statement on TiDB Serverless clusters to avoid unexpected results.

</CustomContent>

> **Note:**
>
> The working principle of `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` is to write the old data of a specific point in time with the latest timestamp, and will not delete the current data. So before using this feature, you need to ensure that there is enough storage space for the old data and the current data.

## Syntax

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
FLASHBACK CLUSTER TO TSO 445494839813079041;
```

### Synopsis

```ebnf+diagram
FlashbackToTimestampStmt ::=
    'FLASHBACK' 'CLUSTER' 'TO' 'TIMESTAMP' stringLit
|   'FLASHBACK' 'CLUSTER' 'TO' 'TSO' LengthNum
```

## Notes

* The time specified in the `FLASHBACK` statement must be within the Garbage Collection (GC) lifetime. The system variable [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (default: `10m0s`) defines the retention time of earlier versions of rows. The current `safePoint` of where garbage collection has been performed up to can be obtained with the following query:

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

* Only a user with the `SUPER` privilege can execute the `FLASHBACK CLUSTER` SQL statement.
* From the time specified in the `FLASHBACK` statement to the time when the `FLASHBACK` is executed, there cannot be a DDL statement that changes the related table structure. If such a DDL exists, TiDB will reject it.
* Before executing `FLASHBACK CLUSTER`, TiDB disconnects all related connections and prohibits read and write operations on these tables until the `FLASHBACK` statement is completed.
* The `FLASHBACK CLUSTER` statement cannot be canceled after being executed. TiDB will keep retrying until it succeeds.

## Example

The following example shows how to flashback a cluster to a specific timestamp to restore newly inserted data:

```sql
mysql> CREATE TABLE t(a INT);
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT * FROM t;
Empty set (0.01 sec)

mysql> SELECT now();
+---------------------+
| now()               |
+---------------------+
| 2022-09-28 17:24:16 |
+---------------------+
1 row in set (0.02 sec)

mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2022-09-28 17:24:16';
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
Empty set (0.00 sec)
```

The following example shows how to flashback a cluster to a specific TSO to precisely restore mistakenly deleted data:

```sql
mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)


mysql> begin;
Query OK, 0 rows affected (0.00 sec)

mysql> select @@tidb_current_ts;  -- Get the current TSO
+--------------------+
| @@tidb_current_ts  |
+--------------------+
| 446113975683252225 |
+--------------------+
1 row in set (0.00 sec)

mysql> rollback;
Query OK, 0 rows affected (0.00 sec)


mysql> DELETE FROM t;
Query OK, 1 rows affected (0.00 sec)


mysql> FLASHBACK CLUSTER TO TSO 446113975683252225;
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)
```

If there is a DDL statement that changes the table structure from the time specified in the `FLASHBACK` statement to the time when the `FLASHBACK` is executed, the `FLASHBACK` statement fails:

```sql
mysql> SELECT now();
+---------------------+
| now()               |
+---------------------+
| 2022-10-09 16:40:51 |
+---------------------+
1 row in set (0.01 sec)

mysql> CREATE TABLE t(a int);
Query OK, 0 rows affected (0.12 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2022-10-09 16:40:51';
ERROR 1105 (HY000): Detected schema change due to another DDL job during [2022-10-09 16:40:51 +0800 CST, now), can't do flashback
```

<CustomContent platform="tidb">

The `FLASHBACK` execution progress can be viewed via the [Raft admin > Peer in Flashback State](/grafana-tikv-dashboard.md#raft-admin) metrics and the log. The following log is an example:

</CustomContent>
<CustomContent platform="tidb-cloud">

Through the log, you can obtain the execution progress of `FLASHBACK`. The following is an example:

</CustomContent>

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
