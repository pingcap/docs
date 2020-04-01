---
title: FLASHBACK TABLE
summary: Learn how to recover tables using the `FLASHBACK TABLE` statement.
category: reference
---

# FLASHBACK TABLE

The `FLASHBACK TABLE` statement is introduced in TiDB 4.0. You can use the `FLASHBACK TABLE` statement to restore the tables and data dropped by `DROP` or `TRUNCATE` within the Garbage Collection (GC) lifetime.

Use the following command to query the TiDB cluster's `tikv_gc_safe_point` and `tikv_gc_life_time`. As long as the table is dropped by `DROP` or `TRUNCATE` after the `tikv_gc_safe_point` time, you can restored the table using the `FLASHBACK TABLE` statement.

{{< copyable "sql" >}}

  ```sql
  select * from mysql.tidb where variable_name in ('tikv_gc_safe_point','tikv_gc_life_time');
  ```

## Syntax

{{< copyable "sql" >}}

```sql
FLASHBACK TABLE table_name [TO other_table_name]
```

## Notes

If a table is dropped and the GC lifetime has passed, you can no longer use the `FLASHBACK TABLE` statement to recover the dropped data. Otherwise, an error will be returned, which is similar to `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST`.

Pay attention to the following conditions and requirements when you enable TiDB Binlog and use the `FLASHBACK TABLE` statement:

* The downstream cluster must also support `FLASHBACK TABLE`.
* The GC lifetime of the slave cluster must be longer than that of the master cluster.
* The delay of replication between the upstream and downstream might also cause the failure to recover data to the downstream.
* If an error occurs when TiDB Binlog is replicating a table, you need filter that table in TiDB Binlog and manually import all data of that table.

## Example

- Recover the table data dropped by `DROP`:

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK TABLE t;
    ```

- Recover the table data dropped by `TRUNCATE`. Because the truncated table `t` still exists, you need to rename the table `t` to be recovered. Otherwise, an error will be returned indicating that table `t` already exists.

    ```sql
    TRUNCATE TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## Implementation principle

When deleting a table, TiDB only deletes the table metadata, and writes the table data (row data and index data) to be deleted to the `mysql.gc_delete_range` table. The GC Worker in the TiDB background periodically removes from the `mysql.gc_delete_range` table the keys that exceed the GC lifetime.

Therefore, to recover a table, you only need to recover the table metadata and delete the corresponding row record in the `mysql.gc_delete_range` table before the GC Worker deletes the table data. You can use a snapshot read of TiDB to recover the table metadata. Refer to [Read Historical Data](/how-to/get-started/read-historical-data.md) for details. The following is the working process of `FLASHBACK TABLE t TO t1`:

1. TiDB searches the recent DDL job history and locates the first DDL operation of the `DROP TABLE` type. If TiDB fails to locate one, an error is returned.
2. TiDB checks whether the starting time of the DDL job is before `tikv_gc_safe_point`. If it is before `tikv_gc_safe_point`, it means that the table dropped by `DROP` or `TRUNCATE` has been cleaned up by the GC and an error is returned.
3. TiDB uses the starting time of the DDL job as the snapshot to read historical data and read table metadata.
4. TiDB deletes GC tasks related to table `t` in `mysql.gc_delete_range`.
5. TiDB changes `name` in the table's meta-information to `t1`, and uses this meta-information to create a new table. Note that only the table name is changed but not the table ID. The table ID is still that of the previously dropped table `t`.

From the above process, you can see that TiDB always operates on the meta-information of the table, and the user data of the table has not been modified. The restored table `t1` has the same table ID as the previously deleted table `t`, so the table `t1` can read the user data of the table `t`.

> **Note:**
>
> You cannot use `FLASHBACK` to restore the same deleted table multiple times, because the table ID of the table restored by `FLASHBACK` is still the table ID of the deleted table, and TiDB requires that all existing tables must have a globally unique table ID.

Table recovery is done by TiDB obtaining the table metadata through snapshot read, and then going through the process of table creation similar to `CREATE TABLE`. Therefore, `RECOVER TABLE` itself is, in essence, a kind of DDL operation.
