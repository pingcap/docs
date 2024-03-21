---
title: PD Microservices
summary: Learn how to enable the microservice mode of PD to improve service quality.
---

# PD Microservices

Starting from v8.0.0, PD supports the microservice mode, which disaggregates the timestamp allocation and cluster scheduling functions of PD into the following two independently deployed microservices. In this way, these two functions are decoupled from the routing function of PD, which allows PD to focus on the routing service for metadata.

- `tso` microservice: provides monotonically increasing timestamp allocation for the entire cluster.
- `scheduling` microservice: provides scheduling functions for the entire cluster, including but not limited to load balancing, hot spot handling, replica repair, and replica placement.

Each microservice is deployed as an independent process. If you configure more than one replica for a microservice, the microservice automatically implements a primary-secondary fault-tolerant mode to ensure high availability and reliability of the service.

## Usage scenarios

PD microservices are typically used to address performance bottlenecks in PD and improve PD service quality. With this feature, you can avoid the following issues:

- Long-tail latency or jitter in TSO allocations due to excessive pressure in PD clusters
- Service unavailability of the entire cluster due to failures in the scheduling module
- Bottleneck issues solely caused by PD

In addition, when the scheduling module is changed, you can update the `scheduling` microservice independently without restarting PD, thus avoiding any impact on the overall service of the cluster.

> **Note:**
>
> If the performance bottleneck of a cluster is not caused by PD, there is no need to enable microservices, because using microservices increases the number of components and raises operational costs.

## Restrictions

- Currently, the `tso` microservice does not support dynamic start and stop. After enabling or disabling the `tso` microservice, you need to restart the PD cluster for the changes to take effect.
- Only the TiDB component supports a direct connection to the `tso` microservice through service discovery, while other components need to forward requests to the `tso` microservice through PD to obtain timestamps.
- Microservices are not compatible with the [Data Replication Auto Synchronous (DR Auto-Sync)](https://docs.pingcap.com/tidb/stable/two-data-centers-in-one-city-deployment) feature.
- Microservices are not compatible with the TiDB system variable [`tidb_enable_tso_follower_proxy`](https://docs.pingcap.com/tidb/stable/system-variables#tidb_enable_tso_follower_proxy-new-in-v530).
- Due to the potential presence of hibernate Regions in a cluster, during a primary and secondary switchover of the `scheduling` microservice, the scheduling function of the cluster might be unavailable for up to five minutes to avoid redundant scheduling.

## Usage

Currently, PD microservices can only be deployed using TiDB Operator. For detailed instructions, refer to the following documents:

- [Deploy PD microservices](configure-a-tidb-cluster.md#deploy-pd-microservices)
- [Configure PD microservices](configure-a-tidb-cluster.md#configure-pd-microservices)
- [Modify PD microservices](modify-tidb-configuration.md#modify-pd-microservices-configuration)
- [Scale PD microservice components](scale-a-tidb-cluster.md#scale-pd-microservice-components)

When deploying and using PD microservices, pay attention to the following:

- After you enable microservices and restart PD for a cluster, PD stops allocating TSO for the cluster. Therefore, you need to deploy the `tso` microservice in the cluster when you enable microservices.
- If the `scheduling` microservice is deployed in a cluster, the scheduling function of the cluster is provided by the `scheduling` microservice. If the `scheduling` microservice is not deployed, the scheduling function of the cluster is still provided by PD.
- The `scheduling` microservice supports dynamic switching, which is enabled by default (`enable-scheduling-fallback` defaults to `true`). If the process of the `scheduling` microservice is terminated, PD continues to provide scheduling services for the cluster by default.

    If the binary versions of the `scheduling` microservice and PD are different, to prevent changes in the scheduling logic, you can disable the dynamic switching function of the `scheduling` microservice by executing `pd-ctl config set enable-scheduling-fallback false`. After this function is disabled, PD will not take over the scheduling service when the process of the `scheduling` microservice is terminated. This means that the scheduling service of the cluster will be unavailable until the `scheduling` microservice is restarted.

## Tool compatibility

Microservices do not affect the normal use of data import, export, and other replication tools.

## FAQs

- How can I determine if PD becomes a performance bottleneck?

  When your cluster is in a normal state, you can check monitoring metrics in the Grafana PD panel. If the `TiDB - PD server TSO handle time` metric shows a notable increase in latency or the `Heartbeat - TiKV side heartbeat statistics` metric shows a significant number of pending items, it indicates that PD becomes a performance bottleneck.