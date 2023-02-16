---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# Determine Your TiDB Size

This document describes how to determine the size of a Dedicated Tier cluster.

> **Note:**
>
> You cannot change the size of a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) cluster.

## Size TiDB

TiDB is for computing only and does not store data. It is horizontally scalable.

You can configure both node size and node quantity for TiDB.

To learn performance test results of different cluster scales, see [TiDB Cloud Performance Reference](/tidb-cloud/tidb-cloud-performance-reference.md).

### TiDB node size

The supported node sizes include the following:

- 2 vCPU, 8 GiB (Beta)
- 4 vCPU, 16 GiB
- 8 vCPU, 16 GiB
- 16 vCPU, 32 GiB

> **Note:**
>
> If the node size of TiDB is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - 2 vCPU TiDB can only be used with 2 vCPU TiKV. 4 vCPU TiDB can only be used with 4 vCPU TiKV.
> - TiFlash is unavailable.

### TiDB node quantity

In general, the TiDB performance increases linearly with the number of TiDB nodes. However, when the number of TiDB nodes exceeds 8, the performance increment becomes slightly less than linearly proportional. For each additional 8 nodes, the performance deviation coefficient is about 5%.
For example:

- When there are 9 TiDB nodes, the performance deviation coefficient is about 5%, so the TiDB performance is about `9 * (1 - 5%) = 8.55` times the performance of a single TiDB node. 
- When there are 16 TiDB nodes, the performance deviation coefficient is about 10%, so the overall performance is `16 * (1 - 10%) = 14.4` times the performance of a single TiDB node.

For a specified latency of a TiDB node, the TiDB performance varies depending on the different read-write ratios.
The performance of an 8 vCPU, 16 GiB TiDB node in different workloads is as follows:

    | Workload | TiDB performance (QPS)  |
    |----------|------------------------|
    | Read     | 18,900                 |
    | Mixed    | 15,500                 |
    | Write    | 18,000                 |

You can estimate the number of TiDB nodes according to your workload type, your overall expected performance (QPS), and the performance of a single TiDB node corresponding to the workload type as follows:
 `node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

When the number of TiDB nodes is less than 8, the performance deviation coefficient is nearly 0%, so the performance of 16 vCPU, 32 GiB TiDB nodes is roughly twice that of 8 vCPU, 16 GiB TiDB nodes. If the number of TiDB nodes exceeds 8, it is recommended to choose 16 vCPU, 32 GiB TiDB nodes as this will require fewer nodes, which means smaller performance deviation coefficient.

Suppose the overall expected performance is 100,000 QPS under a mixed workload, then the number of TiDB nodes can be calculated as follows:

`node num = ceil(100,000 / 15,500 ) = 7`

Since there are 7 nodes, the performance degradation coefficient is 0.

So, 7 TiDB nodes (8 vCPU, 16 GiB) can meet the performance requirements.

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB Cloud cluster.

## Size TiKV

TiKV is responsible for storing data. It is horizontally scalable.

You can configure node size, node quantity, and node storage for TiKV.

To learn performance test results of different cluster scales, see [TiDB Cloud Performance Reference](/tidb-cloud/tidb-cloud-performance-reference.md).

### TiKV node size

The supported node sizes include the following:

- 2 vCPU, 8 GiB (Beta)
- 4 vCPU, 16 GiB
- 8 vCPU, 32 GiB
- 8 vCPU, 64 GiB
- 16 vCPU, 64 GiB

> **Note:**
>
> If the node size of TiKV is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - 2 vCPU TiKV can only be used with 2 vCPU TiDB. 4 vCPU TiKV can only be used with 4 vCPU TiDB.
> - TiFlash is unavailable.

### TiKV node quantity

The number of TiKV nodes should be **at least 1 set (3 nodes in 3 different Available Zones)**.

TiDB Cloud deploys TiKV nodes evenly to all availability zones (at least 3) in the region you select to achieve durability and high availability. In a typical 3-replica setup, your data is distributed evenly among the TiKV nodes across all availability zones and is persisted to the disk of each TiKV node.

Although TiKV is mainly used for data storage, the performance of the TiKV node also varies depending on different workloads. Therefore, when planning the number of TiKV nodes, you need to estimate it according to both your **data volume** and **performance**, and then take the larger of the two estimates as the recommended node number.

> **Note:**
>
> When you scale your TiDB cluster, nodes in the 3 availability zones are increased or decreased at the same time. For how to scale in or scale out a TiDB cluster based on your needs, see [Scale Your TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md).

**Data volume**

You can calculate a recommended number of TiKV nodes according to your data volume as follows:

`node num = ceil( size of your data * compression ratio * the number of replicas ÷ TiKV storage usage ratio ÷ one TiKV capacity ÷ 3 ) * 3`

Generally, the usage ratio of TiKV storage is not recommended to exceed 80%, the number of replicas in TiDB Cloud is 3 by default, and the storage capacity of an 8 vCPU, 64 GiB TiKV node is 4096 GiB.

Supposing the size of your MySQL dump files is 20 TB, the TiDB compression ratio is 40%, the estimate number of TiKV nodes by data volume can be calculated as follows:
 `node num = ceil( 20 TB * 40% * 3 ÷ 0.8 ÷ 4096 GiB ÷ 3 ) * 3 = 9`

**Performance** 

The performance of the TiKV node is generally linearly scalable, but there is some performance degradation when there are a larger number of nodes. We estimate this performance degradation by increasing the performance degradation coefficient by 5% every time the number of nodes reaches 8. 
For example, when there are 9 TiKV nodes, the overall performance is `9 * (1 - 5%) = 8.55` times the performance of a single TiKV node. And when there are 18 TiKV nodes, the overall performance is `18 * (1 - 10%) = 16.2` times the performance of a single TiKV node.

Different workloads involve queries with varying read-write ratios and have different performance in the specified latency for a TiKV node.
The performance of the 8 vCPU, 32 GiB TiKV node in different workloads:

    | workload | TiKV performance (QPS) |
    |----------|------------------------|
    | Read     | 28,000                 |
    | Mixed    | 17,800                 |
    | Write    | 14,500                 |

We estimate the number of TiKV nodes based on the workload type, overall expected performance (QPS), and the performance of a single TiKV node under different workloads:
 `node num = ceil( overall expected perfromance / performance per node * (1 - performance degradation coefficient) )`

In the absence of performance degradation, the performance of 16 vCPU, 64 GiB TiKV nodes is roughly twice that of 8 vCPU, 32 GiB TiKV nodes. If the number of nodes is too large, it is recommended to choose 16 vCPU, 64 GiB TiKV nodes as this will require fewer nodes and have a smaller performance degradation coefficient.

Suppose the overall expected performance is 100,000 QPS under mixed workload, then the number of TiKV nodes can be calculated as follows:

`node num = ceil(100,000 / 17,800 ) = 6`

Since there are 6 nodes, the performance degradation coefficient is 0.

So, 6 TiKV nodes (8 vCPU, 32 GiB) can meet the performance requirements.

### TiKV node storage

The supported node storage of different TiKV node sizes is as follows:

| Node size | Min node storage | Max node storage | Default node storage |
|:---------:|:----------------:|:----------------:|:--------------------:|
| 2 vCPU    | 200 GiB          | 500 GiB          | 200 GiB              |
| 4 vCPU    | 200 GiB          | 2048 GiB         | 500 GiB              |
| 8 vCPU    | 200 GiB          | 4096 GiB         | 500 GiB              |
| 16 vCPU   | 200 GiB          | 4096 GiB         | 500 GiB              |

> **Note:**
>
> You cannot decrease the TiKV node storage after the cluster creation.

## Size TiFlash

TiFlash synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box. It is horizontally scalable.

You can configure node size, node quantity, and node storage for TiFlash.

### TiFlash node size

The supported node sizes include the following:

- 8 vCPU, 64 GiB
- 16 vCPU, 128 GiB

Note that TiFlash is unavailable when the vCPU size of TiDB or TiKV is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**.

### TiFlash node quantity

TiDB Cloud deploys TiFlash nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash nodes in each TiDB Cloud cluster and create at least two replicas of the data for high availability in your production environment.

The minimum number of TiFlash nodes depends on the TiFlash replica counts for specific tables:

Minimum number of TiFlash nodes: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

For example, if you configure the node storage of each TiFlash node on AWS as 1024 GiB, and set 2 replicas for table A (the compressed size is 800 GiB) and 1 replica for table B (the compressed size is 100 GiB), then the required number of TiFlash nodes is as follows:

Minimum number of TiFlash nodes: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlash node storage

The supported node storage of different TiFlash node sizes is as follows:

| Node size | Min node storage | Max node storage | Default node storage |
|:---------:|:----------------:|:----------------:|:--------------------:|
| 8 vCPU    | 200 GiB          | 2048 GiB         | 500 GiB              |
| 16 vCPU   | 200 GiB          | 2048 GiB         | 500 GiB              |

> **Note:**
>
> You cannot decrease the TiFlash node storage after the cluster creation.
