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

    - `StoreHeartbeat`: Contains the overall information of Stores, including disk capacity, available storage, and read/write traffic.
    - `RegionHeartbeat`: Contains the overall information of Regions, including the range of each Region, peer distribution, peer status, data volume, and read/write traffic.

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

    2. `OperatorController` takes the Operator out of the queue and executes it with a certain amount of concurrency based on the configuration. This step is to assign each Operator Step to the corresponding Region Leader.

    3. The Operator is marked as "finish" or "timeout" and removed from the queue.

### Load balancing

Region primarily relies on `balance-leader` and `balance-region` schedulers to achieve load balance. Both schedulers target distributing Regions evenly across all Stores in the cluster but with separate focuses: `balance-leader` deals with Region Leader to balance incoming client requests, whereas `balance-region` concerns itself with each Region Peer to redistribute the pressure of storage and avoid exceptions like out of storage space.

`balance-leader` and `balance-region` share a similar scheduling process:

1. Rate Stores according to their resource availability.
2. `balance-leader` or `balance-region` constantly transfer Leaders or Peers from Stores with high scores to those with low scores.

However, their rating methods are different. `balance-leader` uses the sum of all Region Sizes corresponding to Leaders in a Store, whereas the way of `balance-region` is relatively complicated. Depending on the specific storage capacity of each node, the rating method of `balance-region` might:

- based on the amount of data when there is sufficient storage (to balance data distribution among nodes).
- based on the available storage when there is insufficient storage (to balance the storage availability on different nodes).
- based on the weighted sum of the two factors above when neither of the situations applies.

Because different nodes might differ in performance, you can also set the weight of load balancing for different Stores. `leader-weight` and `region-weight` are used to control the Leader weight and Region weight respectively ("1" by default for both). For example, when the `leader-weight` of a Store is set to "2", the number of Leaders on the node is about twice as many as that of other nodes after the scheduling stabilizes. Similarly, when the `leader-weight` of a Store is set to "0.5", the number of Leaders on the node is about half as many as that of other nodes.

### Hot Regions scheduling

For hot Regions scheduling, use `hot-region-scheduler`. Currently in TiDB 3.0, the process is performed as follows:

1. Count hot Regions by determining read/write traffic that exceeds a certain threshold for a certain period based on the information reported by Stores.

2. Redistribute these Regions in a similar way to load balancing.

For hot write Regions, `hot-region-scheduler` attempts to redistribute both Region Peers and Leaders; for hot read Regions, `hot-region-scheduler` only redistributes Region Leaders.

### Cluster topology awareness

Cluster topology awareness enables PD to distribute replicas of a Region as much as possible. This is how TiKV ensures high availability and disaster recovery capability. PD continuously scans all Regions in the background. When PD finds that the distribution of Regions is not optimal, it generates an Operator to replace Peers and redistribute Regions.

The component to check Region distribution is `replicaChecker`, which is similar to Scheduler except that it cannot be disabled. `replicaChecker` schedules based on the the configuration of `location-labels`. For example, `[zone, rack, host]` defines a three-tier topology for a cluster. PD attempts to schedule Region Peers to different zones first, or to different racks when zones are insufficient (for example, 2 zones for 3 replicas), or to different hosts when racks are insufficient, and so on.

### Scale-down and failure recovery

Scale-down refers to the process when you take a Store offline and mark it as "offline" using a command. PD replicates the Regions on the offline node to other nodes by scheduling. Failure recovery applies when Stores failed and cannot be recovered. In this case, Regions with Peers distributed on the corresponding Store might lose replicas, which requires PD to replenish on other nodes.

The processes of Scale-down and failure recovery are basically the same. `replicaChecker` finds a Region Peer in abnormal states, and then generates an Operator to replace the abnormal Peer with a new one on a healthy Store.

### Region Merge

Region Merge refers to the process of merging adjacent small Regions. It serves to avoid unnecessary resource consumption by a large number of small or even empty Regions after data deletion. Region Merge is performed by `mergeChecker`, which processes in a similar way to `replicaChecker`: PD continuously scans all Regions in the background, and generates an Operator when contiguous small Regions are found.

## Query scheduling status

You can check the status of scheduling system through Metrics, pd-ctl and logs. This section briefly introduces the methods of Metrics and pd-ctl. Refer to [PD monitoring metrics](/dev/reference/key-monitoring-metrics/pd-dashboard.md) and [PD Control](/dev/reference/tools/pd-control.md) for details.

### Operator status

The **Grafana PD/Operator** page shows the statistics about Operators, among which:

- Schedule Operator Create: Operator creating information
- Operator finish duration: Execution time consumed by each Operator
- Operator Step duration: Execution time consumed by the Operator Step

You can query Operators using pd-ctl with the following commands:

- `operator show`: Queries all Operators generated in the current scheduling task
- `operator show [admin | leader | region]`: Queries Operators by type

### Balance status

The **Grafana PD/Statistics - Balance** page shows the statistics about load balancing, among which:

- Store Leader/Region score: Score of each Store
- Store Leader/Region count: The number of Leaders/Regions in each Store
- Store available: Available storage on each Store

You can use store commands of pd-ctl to query balance status of each Store.

### Hot Region status

The **Grafana PD/Statistics - hotspot** page shows the statistics about hot Regions, among which:

- Hot write Region’s leader/peer distribution: Leader/Peer distribution in hot write Regions
- Hot read Region’s leader distribution: Leader distribution in hot read Regions

You can also query the status of hot Regions using pd-ctl with the following commands:

- `hot read`: Queries hot read Regions
- `hot write`: Queries hot write Regions
- `hot store`: Queries the distribution of hot Regions by Store
- `region topread [limit]`: Queries the Region with top read traffic
- `region topwrite [limit]`: Queries the Region with top write traffic

### Region health

The **Grafana PD/Cluster/Region health** panel shows the statistics about Regions in abnormal states, include Pending Peer, Down Peer, Offline Peer and Regions with extra or few Peers.

You can query the list of Regions in abnormal states using pd-ctl with region check commands:

- `region check miss-peer`: Queries Regions without enough Peers
- `region check extra-peer`: Queries Regions with extra Peers
- `region check down-peer`: Queries Regions with Down Peers
- `region check pending-peer`: Queries Regions with Pending Peers

## Control scheduling strategy

You can use pd-ctl to adjust the scheduling strategy from the following three aspects. Refer to [PD Control](/dev/reference/tools/pd-control.md) for more details.

### Add/delete Scheduler manually

PD supports dynamically adding and removing Schedulers directly through pd-ctl. For example:

- `scheduler show`: Shows currently running Schedulers in the system
- `scheduler remove balance-leader-scheduler`: Removes (disable) balance-leader-scheduler
- `scheduler add evict-leader-scheduler-1`: Adds a scheduler to remove all Leaders in Store 1

### Add/delete Operators manually

PD also supports adding or removing Operators directly through pd-ctl. For example:

- `operator add add-peer 2 5`: Adds Peers to Region 2 in Store 5
- `operator add transfer-leader 2 5`: Migrates the Leader of Region 2 to Store 5
- `operator add split-region 2`: Splits Region 2 into two Regions evenly in size
- `operator remove 2`: Removes currently pending Operator in Region 2

### Adjust scheduling parameter

You can check the scheduling configuration using the `config show` command in pd-ctl, and adjust the values using `config set {key} {value}`. Common adjustments include:

- `leader-schedule-limit`: Controls the concurrency of Transfer Leader scheduling
- `region-schedule-limit`: Controls the concurrency of adding/deleting Peer scheduling
- `disable-replace-offline-replica`: Determines whether to disable the scheduling to take nodes offline
- `disable-location-replacement`: Determines whether to disable the scheduling that handles the isolation level of Regions
- `max-snapshot-count`: Controls the maximum concurrency of sending/receiving Snapshots for each Store

## PD scheduling in common scenarios

This section illustrates the best practices of PD scheduling strategies through several typical scenarios.

### Leaders/Regions are not evenly distributed

The rating mechanism of PD determines that Leader Count and Region Count of different Stores cannot fully reflect the load balancing status. Therefore, it is necessary to confirm whether there is load imbalancing from the actual load of TiKV or Storage usage.

Once you have confirmed that Leaders/Regiosn are not evenly distributed, you need to check the rating of different Stores.

If the scores of different Stores are close, it means PD mistakenly believes that Leaders/Regions are evenly distributed. Possible reasons are:

- There are hot Regions that cause load imbalancing. In this case, you need to analyze further based on [hot Regions scheduling](#hot-regions-are-not-evenly-distributed).
- There are a large number of empty Regions or small Regions, which leads to a great difference in the number of Leaders in different Stores and high pressure on Raftstore. This is the time for a [Region Merge](#region-merge-is-slow) scheduling.
- Hardware and software environment varies among Stores. You can adjust the values of `leader-weight` and `region-weight` accordingly to control the distribution of Leader/Region.
- Other unknown reasons. Still you can adjust the values of `leader-weight` and `region-weight` to control the distribution of Leader/Region.

If there is a big difference in the rating of different Stores, you need to examine the Operator-related metrics, with special focus on the generation and execution of Operators. There are two main situations:

- When Operators are generated normally but the scheduling process is slow, it is possible that:

    - The scheduling speed is limited by default for load balancing purpose. You can adjust `leader-schedule-limit` or `region-schedule-limit` to larger values without significantly impacting regular services. In addition, you can also properly ease the restrictions specified by `max-pending-peer-count` and `max-snapshot-count`.
    - Other scheduling tasks are running concurrently, which slows down the balancing. In this case, if the balancing takes precedence over other scheduling tasks, you can stop other tasks or limit their speeds. For example, if you take some nodes offline when balancing is in progress, both operations consume the quota of `region-schedule-limit`. In this case, you can limit the speed of scheduler to remove nodes, or simply set `disable-replace-offline-replica = true` to temporarily disable it.
    - The scheduling process is too slow. You can check the **Operator Step duration** metric to confirm the cause. Generally, steps that do not involve sending and receiving snapshots (such as `TransferLeader`, `RemovePeer`, `PromoteLearner`) should be completed in milliseconds, while steps that involve snapshots (such as `AddLearner` and `AddPeer`) are expected to be completed in tens of seconds. If the duration is obviously too long, it could be caused by high pressure on TiKV or bottleneck in network, etc., which needs specific analysis.

- PD fails to generate the corresponding balancing Scheduler. Possible reasons include:

    - The Scheduler is not activated. For example, the corresponding Scheduler is deleted, or its limit it set to "0".
    - Other constraints. For example, `evict-leader-scheduler` in the system prevents Leaders from being migrating to the corresponding Store. Or Label property is set, which makes some Stores reject Leaders.
    - Restrictions from the cluster topology. For example, in a cluster of 3 replicas across 3 data centers, 3 replicas of each Region are distributed in different data centers due to replica isolation. If the number of Stores is different among these data centers, the scheduling can only reach a balanced state within each data center, but not balanced globally.

### Taking nodes offline is slow

This scenario requires examining the generation and execution of Operators through related metrics.

If Operators are successfully generated but the scheduling process is slow, possible reasons are:

- The scheduling speed is limited by default. You can adjust `leader-schedule-limit` or `replica-schedule-limit` to larger value.s Similarly, you can consider loosening the limits on `max-pending-peer-count` and `max-snapshot-count`.
- Other scheduling tasks are running concurrently and racing for resources in the system. You can refer to the solution in [the previous section](#leadersregions-are-not-evenly-distributed).
- When you take a single node offline, a number of Region Leaders to be processed (around 1/3 under the configuration of 3 replicas) are distributed on the node to remove. Therefore, the speed is limited by the speed at which snapshots are generated by this single node. You can speed it up by manually adding an `evict-leader-scheduler` to migrate Leaders.

If the corresponding Operator fails to generate, possible reasons are:

- The Operator is stopped, or `replica-schedule-limit` is set to "0".
- There is no proper node for Region migration. For example, if the available capacity size of the replacing nodes (of the same label) is less than 20%, PD will stop scheduling to avoid running out of storage space. In such case, you need to add more nodes or delete some data to free the space.

### Bringing nodes online is slow

Currently, bringing nodes online is scheduled through the balance region mechanism. You can refer to [Leaders/Regions are not evenly distributed](#leadersregions-are-not-evenly-distributed) for troubleshooting.

### Hot Regions are not evenly distributed

Hot Regions scheduling issues generally fall into the following categories:

- Hot Regions can be observed via PD metrics, but the scheduling speed cannot keep up to redistribute hot Regions in time.

    **Solution**: adjust `hot-region-schedule-limit` to a larger value, and reduce the limit quota of other schedulers to speed up hot Regions scheduling. Or you can adjust `hot-region-cache-hits-threshold` to a smaller value to make PD more sensitive to traffic changes.

- Hotspot formed on a single Region. For example, a small table is intensively scanned by a massive amount of requests. This can also be detected from PD metrics. Because you cannot actually distribute a single hotspot, you need to manually add a `split-region` Operator to split such a Region.

- The load of some nodes is significantly higher than that of other nodes from TiKV-related metrics, which becomes the bottleneck of the whole system. Currently, PD counts hotspots through traffic analysis only, so it is possible that PD fails to identify hotspots in certain scenarios. For example, when there are intensive point lookup requests for some Regions, it might not be obvious to detect in traffic, but still the high QPS might lead to bottlenecks in key modules.

    **Solutions**: Firstly, locate the table where hot Regions are formed based on the specific business. Then add a `scatter-range-scheduler` scheduler to make all Regions of this table evenly distributed. TiDB also provides an interface in its HTTP AIP to simplify this operation. Refer to [TiDB HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md) for more details.

### Region Merge is slow

Similar to slow scheduling, the speed of Region Merge is most likely limited by the configurations of `merge-schedule-limit` and `region-schedule-limit`, or the Region Merge scheduler is competing with other schedulers. Specifically, the solutions are:

- If it is known from statistics that there are a large number of empty Regions in the system, you can adjust `max-merge-region-size` and `max-merge-region-keys` to smaller values to speed up the merge. This is because the merge process involves replica migration, so the smaller the Region to be merged, the faster the merge is. If the merge operators are already generated rapidly, to further speed up the process, you can set `patrol-region-interval` to `10ms`. This makes Region scanning faster at the cost of more CPU consumption.

- A lot of tables have been created and then emptied (including truncated tables). These empty Regions cannot be merged if the split table attribute is enabled. You can disable this attribute by adjusting the following parameters:

    - TiKV: set `split-region-on-table` to `false`
    - PD: set `namespace-classifier` to ""

For v3.0.4 and v2.1.16 or earlier, the `approximate_keys` of Regions are inaccurate in specific circumstances (most of which occur after dropping tables), which makes the number of keys break the constraints of `max-merge-region-keys`. To avoid this problem, you can adjust `max-merge-region-keys` to a larger value.

### Troubleshoot TiKV node

If a TiKV node fails, PD defaults to setting the corresponding node to the **Down** state after 30 minutes (customizable by configuration item `max-store-down-time`), and rebalancing replicas for Regions involved.

Practically, if a node failure is considered unrecoverable, you can immediately take it offline. This makes PD replenish replicas soon in another node and reduces the risk of data loss. In contrast, if a node is considered recoverable, but the recovery cannot be done in 30 minutes, you can temporarily adjust `max-store-down-time` to a larger value to avoid unnecessary replenishment of the replicas and resources waste after the timeout.