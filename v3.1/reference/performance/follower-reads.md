---
title: Follower Reads
summary: This document describes the use and implementation of Follower Reads.
category: reference
---

# Follower Reads

When you read the Region with hot data in the system, resources of the machine where the Region leader is become fully occupied,causing read bottlenecks. In this situation, enabling follower reads can significantly reduce the load of the leader, and improve the throughput of the whole system by balancing the load among multiple followers. This document introduces the use and implementation mechanism of follower reads.

## Overview

Follower reads refers to the use of the follower of a Region to carry out data reading under the premise of strongly consistency read, to improve the throughput of the TiDB cluster and reduce the load of the leader. Follower reads contains a series of load balancing mechanisms that offload TiKV read loads from the leader of a Region to the follower. The implementation of TiKV's follower reads ensures the linearizability of reading a single row of data, and provides strongly consistent read for users combined with the transaction isolation level in TiDB.

> **Note:**
>
> To achieve strongly consistent read, in the current implementation, the follower incurs additional `ReadIndex` overhead. Therefore, for now, the main benefits of follower reads are to isolate read and write requests of the cluster and to increase overall read throughput. Regarding the latency of a single request, the interaction overhead with `ReadIndex` of the Raft protocol is one more time than the traditional leader reads.

## Usage

To enable TiDB's follower reads, set the value of the session variable `tidb_replica_read` to `follower`:

{{<copyable "sql">}}

```sql
set @@tidb_replica_read = 'follower';
```

Scope: SESSION

Default: leader

This variable is used to set how the current session expects the data to be read：

- When the value of `tidb_replica_read` is set to `leader` or an empty string, TiDB maintains its original behavior and sends all read operations to the leader to perform.
- When the value of `tidb_replica_read` is set to `follower`, TiDB selects a follower of the Region to perform all read operations.

## Implementation mechanism

Before follower reads was introduced, TiDB applied the strong leader policy and submitted all read and write operations to the leader of a Region to complete. Although TiKV can spread Regions evenly on multiple physical nodes, for each Region, only the leader can provide external services, and the other two followers can do nothing to handle read requests but receive the data replicated from the leader and vote to elect a leader in case of a failover.

In order to allow data reading in the follower without violating linearizability or affecting the transaction isolation level (Snapshot Isolation), the follower needs to use `ReadIndex` of the Raft protocol, to ensure that the read request can read the latest data that has been committed on the leader. At the TiDB level, follower reads simply sends read requests to a Region to the follower based on the load balancing policy.

### Strongly consistent read

When the follower processes read requests, it first uses `ReadIndex` of the Raft protocol to interact with the leader of the Region, to obtain the latest commit index of the current Raft group. After the latest commit index of the leader is applied locally to the follower, the processing of read requests starts.

### Follower selection strategy

Because follower reads guarantees linearizability without affecting the transaction isolation level, TiDB can apply Round Robin strategy for selecting the follower. Although TiKV can select any follower to handle any read request, considering the different replication speed among followers, if the load balancing granularity is too fine, it may cause significant fluctuation of latency. Currently, the granularity of the load balancing policy of follower reads is at the connection level. For a TiDB client connected to a specific Region, the selected follower is fixed, and is switched only when it fails or the scheduling policy is adjusted.