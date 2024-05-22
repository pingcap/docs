---
title: Get Started with Recovery Groups
summary: Learn how to create a recovery group in TiDB Cloud and view its details.
---

# Get Started with Recovery Groups

This document describes how to create a recovery group to protect your databases running on TiDB Cloud Dedicated clusters using the TiDB Cloud user interface. It also shows how to view details of the recovery group.

## Prerequisites

A recovery group replicates your databases to another cluster to protect your databases from a regional disaster. To create a recovery group, you need to have two TiDB Cloud Dedicated clusters. One cluster hosts the primary databases, and a second cluster will be used for the replicated copy of the databases. If you have not done so already, follow the steps in [Create a TiDB Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md) to create the necessary clusters.

> **Note**
>
> Currently only TiDB Cloud Dedicated clusters deployed on AWS support recovery groups.

## Create a new recovery group

To create a recovery group, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **Project Settings** in the left navigation pane.

2. On the **Project Settings** navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, click **Create Recovery Group**. A dialog is displayed.

4. In the **Create Recovery Group** dialog box, enter a name for the recovery group.

    > **Note**
    >
    > Currently only one resiliency level is supported.

5. Select the TiDB Cloud cluster that will be the primary cluster for this group.

6. Select the TiDB Cloud cluster that will be the seondary cluster that databases will be replicated to for this group.

7. Select which databases you wish to replicate as part of this recovery group.

    > **Note**
    >
    > When assigning databases to the group, you can select specific databases to the recovery group, or select all (non-system) databases on the primary cluster (current and future).
    > If you **Assign all databases (current and future)** then any future databases added to the cluster will be automatically included in this recovery group and replicated to the secondary cluster.
    > If you **Assign specific databases** then you will select the specific databases on the primary cluster that you want to replicate to the secondary cluster. If any databases are added to the primary cluster in the future, then these databases will not be automatically replicated as part of this recovery group.
    > During the initial synchronization, due to the volume of data transferred, the online query performance at the primary or secondary clusters might be affected. Schedule the initial protection of databases for a less busy period.

    > **Warning**
    > 
    > As part of the initial data replication, the content of the selected databases will be replaced at the secondary cluster by the content of the databases from the primary cluster. If you wish to preserve the unique content on the secondary cluster, complete a backup before completing the setup of the the recovery group.

8. Review the summary information and then click **Create** to begin protecting the databases as part of a new recovery group.

## View recovery group details

After creating a Recovery Group, view the **Recovery Group Detail** page to view status information about the group:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **Project Settings** in the left navigation pane.

2. On the **Project Settings** navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, click the name of the recovery group that you wish to view.

    > **Note**
    >
    > The **Recovery Group Detail** page provides information about the recovery group including the configuration details provided when it was created, and its current status.
    > The page also provides metrics on the throughput of the recovery groups replication, and the replication latency experienced.

4. The status of the recovery group will read as **Available** when the replication relationship is fully established and functioning.

    > **Warning**
    >
    > As part of the setup of a recovery group, an account will be created on the secondary cluster that will be used by the replication process. This account will be named following the pattern `cloud-rg-*`. Deleting or modifying this account will cause the replication to be interrupted.

## What's next

After creating the recovery group, you might want to familiarize yourself with the failover and reprotect operations. These operations are used to **Failover** the primary cluster for the replicated databases from one cluster to the other, and then to later reestablish replication in the opposite direction to **Reprotect** the failed over databases.

- [Failover and Reprotect Databases](/tidb-cloud/recovery-group-failover.md)
