---
title: Recovery Group Overview (Beta)
summary: Learn how to protect your databases against disasters by using TiDB Cloud recovery groups.
---

# Recovery Group Overview (Beta)

A TiDB Cloud recovery group allows you to replicate your databases between TiDB Cloud Dedicated clusters for protection against regional disasters. You can orchestrate the failover of databases from one cluster to another. After a failover to the secondary cluster, if the original primary cluster becomes available again, you can re-establish replication in the reverse direction to reprotect your databases.

## Architecture

A recovery group consists of a set of replicated databases that can be failed over together between two TiDB Dedicated clusters. Each recovery group is assigned a primary cluster, and databases on this primary cluster are associated with the group and are then replicated to the secondary cluster.

![Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-overview.png)

- Recovery Group: a group of databases that are replicated between two clusters
- Primary Cluster: the cluster where the database is actively written by the application
- Secondary Cluster: the cluster where replicas of the database are located

> **Note**
>
> Client connections to the replica databases are not explicitly forced to be read-only by the Recovery Group feature. Ensuring that the application connecting to the replica databases only performs read-only queries is the responsibility of the application.

## Key features and limitations

- Currently, only TiDB Dedicated clusters hosted on AWS support recovery groups.
- Recovery groups are established between two clusters.
- Bi-directional replication of a database is not supported with recovery groups.

> **Warning**
>
> This feature is in beta and not recommended for production environments.

## What's next

- To get started with recovery groups, see [Create Database Recovery Group](/tidb-cloud/recovery-group-get-started.md).
- To learn how to use a recovery group, see [Failover and Reprotect Databases](/tidb-cloud/recovery-group-failover.md).
