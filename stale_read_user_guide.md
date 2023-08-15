# A User's Guide to Stale Read and safe-ts in TiKV

## Introduction

This guide provides a comprehensive overview of Stale Read and safe-ts functionalities in TiKV and offers practical advice on diagnosing common issues related to these features.

## Background: The Role of Stale Read and safe-ts

Stale Read in TiKV relies on safe-ts. If a read request on a region peer has a read timestamp (ts) that is less than or equal to the region's safe-ts, it can safely read the data from the peer. This safety guarantee is achieved by ensuring that safe-ts is always less than or equal to resolved-ts.

## Decoding safe-ts and resolved-ts

### safe-ts: What Is It?

safe-ts is a timestamp maintained in every peer of a region that assures that all transactions with a timestamp less than this value have been applied locally, which enables local stale read.

### The Maintenance of safe-ts

Safe-ts is maintained by a module named `RegionReadProgress`. The region's leader maintains resolved-ts and periodically sends its resolved-ts and the minimum required apply index (which validates this resolved-ts) to the `RegionReadProgerss`es of all replicas, including itself, via the CheckLeader RPC.

When a peer applies any data, it updates the applied_index and checks if any pending resolved-ts can be validated to become the new safe-ts.

### Resolved-ts: What Is It?

Like safe-ts, resolved-ts is a timestamp that guarantees all transactions with a timestamp less than this value have been applied by the leader. It is different from safe-ts in that safe-ts is a per peer concept, while resolved-ts is only maintained by the leader. Followers can have a smaller apply index than the leader, so resolved-ts cannot be directly treated as safe-ts in followers.

### The Maintenance of Resolved-ts

Region leaders manage resolved-ts using a resolver. This resolver tracks locks in the LOCK CF(Column Family) by receiving change logs when Raft applies. When initialized, the resolver scans the entire region to track the locks.

## Diagnosing Issues with Stale Read

### Identifying Issues

In Grafana - TiDB dashboard - KV request row, there are panels showing the hit rate, OPS and traffic of stale read.

![img](/media/stale-read/metrics-hit-miss.png)

![img](/media/stale-read/metrics-ops.png)

![img](/media/stale-read/traffic.png)

The detailed explanation of these metrics can be found in [TiDB Monitoring Metrics](/grafana-tidb-dashboard.md#kv-request)

When stale read encounters problems, changes in these p may be noticeable. The most direct evidence is the WARN log from TiDB, which reports 'DataIsNotReady' along with the region id and `safe-ts` it encounters.

### Commonly Seen Causes

The most typical issues that can hinder the utilization of stale read include:

- Slow-committing ongoing transactions.
- Delays in the CheckLeader's information push from the leader to the follower.

### Using Grafana for Diagnosis

In the tikv-details dashboard, within the resolved-ts row, you can identify the region with the smallest resolved-ts and safe-ts in each TiKV. If these values lag significantly behind real-time, these regions' details should be checked via `tikv-ctl`.

### Using tikv-ctl for Diagnosis

`tikv-ctl` can provide up-to-date details of the resolver and `RegionReadProgress`. For details, check [tikv-control](/tikv-control.md#get-the-state-of-a-regions-regionreadprogress).

An example usage

```
./tikv-ctl --host 127.0.0.1:20160 get-region-read-progress -r 14 --log --min-start-ts 0
```

The output of this command might look like:

```
Region read progress:
    exist: true,
    safe_ts: 0,
    applied_index: 92,
    pending front item (oldest) ts: 0,
    pending front item (oldest) applied index: 0,
    pending back item (latest) ts: 0,
    pending back item (latest) applied index: 0,
    paused: false,
Resolver:
    exist: true,
    resolved_ts: 0,
    tracked index: 92,
    number of locks: 0,
    number of transactions: 0,
    stopped: false,
```

This information can help determine:

- Whether locks are blocking resolved-ts.
- Whether the apply index is too small, preventing safe-ts from being updated.
- If this is a follower peer, whether the leader is sending a sufficiently new resolved-ts.

## Troubleshooting Tips

### Handling Slowly Committing Transactions

Slowly committing transactions are often large transactions. Their prewrite phases leave some locks, but it takes too long before commit phases clean the locks. Try to identify the transactions to which the locks belong and determine why they exist (through logs, etc.)

Useful actions you can take

- Specify `--log` option in the tikv-ctl command, and check TiKV logs to find the specific locks with their start_ts.
- Search the start_ts in both TiDB and TiKV logs, see if anything is wrong with this transaction
    - If a query exceeds 60 seconds, an `Expensive query`  log will be printed. The log includes the SQL statement. You can use start_ts to match the log.
    - `[2023/07/17 19:32:09.403 +08:00] [WARN] [expensivequery.go:145] [expensive_query] [cost_time=60.025022732s] [cop_time=0.00346666s] [process_time=8.358409508s] [wait_time=0.013582596s] [request_count=278] [total_keys=9943616] [process_keys=9943360] [num_cop_tasks=278] [process_avg_time=0.030066221s] [process_p90_time=0.045296042s] [process_max_time=0.052828934s] [process_max_addr=192.168.31.244:20160] [wait_avg_time=0.000048858s] [wait_p90_time=0.00006057s] [wait_max_time=0.00040991s] [wait_max_addr=192.168.31.244:20160] [stats=t:442916666913587201] [conn=2826881778407440457] [user=root] [database=test] [table_ids="[100]"] [`**`txn_start_ts`**`=442916790435840001] [mem_max="2514229289 Bytes (2.34 GB)"] [sql="update t set b = b + 1"]`
- [CLUSTER_TIDB_TRX](https://docs.pingcap.com/tidb/dev/information-schema-tidb-trx#cluster_tidb_trx) table could be useful to find active transactions if logs can't tell us enough info about the locks.
- `show processlist` shows current active connections and their time spent on current command, but it doesn't show start_ts.

If the locks exist due to ongoing large transactions, you should consider modifying your application logic as these locks can hinder the progress of resolve-ts.

If the locks do not belong to any ongoing transactions, it might be due to a coordinator (TiDB) crashing after it prewrites the lock.. In this case, TiDB should automatically resolve the locks. No action is required unless you find that the problem persists and cannot recover.

### Addressing CheckLeader Issues

Check the network and the Check Leader Duration metrics in Grafana.

## An Example

On a Friday night you noticed the miss rate of stale read requests increases from TiDB metrics:

![img](/media/stale-read/example-ops.png)

So you checked the tikv-details - resolved-ts row (explanation of the metrics can be found in [Key Monitoring Metrics of TiKV](/grafana-tikv-dashboard.md#resolved-ts)),

![img](/media/stale-read/example-ts-gap.png)

You find region 3121 and some other regions don't advance their resolved-ts in time.

So you run `./tikv-ctl --host 127.0.0.1:20160 get-region-read-progress -r 3121 --log`to get more details.

The output is:

```
Region read progress:
    exist: true,
    safe_ts: 442918444145049601,
    applied_index: 2477,
    read_state.ts: 442918444145049601,
    read_state.apply_index: 1532,
    pending front item (oldest) ts: 0,
    pending front item (oldest) applied index: 0,
    pending back item (latest) ts: 0,
    pending back item (latest) applied index: 0,
    paused: false,
    discarding: false,
Resolver:
    exist: true,
    resolved_ts: 442918444145049601,
    tracked index: 2477,
    number of locks: 480000,
    number of transactions: 1,
    stopped: false,
```

Applied index equals tracked index in resolver, so the problem is in resolver. You noticed there is 1 transaction that leaves 480000 locks in this region. This might be the cause.

You checked TiKV log to find out the exact transaction and the keys of some of the locks. You greped "locks with" and got a match:

```
[2023/07/17 21:16:44.257 +08:00] [INFO] [resolver.rs:213] ["locks with the minimum start_ts in resolver"] [keys="[74800000000000006A5F7280000000000405F6, ... , 74800000000000006A5F72800000000000EFF6, 74800000000000006A5F7280000000000721D9, 74800000000000006A5F72800000000002F691]"] [start_ts=442918429687808001] [region_id=3121]
```

Now you know the transaction's start_ts. Grep the start_ts in TiDB's log, it gives you more info about the statement and transaction:

```
[2023/07/17 21:16:18.287 +08:00] [INFO] [2pc.go:685] ["[BIG_TXN]"] [session=2826881778407440457] ["key sample"=74800000000000006a5f728000000000000000] [size=319967171] [keys=10000000] [puts=10000000] [dels=0] [locks=0] [checks=0] [txnStartTS=442918429687808001]

[2023/07/17 21:16:22.703 +08:00] [WARN] [expensivequery.go:145] [expensive_query] [cost_time=60.047172498s] [cop_time=0.004575113s] [process_time=15.356963423s] [wait_time=0.017093811s] [request_count=397] [total_keys=20000398] [process_keys=10000000] [num_cop_tasks=397] [process_avg_time=0.038682527s] [process_p90_time=0.082608262s] [process_max_time=0.116321331s] [process_max_addr=192.168.31.244:20160] [wait_avg_time=0.000043057s] [wait_p90_time=0.00004007s] [wait_max_time=0.00075014s] [wait_max_addr=192.168.31.244:20160] [stats=t:442918428521267201] [conn=2826881778407440457] [user=root] [database=test] [table_ids="[106]"] [txn_start_ts=442918429687808001] [mem_max="2513773983 Bytes (2.34 GB)"] [sql="update t set b = b + 1"]
```

Now you basically located the statement that caused the problem. You further checked it by `show processlist`:

```
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
| Id                  | User | Host                | db     | Command | Time | State      | Info                      |
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
| 2826881778407440457 | root | 192.168.31.43:58641 | test   | Query   | 48   | autocommit | update t set b = b + 1    |
| 2826881778407440613 | root | 127.0.0.1:45952     | test   | Execute | 0    | autocommit | select * from t where a=? |
| 2826881778407440619 | root | 192.168.31.43:60428 | <null> | Query   | 0    | autocommit | show processlist          |
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
```

Someone is executing the unexpected `UPDATE` statement, which results in a large transaction and hinders stale read.

You found out the reason, stopped the application running this statement and saved your weekend.