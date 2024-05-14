---
title: Recovery Group Overview (Beta)
summary: Learn how to protect your databases against disasters by using TiDB Cloud Recovery Groups.
---

# Recovery Group Overview (Beta)

TiDB Cloud Recovery Groups allow you to replicate your databases between TiDB Cloud Dedicated clusters for protection against regional disasters. Recovery Groups allow you to orchestrate the failover of databases from one cluster to another. After failover to the secondary cluster, if the original cluster becomes available again, you can re-establish replication in the reverse direction to reprotect the databases.

## Architecture

A Recovery Group consists of a set of replicated databases that can be failed over together between two TiDB Dedicated Clusters. Each Recovery Group is assigned a primary cluster, databases on this primary cluster are associated with the group and are then replicated to the secondary cluster.

![Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-overview.png)

- Recovery Group: a group of databases that are replicated between two clusters
- Primary Cluster: the cluster where the database is actively written by the application
- Secondary Cluster: the cluster where replicas of the database are located

> **Note**
>
> Client connections to the replica copy of the database are not explicitly forced to be read-only by the Recovery Group feature. Ensuring that the application connecting to the replica copy only performs read-only queries is the responsibility of the application.

## Key features/Limitations

- Recovery Groups support TiDB Cloud Dedicated Clusters that are deployed on AWS.
- Recovery Groups are established between two clusters.
- Bi-directional replication of a database is not supported with recovery groups.

> **Warning**
>
> This feature is a beta feature and not recommended for product environments.

## What's next

- To get started with recovery groups, see [Create Database Recovery Group](/tidb-cloud/recovery-group-get-started.md).
- To learn how to use a recovery group, see [Failover Databases](/tidb-cloud/recovery-group-failover.md) and [Reprotect Databases](/tidb-cloud/recovery-group-reprotect.md)
