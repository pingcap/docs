---
title: Store Limit
summary: Learn the feature of Store Limit.
aliases: ['/docs/v3.1/configure-store-limit/']
---

# Store Limit

Store Limit is a feature of PD, introduced in TiDB 3.0. It is designed to control the scheduling speed in a finer manner for better performance in different scenarios.

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

## Usage

The parameters of Store Limit can be configured using `pd-ctl`.

### View setting of the current store

To view the limit setting of the current store, run the following commands:

{{< copyable "shell-regular" >}}

```bash
store limit                         // Shows the speed limit of adding learners/peers in all stores (if a specific type is not set, this command shows the speed of adding learners/peers).
store limit region-add              // Shows the speed limit of adding learners/peers in all stores.
store limit region-remove           // Shows the speed limit of deleting learners/peers in all stores. 
```

### Set limit for all stores

To set the speed limit for all stores, run the following commands:

{{< copyable "shell-regular" >}}

```bash
store limit all 5                   // All stores can at most add 5 learns/peers per minute (if a specific type is not set, this command sets the speed of adding learners/peers).
store limit all 5 region-add        // All stores can at most add 5 learns/peers per minute.
store limit all 5 region-remove     // All stores can at most delete 5 learns/peers per minute.
```

### Set limit for a single store

To set the speed limit for a single store, run the following commands:

{{< copyable "shell-regular" >}}

```bash
store limit 1 5                     // store 1 can at most add 5 learners/peers per minute (if a specific type is not set, this command sets the speed of adding learners/peers).
store limit 1 5 region-add          // store 1 can at most add 5 learners/peers per minute.
store limit 1 5 region-remove       // store 1 can at most delete 5 learners/peers per minute.
```

### Persist store limit modification

Because the store limit is a mapping in the memory, the above modification is reset after the leader is switched or PD is restarted. If you want to persist the modification, run the following command:

{{< copyable "shell-regular" >}}

```bash
config set store-balance-rate 20    // All stores can at most add 20 learners/peers or delete 20 peers per minute.
```
