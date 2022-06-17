---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# Determine Your TiDB Size

This document describes how to determine the size of your TiDB cluster.

## Size TiDB

TiDB is for computing only and does not store data. It is horizontally scalable.

You can configure both vCPUs size and node quantity for TiDB.

### TiDB vCPUs size

The supported vCPU size includes 4 vCPU (Beta), 8 vCPU, and 16 vCPU.

> **Note:**
>
> If the vCPU size of TiDB is set as **4 vCPU (Beta)**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - TiDB can only be used with TiKV with 4 vCPU.
> - TiFlash<sup>beta</sup> is not supported.

### TiDB node quantity

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB Cloud cluster.

## Size TiKV

TiKV is responsible for storing data. It is horizontally scalable.

You can configure vCPUs size, node quantity, and storage size for TiKV.

### TiKV vCPUs size

The supported size includes 4 vCPU (Beta), 8 vCPU, and 16 vCPU.

> **Note:**
>
> If the vCPUs size of TiKV is set as **4 vCPU (Beta)**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - TiKV can only be used with TiDB with 4 vCPU.
> - TiFlash<sup>beta</sup> is not supported.

### TiKV node quantity

The number of TiKV nodes should be **at least 1 set (3 nodes in 3 different Available Zones)**.

TiDB Cloud deploys TiKV nodes evenly to all availability zones (at least 3) in the region you select to achieve durability and high availability. In a typical 3-replica setup, your data is distributed evenly among the TiKV nodes across all availability zones and is persisted to the disk of each TiKV node.

> **Note:**
>
> When you scale your TiDB cluster, nodes in the 3 availability zones are increased or decreased at the same time. For how to scale in or scale out a TiDB cluster based on your needs, see [Scale Your TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md).

Minimum number of TiKV nodes: `ceil(compressed size of your data ÷ one TiKV capacity) × the number of replicas`

Supposing the size of your MySQL dump files is 5 TB and the TiDB compression ratio is 70%, the storage needed is 3584 GB.

For example, if you configure the storage size of each TiKV node on AWS as 1024 GB, the required number of TiKV nodes is as follows:

Minimum number of TiKV nodes: `ceil(3584 ÷ 1024) × 3 = 12`

### TiKV storage size

You can configure the TiKV storage size only when you create or restore a cluster.

## Size TiFlash<sup>beta</sup>

TiFlash<sup>beta</sup> synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box. It is horizontally scalable.

You can configure vCPUs size, node quantity, and storage size for TiFlash<sup>beta</sup>.

### TiFlash<sup>beta</sup> vCPUs size

The supported vCPUs size includes 8 vCPU and 16 vCPU.

If the vCPUs size of TiDB or TiKV is set as **4 vCPU (Beta)**, TiFlash<sup>beta</sup> is not supported.

### TiFlash<sup>beta</sup> node quantity

TiDB Cloud deploys TiFlash<sup>beta</sup> nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash<sup>beta</sup> nodes in each TiDB Cloud cluster and create at least 2 replicas of the data for high availability in your production environment.

The minimum number of TiFlash<sup>beta</sup> nodes depends on the TiFlash<sup>beta</sup> replica counts for specific tables:

Minimum number of TiFlash<sup>beta</sup> nodes: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

For example, if you configure the storage size of each TiFlash<sup>beta</sup> node on AWS as 1024 GB, and set 2 replicas for table A (the compressed size is 800 GB) and 1 replica for table B (the compressed size is 100 GB), then the required number of TiFlash<sup>beta</sup> nodes is as follows:

Minimum number of TiFlash<sup>beta</sup> nodes: `min((800 GB * 2 + 100 GB * 1) / 1024 GB, max(2, 1)) ≈ 2`

### TiFlash<sup>beta</sup> storage size

You can configure the TiFlash<sup>beta</sup> storage size only when you create or restore a cluster.

## Performance reference

This section provides the performance test results of 6 popular scales of TiDB clusters, which can be taken as a reference when you determine the cluster size.

### Test environment

- TiDB version: 5.4.0
- Transaction model：

    - TPCC 5000, about 366 G
    - sysbench tablesize = 10000000, tablecount = 16

        - oltp_insert
        - oltp_point_select
        - oltp_read_write
        - oltp_update_index
        - oltp_update_nonindex

### Performance

Generally, TiDB and TiKV with 4 vCPUs are recommended for learning and exploring TiDB Cloud; TiDB and TiKV with 8 vCPUs and 16 vCPUs are recommended for production applications with mission-critical workloads.

You can click any of the following scales to check its performance data.

<details>
<summary>TiDB: 4 vCPU * 2; TiKV: 4 vCPU * 3</summary>

- Optimal performance with lower latency

    | Transaction model    | Threads | tpmC(TPCC)/TPS | QPS    | Latency (ms ) | IO (MBps ) |
    |----------------------|---------|----------------|--------|----------------|-------------|
    | TPCC                 | 300     | 14,532         | 13,137 | 608            | 13.5        |
    | oltp_insert          | 300     | 8,848          | 8,848  | 36             | 13          |
    | oltp_point_select    | 600     | 46,224         | 46,224 | 13             | 8           |
    | oltp_read_write      | 150     | 719            | 14,385 | 209            | 29          |
    | oltp_update_index    | 150     | 4,346          | 4,346  | 35             | 10          |
    | oltp_update_nonindex | 600     | 13,603         | 13,603 | 44             | 6           |

- Maximum TPS and QPS

    | Transaction Model    | Threads | Maximum TPS/tpmC | Maximum QPS | Latency (ms ) | IO (MBps ) |
    |----------------------|---------|------------------|-------------|---------------|------------|
    | TPCC                 | 1,200   | 15,208           | 13,748      | 2,321.00      | 14.4       |
    | oltp_insert          | 1,500   | 11,601           | 11,601      | 129           | 18         |
    | oltp_point_select    | 600     | 46,224           | 46,224      | 13            | 8          |
    | oltp_read_write      | 150     | 14,385           | 719         | 209           | 29         |
    | oltp_update_index    | 1,200   | 6,526            | 6,526       | 184           | 13         |
    | oltp_update_nonindex | 1,500   | 14,351           | 14,351      | 105           | 9          |

</details>

<details>
<summary>TiDB: 8 vCPU * 2; TiKV: 8 vCPU * 3</summary>

- Optimal performance with lower latency

    | Transaction model    | Threads | tpmC(TPCC)/TPS | QPS    | Latency ( ms ) | IO ( MBps ) |
    |----------------------|---------|----------------|--------|----------------|-------------|
    | TPCC                 | 600     | 32,266         | 29,168 | 548            | 29.1        |
    | oltp_insert          | 600     | 17,831         | 17,831 | 34             | 26          |
    | oltp_point_select    | 600     | 93,287         | 93,287 | 6              | 16          |
    | oltp_read_write      | 300     | 29,729         | 1,486  | 202            | 61          |
    | oltp_update_index    | 300     | 9,415          | 9,415  | 32             | 19          |
    | oltp_update_nonindex | 1,200   | 31,092         | 31,092 | 39             | 12          |

- Maximum TPS and QPS

    | Transaction Model    | Threads | Maximum TPS/tpmC | Maximum QPS | Latency (ms ) | IO (MBps ) |
    |----------------------|---------|------------------|-------------|---------------|------------|
    | TPCC                 | 1,200   | 33,394           | 30,188      | 1,048.00      | 31.2       |
    | oltp_insert          | 2,000   | 23,633           | 23,633      | 84            | 31         |
    | oltp_point_select    | 600     | 93,287           | 93,287      | 6             | 16         |
    | oltp_read_write      | 600     | 30,464           | 1,523       | 394           | 64         |
    | oltp_update_index    | 2,000   | 15,146           | 15,146      | 132           | 27         |
    | oltp_update_nonindex | 2,000   | 34,505           | 34,505      | 58            | 18         |

</details>

<details>
<summary>TiDB: 8 vCPU * 4; TiKV: 8 vCPU * 6</summary>

- Optimal performance with lower latency

    | Transaction model    | Threads | tpmC(TPCC)/TPS | QPS     | Latency ( ms ) | IO ( MBps ) |
    |----------------------|---------|----------------|---------|----------------|-------------|
    | TPCC                 | 1,200   | 62,918         | 56,878  | 310            | 16.3        |
    | oltp_insert          | 1,200   | 33,892         | 33,892  | 23             | 14          |
    | oltp_point_select    | 1,200   | 185,574        | 181,255 | 4              | 9           |
    | oltp_read_write      | 600     | 59,160         | 2,958   | 127            | 36          |
    | oltp_update_index    | 600     | 18,735         | 18,735  | 21             | 12          |
    | oltp_update_nonindex | 2,400   | 60,629         | 60,629  | 23             | 7           |

- Maximum TPS and QPS

    | Transaction Model    | Threads | Maximum TPS/tpmC | Maximum QPS | Latency (ms ) | IO (MBps ) |
    |----------------------|---------|------------------|-------------|---------------|------------|
    | TPCC                 | 2,400   | 65,452           | 59,169      | 570           | 17.6       |
    | oltp_insert          | 4,000   | 47,029           | 47,029      | 43            | 17         |
    | oltp_point_select    | 1,200   | 185,574          | 181,255     | 4             | 9          |
    | oltp_read_write      | 1,200   | 60,624           | 3,030       | 197           | 37         |
    | oltp_update_index    | 4,000   | 30,140           | 30,140      | 67            | 16         |
    | oltp_update_nonindex | 4,000   | 68,664           | 68,664      | 29            | 10         |

</details>

<details>
<summary>TiDB: 16 vCPU * 2; TiKV: 16 vCPU * 3</summary>

- Optimal performance with lower latency

    | Transaction model    | Threads | tpmC(TPCC)/TPS | QPS     | Latency ( ms ) | IO ( MBps ) |
    |----------------------|---------|----------------|---------|----------------|-------------|
    | TPCC                 | 1,200   | 67,941         | 61,419  | 540            | 65.2        |
    | oltp_insert          | 1,200   | 35,096         | 35,096  | 34             | 45          |
    | oltp_point_select    | 1,200   | 228,600        | 228,600 | 5              | 29          |
    | oltp_read_write      | 600     | 73,150         | 3,658   | 164            | 153         |
    | oltp_update_index    | 600     | 18,886         | 18,886  | 32             | 46          |
    | oltp_update_nonindex | 2,000   | 63,837         | 63,837  | 31             | 33          |

- Maximum TPS and QPS

    | Transaction Model    | Threads | Maximum TPS/tpmC | Maximum QPS | Latency (ms ) | IO (MBps ) |
    |----------------------|---------|------------------|-------------|---------------|------------|
    | TPCC                 | 1,200   | 67,941           | 61,419      | 540           | 65.2       |
    | oltp_insert          | 2,000   | 43,338           | 43,338      | 46            | 50         |
    | oltp_point_select    | 1,200   | 228,600          | 228,600     | 5             | 29         |
    | oltp_read_write      | 1,200   | 73,631           | 3,682       | 326           | 158        |
    | oltp_update_index    | 3,000   | 29,576           | 29,576      | 101           | 64         |
    | oltp_update_nonindex | 3,000   | 64,624           | 64,624      | 46            | 33         |

</details>

<details>
<summary>TiDB: 16 vCPU * 4; TiKV: 16 vCPU * 6</summary>

- Optimal performance with lower latency

    | Transaction model    | Threads | tpmC(TPCC)/TPS | QPS     | Latency ( ms ) | IO ( MBps ) |
    |----------------------|---------|----------------|---------|----------------|-------------|
    | TPCC                 | 2,400   | 133,164        | 120,380 | 305            | 35.3        |
    | oltp_insert          | 2,400   | 69,139         | 69,139  | 22             | 25          |
    | oltp_point_select    | 2,400   | 448,056        | 448,056 | 4              | 17          |
    | oltp_read_write      | 1,200   | 145,568        | 7,310   | 97             | 80          |
    | oltp_update_index    | 1,200   | 36,638         | 36,638  | 20             | 25          |
    | oltp_update_nonindex | 4,000   | 125,129        | 125,129 | 17             | 19          |

- Maximum TPS and QPS

    | Transaction Model    | Threads | Maximum TPS/tpmC | Maximum QPS | Latency (ms ) | IO (MBps ) |
    |----------------------|---------|------------------|-------------|---------------|------------|
    | TPCC                 | 2,400   | 133,164          | 120,380     | 305           | 35.3       |
    | oltp_insert          | 4,000   | 86,242           | 86,242      | 25            | 29         |
    | oltp_point_select    | 2,400   | 448,056          | 448,056     | 4             | 17         |
    | oltp_read_write      | 2,400   | 146,526          | 7,326       | 172           | 82         |
    | oltp_update_index    | 6,000   | 58,856           | 58,856      | 51            | 34         |
    | oltp_update_nonindex | 6,000   | 128,601          | 128,601     | 24            | 19         |

</details>

As you can see from the performance data, if you want lower latency, `TiDB: 8 vCPU * 4; TiKV: 8 vCPU * 6` is a better choice than `TiDB: 16 vCPU * 2; TiKV: 16 vCPU * 3`, but `TiDB: 8 vCPU * 4; TiKV: 8 vCPU * 6` gets less QPS.