---
title: TiDB Scheduler
category: components
Summary: Learn how TiDB Scheduler works
---

# TiDB Scheduler

This documents introduces how TiDB Scheduler works.

## TiDB cluster scheduling requirements

The TiDB cluster includes three key components: PD, TiKV, and TiDB. Each consists of multiple nodes: PD is a Raft cluster, and TiKV is a multi-group Raft cluster. Both components are stateful. Therefore, the default scheduling rules of the Kubernetes (K8s) scheduler can no longer meet the TiDB cluster scheduling requirements. To extend the K8s scheduling rules, the TiDB Operator implements the following customized scheduling rules:

### PD

Make sure that the number of PDs scheduled on each Node is less than `Replicas / 2`, for example:

| PD cluster size (Replicas) | Maximum number of PDs scheduled on each node |
| ------------- | ------------- |
| 1  | 1  |
| 2  | 1  |
| 3  | 1  |
| 4  | 1  |
| 5  | 2  |
| ...  |   |

### TiKV

If the number of K8s nodes is less than three (In this case, TiKV is not highly available), arbitrary schedule is supported; otherwise, the formula for calculating the number of TiKV schedulable on each node is: Ceil (Replicas / 3), for example:

| TiKV cluster size (Replicas) | Maximum number of TiKVs scheduled on each node | Best scheduling distribution |
| ------------- | ------------- | ------------- |
| 3  | 1  | 1,1,1  |
| 4  | 2  | 1,1,2  |
| 5  | 2  | 1,2,2  |
| 6  | 2  | 2,2,2  |
| 7  | 3  | 2,2,3  |
| 8  | 3  | 2,3,3  |
| ...  |   |   |

### TiDB

Stable scheduling is achieved. In the case of TiDB rolling upgrade, it tends to be scheduled back to the original nodes. This is helpful for the scenario of manually mounting Node IP and NodePort on the LB backend. It avoids rearranging the LB when the Node IP is changed after the upgrade, thereby reducing the impact on the cluster during rolling upgrade.

## How TiDB Scheduler works

![TiDB Scheduler Overview](/media/tidb-scheduler-overview.png)

TiDB Scheduler adds customized scheduling rules through K8s [Scheduler extender](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/scheduler_extender.md)

The TiDB Scheduler component is deployed as one or more Pods, though only one Pod is working at the same time. Two Containers inside the Pod are implemented as a K8s scheduler extender: one is a native `kube-scheduler`, and the other is a `tidb-scheduler`.

The `.spec.schedulerName` attribute of all Pods created by the TiDB Operator is set to `tidb-scheduler`. This means that the TiDB Scheduler is used for customized scheduling. Change `.spec.schedulerName` into `default-scheduler` to use the built-in K8s scheduler, in the case that testing the cluster does not require high availability. The scheduling process for a Pod is as follows:

- Each Pod is filtered using the default K8s scheduling rules. `kube-scheduler` pulls all Pods that match the criteria: the value of `.spec.schedulerName` is `tidb-scheduler`.
- `kube-scheduler` sends a request to the `tidb-scheduler` service. Then `tidb-scheduler` filters Nodes through the customized scheduling rules (as mentioned above), and returns schedulable Nodes to `kube-scheduler`.
- Finally, `kube-scheduler` determines the Nodes to be scheduled.

If a Pod cannot be scheduled, see the [troubleshooting document](/tidb-in-kubernetes/troubleshoot.md#the-Pod-is-in-the-Pending-state) to diagnose and solve the issue.
