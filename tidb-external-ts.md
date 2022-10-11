---
title: Read Historical Data Using the `tidb_external_ts` Variable
summary: Learn how to read historical data using the `tidb_external_ts` variable.
---

# Read Historical Data Using the `tidb_external_ts` Variable

This document describes how to perform the [Stale Read](/stale-read.md) feature using the [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) system variable to read historical data in TiDB, including specific usage examples.

> **Warning:**
>
> Currently, you cannot use Stale Read together with TiFlash. If you enables `tidb_enable_external_ts_read` and TiDB might read data from TiFlash replicas, you might encounter an error with a message like `ERROR 1105 (HY000): stale requests require tikv backend`.
>
> To fix the problem, disable TiFlash replicas for your Stale Read query. To do that, perform one of the following operations:
>
> - Use the `set session tidb_isolation_read_engines='tidb,tikv'` variable.
> - Use the [hint](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-) to enforce TiDB to read data from TiKV.

## Scenarios

Read with an absolute timestamp is especially useful for data replication software (for example TiCDC). After the data replication software ensures that all data before a timestamp have been synchronized to the downstream, it can set the [`tidb_external_ts`](#tidb_external_ts-new-in-v640) for the downstream TiDB, so that the read queries of the downstream TiDB can read consistent data.

## Usage

The [`tidb_external_ts`](#tidb_external_ts-new-in-v640) variable is used to specify the timestamp of the historical data to be read.

The `tidb_enable_external_ts_read` controls whether TiDB will read with the [`tidb_external_ts`](#tidb_external_ts-new-in-v640) variable. The default value is `OFF`, which means that the [`tidb_external_ts`](#tidb_external_ts-new-in-v640) variable is ignored. If `tidb_enable_external_ts_read` is set `ON` globally, all the queries will read historical data. If `tidb_enable_external_ts_read` is set `ON` for a session, only the queries in the session will read historical data.

When `tidb_enable_external_ts_read` is enabled, TiDB becomes read-only. All the write queries will fail with an error like `ERROR 1836 (HY000): Running in read-only mode`.

Here is an example:

```sql
CREATE TABLE t (c INT);
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
INSERT INTO t VALUES (1), (2), (3);
```

```
Query OK, 3 rows affected (0.00 sec)
```

View the data in the table:

```sql
SELECT * FROM t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

Set the [`tidb_external_ts`](#tidb_external_ts-new-in-v640) to be `@@tidb_current_ts`:

```sql
START TRANSACTION;
SET GLOBAL tidb_external_ts=@@tidb_current_ts;
COMMIT;
```

Insert a new row:

```sql
INSERT INTO t VALUES (4);
```

```
Query OK, 1 row affected (0.001 sec)
```

Confirm that the new row is inserted:

```sql
SELECT * FROM t;
```

```
+------+
| id   |
+------+
|    1 |
|    2 |
|    3 |
|    4 |
+------+
4 rows in set (0.00 sec)
```

However, as [`tidb_external_ts`](#tidb_external_ts-new-in-v640) is set to the timestamp before inserting the new row. After turning on the `tidb_enable_external_ts_read`, the new row will not be read:

```sql
SET tidb_enable_external_ts_read=ON;
SELECT * FROM t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```