---
title: Failover and Reprotect Databases
summary: Learn how to use a Recovery Group to failover and reprotect databases between TiDB Cloud clusters.
---

# Failover and Reprotect Databases

Databases in a recovery group are replicated from one cluster to another, typically in a different region of the cloud service provider.

The **Failover** action promotes the replicated databases in the secondary region to be the new primary copy, ensuring ongoing availability during a regional outage.

When the regional outage is resolved, the ability to reverse the replication from the recovery region back to the original region is done using the **Reprotect** action. This ensures that the databases are protected against future disasters impacting their new region, and prepares them for migration back to the original region if desired.

## Prerequisites

Before performing a failover, a recovery group should have been created and be successfully replicating to the secondary cluster. For more information, see [Get Started with Recovery Groups](/tidb-cloud/recovery-group-get-started.md).

![Protected Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-protected.png)

## Failover databases using a recovery group

In the event of a disaster, you can use the recovery group to failover databases to the secondary cluster.

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to your target project using the combo box in the upper-left corner.

2. In the left navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, locate the name of the recovery group that you wish to failover.

4. Click the **Action** menu for the recovery group, and then click **Failover**. The failover dialog is displayed.

    > **Warning**
    >
    > Performing a failover will sever the existing replication relationship.

5. Select the secondary TiDB Cloud cluster to be promoted to the primary copy. Ensure that the selected cluster is in a healthy state.

6. Confirm that you understand the potentially disruptive nature of a failover by typing **Failover** into the confirmation entry and clicking **I understand, failover group** to begin the failover.

    ![Fail Over Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-failover.png)

## Reprotect databases using a recovery group

After a failover completes, the replica databases on the secondary cluster are now the primary copy. However, these databases are unprotected against future disasters as the replication relationship is stopped by the failover process.

If the original primary cluster that was affected by the disaster can be brought online again, you can re-establish replication from the recovery region back to the original region using the **Reprotect** action.

![Unprotected Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-unprotected.png)

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to your target project using the combo box in the upper-left corner.

2. In the left navigation pane, click **Recovery Group**.

3. On the **Recovery Group** page, locate the name of the recovery group that you wish to reprotect.

    > **Note**
    >
    > The **Recovery Group Detail** page provides information about the recovery group, including current status and replication topology.
    > During the reprotect synchronization, due to the volume of data transferred, the online query performance at the primary or secondary clusters might be affected. It is recommended that you schedule the reprotection of databases for a less busy period.

    > **Warning**
    > 
    > As part of the data replication necessary to perform the reprotect operation, the content of the selected databases will be replaced at the target cluster by the content of the databases from the (new) primary cluster. If you wish to preserve the unique content on the target cluster, complete a backup before performing the Reprotect operation.

4. Click the **Action** menu for the recovery group, and then click **Reprotect**. The reprotect dialog is displayed.

5. Confirm the reprotect operation by clicking **Reprotect** to begin the reprotect operation.

    ![Reprotect Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-reprotected.png)
