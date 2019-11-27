---
title: PD Scheduling
summary: Learn best practice and strategy for PD scheduling.
category: reference
---

# PD Scheduling

This document details the principles and strategies of PD scheduling through common scenarios to facilitate your application. This document assumes that you have a basic understanding of TiDB, TiKV and PD with the following core concepts:

- [Leader/Follower/Learner](/dev/glossary.md#leaderfollowerlearner)
- [Operator](/dev/glossary.md#operator)
- [Operator Step](/dev/glossary.md#operator-step)
- [Pending/Down](/dev/glossary.md#pendingdown)
- [Region/Peer/Raft Group](/dev/glossary.md#regionpeerraft-group)
- [Region Split](/dev/glossary.md#region-split)
- [Scheduler](/dev/glossary.md#scheduler)
- [Store](/dev/glossary.md#store)

> **Note:**
>
> This document initially targets TiDB 3.0. Although some features are not supported in earlier versions (2.x), the underlying mechanisms are similar and this document can still be used as a reference.

## PD scheduling policies

This section introduces the principles and processes involved in the scheduling system.

### Scheduling process

The Scheduling process generally has three steps:

1. Collect information

    Each TiKV node periodically reports two types of heartbeats to PD:

    - `StoreHeartbeat`: contains the overall information of Stores, including disk capacity, available storage, and read/write traffic.
    - `RegionHeartbeat`: contains the overall information of Regions, including the range of each Region, peer distribution, peer status, data volume, and read/write traffic.

    PD collects and restores this information for scheduling decisions.

2. Generate Operators

    Different schedulers generate the Operators based on their own logic and requirements, with constraints such as:

     - Do not add Peers to a Store in abnormal states (disconnected, down, busy, out of space)
     - Do not balance Regions in abnormal states
     - Do not transfer a Leader to a Pending Peer
     - Do not remove a Leader directly
     - Do not break the physical isolation of various Region Peers
     - Do not violate constraints such as Label property

3. Execute Operators

    To execute the Operators, the general procedure is:
    1. The generated Operator first joins a queue managed by `OperatorController`.

    2. `OperatorController` takes the Operator out of the queue and executes it with a certain amount of concurrency based on the configuration. This step is to distribute each Operator Step to the corresponding Region Leader.

    3. The Operator is marked as "finish" or "timeout" and removed from the queue.

### Load balancing

Region primarily relies on `balance-leader` and `balance-region` schedulers to achieve load balance. Both schedulers target distributing Regions evenly across all Stores in the cluster but with separate focuses: `balance-leader` deals with Region Leader to balance incoming client requests, whereas `balance-region` concerns itself with each Region Peer to redistribute the pressure of storage and avoid exceptions like out of storage space.

`balance-leader` and `balance-region` share a similar scheduling process:

1. Rate Stores according to their availability of resources.
2. `balance-leader` or `balance-region` constantly transfer Leaders or Peers from Stores with high scores to those with low scores.

However, their rating methods are different. `balance-leader` uses the sum of all Region Sizes corresponding to Leaders in a Store, whereas the way of `balance-region` is relatively complicated. Depending on the specific storage capacity of each node, the rating method of `balance-region` might be:

- based on the amount of data when there is sufficient storage (to balance data distribution among nodes).
- based on the available storage when there is insufficient storage (to balance the storage availability on different nodes).
- based on the weighted sum of the two factors above when neither of the above situations applies.

Since different nodes might differ in performance, you can also set the weight of load balancing for different Stores. `leader-weight` and `region-weight` are used to control the Leader weight and Region weight respectively ("1" by default for both). For example, when the `leader-weight` of a Store is set to "2", the number of Leaders on the node is about twice as many as that of other nodes after the scheduling stabilizes. Similarly, when the `leader-weight` of a Store is set to "0.5", the number of Leaders on the node is about half as many as that of other nodes.

### Hot Regions scheduling

Use `hot-region-scheduler` for Hot Regions scheduling. Currently in TiDB 3.0, the process is performed as follows:

1. Count hot Regions by determining read/write traffic that exceeds a certain threshold for a certain period based on the information reported by Stores.

2. Redistribute these Regions in a similar way to load balancing.

For hot write Regions, `hot-region-scheduler` attempts to redistribute both Region Peers and Leaders; for hot read Regions, `hot-region-scheduler` only redistributes Region Leaders.

### Cluster topology awareness

Cluster topology awareness (zone/rack/host awareness) is having the knowledge of how data is distributed, which enables PD to distribute Region Peers as much as possible. This is how TiKV ensures high availability and disaster recovery. Because PD continuously scans all Regions in the background, when PD finds that the distribution of Regions is not optimal, it generates an Operator to replace Peers and redistribute Regions.

The component to check Region distribution is `replicaChecker`, which is similar to Scheduler except that it cannot be disabled. The `replicaChecker` schedules based on the the configuration of `location-labels`. For example, `[zone, rack, host]` defines a three-tier topology for a cluster. PD attempts to schedule Region Peers to different zones first, or to different racks when zones are insufficient (for example, 2 zones for 3 replicas), or to different hosts when racks are insufficient, and so on.

### Scale-down and failure recovery

Scale-down refers to the process when you take a Store offline and mark it as "offline" using a command. PD replicates the Regions on the offline node to other nodes by scheduling. Failure recovery applies when Stores failed and cannot be recovered. In this case, Regions with Peers distributed on the corresponding Store might lose replicas, which requires PD to replenish on other nodes.

The processes of Scale-down and failure recovery are basically the same.  `replicaChecker` finds a Region Peer in abnormal states, and then generates an Operator to replace the abnormal Peer with a new one on a healthy Store.

### Region merge

Region merge refers to the process of merging adjacent small Regions by scheduling. It serves to avoid unnecessary resource consumption by a large number of small or even empty Regions after data deletion. Region merge is performed by `mergeChecker`, which processes in a similar way to `replicaChecker`: PD continuously scans all Regions in the background, and generates an Operator when continuous small Regions are found.

## Query scheduling status

You can check the status of scheduling system through Metrics, pd-ctl and logs. This section briefly introduces the methods of Metrics and pd-ctl. Refer to [PD monitoring metrics](/dev/reference/key-monitoring-metrics/pd-dashboard.md) and [PD Control](/dev/reference/tools/pd-control.md) for details.

### Operator status

The **Grafana PD/Operator** page shows the statistics about Operators, among which:

- Schedule Operator Create: Operator creating information, such as the creating reason and the target scheduler
- Operator finish duration: execution time consumed by the Operator
- Operator Step duration: execution time consumed by the Operator Step

You can query Operators using pd-ctl with the following commands:

- `operator show`: queries all Operators generated in the current scheduling task
- `operator show [admin | leader | region]`: queries Operators by type

### Balance status

**Grafana PD/Statistics - Balance** page shows the statistics about load balancing, among which:

- Store Leader/Region score: score of each Store
- Store Leader/Region count: the number of Leaders/Regions in each Store
- Store available: available storage on each Store

You can use store commands of pd-ctl to query balance status of each Store.

### Hot Region status

The **Grafana PD/Statistics - hotspot** page shows the statistics about hot Regions, among which:

- Hot write Region’s leader/peer distribution: Leader/Peer distribution in hot write Regions
- Hot read Region’s leader distribution: Leader distribution in hot read Regions

You can also query the status of hotspots using pd-ctl with the following commands:

- `hot read`: queries hot read Regions
- `hot write`: queries hot write Regions
- `hot store`: queries the distribution of hot Regions by Store
- `region topread [limit]`: queries the Region with top read traffic
- `region topwrite [limit]`: queries the Region with top write traffic

### Region health

The **Grafana PD/Cluster/Region health** panel shows the statistics about Regions in abnormal states, include Pending Peer, Down Peer, Offline Peer and Regions with extra or few Peers.

You can query the list of Regions in abnormal conditions using pd-ctl with region check commands:

- `region check miss-peer`: queries Regions without enough Peers
- `region check extra-peer`: queries Regions with extra Peers
- `region check down-peer`: queries Regions with Down Peers
- `region check pending-peer`: queries Regions with Pending Peers

## Scheduling strategy control

You can use pd-ctl to adjust the scheduling strategy from the following three aspects. Refer to [PD Control](/dev/reference/tools/pd-control.md) for more details.

### Start-stop scheduler

pd-ctl supports dynamically creating and deleting Schedulers. You can use the following commands to control the scheduling behavior of PD:

- `scheduler show`: shows currently running Schedulers in the system
- `scheduler remove balance-leader-scheduler`: removes (disable) balance-leader-scheduler
- `scheduler add evict-leader-scheduler-1`: adds a scheduler to remove all Leaders in Store 1

### Add Operators manually

Pd also supports creating or removing Operators directly through pd-ctl. For example:

- `operator add add-peer 2 5`: adds Peers to Region 2 in Store 5
- `operator add transfer-leader 2 5`: migrates Region 2 Leader to Store 5
- `operator add split-region 2`: splits Region 2 into two Regions evenly in size
- `operator remove 2`: removes currently pending Operator in Region 2

### Adjust scheduling parameter

You can check the scheduling configuration using the `config show` command in pd-ctl, and adjust the values using `config set {key} {value}`. Common adjustments include:

- `leader-schedule-limit`: controls the concurrency of Transfer Leader scheduling
- `region-schedule-limit`: controls the concurrency of adding/deleting Peer scheduling
- `disable-replace-offline-replica`: determines whether to disable the scheduling to take nodes offline
- `disable-location-replacement`: determines whether to disable the scheduling that handles the isolation level of Regions
- `max-snapshot-count`: controls the maximum concurrency of sent/received Snapshots for each Store

## PD scheduling in common scenarios

This section illustrates the best practices of PD scheduling strategies through several typical scenarios.

### Leader/Region are not evenly balanced

The rating mechanism of PD determines that Leader Count and Region Count of different Stores cannot fully reflect the load balancing status. Therefore, it is necessary to confirm whether there is load imbalancing from the actual load of TiKV or Storage usage.

Once you have confirmed that Leader/Region is not evenly distributed, you need to check the rating of different Stores.

If the scores of different Stores are close, it means PD mistakenly believes that Leader/Region is evenly distributed. Possible reasons are:

- There are hot Regions that cause load imbalancing. In this case, you need to analyze further based on [hot Regions scheduling](#hot-regions-are-not-evenly-distributed).
- There are a large number of empty Regions or small Regions, which leads to a great difference in the number of Leaders in different Stores and high pressure on raftstore. This is the time for a [Region Merge](#the-speed-of-region-merge-is-slow) scheduling.
- Hardware and software environment varies among Stores. You can adjust the values of `leader-weight` and `region-weight` accordingly to control the distribution of Leader/Region.
- Other unknown reasons. Still you can adjust the values of `leader-weight` and `region-weight` to control the distribution of Leader/Region.

If there is a big difference in the rating of different Stores, you need to examine the Operator-related metrics, with special focus on the generation and execution of Operators. There are two main situations:

- When a Operator is generated but processes slow, it is possible that:

    - The scheduling speed is limited by default. You can adjust `leader-schedule-limit` or `region-schedule-limit` to a larger value without significantly impacting application. In addition, the `max-pending-peer-count` and `max-snapshot-count` restrictions can also be properly adjusted.
    - Other scheduling tasks are running concurrently and competing in the system, which slows down the balancing speed. In this case, if the balancing priors to other scheduling tasks, you can stop other tasks or limit their speed. For example, if you take some nodes offline when Regions are rebalancing, both operations consume the quota of `region-schedule-limit`. You can limit the speed of taking nodes offline, or simply set `disable-replace-offline-replica = true` to temporarily shut it down.
    - The Operator processes too slow. You can check the time taken by Operator Steps to confirm. Generally, steps that do not involve sending and receiving snapshots (such as TransferLeader, RemovePeer, PromoteLearner, etc.) should be completed in milliseconds, while steps that involve snapshots (such as AddLearner, AddPeer, etc.) should be completed in tens of seconds. If the time taken is obviously too high, it is possible due to the excessive pressure of TiKV or the bottleneck of network, etc., which needs specific analysis.

- PD fails to generate the corresponding balancing task. Possible reasons include:

    - The Scheduler is not activated. For example, the corresponding Scheduler is deleted, or limit being set to 0.
    - Other constraints. For example, `evict-leader-scheduler` in the system prevents Leaders from being migrating to the corresponding Store. Or Label property is set, which makes some Stores reject Leaders.
    - The restrictions of cluster topology. For example, in a cluster of 3 replicas and 3 data centers, 3 replicas of each Region are distributed in different data centers due to replica isolation. If the number of Stores of these data centers are different, the final scheduling reaches a balanced but globally unbalanced state in each data center.

### The speed of taking nodes offline is slow

This scenario requires examining the generation and execution of Operators through related metrics.

When an Operator is successfully generated but processes slow, possible reasons are:

- The schedule speed is limited by default. You can adjust `leader-schedule-limit` or `replica-schedule-limit` to a larger value. Similarly, `max-pending-peer-count` and `max-snapshot-count` can also be properly enlarged.
- Other scheduling tasks are running concurrently and competing in the system. You can refer to the solution in [the previous section](#leaderregion-is-not-evenly-distributed).
- When you take a single node offline, a number of Region Leaders to be operated are concentrated on the offline node (about 1/3 under the configuration of 3 replicas), so the speed is limited by the speed at which this single node generates Snapshots. You can speed it up by manually adding an `evict-leader-scheduler` to migrate Leaders.

If the corresponding Operator fails to generate, possible reasons are:

- The Operator is stopped, or `replica-schedule-limit` is set to 0.
- There is no proper node to migrate Regions. For example, if the capacity of nodes that replace the nodes of same Label is larger than 80%, PD will stop scheduling to avoid running out of storage space. In such case, you need to add more nodes or delete some data to free space.

### The speed of putting nodes online is slow

Currently, to take nodes online is scheduled through balance region mechanism, so you can refer to [Leader/Region is not evenly distributed](#leaderregion-is-not-evenly-distributed) for troubleshooting.

### Hot Regions are not evenly distributed

Hot Regions scheduling generally has the following problems:

- There is a majority of hot Regions, but the scheduling speed cannot keep up with them to redistribute hot Regions in time.

    **Solution**: adjust `hot-region-schedule-limit` to a larger value, and reduce the limit quota of other schedulers to speed up hot Regions scheduling. Or you can adjust `hot-region-cache-hits-threshold` to a smaller value to make PD sensitive to traffic changes.

- A single Region with extensive traffics. For example, to scan a small table extensively is required in the production environment, which can also be detected from PD metrics. Since a single hotspot cannot be resolved by redistributing, you need to manually add a `split-region` Operator to redistribute such a Region.

- The load of some nodes is significantly higher than that of other nodes from TiKV-related metrics, which becomes the bottleneck of the whole system. Currently, PD counts hotspots through traffic analysis. So it is possible that PD fails to identify hotspots in certain scenarios. For example, some Regions have a large number of point-and-check requests, which are not significant in terms of traffic, but high QPS of which leads to bottlenecks in key modules.

    **Solutions**: Firstly, locate the table with extensive traffic by examining operational needs, and add a `scatter-range-scheduler` to make all Regions of this table are evenly distributed. TiDB also provides an interface in its HTTP AIP to simplify this operation. Refer to [TiDB HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md) for more details.

### The speed of Region Merge is slow

Similar to the slow scheduling discussed earlier, the speed of Region Merge is most likely limited by default (`merge-schedule-limit` and `region-schedule-limit`), or Region Merge is competing with other schedulers. Specifically, the solutions are:

- If it is known from statistics that there are a large number of empty Regions in the system, you can adjust `max-merge-region-size` and `max-merge-region-keys` to a smaller value to speed up the merging. This is because merging involves replica migration, so the smaller the Region to be merged, the faster. If the generated Merge Operator is already has hundreds of opm, to further speed up the merging process, you can set `patrol-Region-interval` to `10ms`. This will make Region scanning faster but consume more CPU.

- A lot of tables have been created and then emptied (including truncated tables). These empty Regions cannot be merged if the split table attribute is enabled. You can disable this attribute by adjusting the following parameters:

    - TiKV: set `split-region-on-table` to `false`
    - PD: set `namespace-classifier` to ""

For v3.0.4 and v2.1.16 or earlier, the `approximate_keys` of Regions are inaccurate in specific circumstances (most of which occur after dropping tables), which makes the number of keys break the constraints of `max-merge-region-keys`. To avoid this problem, you can adjust `max-merge-region-keys` to a larger value.

### TiKV node troubleshooting

If a TiKV node fails, after 30 minutes (customizable by configuration item `max-store-down-time`), PD defaults to setting the corresponding node to "Down" state, and rebalancing replicas for Regions involved.

Practically, if a node is deemed unrecoverable, you can immediately take it offline. This makes PD rebalance replicas soon and reduces the risk of data loss. In contrast, if a node is deemed recoverable, but might not be available in 30 minutes, you can temporarily adjust  `max-store-down-time` to a larger value to avoid unnecessary replenishment of the replicas and resources waste after the timeout.