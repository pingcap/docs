---
title: PD Key Metrics
summary: Learn some key metrics displayed on the Grafana PD dashboard.
category: operations
---

# PD Key Metrics

If you use Ansible to deploy the TiDB cluster, the monitoring system is deployed at the same time. For more information, see [Overview of the Monitoring Framework](../op-guide/monitor-overview.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and so on. A lot of metrics are there to help you diagnose.

You can get an overview of the component PD status from the PD dashboard, where the key metrics are displayed. This document provides a detailed description of these key metrics.

## Key metrics description

To understand the key metrics displayed on the Overview dashboard, check the following table:

Row Name | Panel Name | Description | Normal Range
---------------- | ---------------- | ---------------------------------- | --------------
Cluster | PD Role | It indicates that the current PD is leader or follower |
Cluster | Storage Capacity | The total capacity of the cluster |
Cluster | Current Storage Size | The current storage size of the cluster |
Cluster | Number of Regions | The total number of region without replicas |
Cluster | Leader Balance Ratio | The leader ratio difference of the instance with the biggest leader ratio and the smallest leader ratio | It is less than 5% for a balanced situation and becomes bigger when you restart an instance | 
Cluster | Region Balance Ratio | The region ratio difference of the instances with the biggest Region ratio and the smallest Region ratio | It is less than 5% for a balanced situation and becomes bigger when you add or remove an instance |
Cluster | Normal Stores | The count of healthy stores |
Cluster | Abnormal Stores | The count of unhealthy stores | The normal value is `0`. If the number is bigger than `0`, it means some instance(s) are abnormal.
Cluster | Current Storage Usage | The current storage size and used ratio of the cluster |
Cluster | Current Peer Count | The current peer count of the cluster |
Cluster | Metadata Information | It records such as the cluster ID, the last ID the allocator generated, and the last timestamp TSO generated | 
Cluster | Region Label Isolation Level | The number of regions in the different label level |
Cluster | Region Health | It records the unusual regions' count which may have pending peers, down peers, extra peers, offline peers, miss peers, learner peers or incorrect namespace | The number of pending peers should less than `100`. The miss peers should not be continuous greater than `0`
Balance | Store capacity | The capacity size of each TiKV instance |
Balance | Store available | The available size of each TiKV instance |
Balance | Store used | The used size of each TiKV instance |
Balance | Size amplification | The size amplification, which is equal to Store region size over Store used, of each TiKV instance |
Balance | Size available ratio | It is equal to Store available over Store capacity for each TiKV instance |
Balance | Store leader score | The leader score of each TiKV instance |
Balance | Store region score | The region score of each TiKV instance |
Balance | Store leader size | The total leader size of each TiKV instance |
Balance | Store region size | The total region size of each TiKV instance |
Balance | Store leader count | The leader count of each TiKV instance |
Balance | Store region count | The region count of each TiKV instance |
HotRegion | Hot write region's leader distribution | The total leader regions under hot write on each TiKV instance |
HotRegion | Hot write region's peer distribution | The total regions which are not leader under hot write on each TiKV instance |
HotRegion | Hot write region's leader written bytes | The total bytes of hot write on leader regions for each TiKV instance |
HotRegion | Hot write region's peer written bytes | The total bytes of hot write on regions which are not leader for each TiKV instance |
HotRegion | Hot read region's leader distribution | The total leader regions under hot read on each TiKV instance |
HotRegion | Hot read region's peer distribution | The total regions which are not leader under hot read on each TiKV instance |
HotRegion | Hot read region's leader read bytes | The total bytes of hot read on leader regions for each TiKV instance |
HotRegion | Hot read region's peer read bytes | The total bytes of hot read on regions which are not leader for each TiKV instance |
Scheduler | Scheduler is running | The current running schedulers |
Scheduler | Balance leader movement | The leader movement details among TiKV instances |
Scheduler | Balance region movement | The region movement details among TiKV instances |
Scheduler | Balance leader event | The count of balance leader events |
Scheduler | Balance region event | The count of balance region events |
Scheduler | Balance leader scheduler | The inner status of balance leader scheduler |
Scheduler | Balance region scheduler | The inner status of balance region scheduler |
Scheduler | Namespace checker | The namespace checker's status |
Scheduler | Replica checker | The replica checker's status |
Scheduler | Region merge checker | The merge checker's status |
Operator | Schedule operator create | The number of different operators are created |
Operator | Schedule operator check | The number of different operators have been checked. It mainly checks if the current step is finished, and returns the next step to be executed |
Operator | Schedule operator finish | The number of different operators are finished |
Operator | Schedule operator timeout | The number of different operators are timeout |
Operator | Schedule operator replaced or canceled | The number of different operators are replaced or canceled |
Operator | Schedule operators count by state | The number of different status of operators |
Operator | 99% operator finish duration | The time consumed when the operator finish in .99 |
Operator | 50% operator finish duration | The time consumed when the operator finish in .50 |
Operator | 99% operator step duration | The time consumed when the operator step finish in .99 |
Operator | 50% operator step duration | The time consumed when the operator step finish in .50 |
Grpc | completed commands rate | The rate of completing each kind of gRPC commands |
Grpc | 99% completed_cmds_duration_seconds | The time consumed of completing each kind of gRPC commands in .99 |
Etcd | handle_txns_count | The count of Ectd transactions |
Etcd | 99% handle_txns_duration_seconds | The time consumed of handling Ectd transactions in .99 |
Etcd | 99% wal_fsync_duration_seconds | The time consumed of writing WAL into the persistent storage in .99 | The value is less than `1s`.
Etcd | 99% peer_round_trip_time_seconds | The time consumed of the network in .99 | The value is less than `1s`.
Etcd | etcd disk wal fsync rate | The rate of writing WAL into persistent storage |
Etcd | Raft Term | The current term of Raft |
Etcd | Raft Committed Index | The last committed index of Raft |
Etcd | Raft Applied Index | The last applied index of Raft |
TiDB | handle_requests_count | The count of TiDB requests |
TiDB | handle_requests_duration_seconds | The time consumed of handling TiDB requests | .99 should be less than `100ms`
Heartbeat | Region heartbeat report | The count of the heartbeat which each TiKV instance reports to PD |
Heartbeat | Region heartbeat report error | The count of the heartbeat with error status |
Heartbeat | Region heartbeat report active | The count of the heartbeat with ok status |
Heartbeat | Region schedule push | The count of the corresponding schedule command which PD sends to each TiKV instance |
Heartbeat | 99% region heartbeat latency | The heartbeat latency of each TiKV instance in .99 |

## Interface of the PD dashboard

![PD Dashboard](../media/pd_dashboard.png)