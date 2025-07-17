---
title: Scalability
summary: Learn about scalability concepts for TiDB Cloud.
---

# Scalability

TiDB Cloud Dedicated lets you adjust its compute and storage resources separately to match your data volume or workload changes. TiDB Cloud Dedicated can do scaling without any service disruption. This flexibility allows organizations to optimize their infrastructure costs while maintaining high performance and availability.

> **Note:**
>
> [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) scales automatically based on your application's workload changes. However, you cannot manually scale a TiDB Cloud Serverless cluster.

> **Tip:**
>
> For information about how to determine the size of a TiDB Cloud Dedicated cluster, see [Determine Your TiDB Size](/tidb-cloud/size-your-cluster.md).

## Vertical and horizontal scaling

TiDB Cloud Dedicated supports both vertical (scale up) and horizontal (scale out) scaling.

- Horizontal scaling is the process of adding nodes to your dedicated cluster to distribute the workload.
- Vertical scaling is the process of increasing the vCPU and RAM for your dedicated cluster.

A combination of both vertical and horizontal scaling is also supported in TiDB Cloud Dedicated.

## TiDB scalability

TiDB is for computing only and does not store data. You can configure the node number, vCPU, and RAM for TiDB.

In general, TiDB performance increases linearly with the number of TiDB nodes.

## TiKV scalability

TiKV is responsible for storing row-based data. You can configure the node number, vCPU and RAM, and storage for TiKV. The number of TiKV nodes should be at least 1 set (3 nodes in 3 different available zones) and increase by 3 nodes.

TiDB Cloud deploys TiKV nodes evenly to 3 available zones in the region you select to achieve durability and high availability. In a typical 3-replica setup, your data is distributed evenly among the TiKV nodes across all availability zones and is persisted to the disk of each TiKV node. Although TiKV is mainly used for data storage, the performance of the TiKV node also varies depending on different workloads.

## TiFlash scalability

TiFlash is responsible for storing columnar data. TiFlash synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box. You can configure the node number, vCPU and RAM, and storage for TiFlash.

TiDB Cloud deploys TiFlash nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash nodes in each TiDB Cloud cluster and create at least two replicas of the data for high availability in your production environment.