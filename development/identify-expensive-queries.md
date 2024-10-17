---
title: Identify Expensive Queries
aliases: ['/docs/dev/identify-expensive-queries/','/docs/dev/how-to/maintain/identify-abnormal-queries/identify-expensive-queries/']
summary: TiDB helps identify expensive queries by printing information about statements that exceed the execution time or memory usage threshold. This allows for diagnosing and improving SQL performance. The expensive query log includes details such as execution time, memory usage, user, database, and TiKV Coprocessor task information. This log differs from the slow query log as it prints information as soon as the statement exceeds the resource threshold.
---

# Identify Expensive Queries

TiDB allows you to identify expensive queries during SQL execution, so you can diagnose and improve the performance of SQL execution. Specifically, TiDB prints the information about statements whose execution time exceeds [`tidb_expensive_query_time_threshold`](/system-variables.md#tidb_expensive_query_time_threshold) (60 seconds by default) or memory usage exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (1 GB by default) to the [tidb-server log file](/tidb-configuration-file.md#logfile) ("tidb.log" by default).

> **Note:**
>
> The expensive query log differs from the [slow query log](/identify-slow-queries.md) in this way: TiDB prints statement information to the expensive query log **as soon as** the statement exceeds the threshold of resource usage (execution time or memory usage); while TiDB prints statement information to the slow query log **after** the statement execution.

## Expensive query log example

```sql
[expensivequery.go:145] [expensive_query] [cost_time=60.021998785s] [cop_time=0.022540151s] [process_time=28.448316643s] [wait_time=0.045507163s] [request_count=430] [total_keys=3538276] [process_keys=3537846] [num_cop_tasks=430] [process_avg_time=0.066158875s] [process_p90_time=0.140427865s] [process_max_time=0.27903656s] [process_max_addr=tikv-1-peer:20160] [wait_avg_time=0.00010583s] [wait_p90_time=0.000358794s] [wait_max_time=0.001218721s] [wait_max_addr=tikv-1-peer:20160] [stats=usertable:451469035823955972] [conn=1621098504] [user=root] [database=test] [table_ids="[104]"] [txn_start_ts=451469037501677571] [mem_max="621043469 Bytes (592.3 MB)"] [sql="insert /*+ SET_VAR(tidb_dml_type=bulk) */ into usertable_2 select * from usertable limit 5000000"] [session_alias=] ["affected rows"=3505282]]
```

## Fields description

Basic fields:

* `cost_time`: The execution time of a statement when the log is printed.
* `stats`: The version of statistics used by the tables or indexes involved in a statement. If the value is `pseudo`, it means that there are no available statistics. In this case, you need to analyze the tables or indexes.
* `table_ids`: The IDs of the tables involved in a statement.
* `txn_start_ts`: The start timestamp and the unique ID of a transaction. You can use this value to search for the transaction-related logs.
* `sql`: The sql statement.
* `session_alias`: The alias of the current session.
* `affected rows`: The number of rows currently affected by the statement.

Memory usage related fields:

* `mem_max`: Memory usage of a statement when the log is printed. This field has two kinds of units to measure memory usage: byte and other readable and adaptable units (such as MB and GB).

User related fields:

* `user`: The name of the user who executes the statement.
* `conn_id`: The connection ID (session ID). For example, you can use the keyword `con:60026` to search for the log whose session ID is `60026`.
* `database`: The database where the statement is executed.

TiKV Coprocessor task related fields:

* `wait_time`: The total waiting time of all Coprocessor requests of a statement in TiKV. Because the Coprocessor of TiKV runs a limited number of threads, requests might queue up when all threads of Coprocessor are working. When a request in the queue takes a long time to process, the waiting time of the subsequent requests increases.
* `request_count`: The number of Coprocessor requests that a statement sends.
* `total_keys`: The number of keys that Coprocessor has scanned.
* `processed_keys`: The number of keys that Coprocessor has processed. Compared with `total_keys`, `processed_keys` does not include the old versions of MVCC. A great difference between `processed_keys` and `total_keys` indicates that many old versions exist.
* `num_cop_tasks`: The number of Coprocessor requests that a statement sends.
* `process_avg_time`: The average execution time of Coprocessor tasks.
* `process_p90_time`: The P90 execution time of Coprocessor tasks.
* `process_max_time`: The maximum execution time of Coprocessor tasks.
* `process_max_addr`: The address of the Coprocessor task with the longest execution time.
* `wait_avg_time`: The average waiting time of Coprocessor tasks.
* `wait_p90_time`: The P90 waiting time of Coprocessor tasks.
* `wait_max_time`: The maximum waiting time of Coprocessor tasks.
* `wait_max_addr`: The address of the Coprocessor task with the longest waiting time.
