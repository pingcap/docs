---
title: High Availability in TiDB Cloud Dedicated
summary: TiDB Cloud Dedicated supports high availability with Multi-AZ deployments.
---

# High Availability in TiDB Cloud Dedicated

TiDB uses the Raft consensus algorithm to ensure that data is highly available and safely replicated throughout storage in Raft Groups. Data is redundantly copied between storage nodes and placed in different availability zones to protect against machine or data center failures. With automatic failover, TiDB ensures that your service is always on.

TiDB Cloud Dedicated clusters consist of three major components: TiDB node, TiKV node, and TiFlash node. The high availability implementation of each component for TiDB Cloud Dedicated is as follows:

* **TiDB node**

    TiDB is for computing only and does not store data. It is horizontally scalable. TiDB Cloud Dedicated deploys TiDB nodes evenly to different availability zones in a region. When a user executes a SQL request, the request first passes through a load balancer deployed across availability zones, and then the load balancer distributes the request to different TiDB nodes for execution. It is recommended that each TiDB Cloud Dedicated cluster has at least two TiDB nodes for high availability.

* **TiKV node**

    [TiKV](https://docs.pingcap.com/tidb/stable/tikv-overview) is the row-based storage layer of TiDB Cloud Dedicated cluster with horizontal scalability. The minimum number of TiKV nodes for a TiDB Cloud Dedicated cluster is 3. TiDB Cloud Dedicated deploys TiKV nodes evenly to all availability zones (at least 3) in the region you select to achieve durability and high availability. In a typical 3-replica setup, your data is distributed evenly among the TiKV nodes across all availability zones and is persisted to the disk of each TiKV node.

* **TiFlash node**

    [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview), as a columnar storage extension of TiKV, is the key component that makes TiDB essentially a Hybrid Transactional/Analytical Processing (HTAP) database. In TiFlash, the columnar replicas are asynchronously replicated according to the Raft Learner consensus algorithm. TiDB Cloud Dedicated deploys TiFlash nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash nodes in each TiDB Cloud Dedicated cluster and create at least two replicas of the data for high availability in your production environment.
