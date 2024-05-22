---
title: Failover and Reprotect Databases
summary: Learn how to use a Recovery Group to failover and reprotect databases between TiDB Cloud clusters.
---

# Failover and Reprotect Databases

Databases that are part of a recovery group are replicated from one cluster to another (typically in a different region of the cloud service provider).

The **Failover** action promotes the replicated copy of the databases at the secondary region to be the new primary copy. Ensuring ongoing availability in the event of a regional outage.

When the regional outage has concluded, the ability to reverse the replication from the recovery region back to the original region is done using the **Reprotect** action. This ensures that the databases are protected against future disasters impacting their new region, and prepares them for migration back to the original region if desired.

## Prerequisites

Prior to performing a failover, the recovery group should have been created and be successfully replicating to the secondary cluster. See [Get Started with Recovery Groups](/tidb-cloud/recovery-group-get-started.md)

![Protected Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-protected.png)

## Failover databases using a recovery group

In the event of a disaster, the recovery group is used to failover databases to the secondary cluster.

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **Project Settings** in the left navigation pane.

2. On the **Project Settings** navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, click the name of the recovery group that you wish to failover.

4. Click the **Action** menu for the recovery group, and then click **Failover**. The failover dialog will open.

    > **Warning**
    >
    > Performing a failover will sever the existing replication relationship.

5. Select the secondary TiDB Cloud cluster that will be promoted to the primary copy. Ensure that the selected cluster is in a healthy state.

6. Confirm that you understand the potentially disruptive nature of a failover by typing **Failover** into the confirmation entry and clicking **I understand, Failover Group** to begin the failover.

    ![Fail Over Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-failover.png)

## Reprotect databases using a recovery group

After a failover completes, the replica databases on the secondary cluster are now the primary copy. However, these databases are unprotected against future disasters as the replication relationship is stopped by the failover process.

If the cluster that was impacted by the disaster is able to be brought online again, a replication relationship from the recovery region back to the original region can be established. This is performed using the **Reprotect** action.

![Unprotected Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-unprotected.png)

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **Project Settings** in the left navigation pane.

2. On the **Project Settings** navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, click the name of the recovery group that you wish to reprotect.

    > **Note**
    >
    > The **Recovery Group Detail** page provides information about the recovery group including current status and replication topology.
    > During the reprotect synchronization, due to the volume of data transferred, the online query performance at the primary or secondary clusters might be affected. Schedule the reprotection of databases for a less busy period.

    > **Warning**
    > 
    > As part of the data replication necessary to perform the reprotect operation, the content of the selected databases will be replaced at the target cluster by the content of the databases from the (new) primary cluster. If you wish to preserve the unique content on the target cluster, complete a backup before performing the Reprotect operation.

4. Click the **Action** menu for the recovery group, and then click **Reprotect**. The reprotect dialog appears.

5. Confirm the reprotect operation by clicking **I understand, Failover Group** to begin the reprotect operation.

    ![Reprotect Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-reprotected.png)

## What's next

After creating the recovery group, you might want to familiarize yourself with the failover and reprotect operations. These operations are used to **Failover** the primary cluster for the replicated databases from one cluster to the other, and then to later reestablish replication in the opposite direction to **Reprotect** the failed over databases.

- [Failover Databases](/tidb-cloud/recovery-group-failover.md)
- [Failover and Reprotect Databases](/tidb-cloud/recovery-group-failover.md)
