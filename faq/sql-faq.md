---
title: SQL FAQs
summary: Learn about the FAQs related to TiDB SQL.
---

# SQL FAQs

This document summarizes the FAQs related to SQL operations in TiDB.

## Does TiDB support the secondary key?

Yes. You can have the [`NOT NULL` constraint](/constraints.md#not-null) on a non-primary key column with a unique [secondary index](/develop/dev-guide-create-secondary-indexes.md). In this case, the column works as a secondary key.

## How does TiDB perform when executing DDL operations on a large table?

DDL operations of TiDB on large tables are usually not an issue. TiDB supports online DDL operations, and these DDL operations do not block DML operations.

For some DDL operations such as adding columns, deleting columns or dropping indexes, TiDB can perform these operations quickly.

For some heavy DDL operations such as adding indexes, TiDB needs to backfill data, which takes a longer time (depending on the size of the table) and consumes additional resources. The impact on online traffic is tunable. TiDB can do the backfill with multiple threads, and the resource consumed can be set by the following system variables:

- [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
- [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
- [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
- [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

## How to choose the right query plan? Do I need to use hints? Or can I use hints?

TiDB includes a cost-based optimizer. In most cases, the optimizer chooses the optimal query plan for you. If the optimizer does not work well, you can still use [optimizer hints](/optimizer-hints.md) to intervene with the optimizer.

In addition, you can also use the [SQL binding](/sql-plan-management.md#sql-binding) to fix the query plan for a particular SQL statement.

## How to prevent the execution of a particular SQL statement?

You can create [SQL bindings](/sql-plan-management.md#sql-binding) with the [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) hint to limit the execution time of a particular statement to a small value (for example, 1ms). In this way, the statement is terminated automatically by the threshold.

For example, to prevent the execution of `SELECT * FROM t1, t2 WHERE t1.id = t2.id`, you can use the following SQL binding to limit the execution time of the statement to 1ms:

```sql
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ MAX_EXECUTION_TIME(1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **Note:**
>
> The precision of `MAX_EXECUTION_TIME` is roughly 100ms. Before TiDB terminates the SQL statement, the tasks in TiKV might be started. To reduce the TiKV resource consumption in such case, it is recommended to set [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540) to `ON`.

Dropping this SQL binding will remove the limit.

```sql
DROP GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

## What are the MySQL variables that TiDB is compatible with?

See [System Variables](/system-variables.md).

## The order of results is different from MySQL when `ORDER BY` is omitted

It is not a bug. The default order of records depends on various situations without any guarantee of consistency.

The order of results in MySQL might appear stable because queries are executed in a single thread. However, it is common that query plans can change when upgrading to new versions. It is recommended to use `ORDER BY` whenever an order of results is desired.

The reference can be found in [ISO/IEC 9075:1992, Database Language SQL- July 30, 1992](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt), which states as follows:

> If an `<order by clause>` is not specified, then the table specified by the `<cursor specification>` is T and the ordering of rows in T is implementation-dependent.

In the following two queries, both results are considered legal:

```sql
> select * from t;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
+------+------+
2 rows in set (0.00 sec)
```

```sql
> select * from t; -- the order of results is not guaranteed
+------+------+
| a    | b    |
+------+------+
|    2 |    2 |
|    1 |    1 |
+------+------+
2 rows in set (0.00 sec)
```

If the list of columns used in the `ORDER BY` is non-unique, the statement is also considered non-deterministic. In the following example, the column `a` has duplicate values. Thus, only `ORDER BY a, b` is guaranteed deterministic:

```sql
> select * from t order by a;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    1 |
|    2 |    2 |
+------+------+
3 rows in set (0.00 sec)
```

In the following statement, the order of column `a` is guaranteed, but the order of `b` is not guaranteed.

```sql
> select * from t order by a;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
|    2 |    1 |
+------+------+
3 rows in set (0.00 sec)
```

In TiDB, you can also use the system variable [`tidb_enable_ordered_result_mode`](/system-variables.md#tidb_enable_ordered_result_mode) to sort the final output result automatically.

## Does TiDB support `SELECT FOR UPDATE`?

Yes. When using pessimistic locking (the default since TiDB v3.0.8) the `SELECT FOR UPDATE` execution behaves similar to MySQL.

When using optimistic locking, `SELECT FOR UPDATE` does not lock data when the transaction is started, but checks conflicts when the transaction is committed. If the check reveals conflicts, the committing transaction rolls back.

For details, see [description of the `SELECT` syntax elements](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements).

## Can the codec of TiDB guarantee that the UTF-8 string is memcomparable? Is there any coding suggestion if our key needs to support UTF-8?

TiDB uses the UTF-8 character set by default and currently only supports UTF-8. The string of TiDB uses the memcomparable format.

## What is the maximum number of statements in a transaction?

The maximum number of statements in a transaction is 5000 by default.

In the optimistic transaction mode, When transaction retry is enabled, the default upper limit is 5000. You can adjust the limit by using the [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit) parameter.

## Why does the auto-increment ID of the later inserted data is smaller than that of the earlier inserted data in TiDB?

The auto-increment ID feature in TiDB is only guaranteed to be automatically incremental and unique but is not guaranteed to be allocated sequentially. Currently, TiDB is allocating IDs in batches. If data is inserted into multiple TiDB servers simultaneously, the allocated IDs are not sequential. When multiple threads concurrently insert data to multiple `tidb-server` instances, the auto-increment ID of the later inserted data might be smaller. TiDB allows specifying `AUTO_INCREMENT` for the integer field, but allows only one `AUTO_INCREMENT` field in a single table. For details, see [Auto-increment ID](/mysql-compatibility.md#auto-increment-id) and [the AUTO_INCREMENT attribute](/auto-increment.md).

## How do I modify the `sql_mode` in TiDB?

TiDB supports modifying the [`sql_mode`](/system-variables.md#sql_mode) system variables on a SESSION or GLOBAL basis.

- Changes to [`GLOBAL`](/sql-statements/sql-statement-set-variable.md) scoped variables propagate to the rest servers of the cluster and persist across restarts. This means that you do not need to change the `sql_mode` value on each TiDB server.
- Changes to `SESSION` scoped variables only affect the current client session. After restarting a server, the changes are lost.

## Error: `java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation` while using Sqoop to write data into TiDB in batches

In Sqoop, `--batch` means committing 100 statements in each batch, but by default each statement contains 100 SQL statements. So, 100 * 100 = 10000 SQL statements, which exceeds 5000, the maximum number of statements allowed in a single TiDB transaction.

Two solutions:

- Add the `-Dsqoop.export.records.per.statement=10` option as follows:

    {{< copyable "shell-regular" >}}

    ```bash
    sqoop export \
        -Dsqoop.export.records.per.statement=10 \
        --connect jdbc:mysql://mysql.example.com/sqoop \
        --username sqoop ${user} \
        --password ${passwd} \
        --table ${tab_name} \
        --export-dir ${dir} \
        --batch
    ```

- You can also increase the limited number of statements in a single TiDB transaction, but this will consume more memory. For details, see [Limitations on SQL statements](/tidb-limitations.md#limitations-on-sql-statements).

## Does TiDB have a function like the Flashback Query in Oracle? Does it support DDL?

 Yes, it does. And it supports DDL as well. For details, see [Read Historical Data Using the `AS OF TIMESTAMP` Clause](/as-of-timestamp.md).

## Does TiDB release space immediately after deleting data?

None of the `DELETE`, `TRUNCATE` and `DROP` operations release data immediately. For the `TRUNCATE` and `DROP` operations, after the TiDB GC (Garbage Collection) time (10 minutes by default), the data is deleted and the space is released. For the `DELETE` operations, the data is deleted but the space is not immediately released until the compaction is performed.

## Why does the query speed get slow after data is deleted?

Deleting a large amount of data leaves a lot of useless keys, affecting the query efficiency. To solve the problem, you can use the [Region Merge](/best-practices/massive-regions-best-practices.md#method-3-enable-region-merge) feature. For details, see the [deleting data section in TiDB Best Practices](https://en.pingcap.com/blog/tidb-best-practice/#write).

## What should I do if it is slow to reclaim storage space after deleting data?

Because TiDB uses multi-version concurrency control (MVCC), when the old data is overwritten with new data, the old data is not replaced but retained along with the new data. Timestamps are used to identify the data version. Deleting data does not immediately reclaim space. Garbage collection is delayed so that concurrent transactions are able to see earlier versions of rows. This can be configured via the [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (default: `10m0s`) system variable.

## Does `SHOW PROCESSLIST` display the system process ID?

The display content of TiDB `SHOW PROCESSLIST` is almost the same as that of MySQL `SHOW PROCESSLIST`. TiDB `SHOW PROCESSLIST` does not display the system process ID. The ID that it displays is the current session ID. The differences between TiDB `SHOW PROCESSLIST` and MySQL `SHOW PROCESSLIST` are as follows:

- As TiDB is a distributed database, the `tidb-server` instance is a stateless engine for parsing and executing the SQL statements (for details, see [TiDB architecture](/tidb-architecture.md)). `SHOW PROCESSLIST` displays the session list executed in the `tidb-server` instance that the user logs in to from the MySQL client, not the list of all the sessions running in the cluster. But MySQL is a standalone database and its `SHOW PROCESSLIST` displays all the SQL statements executed in MySQL.
- The `State` column in TiDB is not continually updated during query execution. Because TiDB supports parallel query, each statement might be in multiple _states_ at once, and so it is difficult to simplify to a single value.

## How to control or change the execution priority of SQL commits?

TiDB supports changing the priority on a [global](/system-variables.md#tidb_force_priority) or individual statement basis. Priority has the following meaning:

- `HIGH_PRIORITY`: this statement has a high priority, that is, TiDB gives priority to this statement and executes it first.

- `LOW_PRIORITY`: this statement has a low priority, that is, TiDB reduces the priority of this statement during the execution period.

- `DELAYED`: this statement has normal priority and is the same as the `NO_PRIORITY` setting for `tidb_force_priority`.

> **Note:**
>
> Starting from v6.6.0, TiDB supports [Resource Control](/tidb-resource-control.md). You can use this feature to execute SQL statements with different priorities in different resource groups. By configuring proper quotas and priorities for these resource groups, you can gain better scheduling control for SQL statements with different priorities. When resource control is enabled, statement priority will no longer take effect. It is recommended that you use [Resource Control](/tidb-resource-control.md) to manage resource usage for different SQL statements.

You can combine the above two parameters with the DML of TiDB to use them. For example:

1. Adjust the priority by writing SQL statements in the database:

    {{< copyable "sql" >}}

    ```sql
    SELECT HIGH_PRIORITY | LOW_PRIORITY | DELAYED COUNT(*) FROM table_name;
    INSERT HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name insert_values;
    DELETE HIGH_PRIORITY | LOW_PRIORITY | DELAYED FROM table_name;
    UPDATE HIGH_PRIORITY | LOW_PRIORITY | DELAYED table_reference SET assignment_list WHERE where_condition;
    REPLACE HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name;
    ```

2. The full table scan statement automatically adjusts itself to a low priority. [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) has a low priority by default.

## What's the trigger strategy for `auto analyze` in TiDB?

When the number of rows in a table or a single partition of a partitioned table reaches 1000, and the ratio (the number of modified rows / the current total number of rows) of the table or partition is larger than [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio), the [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) statement is automatically triggered.

The default value of the `tidb_auto_analyze_ratio` system variable is `0.5`, indicating that this feature is enabled by default. It is not recommended to set the value of `tidb_auto_analyze_ratio` to be larger than or equal to [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) (the default value is `0.8`), otherwise the optimizer might use pseudo statistics. TiDB v5.3.0 introduces the [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) variable, and when you set it to `OFF`, pseudo statistics are not used even if the statistics are outdated.

To disable `auto analyze`, use the system variable [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610).

## Can I use optimizer hints to override the optimizer behavior?

TiDB supports multiple ways to override the default query optimizer behavior, including [hints](/optimizer-hints.md) and [SQL Plan Management](/sql-plan-management.md). The basic usage is similar to MySQL, with several TiDB specific extensions:

```sql
SELECT column_name FROM table_name USE INDEX（index_name）WHERE where_condition;
```

## DDL Execution

This section lists issues related to DDL statement execution. For detailed explanations on the DDL execution principles, see [Execution Principles and Best Practices of DDL Statements](/ddl-introduction.md).

### How long does it take to perform various DDL operations?

Assume that DDL operations are not blocked, each TiDB server can update the schema version normally, and the DDL Owner node is running normally. In this case, the estimated time for various DDL operations is as follows:

| DDL Operation Type | Estimated Time |
|:----------|:-----------|
| Reorg DDL, such as `ADD INDEX`, `MODIFY COLUMN` (Reorg type data changes) | Depends on the amount of data, system load, and DDL parameter settings. |
| General DDL (DDL types other than Reorg), such as `CREATE DATABASE`, `CREATE TABLE`, `DROP DATABASE`, `DROP TABLE`, `TRUNCATE TABLE`, `ALTER TABLE ADD`, `ALTER TABLE DROP`, `MODIFY COLUMN` (only changes metadata), `DROP INDEX` | About 1 second |

> **Note:**
>
> The above is estimated time for the operations. The actual time might be different.

### Possible reasons why DDL execution is slow

- In a user session, if there is a non-auto-commit DML statement before a DDL statement, and if the commit operation of the non-auto-commit DML statement is slow, it will cause the DDL statement to execute slowly. That is, TiDB commits the uncommitted DML statement before executing the DDL statement.

- When multiple DDL statements are executed together, the execution of the later DDL statements might be slower because they might need to wait in queue. Queuing scenarios include:

    - The same type of DDL statements need to be queued. For example, both `CREATE TABLE` and `CREATE DATABASE` are general DDL statements, so when both operations are executed at the same time, they need to be queued. Starting from TiDB v6.2.0, parallel DDL statements are supported, but to avoid DDL execution using too many TiDB computing resources, there is also a concurrency limit. Queuing occurs when DDL exceeds the concurrency limit.
    - The DDL operations performed on the same table have a dependency relationship between them. The later DDL statement needs to wait for the previous DDL operation to complete.

- After the cluster is started normally, the execution time of the first DDL operation might be relatively long because the DDL module is electing the DDL Owner.

- TiDB is terminated, which causes TiDB to not able to communicate with PD normally (including power-off situations). Or TiDB is terminated by the `kill -9` command, which causes TiDB to not timely clear the registration data from PD.

- A communication problem occurs between a certain TiDB node in the cluster and PD or TiKV, which makes TiDB not able to obtain the latest version information in time.

### What triggers the `Information schema is changed` error?

When executing SQL statements, TiDB determines the schema version of an object based on the isolation level and processes the SQL statement accordingly. TiDB also supports online asynchronous DDL changes. When you execute DML statements, there might be DDL statements being executed at the same time, and you need to ensure that each SQL statement is executed on the same schema. Therefore, when executing DML, if a DDL operation is ongoing, TiDB might report an `Information schema is changed` error. 

Starting from v6.4.0, TiDB has implemented a [metadata lock mechanism](/metadata-lock.md), which allows the coordinated execution of DML statements and DDL schema changes, and avoids most `Information schema is changed` errors.

Now, there are still a few causes for this error reporting:

+ Cause 1: Some tables involved in the DML operation are the same tables involved in the ongoing DDL operation. To check the ongoing DDL operations, use the `ADMIN SHOW DDL` statement.
+ Cause 2: The DML operation goes on for a long time. During this period, many DDL statements have been executed, which causes more than 1024 `schema` version changes. You can modify this default value by modifying the `tidb_max_delta_schema_count` variable.
+ Cause 3: The TiDB server that accepts the DML request is not able to load `schema information` for a long time (possibly caused by the connection failure between TiDB and PD or TiKV). During this period, many DDL statements have been executed, which causes more than 100 `schema` version changes.
+ Cause 4: After TiDB restarts and before the first DDL operation is executed, the DML operation is executed and then encounters the first DDL operation (which means before the first DDL operation is executed, the transaction corresponding to the DML is started. And after the first `schema` version of the DDL is changed, the transaction corresponding to the DML is committed), this DML operation reports this error.

In the preceding causes, only Cause 1 is related to tables. Cause 1 and Cause 2 do not impact the application, as the related DML operations retry after failure. For cause 3, you need to check the network between TiDB and TiKV/PD.

> **Note:**
>
> + Currently, TiDB does not cache all the `schema` version changes.
> + For each DDL operation, the number of `schema` version changes is the same with the number of corresponding `schema state` version changes.
> + Different DDL operations cause different number of `schema` version changes. For example, the `CREATE TABLE` statement causes one `schema` version change while the `ADD COLUMN` statement causes four.

### What are the causes of the "Information schema is out of date" error?

Before TiDB v6.5.0, when executing a DML statement, if TiDB fails to load the latest schema within a DDL lease (45s by default), the `Information schema is out of date` error might occur. Possible causes are:

- The TiDB instance that executed this DML was killed, and the transaction execution corresponding to this DML statement took longer than a DDL lease. When the transaction was committed, the error occurred.
- TiDB failed to connect to PD or TiKV while executing this DML statement. As a result, TiDB failed to load schema within a DDL lease or disconnected from PD due to the keepalive setting.

### Error is reported when executing DDL statements under high concurrency?

When you execute DDL statements (such as creating tables in batches) under high concurrency, a very few of these statements might fail because of key conflicts during the concurrent execution.

It is recommended to keep the number of concurrent DDL statements under 20. Otherwise, you need to retry the failed statements from the client.

### Why is DDL execution blocked?

Before TiDB v6.2.0, TiDB allocates DDL statements to two first-in-first-out queues based on the type of DDL statements. More specifically, Reorg DDLs go to the Reorg queue and General DDLs go to the general queue. Because of the first-in-first-out limitation and the need for serial execution of DDL statements on the same table, multiple DDL statements might be blocked during execution.

For example, consider the following DDL statements:

- DDL 1: `CREATE INDEX idx on t(a int);`
- DDL 2: `ALTER TABLE t ADD COLUMN b int;`
- DDL 3: `CREATE TABLE t1(a int);`

Due to the limitation of the first-in-first-out queue, DDL 3 must wait for DDL 2 to execute. Also, because DDL statements on the same table need to be executed in serial, DDL 2 must wait for DDL 1 to execute. Therefore, DDL 3 needs to wait for DDL 1 to be executed first, even if they operate on different tables.

Starting from TiDB v6.2.0, the TiDB DDL module uses a concurrent framework. In the concurrent framework, there is no longer the limitation of the first-in-first-out queue. Instead, TiDB picks up the DDL task that can be executed from all DDL tasks. Additionally, the number of Reorg workers has been expanded, approximately to `CPU/4` per node. This allows TiDB to build indexes for multiple tables simultaneously in the concurrent framework.

Whether your cluster is a new cluster or an upgraded cluster from an earlier version, TiDB automatically uses the concurrent framework in TiDB v6.2 and later versions. You do not need to make manual adjustments.

### Identify the cause of stuck DDL execution

1. Eliminate other reasons that make the DDL statement execution slow.
2. Use one of the following methods to identify the DDL Owner node:
    - Use `curl http://{TiDBIP}:10080/info/all` to obtain the owner of the current cluster.
    - View the owner during a specific time period from the monitoring dashboard **DDL** > **DDL META OPM**.

- If the owner does not exist, try manually triggering owner election with: `curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`.
- If the owner exists, export the Goroutine stack and check for the possible stuck location.

## SQL optimization

### TiDB execution plan description

See [Understand the Query Execution Plan](/explain-overview.md).

### Statistics collection

See [Introduction to Statistics](/statistics.md).

### How to optimize `select count(1)`?

The `count(1)` statement counts the total number of rows in a table. Improving the degree of concurrency can significantly improve the speed. To modify the concurrency, refer to the [`tidb_distsql_scan_concurrency` document](/system-variables.md#tidb_distsql_scan_concurrency). But it also depends on the CPU and I/O resources. TiDB accesses TiKV in every query. When the amount of data is small, all MySQL is in memory, and TiDB needs to conduct a network access.

Recommendations:

- Improve the hardware configuration. See [Software and Hardware Requirements](/hardware-and-software-requirements.md).
- Improve the concurrency. The default value is 10. You can improve it to 50 and have a try. But usually the improvement is 2-4 times of the default value.
- Test the `count` in the case of large amount of data.
- Optimize the TiKV configuration. See [Tune TiKV Thread Performance](/tune-tikv-thread-performance.md) and [Tune TiKV Memory Performance](/tune-tikv-memory-performance.md).
- Enable the [Coprocessor Cache](/coprocessor-cache.md).

### How to view the progress of the current DDL job?

You can use `ADMIN SHOW DDL` to view the progress of the current DDL job. The operation is as follows:

```sql
ADMIN SHOW DDL;
```

```
*************************** 1. row ***************************
  SCHEMA_VER: 140
       OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
     SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
```

From the above results, you can get that the `ADD INDEX` operation is currently being processed. You can also get from the `RowCount` field of the `RUNNING_JOBS` column that now the `ADD INDEX` operation has added 77312 rows of indexes.

### How to view the DDL job?

- `ADMIN SHOW DDL`: to view the running DDL job
- `ADMIN SHOW DDL JOBS`: to view all the results in the current DDL job queue (including tasks that are running and waiting to run) and the last ten results in the completed DDL job queue
- `ADMIN SHOW DDL JOBS QUERIES 'job_id' [, 'job_id'] ...`: to view the original SQL statement of the DDL task corresponding to the `job_id`; the `job_id` only searches the running DDL job and the last ten results in the DDL history job queue.

### Does TiDB support CBO (Cost-Based Optimization)? If yes, to what extent?

Yes. TiDB uses the cost-based optimizer. The cost model and statistics are constantly optimized. TiDB also supports join algorithms like hash join and sort-merge join.

### How to determine whether I need to execute `analyze` on a table?

View the `Healthy` field using `SHOW STATS_HEALTHY` and generally you need to execute `ANALYZE` on a table when the field value is smaller than 60.

### What is the ID rule when a query plan is presented as a tree? What is the execution order for this tree?

No rule exists for these IDs but the IDs are unique. When IDs are generated, a counter works and adds one when one plan is generated. The execution order has nothing to do with the ID. The whole query plan is a tree and the execution process starts from the root node and the data is returned to the upper level continuously. For details about the query plan, see [Understanding the TiDB Query Execution Plan](/explain-overview.md).

### In the TiDB query plan, `cop` tasks are in the same root. Are they executed concurrently?

Currently the computing tasks of TiDB belong to two different types of tasks: `cop task` and `root task`.

`cop task` is the computing task which is pushed down to the KV end for distributed execution; `root task` is the computing task for single point execution on the TiDB end.

Generally the input data of `root task` comes from `cop task`; when `root task` processes data, `cop task` of TiKV can processes data at the same time and waits for the pull of `root task` of TiDB. Therefore, `cop` tasks can be considered as executed concurrently with `root task`; but their data has an upstream and downstream relationship. During the execution process, they are executed concurrently during some time. For example, the first `cop task` is processing the data in [100, 200] and the second `cop task` is processing the data in [1, 100]. For details, see [Understanding the TiDB Query Plan](/explain-overview.md).

## Database optimization

### Edit TiDB options

See [The TiDB Command Options](/command-line-flags-for-tidb-configuration.md).

### How to avoid hotspot issues and achieve load balancing? Is hot partition or range an issue in TiDB?

To learn the scenarios that cause hotspots, refer to [common hotpots](/troubleshoot-hot-spot-issues.md#common-hotspots). The following TiDB features are designed to help you solve hotspot issues:

- The [`SHARD_ROW_ID_BITS`](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots) attribute. After setting this attribute, row IDs are scattered and written into multiple Regions, which can alleviate the write hotspot issue.
- The [`AUTO_RANDOM`](/troubleshoot-hot-spot-issues.md#handle-auto-increment-primary-key-hotspot-tables-using-auto_random) attribute, which helps resolve hotspots brought by auto-increment primary keys.
- [Coprocessor Cache](/coprocessor-cache.md), for read hotspots on small tables.
- [Load Base Split](/configure-load-base-split.md), for hotspots caused by unbalanced access between Regions, such as full table scans for small tables.
- [Cached tables](/cached-tables.md), for frequently accessed but rarely updated small hotspot tables.

If you have a performance issue caused by hotspot, refer to [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md) to get it resolved.

### Tune TiKV performance

See [Tune TiKV Thread Performance](/tune-tikv-thread-performance.md) and [Tune TiKV Memory Performance](/tune-tikv-memory-performance.md).
