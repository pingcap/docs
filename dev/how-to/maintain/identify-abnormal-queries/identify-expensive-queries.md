---
title: Identify Expensive Queries
category: how to
---

# Identify expensive queries

To help users identify expensive queries during the statement execution, diagnose and improve the performance of SQL execution, TiDB prints the information about statements of which the execution time exceeds [tidb_expensive_query_time_threshold](/dev/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_expensive_query_time_threshold) (the default value is 60 seconds), or the memory usage exceeds [mem-quota-query](/dev/reference/configuration/tidb-server/configuration-file.md#mem-quota-query) (the default value is 32 GB), to the [tidb-server log file](/dev/reference/configuration/tidb-server/configuration-file.md#logfile) (the default file is "tidb.log").

> **Note:**
>
> The difference between the expensive query log and the [slow query log](/dev/how-to/maintain/identify-abnormal-queries/identify-slow-queries.md) is that: the former prints information during the statement execution; the latter prints after the execution. When a statement reaches the threshold of resource usage (be it execution time or memory usage) during execution, TiDB writes information about the statement to the log live.

## Usage example

```sql
[2020/02/05 15:32:25.096 +08:00] [WARN] [expensivequery.go:167] [expensive_query] [cost_time=60.008338935s] [wait_time=0s] [request_count=1] [total_keys=70] [process_keys=65] [num_cop_tasks=1] [process_avg_time=0s] [process_p90_time=0s] [process_max_time=0s] [process_max_addr=10.0.1.9:20160] [wait_avg_time=0.002s] [wait_p90_time=0.002s] [wait_max_time=0.002s] [wait_max_addr=10.0.1.9:20160] [stats=t:pseudo] [conn_id=60026] [user=root] [database=test] [table_ids="[122]"] [txn_start_ts=414420273735139329] [mem_max="1035 Bytes (1.0107421875 KB)"] [sql="insert into t select sleep(1) from t"]
```

## Fields description

Expensive query basics:

* `cost_time`: The execution time for a statement when the log is printed.
* `stats`: Statistical information about tables or indexes involved in statements. `pesudo` indicates that there is no statistical information available; thus, you need to analyze tables or indexes.
* `table_ids`: The ID of tables involved in the statements.
* `txn_start_ts`: The start timestamp and the unique ID of a transaction. You can use this value to search for the transaction-related logs.
* `sql`: The sql statement.

Memory usage fields:

* `mem_max`: Memory used for the statement when the log is printed. The item uses two units to identify memory usage: byte and other readable and adaptable unit (such as MB, GB and so forth).

User fields:

* `user`: The name of the user who executes the statement.
* `conn_id`: The Connection ID (session ID). For example, you can use the keyword `con:60026` to search for the log whose session ID is `60026`.
* `database`: The current database.

TiKV Coprocessor Task fields:

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
