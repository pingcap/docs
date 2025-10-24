---
title: Follower Read
summary: This document describes the use and implementation of Follower Read.
---

# Follower Read

In TiDB, to ensure high availability and data security, TiKV stores multiple replicas for each Region, one of which is the leader and the others are followers. By default, all read and write requests are processed by the leader. The Follower Read feature allows reading data from the follower replicas of a Region while maintaining strong consistency, thereby distributing the read pressure on the leader and improving the overall read throughput of the cluster.

When performing Follower Read, TiDB selects the appropriate replica based on the topology information. Specifically, TiDB uses the `zone` label to determine whether a replica is a local replica: when the `zone` label of TiDB is the same as that of the target TiKV, TiDB considers the replica as a local replica. For more information, see [Schedule replicas by topology labels](schedule-replicas-by-topology-labels.md).

By allowing followers to participate in data reading, Follower Read can achieve the following goals:

- Distribute read hotspots and reduce leader load.
- In multi-AZ or multi-datacenter deployments, prioritize reading local replicas to reduce cross-region traffic.

## Applicable scenarios

Follower Read is suitable for the following scenarios:

- Businesses with large read request volume and obvious read hotspots.
- Scenarios where it is desirable to prioritize reading local replicas in multi-AZ deployments to save bandwidth.
- In a read-write separation architecture, it is desirable to further improve the overall read performance of the cluster.

> **Note:**
>
> To ensure the strong consistency of the read results, Follower Read needs to communicate with the leader to confirm the current commit progress (by executing the Raft `ReadIndex` operation) before reading, which introduces an additional network interaction. Therefore, Follower Read is most effective when there are a large number of read requests or read-write isolation is required; however, the performance improvement may not be significant for low-latency single queries.

## Usage

To enable TiDB's Follower Read feature, set the value of the `tidb_replica_read` variable to the desired value:

{{< copyable "sql" >}}

```sql
set [session | global] tidb_replica_read = '<target_value>';
```

Scope: SESSION | GLOBAL

Default: leader

This variable is used to set the expected data read mode. From v8.5.4, this variable only takes effect on read-only SQL statements.

In scenarios where you need to save cross-region traffic by reading local replicas, the following configurations are recommended:

- The default value `leader` provides the best performance.
- `closest-adaptive` saves traffic as much as possible with minimal performance loss.
- `closest-replicas` can save network traffic to the greatest extent.

If you are currently using other configurations, refer to the following table to modify them to the recommended configurations:

| Configuration being used | Recommended configuration to modify to |
| ------------- | ------------- |
| `follower` | `closest-replicas` |
| `leader-and-follower` | `closest-replicas` |
| `prefer-leader` | `closest-adaptive` |
| `learner` | `closest-replicas` |

If you want to use a more precise read replica selection policy, refer to the complete list of optional configurations:

- When you set the value of `tidb_replica_read` to `leader` or an empty string, TiDB maintains its default behavior and sends all read operations to the leader replica to perform.
- When you set the value of `tidb_replica_read` to `follower`, TiDB selects a follower replica of the Region to perform read operations. If the Region has learner replicas, TiDB also considers them for reads with the same priority. If no available follower or learner replicas exist for the current Region, TiDB reads from the leader replica.
- When the value of `tidb_replica_read` is set to `leader-and-follower`, TiDB can select any replicas to perform read operations. In this mode, read requests are load balanced between the leader and follower.
- When the value of `tidb_replica_read` is set to `prefer-leader`, TiDB prefers to select the leader replica to perform read operations. If the leader replica is obviously slow in processing read operations (such as caused by disk or network performance jitter), TiDB will select other available follower replicas to perform read operations.
- When the value of `tidb_replica_read` is set to `closest-replicas`, TiDB prefers to select a replica in the same availability zone to perform read operations, which can be a leader or a follower. If there is no replica in the same availability zone, TiDB reads from the leader replica.
- When the value of `tidb_replica_read` is set to `closest-adaptive`:

    - If the estimated result of a read request is greater than or equal to the value of [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630), TiDB prefers to select a replica in the same availability zone for read operations. To avoid unbalanced distribution of read traffic across availability zones, TiDB dynamically detects the distribution of availability zones for all online TiDB and TiKV nodes. In each availability zone, the number of TiDB nodes whose `closest-adaptive` configuration takes effect is limited, which is always the same as the number of TiDB nodes in the availability zone with the fewest TiDB nodes, and the other TiDB nodes automatically read from the leader replica. For example, if TiDB nodes are distributed across 3 availability zones (A, B, and C), where A and B each contains 3 TiDB nodes and C contains only 2 TiDB nodes, the number of TiDB nodes whose `closest-adaptive` configuration takes effect in each availability zone is 2, and the other TiDB node in each of the A and B availability zones automatically selects the leader replica for read operations.
    - If the estimated result of a read request is less than the value of [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630), TiDB can only select the leader replica for read operations.

- When you set the value of `tidb_replica_read` to `learner`, TiDB reads data from the learner replica. If no learner replica is available for the current Region, TiDB reads from an available leader or follower replica.

<CustomContent platform="tidb">

> **Note:**
>
> When you set `tidb_replica_read` to `closest-replicas` or `closest-adaptive`, to ensure that replicas are distributed across availability zones according to the specified configuration, you need to configure `location-labels` for PD and set the correct `labels` for TiDB and TiKV according to [Schedule replicas by topology labels](/schedule-replicas-by-topology-labels.md). TiDB depends on the `zone` label to match TiKV nodes in the same availability zone, so you need to make sure that the `zone` label is included in the `location-labels` of PD and `zone` is included in the configuration of each TiDB and TiKV node. If your cluster is deployed using TiDB Operator, refer to [High availability of data](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data).
>
> For TiDB v7.5.0 and earlier versions:
>
> - If you set `tidb_replica_read` to `follower` and no follower or learner replicas are available, TiDB returns an error.
> - If you set `tidb_replica_read` to `learner` and no learner replicas are available, TiDB returns an error.

</CustomContent>

## Basic monitoring

By observing the [**TiDB** > **KV Request** > **Read Req Traffic** panel (new in v8.5.4)](/grafana-tidb-dashboard.md#kv-request), you can determine whether you need to use Follower Read and view the effect of saving traffic after enabling Follower Read.

## Implementation mechanism

Before the Follower Read feature was introduced, TiDB applied the strong leader principle and submitted all read and write requests to the leader node of a Region to handle. Although TiKV can distribute Regions evenly on multiple physical nodes, for each Region, only the leader can provide external services. The other followers could not handle read requests, and they only receive the data replicated from the leader at all times and prepare for voting to elect a leader in case of a failover.

Follower Read includes a series of load balancing mechanisms that offload TiKV read load from Region leader replicas to follower replicas. To allow data reading in the follower node without violating linearizability or affecting Snapshot Isolation in TiDB, the follower node needs to use `ReadIndex` of the Raft protocol to ensure that the read request can read the latest data that has been committed on the leader node. At the TiDB level, the Follower Read feature simply needs to send the read request of a Region to a follower replica based on the load balancing policy.

### Strongly consistent reads

When the follower node processes a read request, it first uses `ReadIndex` of the Raft protocol to interact with the leader node of the Region to obtain the latest commit index (read index) of the current Raft group. After the latest commit index of the leader node is applied locally to the follower, the processing of a read request starts.

![read-index-flow](/media/follower-read/read-index.png)

### Follower replica selection strategy

The Follower Read feature does not affect TiDB's Snapshot Isolation transaction isolation level. TiDB selects a replica for the first time based on the configuration of `tidb_replica_read`. From the second retry, TiDB will prioritize ensuring successful reading. Therefore, when the selected follower node is inaccessible or has other errors, it will switch to the leader for service.

#### `leader`

- Select the leader replica for reading, regardless of replica location.

#### `closest-replicas`

- When the replica in the same AZ as TiDB is the leader node, TiDB does not use Follower Read for it.
- When the replica in the same AZ as TiDB is a follower node, TiDB uses Follower Read for it.

#### `closest-adaptive`

- If the estimated return result is not large enough, use the `leader` policy and do not perform Follower Read.
- If the estimated return result is large enough, use the `closest-replicas` policy.

### Follower Read performance overhead

To ensure strong data consistency, Follower Read needs to perform a `ReadIndex` regardless of how much data is read, which inevitably consumes more TiKV CPU resources. Therefore, in small query scenarios (such as point queries), the performance loss of Follower Read is relatively more obvious. At the same time, because the traffic saved by local reading for small queries is limited, Follower Read is more recommended for large query or batch reading scenarios.
When `tidb_replica_read` is `closest-adaptive`, TiDB does not use Follower Read for small queries, so the extra overhead of TiKV CPU compared to the `leader` policy is generally within +10% in various workloads.
