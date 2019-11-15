---
title: PD Scheduling
summary: Learn best practice and strategy for PD scheduling.
category: reference
---

# PD Scheduling

This document details the principles and strategies of PD scheduling through common scenarios to facilitate user application. This document assumes that you have a basic understanding of TiDB, TiKV and PD with the following core concepts:

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
> This document initially targets TiDB 3.0. Though some functions are not supported in earlier versions (2.x), but this document still can be used as a reference for similar principles.

## PD scheduling policies

This section introduces the principle and process involved in the scheduling system.

### Scheduling process

Scheduling process generally has three steps:

1. Collect information

    Each TiKV node periodically reports two heartbeats to PD: `StoreHeartbeat` and `RegionHeartbeat`. `StoreHeartbeat` contains the overall information of Stores including disk capacity, remaining storage, reads and writes traffic. `RegionHeartbeat` contains the overall information of Regions including the range of each Region, peer distribution, peer status, data volume, and reads and writes traffic. PD collects and restores these information for scheduling decisions.

2. Generate Operators

    Different schedulers generate Operators to be executed based on their own logic and requirements, with the consideration of constraints and limitations include:

     - Do not add Peers to a Store with abnormal states (disconnect, down, busy, out of space, with extensive sent/received Snapshots)
     - Do not balance Regions with abnormal states
     - Do not attempt to transfer a Leader to a Pending Peer
     - Do not attempt to remove a Leader directly
     - Do not break the physical isolation of various Region Peers
     - Do not break constraints such as Label property

3. Execute scheduling tasks

    The generated Operator first joins a queue managed by `OperatorController` rather than be executed immediately. The `OperatorController` takes the Operator out of the queue and executes it with a certain amount of concurrency based on the configuration. The procedure is to distribute each Operator Step to the corresponding Region Leader. In the end, the Operator is marked as finish or timeout and removed from the execution list.

### Load balancing

Region primarily relies on `balance-leader` and `balance-region` schedulers to achieve load balance. Both schedulers target distributing Regions evenly across all Stores in the cluster but with separate focuses: `balance-leader` attends Region Leader to balance incoming client requests. `balance-region` centers each Region Peer to redistribute the pressure of storage while avoid exceptions like storage failure.

`balance-leader` and `balance-region` share a similar scheduling process. First, they grade different Stores according to their amount of resources. Then, `balance-leader` and `balance-region` constantly select Leaders or Peers from Stores with high scores and transfer them to Stores with low scores. Their grading methods vary though: `balance-leader` uses the sum of all Region Sizes corresponding to Leaders in a Store whereas the way of `balance-region` is relatively complicated. Since the storage capacity of different nodes might be inconsistent, the grading of `balance-region` is:

- based on the amount of data when there is abundant storage (to make the amount of data of different nodes balanced)
- based on the remaining storage when there is insufficient storage (to make the remaining storage of different nodes balanced)
- based on the weighted sum of the two factors above when storage is neither abundant nor insufficient.

Since different nodes might differ in performance, you can also set the weight of load balance for different Stores. `leader-weight` and `region-weight` are used to control the Leader weight and Region weight respectively (1 by default). For example, when the `leader-weight` of a Store is set to 2, the number of Leaders of the node is about twice as large as that of other nodes after the scheduling is stable. Similarly, when the `leader-weight` of a Store is set to 0.5, the number of Leaders of the node is about half as large as that of other nodes.

### Hot Regions scheduling

Hot Regions scheduling uses `hot-region-scheduler`. Currently in v3.0, the only way to count hot Regions is to determine whether the read/write traffic exceeds a certain threshold for a certain period based on the information reported by Stores. Then, redistribute these Regions in a similar way to load balancing.

For hot write Region, `hot-region-scheduler` attempts to redistribute both Region Peers and Leaders; for hot read Region, `hot-region-scheduler` only redistributes Region Leaders.

### Cluster topology awareness

Cluster topology awareness (zone/rack/host awareness) is having the knowledge of cluster topology or more specifically how the different data nodes are distributed. This is to make the different Regions Peers as distributed as possible through scheduling, hence to achieve high availability and disaster recovery. PD continuously scans all Regions in the background. When PD finds that the distribution of Regions is not optimal, it generates a Operator to replace Peers and redistribute Regions.

The component to check the distribution of Regions is `replicaChecker`, which is similar to Scheduler except that it cannot be disabled. `replicaChecker` checks and schedules based on the information provided by the configuration item `location-labels`. For example, `[zone, rack, host]` defines a three-tier topology: the cluster is configured with multiple available zones, with multiple racks under each zone and multiple hosts under each rack. PD attempts to schedule Region Peers to different zones first, or to different racks when zones are limited, or to different hosts when racks are limited.

### Scale-down and failure recovery

Scale-down refers to taking a Store offline. You can use commands to mark the Store as `Offline` while PD replicates the data the offline node held onto other nodes by scheduling. Failure recovery applies when Stores failed and cannot be recovered. In such case, a Region with Peers distributed on the corresponding Store might lose replicas, which requires PD to replenish replicas for these Regions on other nodes.

The processes of Scale-down and failure recovery are basically the same.  `replicaChecker` finds a Region Peer with abnormal states, and then generates a scheduling task to create a new replica on a healthy Store to replace the abnormal one.

### Region merge

Region merge refers to the process of merging adjacent small Regions by scheduling. It serves to avoid unnecessary resources consumption by a large number of small or even empty Regions after data deletion. The component used is `mergeChecker`, which processes in a similar way to `replicaChecker`: PD continuously scans all Regions in the background, and generates a scheduling task when contiguous small Regions are found.

## Query scheduling status

You can check the status of scheduling system through Metrics, pd-ctl and log. This section briefly introduces methods of Metrics and pd-ctl. Refer to [PD monitoring metrics](/dev/reference/key-monitoring-metrics/pd-dashboard.md) and [PD Control user guide](/dev/reference/reference/tools/pd-control.md) for details.

### Operator status

**Grafana PD/Operator** page shows the statistics about Operators, among which:

- Schedule Operator Create: information include the reason and target scheduler created by a Operator
- Operator finish duration: execution time consumed by each Operator
- Operator Step duration: execution time consumed by each Operator Step

You can query Operators using pd-ctl with the following commands:

- `operator show`: query all Operators generated iny the current scheduling task
- `operator show [admin | leader | region]`: query Operators by type

### Balance status

**Grafana PD/Statistics - Balance** page shows the statistics about load balancing, among which:

- Store Leader/Region score: score of each Store
- Store Leader/Region count: the number of Leaders/Regions in each Store
- Store available: remaining storage of each Store

You can use store commands of pd-ctl to query balance status of each Store.

### Hotspot status

**Grafana PD/Statistics - hotspot** page shows the statistics about hotspots, among which:

- Hot write Region’s leader/peer distribution: Leader/Peer distribution in hot write Regions
- Hot read Region’s leader distribution: Leader distribution in hot read Regions

You can also query the status of hotspots using pd-ctl with the following commands:

- `hot read`: query hot read Regions
- `hot write`: query hot write Regions
- `hot store`: query the distribution of hot Regions by Store
- `region topread [limit]`: query the Region with top read traffic
- `region topwrite [limit]`: query the Region with top write traffic

### Region health

**Grafana PD/Cluster/Region health** panel shows the statistics about Regions in abnormal states, include Pending Peer, Down Peer, Offline Peer and Regions with extra or few Peers.

You can query the list of Regions in abnormal conditions using pd-ctl with region check commands:

- `region check miss-peer`: Regions without enough Peers
- `region check extra-peer`: Regions with extra Peers
- `region check down-peer`: Regions with Down Peers
- `region check pending-peer`: Regions with Pending Peers

## Scheduling strategy control

You can use pd-ctl to adjust the scheduling strategy from the following three aspects. Refer to [PD Control](/dev/reference/tools/pd-control.md) for more details.

### Start-stop scheduler

pd-ctl supports dynamically creating and deleting Schedulers. You can use the following commands to control the scheduling behavior of PD:

- `scheduler show`: show currently working Schedulers in the system
- `scheduler remove balance-leader-scheduler`: delete (disable) balance-leader-scheduler
- `scheduler add evict-leader-scheduler-1`: add a scheduler to remove all Leaders in Store 1

### Add Operators manually

Pd also supports creating or removing Schedulers directly through pd-ctl. For example:

- `operator add add-peer 2 5`: add Peers to Region 2 in Store 5
- `operator add transfer-leader 2 5`: migrate Region 2 Leader to Store 5
- `operator add split-region 2`: split Region 2 into two Regions evenly in size
- `operator remove 2`: remove currently pending Operator in Region 2

### Adjust scheduling parameter

You can check the scheduling configuration using pd-ctl with `config show` command, and adjust the value using `config set {key} {value}`. Common adjustments include:

- `leader-schedule-limit`: control the number of concurrency of Transfer Leader scheduling
- `region-schedule-limit`: control the number of concurrency of adding/rdeleting Peer scheduling
- `disable-replace-offline-replia`: stop taking nodes offline
- `disable-location-replacement`: stop adjusting the isolation level of Regions
- `max-snapshot-count`: control the maximum of sent/received Snapshots concurrently of each Store

## PD scheduling in common scenarios

This section illustrates the best practice of PD scheduling strategies through several scenarios and their scheduling plans.

### Leader/Region is not evenly distributed

The grading mechanism of PD determines that Leader Count and Region Count of different Stores cannot fully explain the load balance status. Therefore, it is necessary to confirm whether there is load imbalance from the actual load of TiKV or Storage usage.

Once you have confirmed that Leader/Region is not evenly distributed, you need to check the grading of different Stores.

If the scores of different Stores are close, it means PD mistakenly believes that Leader/Region is evenly distributed. Possible reasons are:

- There are hotspots which cause load imbalance. In such case, you need to collect information about hot Regions scheduling before taking the next step. For more details, refer to [hotspot scheduling](#hot-regions-is-not-evenly-distributed) below.
- There are a large number of empty Regions or small Regions, which leads to a great difference in the number of Leaders in different Stores and further burdens raftstore. This is the time for a Region Merge and quicken merging process. For more details, refer to the [Region Merge](#the-speed-of-region-merge-is-slow) section below.
- Hardware and software environment varies from Store to Store. You can accordingly adjust the value of `leader-weight` and `region-weight` to control the distribution of Leader/Region.
- Other unknown reasons. Still you can adjust the value of `leader-weight` and `region-weight` to control the distribution of Leader/Region.

If there is a big difference in the grading of different Stores, you need to examine the Operator-related metrics, with special focus on the generation and execution of Operators. There are two situations in general:

- When a Operator is generated but processes slow, it is possible that:

    - the scheduling speed is limited by default. You can adjust `leader-schedule-limit` or `region-schedule-limit` to a larger value without significantly impacting application. In addition, the `max-pending-peer-count` and `max-snapshot-count` restrictions can also be properly adjusted.
    - other scheduling tasks are running concurrently and competing in the system, which slows down the balancing speed. In this case, if the balancing priors to other scheduling tasks, you can stop other tasks or limit their speed. For example, if you take some nodes offline when Regions are rebalancing, both operations consume the quota of `region-schedule-limit`. You can limit the speed of taking nodes offline, or simply set `disable-replace-offline-replica = true` to temporarily shut it down.
    - The Operator processes too slow. You can check the time taken by Operator Steps to confirm. Generally, steps that do not involve sending and receiving snapshots (such as TransferLeader, RemovePeer, PromoteLearner, etc.) should be completed in milliseconds, while steps that involve snapshots (such as AddLearner, AddPeer, etc.) should be completed in tens of seconds. If the time taken is obviously too high, it is possible due to the excessive pressure of TiKV or the bottleneck of network, etc., which needs specific analysis.

- PD fails to generate the corresponding balancing task. Possible reasons include:

    - Scheduler is not enabled. For example, the corresponding Scheduler is deleted, or limit being set to 0.
    - other constraints. For example, `evict-leader-scheduler` in the system prevents Leaders from being migrating to the corresponding Store. Or Label property is set, which makes some Stores reject Leaders.
    - the restrictions of cluster topology. For example, in a cluster of 3 replicas and 3 data centers, 3 replicas of each Region are distributed in different data centers due to replica isolation. If the number of Stores of these data centers are different, the final scheduling reaches a balanced but globally unbalanced state in each data center.

### The speed of taking nodes offline is slow

This scenario requires examining the generation and execution of Operators through related metrics.

When a Operator is successfully generated but processes slow, possible reasons are:

- the schedule speed is limit by default. You can adjust `leader-schedule-limit` or `replica-schedule-limit` to a larger value. Similarly, `max-pending-peer-count` and `max-snapshot-count` can also be properly enlarged.
- other scheduling tasks are running concurrently and competing in the system. You can refer to the solution in [the previous section](#leaderregion-is-not-evenly-distributed).
- when you take a single node offline, since a number of Region Leaders to be operated are concentrated on the offline node (about 1/3 under the configuration of 3 replicas), the speed is limited by the speed at which this single node generates Snapshots. You can speed it up by manually adding an `evict-leader-scheduler` to migrate Leaders.

If the corresponding Operator fails to generate, possible reasons are:

- The Operator is stopped, or `replica-schedule-limit` is set to 0.
- there is no proper node to migrate Regions. For example, if the capacity of nodes that replace the nodes of same Label is larger than 80%, PD will stop scheduling to avoid the risk of storage failure. In such case, you need to add more nodes or delete some data to free space.

### The speed of putting nodes online is slow

Currently, to take nodes online is scheduled through balance region mechanism, so you can refer to [Leader/Region is not evenly distributed](#leaderregion-is-not-evenly-distributed) for troubleshooting.

### Hotspots are not evenly distributed

Hotspots scheduling generally has the following problems:

- There is a majority of hot Regions, but the scheduling speed cannot keep up with them to redistribute hot Regions in time.

    **Solution**: adjust `hot-region-schedule-limit` to a larger value, and reduce the limit quota of other schedulers to speed up hot Regions scheduling. Or you can adjust `hot-region-cache-hits-threshold` to a smaller value to make PD sensitive to traffic changes.

- A single Region with extensive traffics. For example, to scan a small table extensively is required in the production environment, which can also be detected from PD metrics. Since a single hotspot cannot be resolved by redistributing, you need to manually add a `split-region` Operator to redistribute such a Region.

- the load of some nodes is significantly higher than that of other nodes from TiKV-related metrics, which becomes the bottleneck of the whole system. Currently, PD counts hotspots through traffic analysis. So it is possible that PD fails to identify hotspots in certain scenarios. For example, some Regions have a large number of point-and-check requests, which are not significant in terms of traffic, but high QPS of which leads to bottlenecks in key modules.

    **Solutions**: Firstly, locate the table with extensive traffic by examining operational needs, and add a `scatter-range-scheduler` to make all Regions of this table are evenly distributed. TiDB also provides an interface in its HTTP AIP to simplify this operation. Refer to [TiDB HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md) for more details.

### The speed of Region Merge is slow

Similar to the slow scheduling discussed earlier, the speed of Region Merge is most likely limited by default (`merge-schedule-limit` and `region-schedule-limit`), or Region Merge is competing with other schedulers. Specifically, the solutions are:

- if it is known from statistics that there are a large number of empty Regions in the system, you can adjust `max-merge-region-size` and `max-merge-region-keys` to a smaller value to speed up the merging. This is because merging involves replica migration, so the smaller the Region to be merged, the faster. If the generated Merge Operator is already has hundreds of opm, to further speed up the merging process, you can set `patrol-Region-interval` to `10ms`. This will make Region scanning faster but consume more CPU.

- a lot of tables have been created and then emptied (including truncated tables). These empty Regions cannot be merged if the split table attribute is enabled. You can disable this attribute by adjusting the following parameters:

    - TiKV: set `split-region-on-table` to `false`
    - PD: set `namespace-classifier` to ""

For v3.0.4 and v2.1.16 or earlier, the `approximate_keys` of Regions are inaccurate in specific circumstances (most of which occur after dropping tables), which makes the number of keys break the constraints of `max-merge-region-keys`. To avoid this problem, you can adjust `max-merge-region-keys` to a larger value.

### TiKV node troubleshooting

If a TiKV node fails, after 30 minutes (customizable by configuration item `max-store-down-time`), PD defaults to setting the corresponding node to "Down" state, and rebalancing replicas for Regions involved.

Practically, if a node is deemed unrecoverable, you can immediately take it offline. This makes PD rebalance replicas soon and reduces the risk of data loss. In contrast, if a node is deemed recoverable, but might not be available in 30 minutes, you can temporarily adjust  `max-store-down-time` to a larger value to avoid unnecessary replenishment of the replicas and resources waste after the timeout.