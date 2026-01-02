---
title: TiDB X Architecture
summary: An introduction to the TiDB X architecture
---

# TiDB X Introduction

TiDB X represents a fundamental architectural shift in the evolution of TiDB, transitioning from a classic 'Shared-Nothing' architecture to a modern 'Shared-Storage' system. Built on Object Storage (e.g., Amazon S3), this design delivers the massive cloud scalability needed for the AI era.

While classic TiDB decouples storage from compute, TiDB X introduces a novel "Separation of Compute and Compute" design that isolates online transactional workloads from heavy maintenance tasks. The result is a system that offers elastic scalability, predictable performance, and optimized Total Cost of Ownership (TCO).

This document details the challenges of the classic TiDB architecture, the architecture of TiDB X, and its key innovations.

# The Successes and Challenges of Classic TiDB

## Why Classic TiDB Changed the Game

The "Shared-Nothing" architecture of classic TiDB, effectively overcoming the limitations of traditional monolithic databases. By decoupling compute from storage and utilizing the Raft consensus algorithm, it delivered a level of resilience and scale that defined the modern NewSQL era.

Its success was built on several foundational strengths:

- Massive Horizontal Scalability: Classic TiDB proved that you didn't have to choose between scale and SQL. It allowed businesses to scale both read and write performance linearly with their workload, easily reaching millions of QPS and supporting massive clusters exceeding 1+ PiB of data.
- True HTAP Capabilities: It unified transactional and analytical processing. By pushing down heavy aggregation and join operations to TiFlash (the columnar engine), it provided predictable, real-time analytics on fresh transactional data without complex ETL pipelines.
- Non-Blocking Operations: Its implementation of Fully Online DDL meant that schema changes were non-blocking for reads and writes, allowing businesses to evolve their data models with minimal impact on latency or uptime.
- Always-Online Availability: The architecture supported seamless cluster upgrades and scaling operations (up/down), ensuring critical services remained online during maintenance.
- Freedom from Lock-in: As an open-source solution supporting AWS, GCP, and Azure, it offered true cloud neutrality, preventing vendor lock-in.

## The Architectural Ceiling: Challenges Hard to Overcome

Despite these massive achievements, the "Shared-Nothing" architecture of classic TiDB, where storage and compute are tightly coupled on local nodes—eventually hit physical limitations in extreme large-scale environments. As data volumes exploded and cloud-native expectations evolved, inherent structural challenges emerged that were difficult to resolve without a fundamental redesign.

- Scalability Limitations: In classic TiDB, scaling out (adding nodes) or scaling in (removing nodes) requires physically copying massive amounts of data (SST files) between nodes. This process is time-consuming for large datasets and can impact online traffic due to the heavy CPU and I/O required to move data.
The underlying storage engine (RocksDB) in classic TiDB uses a single LSM-tree protected by a global mutex. This creates a scalability ceiling where the system struggles to handle large datasets (e.g., 3TB+ data per tikv node or 100k+ SST files), preventing it from utilizing the full capacity of the hardware.

- Stability and Performance Challenges: Heavy write traffic triggers massive local compaction jobs to merge SST files. In the Classic architecture, these compaction jobs run on the same TiKV nodes serving online traffic, consuming significant CPU and I/O resources and can impact the online traffic.
There is no physical isolation between logical regions and physical SST files. Operations like adding an index or moving a region (balancing) create compaction overhead that competes directly with user queries, leading to performance jitter. Under heavy write pressure, if the background compaction cannot keep up with the foreground write traffic, the system can trigger flow control mechanisms to protect the storage engine, which results in write throughput throttling and latency spikes for the application.

- Lack of Cost Effectiveness: To keep the production system stable and ensure good performance during peak traffic, customers are forced to over-provision hardware resources.  Resources must be planned for the "high water mark" of both online traffic and heavy background tasks. Besides, data size on single tikv nodes is limited, users often have to add more expensive compute nodes just to get more storage capacity, even if they don't need the extra CPU power.

## The Motivation of TiDB X

These challenges were constraints of the physical binding of data to compute. To break through these ceilings—to achieve 10x faster scaling, zero-interference background tasks, and true pay-as-you-go elasticity. We need to move from "Shared-Nothing" architecute to TiDB X.

The motivation of TiDB X is documented in the blog [The Making of TiDB X: Origins, Architecture, and What’s to Come](https://www.pingcap.com/blog/tidbx-origins-architecture/)

# TiDB X Architecture

TiDB X is a cloud-native evolution that unlocks the full potential of classic TiDB’s original distributed design. TiDB X inherits the advantages of classic TiDB:

- The SQL layer (tidb-server) was already stateless. It handled query parsing, optimization, and execution but never stored persistent data.
- TiProxy(or load balancers) is designed to maintain persistent client connections and route SQL traffic seamlessly. TiProxy originally supported online upgrades, now became a natural gateway service.
- TiKV’s dynamic range-based sharding already existed, called Regions (256MB by default). TiKV splits data into millions of regions. The system automatically managed the movement and balancing of these Regions across nodes.

TiDB X evolves the proven stateless SQL and dynamic sharding foundation of classic TiDB by replacing the local "Shared-Nothing" storage with a cloud-native "Shared-Storage" object storage backbone, enabling a novel "Separation of Compute and Compute" that offloads heavy tasks to elastic pools for instant scalability and predictable performance.

![TiDB X Architecture](/media/tidb-x/tidb-x-architecture.png)

## Object Storage Support

As depicted in the "Object storage" layer of the diagram, TiDB X utilizes object storage (such as Amazon S3) as the single source of truth for all data. Unlike classic architectures where data resides on local disks, in TiDB X the persistent copy of all data is stored in the shared object storage layer. The "Shared Cache Layer" above it (Row Engine and Columnar Engine) acts as a high-performance cache to ensure low latency. Because the authoritative data is already in robust object storage, backing up simply relies on incremental Raft logs and metadata stored in S3. This allows backups to finish in seconds, regardless of the data volume. New compute or cache nodes can come online almost instantly because they do not need to physically copy data from other nodes. They simply connect to the object storage and load the necessary data, making scale-out operations significantly faster.

## Auto-Scaling Mechanism

The architecture is explicitly designed for elasticity, facilitated by the load balancer and the stateless nature of the "Isolated SQL Layer". Since the compute nodes in the SQL layer are decoupled from the data residing in object storage, the system can auto-scale by adding or removing compute pods in seconds to match real-time workload demands. This technical elasticity enables a true consumption-based Pay-As-You-Go pricing model. Users no longer need to provision resources for peak load 24/7; the system automatically provisions resources during traffic spikes and scales down during quiet periods to minimize costs.

## Microservice and Workload Isolation

The architecture diagram highlights a sophisticated separation of duties, ensuring that different types of work do not interfere with each other. The top "Isolated SQL Layer" consists of separate groups of compute nodes, which allows for multi-tenancy or workload isolation where different applications can have dedicated compute resources while sharing the same underlying data. Beneath this, the "Shared Services" layer breaks down heavy database tasks into independent microservices for operations like compaction, analyze, and DDL. By offloading expensive background operations—such as adding an index, Online DDL, or massive data imports—to the Shared Services layer, the system ensures these heavy jobs never compete for CPU or memory with the "Compute" nodes serving online user traffic. This guarantees predictable performance for critical applications and allows each component—Gateway, SQL Compute, Cache, and Background Services—to scale independently based on specific bottlenecks.

# Key innovations of TiDB X

The following figure shows the key architectural differences between classic TiDB and TiDB X.

![Classic TiDB vs TiDB X](/media/tidb-x/tidb-classic-vs-tidb-x-1.png)

## Separation of Compute and Compute

While classic TiDB already separats compute (SQL) from storage (TiKV), TiDB X introduces a secondary layer of separation within both the SQL layer and the storage layer themself:

- Lightweight Compute: Dedicated resources for lightweight OLTP workloads (user queries).
- Heavy Compute: A separate "Elastic Compute Pool" for heavy jobs (e.g., compaction, backups, scale operations, analyze, load data, and slow queries).

By offloading heavy tasks to the elastic compute pool, TiDB X ensures that maintenance tasks and heavy background jobs do not interfere with online transaction performance. The system delivers stable, predictable latency for OLTP workloads even during heavy operations.

## Transition to "Shared-Storage" Architecture

TiDB X moves away from the classic "Shared-Nothing" architecture (where data is copied between `TiKV` nodes) to a modern "Shared-Storage" model. In this model, object storage (like S3) serves as the single source of truth for all persistent data, rather than local disks. This removes the need for physical data copying during scaling, enabling rapid elasticity.

The introduction of object storage does not impact the performance of foreground read and write operations. For read operations, only heavy read requests are offloaded to the remote elastic coprocessor workers. For write operations, the interaction with object storage is asynchronous and does not impact write performance. The Raft log is persisted on local disk first, and then the Raft WAL (Write-Ahead Log) chunks are uploaded to object storage in the background. When the data in a MemTable is full and flushed to local disk, the region leader uploads the SST file to object storage. After the remote compaction is done on elastic compaction workers, the `TiKV` nodes are notified to load the compacted SST files from object storage.


## Elastic Scalability (5x-10x Faster)

Because data resides in shared object storage, adding or removing nodes no longer requires massive data migration between machines. Scale-in and scale-out operations are 5 to 10 times faster than classic TiDB and have zero impact on live traffic.

## Elastic TCO (Pay-As-You-Go)

classic TiDB required over-provisioning hardware to handle peak traffic and background tasks (like compaction overhead) simultaneously. TiDB X enables auto-scaling, allowing users to pay only for the resources they use (Pay-As-You-Go). Background resources for heavy jobs spin up on demand and spin down when finished, eliminating wasted cost.

## From LSM-tree to LSM forest

In the classic architecture, every TiKV node runs a single, massive RocksDB instance. This means all data from thousands of different "Regions" (logical data shards) is mixed together into one giant "single LSM-tree" structure. Because data is mixed, operations like moving a Region, scaling in/out, or importing data require rewriting massive amounts of existing data (compaction) to separate or merge it. This consumes huge CPU and I/O resources and impacts online traffic. The single LSM-tree is protected by a global mutex. As data size grows (3TB+) or file count increases (100k+ SST files), contention on this global lock will impact both the read and write operations.

While TiDB X retains the logical region concept from classic TiDB, it fundamentally redesigns the storage engine by shifting from a single LSM tree to an LSM Forest. Instead of one giant tree for all data, TiDB X assigns each region its own separate, independent LSM Tree. The most critical benefit of this physical isolation is the elimination of compaction overhead during cluster operations (scale-in, scale-out, region movement, load data). Operations on one Region (like a heavy write or a split) are isolated to its specific tree. There is no global mutex lock contention.

![Classic TiDB vs TiDB X](/media/tidb-x/tidb-classic-vs-tidb-x-2.png)