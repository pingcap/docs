---
 title: Slow Query Log
 summary: Use the slow query log to locate inappropriate SQL statements
 category: user guide
 ---

 # Slow Query Log

 An inappropriate SQL statement can increase the pressure on the entire cluster, resulting in a longer response time. To solve this problem, you can use the slow query log to locate the questionable statements and thus improve the performance.

 ### Obtain the log

By grepping the keyword `SLOW_QUERY` in the log file of TiDB, you can obtain the logs of statements whose execution time exceeds [slow-threshold](../op-guide/tidb-config-file.md#slow-threshold).

`slow-threshold` can be edited in the configuration file and its default value is 300ms. If you configure the [slow-query-file](../op-guide/tidb-config-file.md#slow-query-file), all of the slow query log will be written in this file. 

 ### Usage

```
2018/08/20 19:52:08.632 adapter.go:363: [warning] [SLOW_QUERY] cost_time:18.647928814s
process_time:1m6.768s wait_time:12m11.212s backoff_time:600ms request_count:2058
total_keys:1869712 processed_keys:1869710 succ:true con:3 user:root@127.0.0.1
txn_start_ts:402329674704224261 database:test table_ids:[31],index_ids:[1],
sql:select count(c) from sbtest1 use index (k_1)
```

### Fields Explanation

#### `cost_time`

The execution time of this statement. Only the statements whose execution time exceeds [slow-threshold](../op-guide/tidb-config-file.md#slow-threshold) output the slow query log.

#### `process_time`

The total processing time that TiKV spends on this statement. Since data is sent to TiKV concurrently for execution, this value may exceed `cost_time`.

#### `wait_time`

The total waiting time that TiKV spends on this statement. Since the `coprocessor` of TiKV runs a limited number of threads, requests may queue up when all threads of `coprocessor` are working. When some request in the queue takes a long time to process, the waiting time of the following requests will increase.

#### `backoff_time`

The waiting time that TiKV spends before retrying when the mistakes in need of retrying occur. The common mistakes which requires retrying include: lock, Region split, TiKV server is busy, etc.

#### `request_count`

The number of `coprocessor` requests that this statement sends.

#### `total_keys`

The number of keys that `coprocessor` has scanned.

#### `processed_keys`

The number of keys that `coprocessor` has processed. Compared with `total_keys`, `processed_keys`
does not include the old versions of MVCC or the MVCC delete flags. A great difference between `processed_keys` and `total_keys` indicates that the number of old versions are relatively large.

#### `succ`

Whether the execution of the request succeeds or not.

#### `con`

Connection ID or session ID. For example, you can use the keyword `con:3` to grep the log whose session ID is 3.

#### `user`

The username of the executed statement.

#### `txn_start_ts`

The start timestamp of the transaction, that is, the ID of the transaction. You can use this value to grep the transaction-related logs.

#### `database`

The current database.

#### `table_ids`

The IDs of the tables involved in the statement.

#### `index_ids`

The IDs of the indexes involved in the statement.

#### `sql`

The SQL statements.

### Ways of locating questionable statements

Not all of the `SLOW_QUERY` statements are questionable. Only those whose `process_time` is very large will increase the pressure on the entire cluster. 

The statements whose `wait_time` is very large and `process_time` is very small are usually not questionable. They are blocked by the real questionable statements so that they have to wait in the execution queue and thus have a much longer response time.
