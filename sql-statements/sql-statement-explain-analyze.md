---
title: EXPLAIN ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN ANALYZE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-explain-analyze/','/docs/dev/reference/sql/statements/explain-analyze/']
---

# EXPLAIN ANALYZE

The `EXPLAIN ANALYZE` statement works similar to `EXPLAIN`, with the major difference being that it will actually execute the statement. This allows you to compare the estimates used as part of query planning to actual values encountered during execution.  If the estimates differ significantly from the actual values, you should consider running `ANALYZE TABLE` on the affected tables.

> **Note:**
>
> When you use `EXPLAIN ANALYZE` to execute DML statements, modification to data is normally executed. Currently, the execution plan for DML statements **cannot** be shown yet.

## Synopsis

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## EXPLAIN ANALYZE output format

Different from `EXPLAIN`, `EXPLAIN ANALYZE` executes the corresponding SQL statement, records its runtime information, and returns the information together with the execution plan. Therefore, you can regard `EXPLAIN ANALYZE` as an extension of the `EXPLAIN` statement. Compared to `EXPLAIN`, the return results of `EXPLAIN ANALYZE` include columns of information such as `actRows`, `execution info`, `memory`, and `disk`. The details of these columns are shown as follows:

| attribute name          | description |
|:----------------|:---------------------------------|
| actRows       | Number of rows output by the operator. |
| execution info  | Execution information of the operator. `time` represents the total `wall time` from entering the operator to leaving the operator, including the total execution time of all sub-operators. If the operator is called many times by the parent operator (in loops), then the time refers to the accumulated time. `loops` is the number of times the current operator is called by the parent operator. |
| memory  | Memory space occupied by the operator. |
| disk  | Disk space occupied by the operator. |

## Examples

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object | execution info                                                 | operator info | memory | disk |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:t1      | time:757.205µs, loops:2, Get:{num_rpc:1, total_time:697.051µs} | handle:1      | N/A    | N/A  |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1;
```

```sql
+-------------------+---------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| id                | estRows | actRows | task      | access object | execution info                                                                                                                                                                                                  | operator info                  | memory    | disk |
+-------------------+---------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| TableReader_5     | 13.00   | 13      | root      |               | time:923.459µs, loops:2, cop_task: {num: 4, max: 839.788µs, min: 779.374µs, avg: 810.926µs, p95: 839.788µs, max_proc_keys: 12, p95_proc_keys: 12, rpc_num: 4, rpc_time: 3.116964ms, copr_cache_hit_ratio: 0.00} | data:TableFullScan_4           | 632 Bytes | N/A  |
| └─TableFullScan_4 | 13.00   | 13      | cop[tikv] | table:t1      | proc max:0s, min:0s, p80:0s, p95:0s, iters:4, tasks:4                                                                                                                                                           | keep order:false, stats:pseudo | N/A       | N/A  |
+-------------------+---------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## Operator Execution info

In addition to basic `time` and `loop` execution information, ʻexecution info` also contains operator-specific execution information, which mainly includes the time-consuming information of the operator sending RPC and other steps.

### Point_Get

The execution information from a `Point_Get` operator will typically contain the following:

- `Get:{num_rpc:1, total_time:697.051µs}`: The number of RPC requests (`num_rpc`) of type `Get` sent to TiKV and the total time-consuming(`total_time`) of all RPC requests.
- `ResolveLock:{num_rpc:1, total_time:12.117495ms}`: When reading data encounters a lock, TiDB has to resolve lock first before reading data. Generally, it will appear in the scene of read-write conflict.
- `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}`: When an RPC request fails, TiDB will wait the backoff time before retrying. Backoff statistics include the type of backoff (such as `regionMiss`, `tikvRPC`), the total time waiting (`total_time`) and the total number of backoffs (`num`).

### Batch_Point_Get

The execution information of the `Batch_Point_Get` operator is similar to the `Point_Get` operator, but `Batch_Point_Get` generally sends `BatchGet` RPC requests to TiKV to read the data.

- `BatchGet:{num_rpc:2, total_time:83.13µs}`: The number of RPC requests (`num_rpc`) of type `BatchGet` sent to TiKV and the total time-consuming (`total_time`) of all RPC requests.

### TableReader

The execution information from a `TableReader` operator will typically contain the following:

```
cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 6, rpc_time: 5.313996 ms, copr_cache_hit_ratio: 0.00}
```

- `cop_task`: Contains the information about executing cop task, such as:
     - `num`: the number of cop tasks
     - `max`, `min`, `avg`, `p95`: the maximum, minimum, average and P95 value of the execution time-consuming of executing cop tasks.
     - `max_proc_keys`, `p95_proc_keys`: The maximum, P95 value of tikv scan key/value in all cop tasks. If the difference between max and p95 is large, the data distribution may be not balanced.
     - `rpc_num`, `rpc_time`: The total number and total time-consuming of `Cop` RPC requests sent to TiKV.
     - `copr_cache_hit_ratio`: Coprocessor Cache cache hit rate requested by cop task. [Coprocessor Cache Configuration](/tidb-configuration-file.md).
- `backoff`: Contains different types of backoff and total backoff waiting time.

### Insert

The `Insert` operator may contain the following execution information:

```
prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs }}}
```

- `prepare`: Time-consuming of preparing to write, including expression, default value and auto-increment value calculations.
- `check_insert`: This information generally appears in ʻinsert ignore` and ʻinsert on duplicate` statements, it including conflict checking and time-consuming writing to TiDB transaction cache. Note that this time-consuming does not include the time-consuming of transaction commit. It contains the following information:
    - `total_time`: the total time spent in the `check_insert` step.
    - `mem_insert_time`: The time-consuming of writing data to the TiDB transaction cache.
    - `prefetch`: The time-consumed retrieving data that needs to be checked for conflicts from TiKV. This step is mainly to send a `Batch_Get` RPC request to TiKV to retrieve data.
    - `rpc`: The total time-consuming of sending RPC requests to TiKV, which generally includes two types of RPC time, `BatchGet` and `Get`, among which:
        - `BatchGet` RPC request is sent by the `prefetch` step.
        - `Get` RPC request is sent by `insert on duplicate` statement when executing `duplicate update` step.
- `backoff`: Contains different types of backoff and total backoff waiting time.

### IndexJoin

The `IndexJoin` operator has 1 outer worker and N inner workers to executed in parallel. The join result preserves the order of the outer table and support batch lookup. The specific execution process is as follows:

1. The outer worker reads N outer rows, builds a task and sends it to the result channel and inner worker channel.
2. The inner worker receives the task, builds key ranges from outer rows, and fetch inner rows. It then builds the inner row hash map.
3. The main thread receives the task, waits for the inner worker to finish handling the task.
4. The main thread joins each outer row by look up to the inner rows hash map.

The `IndexJoin` operator contains the following execution information:

```
inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms
```

- `Inner`: the execution information of inner worker:
    - `total`: the total time-consuming by the inner worker.
    - `concurrency`: the number of parallel execution inner workers.
    - `task`: The total number of tasks processed by the inner worker.
    - `construct`: the preparation time before the inner worker reads the inner table rows corresponding to the task.
    - `fetch`: The total time-consuming it takes for inner worker to read inner table rows.
    - `Build`: The total time-consuming it takes for inner worker to construct the hash map of the corresponding inner table rows.
- `probe`: the total time consumed by the main thread of `IndexJoin` to do join with the outer table rows and the hash map of inner table rows.

### IndexHashJoin

The execution process of the `IndexHashJoin` operator is similar to the `IndexJoin` operator. `IndexHashJoin` operator also has 1 outer worker and N inner workers to executed in parallel, but the output order is not promised. The specific execution process is as follows:

1. The outer worker reads N outer rows, builds a task and sends it to the
inner worker channel.
2. The inner worker receives the tasks and does 3 things for every task:
   a. builds hash table from the outer rows
   b. builds key ranges from outer rows and fetches inner rows
   c. probes the hash table and sends the join result to the result channel.
   Note: step a and step b are running concurrently.
3. The main thread of ʻIndexHashJoin`  receives the join results from the result channel.

The `IndexHashJoin` operator contains the following execution information:

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

- `Inner`: the execution information of inner worker:
    - `total`: the total time-consuming by the inner worker.
    - `concurrency`: the number of inner workers.
    - `task`: The total number of tasks processed by the inner worker.
    - `construct`: the prepare time before the inner worker reads the inner table rows.
    - `fetch`: The total time-consuming of inner worker to read inner table rows.
    - `Build`: The total time-consuming of inner worker to construct the hash map of the outer table rows.
    - `join`:  The total time-consuming of inner worker to do join with the inner table rows and the hash map of outer table rows.

### HashJoin

The `HashJoin` operator has an inner worker, an outer worker and N join workers. The specific execution process is as follows:

1. The inner worker reads inner table rows and constructs a hash map.
2. The outer worker reads the outer table rows, then wraps it into a task and sends it to the join worker.
3. Wait for the completion of the hash map construction in step 1.
4. The join worker uses the outer table rows and hash map in the task to do join, and then sends the join result to the result channel.
5. The main thread of `HashJoin` receives the join result from the result channel.

The `HashJoin` operator contains the following execution information:

```
build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}
```

- `build_hash_table`: Read the data of the inner table and construct the execution information of the hash map:
    - `total`: total time spent.
    - `fetch`: The total time spent reading inner table data.
    - `build`: The total time spent constructing a hash map.
- `probe`: execution information of join worker:
    - `concurrency`: the number of join workers.
    - `total`: the total time consumed by all join workers.
    - `max`: The maximum time for a single join worker to execute.
    - `probe`: The total time consumed for joining with outer table rows and hash map.
    - `fetch`: The total time that the join worker waits to read the outer table rows data.

## Other execution info

### lock_keys execution information

When executing a DML statement in a pessimistic transaction, the execution information of the operator may also include the execution information of `lock_keys`, an example is as follows:

```
lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}
```

- `time`: The total time to execute the `lock_keys` operation.
- `region`: The number of regions involved in executing the `lock_keys` operation.
- `keys`: The number of `Key` that need `Lock`.
- `lock_rpc`: The total time spent sending a RPC of type `Lock` to TiKV. Because multiple RPC requests can be sent in parallel, the total RPC time-consuming may be greater than the total time-consuming `lock_keys` operation.
- `rpc_count`: The total number of RPCs of `Lock` type sent to TiKV.

### commit_txn execution information

When executing a write-type DML statement in a transaction with `autocommit=1`, the execution information of the write operator will also include the time-consuming information of the transaction commit. For example:

```
commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}
```

- `prewrite`: The time-consuming of the `prewrite` phase of the 2PC commit of the transaction.
- `wait_prewrite_binlog:`: The time-consuming of waiting to write the prewrite Binlog.
- `get_commit_ts`: The time-consuming of getting the transaction commit timestamp.
- `commit`: The time-consuming in the `commit` phase during the 2PC commit of the transaction.
- `write_keys`: The total `keys` written in the transaction.
- `write_byte`: The total bytes of `key/value` writtten in the transaction, the unit is byte.

## MySQL compatibility

`EXPLAIN ANALYZE` is a feature of MySQL 8.0, but both the output format and the potential execution plans in TiDB differ substantially from MySQL.

## See also

* [Understanding the Query Execution Plan](/explain-overview.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
