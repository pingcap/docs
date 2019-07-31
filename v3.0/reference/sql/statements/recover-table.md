---
title: RECOVER TABLE
summary: An overview of the usage of RECOVER TABLE for the TiDB database.
category: reference
---

# RECOVER TABLE

`RECOVER TABLE` is used to recover the deleted table and the data on it within the GC life time after the `DROP TABLE` statement is executed.

## Syntax

{{< copyable "sql" >}}

```sql
RECOVER TABLE table_name
```

{{< copyable "sql" >}}

```sql
RECOVER TABLE BY JOB ddl_job_id
```

> **Note:**
>
> + `RECOVER TABLE` can not be used to recover the table beyond the GC life time. In this attempt, an error is returned: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`.
>
> + If the TiDB version is 3.0.0 or later, it is not recommended to use `RECOVER TABLE` when the Binglog is being applied.
>
> + `RECOVER TABLE` is supported in the Binlog version 3.0.1, so you can use `RECOVER TABLE` in the following three situations:
>
>   - Binglog version is 3.0.1 or later.
>   - TiDB v3.0 is used both in the master cluster and the slave cluster.
>   - The GC life time of the slave cluster must be longer than that of the master cluster. However, as latency occurs during the data replication between upstream and downstream, data recovery might fail in the downstream.

### Troubleshoot errors during the TiDB Binlog replication

When you use `RECOVER TABLE` in the upstream TiDB during the TiDB Binlog replication, the TiDB Binlog might be interrupted in the following three situations:

+ The downstream database does not support the `RECOVER TABLE` statement. An example of the error: `check the manual that corresponds to your MySQL server version for the right syntax to use near 'RECOVER TABLE table_name'`.

+ The GC life time is not consistent between the upstream database and the downstream database. An example of the error: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`.

+ Latency occurs during the replication between upstream and downstream. An example of the error: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`.

For the above three situations, you must recover the data replication of TiDB Binlog by the [full import of the deleted table](how-to/migrate/overview.md#full-data-migration-from-mysql).

## Examples

+ Recover the deleted table according to the table name.

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    RECOVER TABLE t;
    ```

    This method searches the DDL operations of the `DROP TABLE` type that appears first in the recent history of `DDL JOB`, and then recovers the table where the table name of the `DROP TABLE` is identical with the table name specified in the `RECOVER TABLE` statement.

+ Recover the deleted table according to the table's `DDL JOB ID` used when the it is being deleted.

    Suppose that you delete the table `t`, create another `t`, and again delete the newly created `t`. Then, if you want to recover the table `t` deleted in the first place, you must use the statements that specify the `DDL JOB ID`.

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    The second statement above is used to search the table's `DDL JOB ID` used when `t` is being deleted. In the following example, the ID is `53`.

    ```
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE   | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    | 53     | test    |            | drop table | none         | 1         | 41       | 0         | 2019-07-10 13:23:18.277 +0800 CST | synced |
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    ```

    {{< copyable "sql" >}}

    ```sql
    RECOVER TABLE BY JOB 53;
    ```

    This method recovers the deleted table via the searched `DDL JOB ID`. If the `DDL JOB` of the specified `DDL JOB ID` is not the `DROP TABLE` type, an error occurs.

## Principle

When deleting a table, TiDB only deletes the table metadata, and writes the table data (row data and index data) to be deleted to the `mysql.gc_delete_range` table. The GC Worker in the TiDB background periodically removes from the `mysql.gc_delete_range` table the keys that exceeds the GC life time for deletion.

Therefore, to recover a table, you only need to recover the table metadata and delete the corresponding row record in the `mysql.gc_delete_range` table before the GC Worker deletes the table data. You can use a snapshot read of TiDB to recover the table metadata. Refer to [Read Historical Data](/how-to/get-started/read-historical-data.md) for details.

The recovery of the table metadata is done by obtaining the table metadata through the snapshot read, and then going through the process of table creation similar to `CREATE TABLE`. Therefore, `RECOVER TABLE` itself is actually a kind of DDL operation.
