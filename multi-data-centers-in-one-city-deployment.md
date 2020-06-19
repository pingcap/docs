---
title: Deployment Solution for Multiple Data Centers in One City
summary: Learn the deployment solution for multi-data centers in one city.
category: how-to
aliases: ['/docs/dev/how-to/deploy/geographic-redundancy/overview/','/docs/dev/geo-redundancy-deployment/']
---

# Deployment Solution for Multiple Data Centers in One City

As a NewSQL database, TiDB excels in the best features of the traditional relational database and the scalability of the NoSQL database and is of course, highly available across data centers (DC). This document introduces the deployment solution for multiple DCs in one city.

## Raft protocol

Raft is a distributed consensus algorithm. Using this algorithm, both PD and TiKV, among components of the TiDB cluster, achieve disaster recovery of data, which is implemented through the following mechanisms:

- In essence, Raft members are log replication and state machines. Among Raft members, data replication is implemented by replicating logs. Raft members change their own states in different conditions so as to elect a leader to provide services to the outside.
- Raft is a voting system, which follows a majority protocol. In a Raft group, if a member gets the majority of votes, its membership changes to leader. This is to say when the majority of nodes remain in the Raft group, a leader can be elected to provide services to the outside.

To take advantage of Raft's reliability, the following conditions must be met in a real deployment scenario:

- At least three servers are provided in case one server fails.
- At lease three racks are provided in case one rack fails.
- At lease three DCs are provided in case one DC fails.
- At lease three cities are planned for deployment in case data safety issue occurs in one city.

From the conditions above, you can see that the native Raft protocol's support for even number of replicas is not so good. Considering the impact of cross-city network latency, three DCs in the same city might be most suitable for a highly available and disaster tolerant solution of Raft deployment.

## Deployment solution for three DCs in one city

TiDB clusters can be deployed in three DCs in the same city. In this solution, data replication across the three DCs is implemented using the Raft protocol within the cluster. These three DCs can provide read and write services to the outside at the same time. Data consistency is not affected even if one DC fails.

### Architecture

TiDB, TiKV and PD are distributed among three DCs, which is the most common deployment solution with the highest availability.

![3-DC Deployment Architecture](/media/deploy-3dc.png)

**Advantages:**

- All replicas are distributed among three DCs, with high availability and disaster recovery capability.
- No data will be lost if one DC is down (RPO = 0).
- Even if one DC is down, the other two DCs will initiate leader election and automatically resume services within a reasonable amount of time (within 20 seconds (s) in most cases) and no data is lost (RTO <= 20s). See the following diagram for more information:

![Disaster Recovery for 3-DC Deployment](/media/deploy-3dc-dr.png)

**Disadvantages**

The performance is affected by the network latency.

- For writes, all the data has to be replicated to at least 2 DCs. Because TiDB uses 2-phase commit for writes, the write latency is at least twice the latency of the network between two DCs.
- The read performance will also suffer if the leader is not in the same DC as the TiDB node with the read request.
- Each TiDB transaction needs to obtain TimeStamp Oracle (TSO) from the PD leader. So if TiDB and PD leader are not in the same DC, the performance of the transactions will also be impacted by the network latency because each transaction with write request will have to get TSO twice.

### Optimizations

If not all of the three DCs need to provide service to the applications, you can dispatch all the requests to one DC and configure the scheduling policy to migrate all the TiKV Region leader and PD leader to the same DC. In this way, neither obtaining TSO or reading TiKV Regions will be impacted by the network latency across DCs. If this DC is down, the PD leader and Region leader will be automatically elected in other surviving DCs, and you just need to switch the requests to the DC that are still online.

![Read Performance Optimized 3-DC Deployment](/media/deploy-3dc-optimize.png)

**Advantages:**

The cluster's read performance and the capability to get TSO are improved. A configuration template of scheduling policy is as follows:

```shell
-- Evicts all leaders of other DCs to the DC that provides services to the application.
config set label-property reject-leader LabelName labelValue

-- Migrates PD leaders and sets priority.
member leader transfer pdName1
member leader_priority pdName1 5
member leader_priority pdName2 4
member leader_priority pdName3 3
```

**Disadvantages:**

- Write scenarios are still affected by network latency across DCs. This is because Raft follows the majority protocol and all written data must be replicated to at least two DCs.
- The TiDB server is in one DC.
- All application traffic is processed by one DC and the performance is limited by the network bandwidth pressure of that DC.
- The capability to get TSO and the read performance are affected by whether the PD server and TiKV server are up in the DC that processes application traffic. If these servers are down, application is still affected by the cross-center network latency.

### Deployment example

#### Topology example

The following example assumes that three DCs (IDC1, IDC2, and IDC3) are located in one city; each IDC has two sets of racks and each rack has three servers. The example ignores the hybrid deployment or the scenario where one machine is deployed on multiple instances. The deployment of a TiDB cluster (three replicas) for three DCs in one city is as follows:

![3-DC in One City](/media/multi-data-centers-in-one-city-deployment-sample.png)

#### TiKV labels

TiKV is a multi-Raft system where data is divided into Regions and each Region is 96 MB by default. Three replicas of each Region form a Raft group. For a TiDB cluster of three replicas, because the number of Region replicas is independent of the TiKV instance numbers, three replicas of a Region are only scheduled to three TiKV instances. This means that even if the cluster is scaled out to have N TiKV instances, it is still a cluster of three replicas.

Because a Raft group of three replicas tolerates failure of only one replica, even if the cluster is scaled out to have N TiKV instances, this cluster still tolerates failure of only one replica. Two failed TiKV instances might cause some Regions to lose replicas and the data in this cluster is no longer complete. SQL requests that access data from these Regions will fail. The probability of two simultaneous failures among N TiKV instances is much higher than the probability of two simultaneous failures among 3 TiKV instances. This means that the more TiKV instances the multi-Raft system is scaled out to have, the less the availability of the system.

Because of the limitation described above, `label` is used to describe the location information of TiKV. The label information is refreshed to the TiKV startup configuration file with deployment or rolling upgrade operations. The started TiKV reports its latest label information to PD. Based on the user-registered label name (the label metadata) and the TiKV topology, PD optimally schedules Region replicas and improves the system availability.

#### TiKV labels planning example

You need to design and plan TiKV labels according to your existing physical resources and the disaster recovery capability, which improves the availability and disaster recovery of the system. You also need to configure the relevant `tidb-ansible inventory.ini` file according to the planned topology:

```ini
[tikv_servers]
TiKV-30   ansible_host=10.63.10.30     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170 tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r1,host=30"
TiKV-31   ansible_host=10.63.10.31     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r1,host=31"
TiKV-32   ansible_host=10.63.10.32     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r2,host=30"
TiKV-33   ansible_host=10.63.10.33     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z1,dc=d1,rack=r2,host=30"

TiKV-34   ansible_host=10.63.10.34     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r1,host=34"
TiKV-35   ansible_host=10.63.10.35     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r1,host=35"
TiKV-36   ansible_host=10.63.10.36     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r2,host=36"
TiKV-37   ansible_host=10.63.10.36     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z2,dc=d1,rack=r2,host=37"

TiKV-38   ansible_host=10.63.10.38     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r1,host=38"
TiKV-39   ansible_host=10.63.10.39     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r1,host=39"
TiKV-40   ansible_host=10.63.10.40     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r2,host=40"
TiKV-41   ansible_host=10.63.10.41     deploy_dir=/data/tidb_cluster/tikv  tikv_port=20170   tikv_status_port=20180 labels="zone=z3,dc=d1,rack=r2,host=41"

## Group variables
[pd_servers:vars]
location_labels = ["zone","dc","rack","host"]
```

In the example above, `zone` is the logical availability zone level and used to control the isolation of replicas (currently three replicas are in the cluster).

Considering that the DC might be scaled out in the future, the three-layer label structure (`dc`, `rack`, `host`) is not directly adopted. Assume that `d2`, `d3`, and `d4` are to be scaled out, you only need to scale out the DCs in the corresponding availability zone and scale out the racks in the corresponding DC.

If this three-layer label structure is directly adopted, after scaling out a DC, you might need to use a new label and data in TiKV as a whole needs to be rebalanced.

### High availability and disaster recovery analysis

The deployment solution for multiple DCs in one city guarantees when one DC fails, the cluster can automatically recover services without manual intervention. Data consistency is also guaranteed. Note that scheduling policies help optimize performance. But when failure occurs, these policies prioritize availability over performance.
