---
title: TiDB X Architecture
summary: The architecture introduction of the TiDB X
---

# TiDB X Introduction

TiDB X represents a fundamental architectural shift in the TiDB evolution, transitioning from a classic "Share-Nothing" distributed database to a modern, "Share-Everything" Service-Oriented Architecture (SOA). Designed for the AI era and massive cloud scalability, TiDB X leverages Object Storage (e.g., Amazon S3) as the single source of truth.

TiDB classic architecture decouples storage from compute entirely, TiDB X introduces a novel "Separation of Compute and Compute" design that isolates online transactional workloads from heavy maintenance tasks. The result is a system that offers elastic scalability, predictable performance, and optimized Total Cost of Ownership (TCO).

This document details the challenges of TiDB classic, the architecture and key innovations of TiDB X.

# Challenges of TiDB Classic

The motivation of TiDB X is documented in the blog [The Making of TiDB X: Origins, Architecture, and What’s to Come](https://www.pingcap.com/blog/tidbx-origins-architecture/)

TiDB Classic has faced several challenges in large-scale production environments, primarily stemming from its "Share-nothing" architecture.

## Scalability Limitations

In TiDB Classic, scaling out (adding nodes) or scaling in (removing nodes) requires physically copying massive amounts of data (SST files) between nodes. This process is time-consuming for large datasets and can impact online traffic due to the heavy CPU and I/O required to move data.

The underlying storage engine (RocksDB) in TiDB Classic uses a single LSM-tree protected by a global mutex. This creates a scalability ceiling where the system struggles to handle large datasets (e.g., 3TB+ data per tikv node or 100k+ SST files), preventing it from utilizing the full capacity of the hardware.

## Stability and Performance Challenges

Heavy write traffic triggers massive local compaction jobs to merge SST files. In the Classic architecture, these compaction jobs run on the same TiKV nodes serving online traffic, consuming significant CPU and I/O resources and can impact the online traffic.

There is no physical isolation between logical regions and physical SST files. Operations like adding an index or moving a region (balancing) create compaction overhead that competes directly with user queries, leading to performance jitter. Under heavy write pressure, if the background compaction can not keep up with the forground write traffic, the system can trigger flow control mechanisms to protect the storage engine, which results in write throughput throttle and latency spikes for the application.

## Lack of Cost Effectiveness

To keep the production system stable and ensure good performance during peak traffic, customers are forced to over-provision hardware resources.  Resources must be planned for the "high water mark" of both online traffic and heavy background tasks. Besides, data size on single tikv nodes is limited, users often have to add more expensive compute nodes just to get more storage capacity, even if they don't need the extra CPU power.

## Heavy Background Job Interference

Resource Conflict: Heavy background jobs—such as scale operations, backup, compaction, analyze, and data import (Load Data)—run on the same nodes as foreground OLTP traffic.

Performance Degradation: These tasks are resource-intensive and often interfere with online traffic, causing latency increases or throughput drops.

Maintenance Windows: Due to this interference, administrators often have to schedule maintenance operations (like index creation or backups) during off-peak hours to avoid impacting the business, reducing operational agility.


# TiDB X Architecture

This architecture represents a modern, cloud-native Share-Everything design that decouples storage from compute and further separates foreground transaction processing from background maintenance tasks.

![TiDB X Architecture](/media/tidb-x/tidb-x-architecture.png)

## Object Storage Support

As depicted in the "Object storage" layer of the diagram, TiDB X utilizes object storage (such as Amazon S3) as the single source of truth for all data. Unlike classic architectures where data resides on local disks, here the persistent copy of all data is stored in the shared object storage layer. The "Shared Cache Layer" above it (Row Engine and Columnar Engine) acts as a high-performance cache to ensure low latency. Because the authoritative data is already in robust object storage, backing up simply relys on incremental Raft logs and metadata stored in S3. This allows backups to finish in seconds no matter of the data volumes. New compute or cache nodes can come online almost instantly because they do not need to physically copy data from other nodes. They simply connect to the object storage and load the necessary data, making scale-out operations significantly faster.

## Auto-Scaling Mechanism

The architecture is designed for elasticity, facilitated by the "Load balancer" and the stateless nature of the "Isolated SQL Layer".

Scaling within Seconds: Since compute nodes (in the SQL layer) are decoupled from the data (in object storage), the system can auto-scale by adding or removing compute pods in seconds to match real-time workload demands.

Pay-As-You-Go Model: This elasticity enables a true consumption-based pricing model. Users no longer need to provision for peak load 24/7; the system automatically provisions resources during traffic spikes and scales down during quiet periods to minimize costs.

## Microservice and Workload Isolation

The architecture diagram highlights a sophisticated separation of duties, ensuring that different types of work do not interfere with each other.

Isolated SQL Layer: The top "Isolated SQL Layer" shows separate groups of Compute nodes. This allows for multi-tenancy or workload isolation, where different applications or users can have dedicated compute resources while sharing the same underlying data.

Shared Services (Microservices): The bottom layer, "Shared Services", breaks down heavy database tasks into independent microservices like Compaction, Analyze, and DDL.

Zero Impact from Heavy Tasks: Expensive background operations—such as adding an index, Online DDL, or massive data imports—are offloaded to the Shared Services layer. This ensures that heavy jobs never compete for CPU or memory with the "Compute" nodes serving online user traffic, guaranteeing predictable performance for critical applications.

Independent Scaling: Each component (Gateway, SQL Compute, Cache, Background Services) can be scaled independently based on specific bottlenecks, and failovers are smoother as services are loosely coupled.

# TiDB X Key innovations

Here is the figure to show the key archtecture difference between TiDB Classic and TiDB X.

![TiDB Classic vs TiDB X](/media/tidb-x/tidb-classic-vs-tidb-x-1.png)

## Separation of Compute and Compute

While TiDB Classic already separated compute (SQL) from storage (TiKV), TiDB X introduces a secondary layer of separation within the compute layer itself:

- Lightweight Compute: Dedicated resources for lightweight OLTP workloads (user queries).
- Heavy Compute: A separate "Elastic Compute Pool" for heavy jobs (e.g., compaction, backups, scale operations, analyze, load data, and slow queries).

By offloading heavy tasks to the elastic compute pool, TiDB X ensures that maintenance tasks and heavy background jobs do not interfere with online transaction performance. The system delivers stable, predictable latency for OLTP workloads even during heavy operations.

## Transition to "Share-Everything" Architecture

TiDB X moves away from the classic "Share-Nothing" architecture (where data is copied between tikv nodes) to a modern "Share-Everything" model. Object storage as single source of truth: All persistent data relies on object storage (like S3) rather than local disks. This removes the need for physical data copying during scaling, enabling rapid elasticity.

The introduction of the object storage will not impact the performance of forground read and write operations. For the read operation, only the heavy read request will be offloaded to the remote elastic coprocessor workers. For the write operation, the interaction with object storage is asynchronous and will not impact the write performance. The Raft log is perssisted on local disk first, the Raft WAL(Write-Ahead Log) chunks are uploaded to object storage in background later. When the data in a MemTable is full and flushed to local disk, the region leader will upload the sst file to object storage. After the remote compaction is done on elastic compaction workers, the tikv nodes will be notified to load the compacted sst files from object stroage.


## Elastic Scalability (5x-10x Faster)

Because data resides in shared object storage, adding or removing nodes no longer requires massive data migration between machines. Scale-in and scale-out operations are 5 to 10 times faster than TiDB Classic and have zero impact on live traffic.

## Elastic TCO (Pay-As-You-Go)

TiDB Classic required over-provisioning hardware to handle peak traffic and background tasks (like compaction overhead) simultaneously. TiDB X enables auto-scaling, allowing users to pay only for the resources they use (Pay-As-You-Go). Background resources for heavy jobs spin up on demand and spin down when finished, eliminating wasted cost.

## From LSM tree to LSM Forest

In the classic architecture, every TiKV node runs a single, massive RocksDB instance. This means all data from thousands of different "Regions" (logical data shards) is mixed together into one giant "Single LSM Tree" structure. Because data is mixed, operations like moving a Region, scaling in/out, or importing data require rewriting massive amounts of existing data (compaction) to separate or merge it. This consumes huge CPU/IO resources and impacts online traffic. The single LSM tree is protected by a global mutex. As data size grows (3TB+) or file count increases (100k+ SST files), contention on this global lock will impact both the read and write operations.

TiDB X completely redesigns the storage engine by moving from a single tree to an LSM Forest. Instead of one giant tree for all data, TiDB X assigns each Region its own separate, independent LSM Tree. The most critical benefit of this physical isolation is the elimination of compaction overhead during cluster operations (scale-in, scale-out, region movement, load data). Operations on one Region (like a heavy write or a split) are isolated to its specific tree. There is no global mutex lock contention.

![TiDB Classic vs TiDB X](/media/tidb-x/tidb-classic-vs-tidb-x-2.png)