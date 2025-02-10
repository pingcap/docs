---
title: Store Limit
summary: Learn the feature of Store Limit.
---

# Store Limit

Store Limit is a feature of PD. It is designed to control the scheduling speed in a finer manner for better performance in different scenarios.

## Implementation principles

PD performs scheduling at the unit of operator. An operator might contain several scheduling operations. For example:

```
"replace-down-replica {mv peer: store [2] to [3]} (kind:region,replica, region:10(4,5), createAt:2020-05-18 06:40:25.775636418 +0000 UTC m=+2168762.679540369, startAt:2020-05-18 06:40:25.775684648 +0000 UTC m=+2168762.679588599, currentStep:0, steps:[add learner peer 20 on store 3, promote learner peer 20 on store 3 to voter, remove peer on store 2])"
```

In this above example, the `replace-down-replica` operator contains the following specific operations:

1. Add a learner peer with the ID `20` to `store 3`.
2. Promote the learner peer with the ID `20` on `store 3` to a voter.
3. Delete the peer on `store 2`.

Store Limit achieves the store-level speed limit by maintaining a mapping from store IDs to token buckets in memory. The different operations here correspond to different token buckets. Currently, Store Limit only supports limiting the speed of two operations: adding learners/peers and deleting peers. That is, each store has two types of token buckets.

Every time an operator is generated, it checks whether enough tokens exist in the token buckets for its operations. If yes, the operator is added to the scheduling queue, and the corresponding token is taken from the token bucket. Otherwise, the operator is abandoned. Because the token bucket replenishes tokens at a fixed rate, the speed limit is thus achieved.

Store Limit is different from other limit-related parameters in PD (such as `region-schedule-limit` and `leader-schedule-limit`) in that it mainly limits the consuming speed of operators, while other parameters limits the generating speed of operators. Before introducing the Store Limit feature, the speed limit of scheduling is mostly at the global scope. Therefore, even if the global speed is limited, it is still possible that the scheduling operations are concentrated on some stores, affecting the performance of the cluster. By limiting the speed at a finer level, Store Limit can better control the scheduling behavior.

Store Limit defines the maximum number of operations per minute. With a Store Limit of 5 operations per minute, adding a new node to the cluster will process 5 Regions per minute (`add-peer` operations). If 15 Regions require an `add-peer`, the operation will take 3 minutes (15 / 5 = 3) and consume up to 8 MiB/s ((5 × 96) / 60 = 8), assuming each Region is 96 MiB.

## Usage

The parameters of Store Limit can be configured using [`PD Control`](/pd-control.md).

### View setting of the current store

To view the limit setting of the current store, run the following commands:

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit                         // Shows the speed limit of adding and deleting peers in all stores.
tiup ctl:v<CLUSTER_VERSION> pd store limit add-peer                // Shows the speed limit of adding peers in all stores.
tiup ctl:v<CLUSTER_VERSION> pd store limit remove-peer             // Shows the speed limit of deleting peers in all stores.
```

### Set limit for all stores

To set the speed limit for all stores, run the following commands:

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5                   // All stores can at most add and delete 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5 add-peer          // All stores can at most add 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit all 5 remove-peer       // All stores can at most delete 5 peers per minute.
```

### Set limit for a single store

To set the speed limit for a single store, run the following commands:

```bash
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5                     // store 1 can at most add and delete 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5 add-peer            // store 1 can at most add 5 peers per minute.
tiup ctl:v<CLUSTER_VERSION> pd store limit 1 5 remove-peer         // store 1 can at most delete 5 peers per minute.
```

### Principles of store limit v2

When [`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710) is set to `v2`, store limit v2 takes effect. In v2 mode, the limit of operators are dynamically adjusted based on the capability of TiKV snapshots. When TiKV has fewer pending tasks, PD increases its scheduling tasks. Otherwise, PD reduces the scheduling tasks for the node. Therefore, you do not need to manually set `store limit` to speed up the scheduling process.

In v2 mode, the execution speed of TiKV becomes the main bottleneck during migration. You can check whether the current scheduling speed has reached the upper limit through the **TiKV Details** > **Snapshot** > **Snapshot Speed** panel. To increase or decrease the scheduling speed of a node, you can adjust the TiKV snapshot limit ([`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec)).
