---
title: TiDB X Architecture
summary: The architecture introduction of the TiDB X
---

# TiDB X Architecture

TiDB X represents a fundamental architectural shift in the TiDB evolution, transitioning from a classic "Share-Nothing" distributed database to a modern, "Share-Everything" Service-Oriented Architecture (SOA). Designed for the AI era and massive cloud scalability, TiDB X leverages Object Storage (e.g., Amazon S3) as the single source of truth.

TiDB classic architecture decouples storage from compute entirely, TiDB X introduces a novel "Separation of Compute and Compute" design that isolates online transactional workloads from heavy maintenance tasks. The result is a system that offers elastic scalability, predictable performance, and optimized Total Cost of Ownership (TCO).

This document details the architecture of TiDB X, including its storage, computing, and scheduling mechanisms.

# Challenges of TiDB Classic

The motivation of TiDB X is documented in the blog [The Making of TiDB X: Origins, Architecture, and What’s to Come](https://www.pingcap.com/blog/tidbx-origins-architecture/)

TiDB Classic has faced several critical challenges in large-scale production environments, primarily stemming from its "Share-nothing" architecture.

## Scalability Limitations

Slow Scale Operations: In TiDB Classic, scaling out (adding nodes) or scaling in (removing nodes) requires physically copying massive amounts of data (SST files) between nodes. This process is time-consuming and can take hours to complete for large datasets.

Global Mutex Bottlenecks: The underlying storage engine (RocksDB) in TiDB Classic uses a single LSM-tree protected by a global mutex. This creates a scalability ceiling where the system struggles to handle extremely large datasets (e.g., 3TB+ data per node or 100k+ SST files), preventing it from utilizing the full capacity of the hardware.

Impact on Traffic: Scale-in and scale-out operations are not fast enough and often impact online traffic due to the heavy I/O required to move data.

## Stability and Performance Challenges

Compaction Overhead: Heavy write traffic triggers massive local compaction jobs to merge SST files. In the Classic architecture, these compaction jobs run on the same TiKV nodes serving online traffic, consuming significant CPU and I/O resources.

Resource Contention: There is no physical isolation between logical regions and physical SST files. Operations like adding an index or moving a region (balancing) create overhead that competes directly with user queries, leading to performance jitter.

Flow Control Issues: Under heavy write pressure, the system often triggers flow control mechanisms to protect the storage engine, which results in latency spikes and unpredictable performance for the application.

## Lack of Cost Effectiveness

Over-Provisioning: To keep the production system stable and ensure good performance during peak traffic, customers are forced to over-provision hardware resources.

Static Resource Allocation: Resources must be planned for the "high water mark" of both online traffic and heavy background tasks. Users cannot easily scale resources down during quiet periods, leading to wasted compute capacity and higher TCO.

Coupled Costs: Because data size on single tikv nodes is limited, users often have to add more expensive compute nodes just to get more storage capacity, even if they don't need the extra CPU power.

## Heavy Background Job Interference

Resource Conflict: Heavy background jobs—such as scale operations, backup, compaction, analyze, and data import (Load Data)—run on the same nodes as foreground OLTP traffic.

Performance Degradation: These tasks are resource-intensive and often interfere with online traffic, causing latency increases or throughput drops.

Maintenance Windows: Due to this interference, administrators often have to schedule maintenance operations (like index creation or backups) during off-peak hours to avoid impacting the business, reducing operational agility.


# TiDB X Architecture

This architecture represents a modern, cloud-native Share-Everything design that decouples storage from compute and further separates foreground transaction processing from background maintenance tasks.

## Object Storage Support
As depicted in the "Object storage" layer of the diagram, TiDB X utilizes object storage (such as Amazon S3) as the single source of truth for all data.

Full Data on Object Storage: Unlike classic architectures where data resides on local disks, here the persistent copy of all data is stored in the shared object storage layer. The "Shared Cache Layer" above it (Row Engine and Columnar Engine) acts as a high-performance cache to ensure low latency.

Rapid Backups: Because the authoritative data is already in robust object storage, backing up terabytes (TB) of data involves simply capturing metadata and log markers. This allows TB-level backups to finish in seconds rather than hours.

Faster Node Scaling: New compute or cache nodes can come online almost instantly because they do not need to physically copy data from other nodes. They simply connect to the object storage and load the necessary metadata, making scale-out operations significantly faster.

## Auto-Scaling Mechanism
The architecture is designed for elasticity, facilitated by the "Load balancer" and the stateless nature of the "Isolated SQL Layer".

Scaling within Seconds: Since compute nodes (in the SQL layer) are decoupled from the data (in object storage), the system can auto-scale by adding or removing compute pods in seconds to match real-time workload demands.

Pay-As-You-Go Model: This elasticity enables a true consumption-based pricing model. Users no longer need to provision for peak load 24/7; the system automatically provisions resources during traffic spikes and scales down during quiet periods to minimize costs.

## Microservice and Workload Isolation
The diagram highlights a sophisticated separation of duties, ensuring that different types of work do not interfere with each other.

Isolated SQL Layer: The top "Isolated SQL Layer" shows separate groups of Compute nodes. This allows for multi-tenancy or workload isolation, where different applications or users can have dedicated compute resources while sharing the same underlying data.

Shared Services (Microservices): The bottom layer, "Shared Services", breaks down traditional database maintenance tasks into independent microservices like Compaction, Analyze, and DDL.

Zero Impact from Heavy Tasks: Expensive background operations—such as adding an index, Online DDL, or massive data imports—are offloaded to these "extra TiDB workers" in the Shared Services layer. This ensures that heavy maintenance jobs never compete for CPU or memory with the "Compute" nodes serving online user traffic, guaranteeing predictable performance for critical applications.

Independent Scaling: Each component (Gateway, SQL Compute, Cache, Background Services) can be scaled independently based on specific bottlenecks, and failovers are smoother as services are loosely coupled.