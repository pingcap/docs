---
title: TiDB X Architecture
summary: Learn how the shared-storage, cloud-native TiDB X architecture delivers elastic scalability, predictable performance, and optimized total cost of ownership.
---

# TiDB X Architecture

TiDB X is a new distributed SQL architecture that makes cloud-native object storage the backbone of TiDB. This architecture enables elastic scalability, predictable performance, and optimized total cost of ownership (TCO) for AI-era workloads.

TiDB X represents a fundamental evolution from [classic TiDB](/tidb-architecture.md)'s shared-nothing architecture to a cloud-native shared-storage architecture. By leveraging object storage as the shared persistent storage layer, TiDB X introduces a separation of compute workloads that isolates online transactional workloads from resource-intensive background tasks.

This document introduces the TiDB X architecture, explains the motivation behind TiDB X, and describes the key innovations compared with the classic TiDB architecture.

## Limitations of classic TiDB

This section analyzes the architecture of classic TiDB and its limitations that motivate the development of TiDB X.

### Strengths of classic TiDB

The shared-nothing architecture of classic TiDB addresses the limitations of traditional monolithic databases. By decoupling compute from storage and utilizing the Raft consensus algorithm, it provides the resilience and scalability required for distributed SQL workloads.

The classic TiDB architecture is built on several foundational capabilities:

- Horizontal scalability: It supports linear scaling for both read and write performance. Clusters can scale to handle millions of queries per second (QPS) and manage over 1 PiB of data across tens of millions of tables.
- Hybrid Transactional and Analytical Processing (HTAP): It unifies transactional and analytical workloads. By pushing down heavy aggregation and join operations to TiFlash (the columnar storage engine), it provides predictable, real-time analytics on fresh transactional data without complex ETL pipelines.
- Non-blocking schema changes: It utilizes a fully online DDL implementation. Schema changes do not block reads or writes, allowing data models to evolve with minimal impact on application latency or availability.
- High availability: It supports seamless cluster upgrades and scaling operations. This ensures that critical services remain accessible during maintenance or resource adjustment.
- Multi-cloud support: It operates as an open-source solution with support for Amazon Web Services (AWS), Google Cloud, and Microsoft Azure. This provides cloud neutrality without vendor lock-in.

### Challenges of classic TiDB

Despite these massive achievements, the "Shared-Nothing" architecture of classic TiDB, where storage and compute are tightly coupled on local nodes—eventually hit physical limitations in extreme large-scale environments. As data volumes exploded and cloud-native expectations evolved, inherent structural challenges emerged that were difficult to resolve without a fundamental redesign.

- Scalability limitations: In classic TiDB, scaling out (adding nodes) or scaling in (removing nodes) requires physically copying massive amounts of data (SST files) between nodes. This process is time-consuming for large datasets and can impact online traffic due to the heavy CPU and I/O required to move data.

    The underlying storage engine (RocksDB) in classic TiDB uses a single LSM-tree protected by a global mutex. This creates a scalability ceiling where the system struggles to handle large datasets (e.g., 6TB+ data or 200k+ SST files per TiKV node), preventing it from utilizing the full capacity of the hardware.

- Stability and performance challenges: Heavy write traffic triggers massive local compaction jobs to merge SST files. In the Classic architecture, these compaction jobs run on the same TiKV nodes serving online traffic, consuming significant CPU and I/O resources and can impact the online traffic.

    There is no physical isolation between logical regions and physical SST files. Operations like adding an index or moving a region (balancing) create compaction overhead that competes directly with user queries, leading to performance jitter. Under heavy write pressure, if the background compaction cannot keep up with the foreground write traffic, the system can trigger flow control mechanisms to protect the storage engine, which results in write throughput throttling and latency spikes for the application.

- Lack of cost effectiveness: To keep the production system stable and ensure good performance during peak traffic, customers are forced to over-provision hardware resources.

    Resources must be planned for the "high water mark" of both online traffic and heavy background tasks. Besides, data size on single TiKV nodes is limited, users often have to add more expensive compute nodes just to get more storage capacity, even if they don't need the extra CPU power.

### Motivation for TiDB X

These challenges stemmed from the physical binding of data to compute. To break through these ceilings—to achieve 10x faster scaling, zero-interference background tasks, and true pay-as-you-go elasticity—we need to move from "Shared-Nothing" architecture to TiDB X.

The motivation of TiDB X is documented in the blog [The Making of TiDB X: Origins, Architecture, and What’s to Come](https://www.pingcap.com/blog/tidbx-origins-architecture/)

## TiDB X architecture overview

TiDB X is a cloud-native evolution that unlocks the full potential of classic TiDB’s original distributed design. TiDB X inherits the advantages of classic TiDB:

- The SQL layer (tidb-server) was already stateless. It handled query parsing, optimization, and execution but never stored persistent data.
- TiProxy (or load balancers) is designed to maintain persistent client connections and route SQL traffic seamlessly. TiProxy originally supported online upgrades and has now become a natural gateway service.
- TiKV’s dynamic range-based sharding already existed, called Regions (256MB by default). TiKV splits data into millions of regions. The system automatically managed the movement and balancing of these Regions across nodes.

TiDB X evolves the proven stateless SQL and dynamic sharding foundation of classic TiDB by replacing the local "Shared-Nothing" storage with a cloud-native "Shared-Storage" object storage backbone, enabling a novel "Separation of Compute and Compute" that offloads heavy tasks to elastic pools for instant scalability and predictable performance.

![TiDB X Architecture](/media/tidb-x/tidb-x-architecture.png)

### Object storage support

As depicted in the "Object storage" layer of the diagram, TiDB X utilizes object storage (such as Amazon S3) as the single source of truth for all data. Unlike classic architectures where data resides on local disks, in TiDB X the persistent copy of all data is stored in the shared object storage layer. The "Shared Cache Layer" above it (Row Engine and Columnar Engine) acts as a high-performance cache to ensure low latency. Because the authoritative data is already in robust object storage, backing up simply relies on incremental Raft logs and metadata stored in S3. This allows backups to finish in seconds, regardless of the data volume. New TiKV nodes do not need to physically copy data from other nodes. They simply connect to the object storage and load the necessary data, making scale-out operations significantly faster.

### Auto-scaling mechanism

The architecture is explicitly designed for elasticity, facilitated by the load balancer and the stateless nature of the "Isolated SQL Layer". Since the compute nodes in the SQL layer are decoupled from the data residing in object storage, the system can auto-scale by adding or removing compute pods in seconds to match real-time workload demands. This technical elasticity enables a true consumption-based Pay-As-You-Go pricing model. Users no longer need to provision resources for peak load 24/7; the system automatically provisions resources during traffic spikes and scales down during quiet periods to minimize costs.

### Microservice and workload isolation

The architecture diagram highlights a sophisticated separation of duties, ensuring that different types of work do not interfere with each other. The top "Isolated SQL Layer" consists of separate groups of compute nodes, which allows for multi-tenancy or workload isolation where different applications can have dedicated compute resources while sharing the same underlying data. Beneath this, the "Shared Services" layer breaks down heavy database tasks into independent microservices for operations like compaction, analyze, and DDL. By offloading expensive background operations—such as adding an index, or massive data imports—to the Shared Services layer, the system ensures these heavy jobs never compete for CPU or memory with the "Compute" nodes serving online user traffic. This guarantees predictable performance for critical applications and allows each component—Gateway, SQL Compute, Cache, and Background Services—to scale independently based on specific bottlenecks.

## Key innovations of TiDB X

The following figure shows side-by-side comparison of classic TiDB and TiDB X architectures, highlighting the shift from Shared-Nothing to Shared-Storage design and the introduction of Compute Workload separation.

In Classic TiDB, the Raft-engine manages the Multi-Raft log, while RocksDB handles physical data storage on local disks. TiDB X replaces these components with the new RF Engine (Raft Engine) and a redesigned KV Engine (an LSM-tree engine replacing RocksDB). Both new engines are specifically optimized for high performance and seamless integration with object storage.

The dotted lines in the diagram represent background read and write operations to object storage. In TiDB X, these interactions between the RF/KV Engines and object storage are decoupled from foreground processes, ensuring that online traffic latency is not affected.

![Classic TiDB vs TiDB X](/media/tidb-x/tidb-classic-vs-tidb-x-1.png)

### Separation of compute and compute

While classic TiDB already separates compute (SQL) from storage (TiKV), TiDB X introduces a secondary layer of separation within both the SQL layer and the storage layer themselves:

- Lightweight Compute: Dedicated resources for lightweight OLTP workloads (user queries).
- Heavy Compute: A separate "Elastic Compute Pool" for heavy jobs (e.g., compaction, backups, analyze, load data, and slow queries).

For lightweight OLTP workloads, since the heavy compute is separated to the elastic compute pool, TiKV servers are dedicated compute resources that are exclusively reserved for user traffic. TiDB X provides faster and more stable performance with fewer resources. Also, TiDB X ensures that heavy compute tasks do not interfere with online transaction performance.

For heavy compute tasks such as DDL operations and large-scale data imports, TiDB X can leverage auto-elastic compute resources to run these workloads at full speed with minimal impact on online traffic. When you add a new index on TiDB X, TiDB workers, coprocessor workers and tikv workers are provisioned seamlessly based on data volume. The provisioned elastic compute resources are isolated with the TiDB and TiKV servers that are serving the online traffic. This separation ensures that resource-intensive operations no longer compete with critical OLTP queries. In real-world use cases, compared to the default classic TiDB performance, adding an index is 5x faster on TiDB X with no impact on online service. This represents a significant improvement in DDL performance while maintaining online service stability.

### Transition from shared-nothing to shared-storage

TiDB X moves away from the classic "Shared-Nothing" architecture (where data is copied between TiKV nodes) to a modern "Shared-Storage" model. In this model, object storage (like S3) serves as the single source of truth for all persistent data, rather than local disks. This removes the need for physical data copying during scaling, enabling rapid elasticity.

The introduction of object storage does not impact the performance of foreground read and write operations. For read operations, only heavy read requests are offloaded to the remote elastic coprocessor workers. For write operations, the interaction with object storage is asynchronous and does not impact write performance. The Raft log is persisted on local disk first, and then the Raft WAL (Write-Ahead Log) chunks are uploaded to object storage in the background. When the data in a MemTable is full and flushed to local disk, the region leader uploads the SST file to object storage. After the remote compaction is done on elastic compaction workers, the TiKV nodes are notified to load the compacted SST files from object storage.

### Elastic TCO (Pay-As-You-Go)

Classic TiDB required over-provisioning hardware to handle peak traffic and background tasks (like compaction overhead) simultaneously. TiDB X enables auto-scaling, allowing users to pay only for the resources they use (Pay-As-You-Go). Background resources for heavy jobs spin up on demand and spin down when finished, eliminating wasted cost.

A Request Capacity Unit (RCU) is a unit of measure used to represent the provisioned compute capacity for your TiDB X cluster. A RCU provides a fixed amount of compute resources that can process a certain number of SQL requests. The number of RCUs you provision determines your cluster’s baseline performance and throughput capacity. In TiDB X, cost is based on the actual consumption of RCU. You can maintain full financial control by setting an upper limit on these units, preventing unexpected costs while still enjoying the benefits of elasticity.

### From LSM tree to LSM forest

In the classic architecture, every TiKV node runs a single, massive RocksDB instance. This means all data from thousands of different regions is mixed together into one giant "single LSM-tree" structure. Because data is mixed, operations like moving a Region, scaling in/out, or importing data can require rewriting massive amounts of existing data (compaction) to separate or merge it. This can consume huge CPU and I/O resources and impact online traffic. The single LSM-tree is protected by a global mutex. As data size grows, at scale (typically 6TB+ data or 200k+ SST files per TiKV node), increased contention on this global lock impacts both read and write operations.

While TiDB X retains the logical region concept from classic TiDB, it fundamentally redesigns the storage engine by shifting from a single LSM tree to an LSM Forest. Instead of one giant tree for all data, TiDB X assigns each region its own separate, independent LSM Tree. The most critical benefit of this physical isolation is the elimination of compaction overhead during cluster operations (scale-in, scale-out, region movement, load data). Operations on one Region (like a heavy write or a split) are isolated to its specific tree. There is no global mutex lock contention.

![Classic TiDB vs TiDB X](/media/tidb-x/tidb-classic-vs-tidb-x-2.png)

### Rapid elastic scalability (5x-10x faster)

In TiDB X, data resides in shared object storage with fully isolated LSM-trees for each Region. The system eliminates the need for physical data migration or compaction when adding or removing TiKV nodes. The result is a 5x–10x improvement in scaling speed compared to classic TiDB, maintaining stable latency for online traffic.
