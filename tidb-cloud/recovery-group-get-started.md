---
title: Get Started with Recovery Groups
summary: Learn how to create a recovery group in TiDB Cloud and view its details.
---

# Get Started with Recovery Groups

This document describes how to create a recovery group to protect your databases running on TiDB Cloud Dedicated clusters using the [TiDB Cloud console](https://tidbcloud.com/). It also shows how to view details of a recovery group.

## Prerequisites

- A recovery group replicates your databases to another cluster to protect your databases from regional disasters. Before creating a recovery group, you need to have two TiDB Cloud Dedicated clusters. One cluster hosts the primary databases, and a second cluster hosts the replicas of the primary databases. If you have not done so already, follow the steps in [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md) to create the necessary clusters.
- To create a recovery group, you must be in the `Organization Owner` role of your organization or the `Project Owner` role of the target project.

> **Note**
>
> Currently, only TiDB Cloud Dedicated clusters hosted on AWS support recovery groups.

## Create a new recovery group

To create a recovery group, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to your target project using the combo box in the upper-left corner.

2. In the left navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, click **Create Recovery Group**.

4. On the **Create Recovery Group** page, enter a name for the recovery group.

    > **Note**
    >
    > Currently only one resiliency level is supported. For more information, see [About resiliency levels](#about-resiliency-levels).

5. Select the TiDB Cloud Dedicated cluster that will be the primary cluster for this group.

6. Select the TiDB Cloud Dedicated cluster that will be the secondary cluster where databases will be replicated for this group.

7. Select which databases you wish to replicate as part of this recovery group.

    > **Note**
    >
    > When assigning databases to the group, you can select specific databases, or select all (non-system) databases on the primary cluster (current and future).
    >
    > - If you **Assign all databases (current and future)**, any future databases added to the cluster will be automatically included in this recovery group and replicated to the secondary cluster.
    > - If you **Assign specific databases**, select the specific databases on the primary cluster that you want to replicate to the secondary cluster. If any databases are added to the primary cluster in the future, these new databases will not be automatically replicated as part of this recovery group.
   >
    > During the initial replication, due to the volume of data transferred, the online query performance at the primary or secondary clusters might be affected. Schedule the initial protection of databases for a less busy period.

    > **Warning**
    > 
    > During the initial replication, the content of the selected databases at the primary cluster will replace the content of the databases at the secondary cluster. If you wish to preserve the unique content at the secondary cluster, complete a backup before setting up the recovery group.

8. Review the summary information, and then click **Create** to begin protecting the databases as part of the new recovery group.

## View recovery group details

After creating a recovery group, you can view its status information on the **Recovery Group Detail** page:

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to your target project using the combo box in the upper-left corner.

2. In the left navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, click the name of the recovery group that you wish to view.

    The **Recovery Group Detail** page provides information about a recovery group, including its configuration details, status, and metrics on the replication throughput and latency. 

4. When a replication relationship is fully established and functioning, the status is displayed as **Available**.

    > **Warning**
    >
    > During the setup of a recovery group, an account named following the pattern `cloud-rg-*` will be created on the secondary cluster for the replication process. Deleting or modifying this account will interrupt the replication.

## About resiliency levels

A resiliency level defines the consistency characteristics of data reading in different scenarios of a recovery group. Currently, TiDB Cloud only provides the following resiliency level:

- No consistency guaranteed. During the replication of a recovery group, the downstream cluster does not guarantee transaction consistency read. When the upstream cluster becomes unavailable, you can not restore the data in the downstream cluster to a transaction consistency state.

TiDB Cloud will provide two additional resiliency levels in the near future:

- Eventual consistency. During the replication of a recovery group, the downstream cluster does not guarantee transaction consistency read. However, when the upstream cluster becomes unavailable, you can restore the data in the downstream cluster to a transaction consistency state.
- Near real-time consistency. During the replication of a recovery group, the downstream cluster provides approximately real-time transaction consistency read. When the upstream cluster becomes unavailable, you can restore the data in the downstream cluster to a transaction consistency state.

## What's next

After creating the recovery group, you might want to familiarize yourself with the failover and reprotect operations. These operations are used to **Failover** the primary cluster for the replicated databases from one cluster to the other, and then to later re-establish replication in the opposite direction to **Reprotect** the failed over databases.

- [Failover and Reprotect Databases](/tidb-cloud/recovery-group-failover.md)
