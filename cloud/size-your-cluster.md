---
title: Size Your TiDB Cluster
summary: Learn how to select the number of nodes for your TiDB cluster.
---

# Size Your TiDB Cluster

This document describes how to select the number of nodes for your TiDB cluster.

## Size TiDB

TiDB is for computing only and does not store data. It is horizontally scalable. Each TiDB Cloud cluster requires at least two TiDB nodes.

## Size TiKV

TiKV is responsible for storing data. It is horizontally scalable and the number of nodes should be **at least 1 set (3 nodes in 3 different Available Zones)**.

Data in each TiDB Cloud cluster has 3 replicas, and each replica is distributed in a different availability zone.

> **Note:**
>
> When you scale your TiDB cluster, nodes in the 3 availability zones are increased or decreased at the same time. For how to scale in or scale out a TiDB cluster based on your needs, see [Scale Your TiDB Cluster]\cloud\scale-tidb-cluster.md).

Minimum number of TiKV nodes: `ceil(compressed size of your data ÷ one TiKV capacity) × the number of replicas`

Supposing the size of your MySQL dump files is 5 TB and the TiDB compression ratio is 70%, the storage needed is 3584 GB.

For example, if you configure the storage size of each TiKV node on AWS as 1024 GB, the required number of TiKV nodes is as follows:

Minimum number of TiKV nodes: `ceil(3584 ÷ 1024) × 3 = 12`

## Size TiFlash<sup>beta</sup>

TiFlash<sup>beta</sup> synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box, It is horizontally scalable. You can specify TiFlash<sup>beta</sup> nodes of Dedicated Tier cluster.

The minimum number of TiFlash<sup>beta</sup> nodes depends on the TiFlash<sup>beta</sup> replica counts for specific tables:

Minimum number of TiFlash<sup>beta</sup> nodes: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

For example, if you configure the storage size of each TiFlash<sup>beta</sup> node on AWS as 1024 GB, and set 2 replicas for table A (the compressed size is 800 GB) and 1 replica for table B (the compressed size is 100 GB), then the required number of TiFlash<sup>beta</sup> nodes is as follows:

Minimum number of TiFlash<sup>beta</sup> nodes: `min((800 GB * 2 + 100 GB * 1) / 1024 GB, max(2, 1)) ≈ 2`
