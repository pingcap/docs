---
title: TiDB Architecture
summary: The key architecture components of the TiDB platform
category: introduction
aliases: ['/docs/dev/architecture/']
---

# TiDB Architecture

Compared to traditional databases, TiDB has the following advantages: 
* Has distributed architecture and supports elastic scalability, flexible capacity expansion & reduction
* Fully compatible with the MySQL protocol and the common features and syntax of MySQL, able to directly replicate from MySQL in most scenarios
* Supports high availability in default and executes data recovery and failover autometicly; transparent to the business
* Supports ACID transaction, suitable for scenarios requiring strong consistency such as bank transfer
* A rich toolchain ecosystem covers a variety of scenarios including data migration, synchronization, backup, etc.

![TiDB Architecture](/media/tidb-architecture-1.png)

## TiDB server

The TiDB server is in charge of external exposure the MySQL protocol connection endpoint, receiving SQL requests, processing and optimizing SQL related logics, and generates distributed execution plans finally. The TiDB server itself is stateless. It is horizontally scalable and provides the unified interface to the outside through the load balancing components such as Linux Virtual Server (LVS), HAProxy, or F5. It does not store data and is for computing and SQL analyzing only, transmitting actual data read request to TiKV nodes (or TiFlash nodes).

## Placement Driver (PD) server

The PD server is the managing component of the entire cluster and is in charge of storing real-time data distribution of every single TiKV node and overall topology structure of the entire TiDB cluster, providing Dashboard management UI, and allocating transaction IDs. The PD server can be seen as ‘The Brain’ of the entire cluster’ since it is not only for storage the metadata of the cluster, but also scheduling and load balancing regions in the TiKV cluster. Besides, The PD server at least three nodes which leads to high availability. It is recommended to deploy PD as an odd number of nodes.

## Storage servers
### TiKV server

The TiKV server is responsible for storing data. From an external view, TiKV is a distributed transactional Key-Value storage engine. Region is the basic unit to store data. Each Region stores the data for a particular Key Range which is a left-closed and right-open interval from StartKey to EndKey. There are multiple Regions in each TiKV node. APIs of TiKV provides native supports to distributed transactions as in Key-Value and supports SI (Snapshot Isolation) level isolation in default, which is the core of how TiDB supports distributed transactions at SQL level. After processing SQL, SQL plan will transfer to actual calling of TiKV APIs. As a result, data will be stored in TiKV. Besides, all data will be autometically maintained as multiple replicas (Three replicas in default), which supports high availability and failover naturally.

### TiFlash Server

The TiFlash Server is a special kind of storage server. Differs to normal TiKV, TiFlash is a kind of column-oriented storage server which is mainly designed for OLAP scenarios. 
