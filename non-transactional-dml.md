---
title: Non-Transactional DML Statements
summary: Learn the non-transactional DML statements in TiDB. At the expense of atomicity and isolation, a DML statement is split into multiple statements to be executed in sequence, which improves the stability and ease of use in batch data processing scenarios.
---

# Non-Transactional DML Statements

This document describes the usage scenarios, usage methods, restrictions of, and the frequently asked questions about non-transactional DML statements in TiDB.

A non-transactional DML statement is a DML statement split into multiple SQL statements (which is, multiple batches) to be executed in sequence, which enhances the performance and ease of use in the scenarios of batch data processing, at the expense of transactional atomicity and isolation.

Non-transactional DML statements include `INSERT`, `UPDATE`, and `DELETE`. TiDB currently only supports the non-transactional DML statements of `DELETE`. For detailed syntax, see [`BATCH`](/sql-statements/sql-statement-batch.md).

> **Note:**
>
> A non-transactional DML statement does not guarantee the atomicity and isolation of the statement, and is not equivalent to the original DML statement.

## Usage scenarios

In the scenarios of large data processing, you might often need to perform the same operation on a large batch of data. If you perform the operations directly using one SQL statement, the transaction size will exceed the limit and affect the execution performance.

Batch data processing often has no overlap of time or data with the online application operations. Data isolation is unnecessary when no concurrent operations exist. Atomicity is also unnecessary if bulk data operations are idempotent or easily retryable. If your application needs neither data isolation nor atomicity, you can consider using non-transactional DML statements.

Non-transactional DML statements are used to bypass the size limit on large transactions in certain scenarios. One statement is used to complete tasks that might need to be split into multiple transactions, with higher execution efficiency and less resource consumption.

For example, to delete expired data, if you ensure that no application will access the expired data, you can use a non-transactional DML statement to improve the `DELETE` performance.

## Prerequisites

Before using non-transactional DML statements, make sure that the following conditions are met:

- The statement does not require atomicity, which permits some rows to be modified and some rows to remain unmodified in the execution result.
- The statement is idempotent, or you are prepared to retry some data based on the error message. If the system variables `tidb_redact_log = 1` and `tidb_nontransactional_ignore_error = 1`, this statement must be idempotent. Otherwise, when the statement partially fails, the failed part cannot be accurately located.
- The data to be operated on by the statement has no other concurrent writes, which means it is not updated by other statements at the same time. Otherwise, unexpected result such as missing deletions and multiple deletions might occur.
- The statement does not modify the data to be read by the statement itself. Otherwise, the following batch will read the data written by the previous batch and easily causes unexpected result.
- The statement meets the [restrictions](#restrictions).
- It is not recommended to perform concurrent DDL operations on the table to be read and written by this DML statement.

> **WARNING:**
>
> If `tidb_redact_log` and `tidb_nontransactional_ignore_error` are enabled at the same time, you might not get the complete error information of each batch, and you cannot retry only the failed batch. Therefore, if both of the system variables are turned on, the non-transactional DML statement must be idempotent.

## Usage examples

### Use a non-transactional DML statement

The following sections describe the use of non-transactional DML statements with examples:

Create a table `t` with the following schema:

{{< copyable "sql" >}}

```sql
CREATE TABLE t(id int, v int, key(id));
```

```sql
Query OK, 0 rows affected
```

Insert some data into table `t`.

{{< copyable "sql" >}}

```sql
INSERT INTO t VALUES (1,2),(2,3),(3,4),(4,5),(5,6);
```

```sql
Query OK, 5 rows affected
```

The following operation uses a non-transactional DML statement to delete rows with values less than the integer 6 on column `v` of table `t`. This statement is split into two SQL statements, with a batch size of 2, divided by the `id` column and executed.

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE FROM t where v < 6;
```

```sql
+----------------+---------------+
| number of jobs | job status    |
+----------------+---------------+
| 2              | all succeeded |
+----------------+---------------+
1 row in set
```

Check the deletion results of the non-transactional DML statement.

{{< copyable "sql" >}}

```sql
SELECT * FROM t;
```

```sql
+----+---+
| id | v |
+----+---+
| 5  | 6 |
+----+---+
1 row in set
```

### Check the execution progress

During the execution of a non-transactional DML statement, you can view the execution progress using `SHOW PROCESSLIST`. The `Time` field in the returned result indicates the time consumption of the current batch execution. Logs and slow logs also record the progress of each split statement throughout the non-transactional DML execution. For example:

{{< copyable "sql" >}}

```sql
show processlist;
```

```sql
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| Id   | User | Host               | db     | Command | Time | State      | Info                                                                                               |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| 1203 | root | 100.64.10.62:52711 | test   | Query   | 0    | autocommit | /* job 506/500000 */ DELETE FROM `test`.`t1` WHERE `test`.`t1`.`_tidb_rowid` BETWEEN 2271 AND 2273 |
| 1209 | root | 100.64.10.62:52735 | <null> | Query   | 0    | autocommit | show full processlist                                                                              |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
```

### Terminate a non-transactional DML statement

To terminate a non-transactional DML statement, you can use `KILL TIDB`. Then TiDB will cancel all batches after the batch that is currently being executed. You can get the execution result from the log.

### Query the batch-dividing statement

During the execution of a non-transactional DML statement, a statement is internally used to divide the DML statement into multiple batches. To query this batch-dividing statement, you can add `DRY RUN QUERY` to this non-transactional DML statement. Then TiDB will not actually execute this query and the subsequent DML operations.

The following statement queries the batch-dividing statement during the execution of `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6`:

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DRY RUN QUERY DELETE FROM t WHERE v < 6;
```

```sql
+--------------------------------------------------------------------------------+
| query statement                                                                |
+--------------------------------------------------------------------------------+
| SELECT `id` FROM `test`.`t` WHERE (`v` < 6) ORDER BY IF(ISNULL(`id`),0,1),`id` |
+--------------------------------------------------------------------------------+
1 row in set
```

### Query the statements corresponding to the first and the last batches

To query the actual DML statements corresponding to the first and last batches in a non-transactional DML statement, you can add `DRY RUN` to this non-transactional DML statement. Then, TiDB only divides batches and does not execute these SQL statements. Because there might be many batches, not all batches are displayed, and only the first one and the last one are displayed.

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DRY RUN DELETE FROM t where v < 6;
```

```sql
+-------------------------------------------------------------------+
| split statement examples                                          |
+-------------------------------------------------------------------+
| DELETE FROM `test`.`t` WHERE (`id` BETWEEN 1 AND 2 AND (`v` < 6)) |
| DELETE FROM `test`.`t` WHERE (`id` BETWEEN 3 AND 4 AND (`v` < 6)) |
+-------------------------------------------------------------------+
2 rows in set
```

### Use the optimizer hint

If an optimizer hint is originally supported in the `DELETE` statement, the optimizer hint is also supported in the non-transactional `DELETE` statement. The position of the hint is the same as that in the ordinary `DELETE` statement:

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE /*+ USE_INDEX(t)*/ FROM t where v < 6;
```

## Best practices

To use a non-transactional DML statement, the following steps are recommended:

1. Select an appropriate [dividing column](#parameter-description). Integer or string types are recommended.
2. (Optional) Add `DRY RUN QUERY` to the non-transactional DML statement, execute the query manually, and confirm whether the data range affected by the DML statement is roughly correct.
3. (Optional) Add `DRY RUN` to the non-transactional DML statement, execute the query manually, and check the split statements and the execution plans. You need to pay attention to the index selection efficiency.
4. Execute the non-transactional DML statement.
5. If an error is reported, get the specific failed data range from the error message or log, and retry or handle it manually.

## Parameter description

| Parameter | Description | Default value | Required or not | Recommended value |
| :-- | :-- | :-- | :-- | :-- |
| Dividing column | The column used to batches, such as the `id` column in the above non-transactional DML statement `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6`. | TiDB tries to automatically select a dividing column. | No | Select a column that can meet the `WHERE` condition in a most efficient way. |
| Batch size | Used to control the size of each batch. The number of batches is the number of SQL statements into which DML operations are split, such as `LIMIT 2` in the above non-transactional DML statement `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 2`. The more batches, the smaller the batch size. | N/A | Yes | 1000-1000000. Too small or too large a batch will lead to performance degradation. |

### Column selection

A non-transactional DML statement uses a column as the basis for data batching, which is the dividing column. For higher execution efficiency, a dividing column is expected to use index. The execution efficiency brought by different indexes and dividing columns might vary by dozens of times. When choosing to dividing columns, consider the following suggestions:

- When you have a certain understanding of the application data distribution, according to the `WHERE` condition, choose the column  that divides data with smaller ranges after the batching.
    - Ideally, the `WHERE` condition can take advantage of the index of the dividing column to reduce the amount of data to be scanned per batch. For example, there is a transaction table that records the start and end time of each transaction, and you want to delete all transaction records whose end time is before one month. If there is an index on the start time of the transaction, and the start and end times of the transaction are relatively close, then you can select the start time column as the dividing column.
    - In a less-than-ideal case, the data distribution of the dividing column is completely independent of the `WHERE` condition, and the index of the dividing column cannot be used to reduce the scope of the data scan.
- When a clustered index exists, it is recommended to use the primary key (including an `INT` primary key and `_tidb_rowid`) as the dividing column, so that the execution efficiency is higher.

You can also choose not to specify a dividing column. Then, TiDB will use the first column of `handle` as the dividing column by default. But if the first column of the primary key of the clustered index is of a data type not supported by non-transactional DML statements (which is `ENUM`, `BIT`, `SET`, `JSON`), TiDB will report an error. You can choose an appropriate dividing column according to your application needs.

### Batch size selection

In non-transactional DML statements, the larger the batch size is, the fewer SQL statements are split and the slower each SQL statement is executed. The optimal batch size depends on the workload. It is recommended to start from 50000. Both too small and too large batch sizes will cause decreased execution efficiency.

The information of each batch is stored in memory, so too many batches can significantly increase memory consumption. This explains why the batch size cannot be too small. The upper limit of memory consumed by non-transactional statements for storing batch information is the same as [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), and the action triggered when this limit is exceeded is determined by the configuration item [`oom-action`](/tidb-configuration -file.md#oom-action).

------------

## usage restrictions

Hard restrictions on non-transactional DML statements, TiDB will report an error if these conditions are not met.

- You can only operate on a single table, and multi-table joins are not currently supported.
- DML statements cannot contain `ORDER BY` or `LIMIT` clauses.
- The column used for splitting must be indexed. The index can be a single-column index, or the first column of a joint index.
- Must be used in [`autocommit`](/system-variables.md#autocommit) mode.
- Cannot be used when batch-dml is enabled.
- Cannot be used when [`tidb_snapshot`](/read-historical-data.md#operation flow) is set.
- Cannot be used with the `prepare` statement.
- `ENUM`, `BIT`, `SET`, `JSON` types are not supported for partition columns.
- Not supported for [temporary tables](/temporary-tables.md).
- [Common Table Expression](/develop/use-common-table-expression.md) is not supported.

## Control batch execution failure

Non-transactional DML statements do not satisfy atomicity, and some batches may succeed and some fail. The system variable [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error - introduced since -v610-) controls the behavior of non-transactional DML statements to handle errors.

An exception is that if the first batch fails to execute, there is a high probability that the statement itself is wrong, and the entire non-transactional statement will directly return an error.

## Implementation principle

The implementation principle of non-transactional DML statements is to build in the splitting of SQL statements that need to be manually executed on the user side as a function of TiDB to simplify user operations. To understand the behavior of a non-transactional DML statement, think of it as a user script doing the following:

For non-transactional DML `BATCH ON $C$ LIMIT $N$ DELETE FROM ... WHERE $P$`, where `$C$` is the column used for splitting, `$N$` is the batch size, `$ P$` is the filter condition.

1. According to the filter condition `$P$` of the original statement and the specified column `$C$` for splitting, TiDB queries all `$C$` that satisfy `$P$`. Sort these `$C$` into groups `$B_1 \dots B_k$` by `$N$`. For all `$B_i$`, keep its first and last `$C$` as `$S_i$` and `$E_i$`. The query statement executed in this step can be viewed through [`DRY RUN QUERY`](/non-transactional-dml.md# query non-transactional-dml-statement divided-batch-statement).
2. The data involved in `$B_i$` is a subset that satisfies ```$P_i$:`C BETWEEN <S_i> AND <E_i>` ```. You can use `$P_i$` to narrow down the range of data that each batch needs to process.
3. For `$B_i$`, embed the above condition into the `WHERE` condition of the original statement, making it `WHERE ($P_i$) AND ($P$)`. The execution result of this step can be viewed through [`DRY RUN`](/non-transactional-dml.md# query the statement corresponding to the first and last -batch- in the non-transactional-dml-statement).
4. For all batches, execute new statements in sequence. The errors for each grouping are collected and combined, and returned as the result of the entire non-transactional DML statement after all groupings are complete.

## Similarities and differences with batch-dml

batch-dml is a mechanism for splitting a transaction into multiple transaction commits during DML statement execution.

> **Note:**
>
> When the batch-dml function is used improperly, there is a risk of data index inconsistency. This function will be deprecated in subsequent versions of TiDB, so it is not recommended to use it.

Non-transactional DML statements are not yet a replacement for all batch-dml use cases. Their main differences are:

- Performance: In the case of high [Partition Efficiency] (#selection of partition columns), the performance of non-transactional DML statements and batch-dml are close. Non-transactional DML statements can be significantly slower than batch-dml in cases where partitioning is less efficient.

- Stability: batch-dml is prone to data index inconsistencies due to improper use. Non-transactional DML statements do not cause data index inconsistencies. However, when used incorrectly, non-transactional DML statements are not equivalent to the original statements, and applications may observe unexpected behavior. See [FAQ](#FAQ) for details.

## common problem

### An error occurs during execution `Failed to restore the delete statement, probably because of unsupported type of the shard column`

The type of partition column does not support `ENUM`, `BIT`, `SET`, `JSON` types, please try to specify a new partition column. Columns of type integer or string are recommended. If the partition column is not of these types, please contact PingCAP technical support.

### Non-transactional `DELETE` has "exceptional" behavior that is not equivalent to normal `DELETE`

A non-transactional DML statement is not equivalent to the original form of this DML statement, which may be due to the following reasons:

- There are other writes concurrently.
- A non-transactional DML statement modifies a value that the statement itself would read.
- The actual execution of the SQL statement in each batch may cause the execution plan and expression calculation order to be different due to the change of the `WHERE` condition, resulting in different execution results.
- DML statements contain non-deterministic operations.

## Compatibility information

Non-transactional statements are unique to TiDB and are not compatible with MySQL.

## Explore more

* [BATCH](/sql-statements/sql-statement-batch.md) syntax
* [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-introduced from -v610-)
