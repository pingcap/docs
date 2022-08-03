# TiDB Latency Formula

This document breaks down the latency into metrics, for those who have interests in observation of the metrics, it's a guide of TiDB's critical path diagnosis.

Generally, OLTP workload can be divided into read and write queries, they share some critical code.
This document will break down the latency and then analyze it from user's perspective. It's better to read [Performance Analysis and Tuning](/performance-tuning-methods.md) before this document.
Note when breaking down latency through metrics in this document, we are calculating the average duration or latency instead of some specific slow queries.
Many metrics are collected as histogram, which is a distribution of the duration or latency, when calculating the average latency, you need to use the sum and count counter.

```
avg = ${metric_name}_sum / ${metric_name}_count
```

Metrics in this document can be read directly from prometheus of TiDB.

## General SQL Layer

This part of latency is on the top level of TiDB and shared by any queries.

```
e2e duration =
    tidb_server_get_token_duration_seconds +
    tidb_session_parse_duration_seconds +
    tidb_session_compile_duration_seconds +
    tidb_session_execute_duration_seconds{type="general"}
```

`tidb_server_get_token_duration_seconds` should be small enough to be ignored, usually less than 1 microsecond.

`tidb_session_parse_duration_seconds` records the duration pf parsing sql query text to AST, which can be skipped by `prepare/execute` statements.

`tidb_session_compile_duration_seconds` records the duration of compiling AST to physical plan, which can be skipped by [plan cache](/sql-prepared-plan-cache.md).

`tidb_session_execute_duration_seconds{type="general"}` records the duration of executing duration, which mixes all types of user queries. It need to be broken down into fine-grained durations for analyzing performance issue or bottlenecks.

Now we start dividing read and write queries, they are executed in kind of different ways.

## Read Queries

We start from read queries, which is processed in a single form.

### Point Get

```
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handle duration +
    read value duration
```

`pd_client_cmd_handle_cmds_duration_seconds{type="wait"}` records the duration of fetching TSO from PD, it will be skipped with in-txn snapshot read or reading with clustered primary index.

```
read handle duration = read value duration =
    tidb_tikvclient_txn_cmd_duration_seconds{type="get"} =
    send request duration =
    tidb_tikvclient_request_seconds{type="Get"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_get"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

Get requests are sent directly to TiKV via a batched gRPC wrapper. The detail is in [batch client section](#batch-client).

```
tikv_grpc_msg_duration_seconds{type="kv_get"} =
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    tikv_engine_seek_micro_seconds{type="seek_max"} +
    read value duration +
    read value duration
```

Now the requests are in TiKV. TiKV process get request by a seek and 1-2 read actions(short value are encoded in write column family, one time of reading is enough). Before processing read request, TiKV will get a snapshot, see [TiKV Snapshot secion](#tikv-snapshot).

```
read value duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="get/batch_get_command"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="get/batch_get_command"}))
```

TiKV uses RocksDB as its storage engine, when the required value is missing in block cache, it need to load value from disk. Get request can be either `get` or `batch_get_command`.

### Batch Point Get

```
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handles duration +
    read values duration
```

Batch point get read multi values in the same time, besides, the process is almost same with point get.

```
read handles duration = read values duration =
    tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"} =
    send request duration =
    tidb_tikvclient_request_seconds{type="BatchGet"} =
    tidb_tikvclient_batch_wait_duration(tranasction) +
    tidb_tikvclient_batch_send_latency(tranasction) +
    tikv_grpc_msg_duration_seconds{type="kv_get"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}(tranasction)
```

The durations in batch client are explained in [batch client section](#batch-client).

```
tikv_grpc_msg_duration_seconds{type="kv_batch_get"} =
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    n * (
        tikv_engine_seek_micro_seconds{type="seek_max"} +
        read value duration +
        read value duration
    )

read value duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="batch_get"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="batch_get"}))
```

After [getting snapshot](#tikv-snapshot), TiKV read multi values from the same snapshot. The read duration is same with point get.
When loading data from disk, the average duration can be calculated by `tikv_storage_rocksdb_perf` with `req="batch_get"`.

### Table Scan & Index Scan

```
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    n * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    )
    tidb_distsql_handle_query_duration_seconds{sql_type="general"} <= send request duration
```

Table scan and index scan are processed in the same way. `n` is the distributed task count.
Because coprocessor execution and data responsing to client are in different threads, `tidb_distsql_handle_query_duration_seconds{sql_type="general"}` is the wait time and it's less than the send request duration.

```
send request duration =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="coprocessor"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}

tikv_grpc_msg_duration_seconds{type="coprocessor"} =
    tikv_coprocessor_request_wait_seconds{type="snapshot"} +
    tikv_coprocessor_request_wait_seconds{type="schedule"} +
    tikv_coprocessor_request_handler_build_seconds{type="index/select"} +
    tikv_coprocessor_request_handle_seconds{type="index/select"}
```

In TiKV, table scan is the type `select` and index scan is the type `index`, the duration details are same.

### Index Look Up

```
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    n * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    ) +
    m * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    )
```

Index look up combines index scan and table scan, they are processed in a pipelined way.

## Write Queries

Write queries are much more complex, there are some variants.

|| Pessimistic Txn | Optimistic Txn |
|-|-|-|
| Auto-commit | execute + lock + commit | execute + commit |
| Non auto-commit | execute + lock | execute |

We divide the write into 3 phases:

- execute phase, execute and write mutation into the memory of TiDB.
- lock phase, acquire pessimistic locks for the execution result.
- commit phase, commit the transaction via 2PC protocol.

In execution phase, TiDB manipulate data in memory, the main latency comes from reading the required data.
Like update and delete, TiDB read data from TiKV first, then update or delete the row in-mem.

The exception is cursor operations(`select for update`), cursor operation with point get and batch point get, which performs read and lock in a single RPC.

### Cursor Point Get

```
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    2 * tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

Cursor point get locks key with value returned, compare with lock phase after execution, this save 1 round RPC. The duration of cursor point get can be treat same as lock duration.

### Cursor Batch Point Get

```
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"} +
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

Cursor batch point get executes similar to cursor point get, but read multiple values in a single RPC.
The details of `tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"}` can be found in [batch point get section](#batch-point-get).

### Lock

This section describes the lock duration.

```
ratio = [
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_pessimistic_lock"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_pessimistic_lock"})) /
    128
] + 1

lock = tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"} =
    ratio * tidb_tikvclient_request_seconds{type="PessimisticLock"}
```

Locks are acquired through the 2PC struct, which has a flow control mechanism. The flow control limit the concurrent on-fly requests, the default value is `128`. For simplicity, the flow control can be treat as an amplification of request latency(`ratio`).

```
tidb_tikvclient_request_seconds{type="PessimisticLock"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

The detail of batch client is in [batch client section](#batch-client).

```
tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} =
    tikv_scheduler_latch_wait_duration_seconds{type="acquire_pessimistic_lock"} +
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    (lock in-mem key count + lock on-disk key count) * lock read duration +
    lock on-disk key count / (lock in-mem key count + lock on-disk key count) *
    lock write duration
```

From 6.0, TiKV uses [in-mem pessimisitc lock](/pessimistic-transaction.md#in-memory-pessimistic-lock) by default. In-mem pessimistic lock bypass the async write process.
The snapshot duration is explained in [TiKV Snapshot section](#tikv-snapshot).
`lock write duration` is the duration of writing on-disk lock, which is explained in the [Async Write section](#async-write).

```
lock in-mem key count =
    sum(rate(tikv_in_memory_pessimistic_locking{result="success"})) /
    sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))

lock on-disk key count =
    sum(rate(tikv_in_memory_pessimistic_locking{result="full"})) /
    sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))
```

The count of in-mem and on-disk locked keys can be calculated by in-mem lock counter.

```
lock read duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="acquire_pessimistic_lock"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="acquire_pessimistic_lock"}))
```

TiKV reads the value of the keys before acquiring the locks, the read duration can be calculated by RocksDB perf context.

### Commit

```
commit =
    Get_latest_ts_time +
    Prewrite_time +
    Get_commit_ts_time +
    Commit_time

Get_latest_ts_time = Get_commit_ts_time =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"}

prewrite_ratio = [
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_prewrite"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_prewrite"})) /
    128
] + 1

commit_ratio = [
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_commit"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_commit"})) /
    128
] + 1

Prewrite_time =
    prewrite_ratio * tidb_tikvclient_request_seconds{type="Prewrite"}

Commit_time =
    commit_ratio * tidb_tikvclient_request_seconds{type="Commit"}
```

The commit duration can be broken down as for sections:

- `Get_latest_ts_time` records the duration of get latest TSO in async-commit or 1PC transaction.
- `Prewrite_time` records the duration of prewrite phase.
- `Get_commit_ts_time` records the duration of common 2PC transaction.
- `Commit_time` records the duration of commit phase, async-commit or 1PC transaction does not have this phase.

Like pessimistic lock, flow control acts as an amplification of latency(`prewrite_ratio` and `commit_ratio`).

```
tidb_tikvclient_request_seconds{type="Prewrite"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_prewrite"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}

tidb_tikvclient_request_seconds{type="Commit"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_commit"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

The detail of batch client is in [batch client section](#batch-client).

```
tikv_grpc_msg_duration_seconds{type="kv_prewrite"} =
    prewrite key count * prewrite read duration +
    prewrite write duration

prewrite key count =
    sum(rate(tikv_scheduler_kv_command_key_write_sum{type="prewrite"})) /
    sum(rate(tikv_scheduler_kv_command_key_write_count{type="prewrite"}))

prewrite read duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="prewrite"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="prewrite"}))
```

Like lock in TiKV, prewrite is processed in read and write 2 phases. The read duration can be calculated from RocksDB perf context.
The write duration is explained in [async write](#async-write).

```
tikv_grpc_msg_duration_seconds{type="kv_commit"} =
    commit key count * commit read duration +
    commit write duration

commit key count =
    sum(rate(tikv_scheduler_kv_command_key_write_sum{type="commit"})) /
    sum(rate(tikv_scheduler_kv_command_key_write_count{type="commit"}))

commit read duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="commit"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="commit"})) (storage)
```

The duration of commit is almost same as prewrite, also the write duration is explained in [async write](#async-write).

### Async Write

```
async write duration(async io disabled) =
    propose +
    async io disabled commit +
    tikv_raftstore_apply_wait_time_duration_secs +
    tikv_raftstore_apply_log_duration_seconds

async write duration(async io enabled) =
    propose +
    async io enabled commit +
    tikv_raftstore_apply_wait_time_duration_secs +
    tikv_raftstore_apply_log_duration_seconds
```

Async write can be broken down into 3 phases:

- Propose
- Commit
- Apply(`tikv_raftstore_apply_wait_time_duration_secs + tikv_raftstore_apply_log_duration_seconds`)

```
propose =
    propose wait duration +
    propose duration

propose wait duration =
    tikv_raftstore_store_wf_batch_wait_duration_seconds

propose duration =
    tikv_raftstore_store_wf_send_to_queue_duration_seconds -
    tikv_raftstore_store_wf_batch_wait_duration_seconds
```

The Raft process is recorded in a waterfall manner. So the propose duration is calculated from the diff of 2 metrics.

```
async io disabled commit = max(
    persist log locally duration,
    replicate log duration
)

async io enabled commit = max(
    wait by write worker duration,
    replicate log duration
)
```

TiKV supports Async IO Raft since v5.3.0, which changes the process of commit.

```
persist log locally duration =
    batch wait duration +
    write to raft db duration

batch wait duration =
    tikv_raftstore_store_wf_before_write_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds

write to raft db duration =
    tikv_raftstore_store_wf_write_end_duration_seconds -
    tikv_raftstore_store_wf_before_write_duration_seconds

wait by write worker duration =
    tikv_raftstore_store_wf_persist_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds
```

The difference between with Async IO or not is the duration of persisting log locally,
with Async IO, the duration of persisting log locally can be calculated from the waterfall metrics directly(skip wait duration).

```
replicate log duration =
    raftmsg send wait duration +
    commit log wait duration

raftmsg send wait duration =
    tikv_raftstore_store_wf_send_proposal_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds

commit log wait duration =
    tikv_raftstore_store_wf_commit_log_duration -
    tikv_raftstore_store_wf_send_proposal_duration_seconds
```

The replicate log duration records the duration of log persisted in quorum peers,
which contains an RPC duration and the duration of log persisting in majority.

### Raft DB

```
write to raft db duration = raft db write duration
commit log wait duration >= raft db write duration

raft db write duration(raft engine enabled) =
    raft_engine_write_preprocess_duration_seconds +
    raft_engine_write_leader_duration_seconds +
    raft_engine_write_apply_duration_seconds

raft db write duration(raft engine disabled) =
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_thread_wait"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_scheduling_flushes_compactions_time"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_wal_time"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_memtable_time"}
```

Because `commit log wait duration` is the slowest duration of quorum peers, it may be larger than `raft db write duration`.

From v6.1.0, TiKV uses [Raft Engine](/tikv-configuration-file.md#raft-engine) as its default log storage engine, which changes the process of writing log.

### KV DB

```
tikv_raftstore_apply_log_duration_seconds =
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_thread_wait"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_scheduling_flushes_compactions_time"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_wal_time"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_memtable_time"}
```

In the async write process, committed log need to be applied into KV DB, the duration of apply can be calculated from the RocksDB perf context.

## TiKV Snapshot

```
tikv_storage_engine_async_request_duration_seconds{type="snapshot"} =
    tikv_coprocessor_request_wait_seconds{type="snapshot"} =
    tikv_raftstore_request_wait_time_duration_secs +
    tikv_raftstore_commit_log_duration_seconds +
    get snapshot from rocksdb duration
```

When leader lease is expired, TiKV will propose a read index command before getting a snapshot from rocksdb.
`tikv_raftstore_request_wait_time_duration_secs` and `tikv_raftstore_commit_log_duration_seconds` are the duration of committing read index command.

Getting snapshot from rocksdb duration is usually a fast operation, so we do not record such duration.

## Batch Client

```
tidb_tikvclient_request_seconds{type="?"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_?"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

- `tidb_tikvclient_batch_wait_duration` records the waiting duration in the batch system.
- `tidb_tikvclient_batch_send_latency` records the encode duration in the batch system.
- `tikv_grpc_msg_duration_seconds{type="kv_?"}` is TiKV processing duration.
- `tidb_tikvclient_rpc_net_latency_seconds` records the network latency.

## Diagnosis

We've explained the details of query duration above. This section will describe the duration analysis of real use cases.

It would be hard for users to engage in the duration break down since they may not know where to start. So we analyze this problem from two obvious appearance, the system is slow at read queries or write queries, which can be checked by the DB time panel in performance overview dashboard.

### Slow Read Queries

If select statements account for a significant portion of the DB time, we can assume that the DB is slow at read queries.

It's good to know the execute plan of your read queries when diagnosing with slow read queries. You can find the plan from [SQL statements panel](/dashboard/dashboard-overview.md#top-sql-statements) in TiDB dashboard.
For [point get](#point-get), [batch point get](#batch-point-get) and some [simple coprocessor queries](#table-scan--index-scan), go on analyze the duration as the description above.

### Slow Write Queries

Before investigating slow writes, you need to troubleshoot the cause of the conflict. Check `tikv_scheduler_latch_wait_duration_seconds_sum{type="acquire_pessimistic_lock"} by (instance)`.

- If this metric is high in some specific TiKV instances, there may be some conflict hot regions.
- If this metric is high across all instances, there may be conflict in the application.

After investigating the conflict and make sure it's reasonable, you can goon analyzing the duration of [lock](#lock) and [commit](#commit).
