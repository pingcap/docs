---
title: Failover and Reprotect Databases
summary: Learn how to use a Recovery Group to Failover and Reprotect databases between TiDB Cloud clusters
---

# Failover and Reprotect Databases

Databases that are part of a replication group are replicated from one cluster to another (typucally in a different region of the cloud service provider).

The **Failover** action promotes the replicated copy of the databases at the secondary region to be the new primary copy. Ensuring ongoing availability in the event of a regional outage.

When the regional outage has concluded, the ability to reverse the replication from the recovery region back to the original region is done using the **Reprotect** action. This ensures that the databases are protected against future disasters impacting their new region, and prepares them for migration back to the original region if desired.

## Prerequisites

Prior to performing a failover, the Recovery Group should have been created and be successfully replicating to the secondary cluster. See [Get Started with Recovery Groups](/tidb-cloud/recovery-group-get-started.md)

![Protected Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-protected.png)

## Failover Databases using Recovery Group

In the event of a disaster the recovery group is used to fail over databases to the secondary cluster.

1. In the TiDB Cloud console, click **Project Settings** in the left navigation pane.

2. On the project settings navigation pane, click **Recovery Group**.

3. On the recovery group page, click the name of the recovery group that you wish to failover.

4. Click the action menu for the recovery group, and click **Failover**. The failover dialog will open.

    > **Warning**
    >
    > Performing a failover will sever the existing replication relationship.

5. Select the secondary TiDB Cloud cluster that will be promoted to the primary copy. Ensure that the selected cluster is in a healthy state.

6. Confirm that you understand the potentially disruptive nature of a failover by typing **Failover** into the confirmation entry and clicking **I understand, Failover Group** to begin the failover.

    ![Fail Over Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-failover.png)

## Reprotect Databases using Recovery Group

After a failover completes, the replica databases on the secondary cluster are now the primary copy. However, these databases are unprotected against future disasters as the replication relationship is stopped by the failover process.

If the cluster that was impacted by the disaster is able to be brought online again, a replication relationship from the recovery region back to the original region can be established. This is performed using the **Reprotect** action.

![Unprotected Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-unprotected.png)

1. In the TiDB Cloud console, click **Project Settings** in the left navigation pane.

2. On the project settings navigation pane, click **Recovery Group**.

3. On the recovery group page, click the name of the recovery group that you wish to reprotect.

    > **Note**
    >
    > The **Recovery Group Detail** page provides information about the recovery group including current status and replication topology.

4. Click the action menu for the recovery group, and click **Reprotect**. The reprotect dialog will open.

5. Confirm the reprotect operation by clicking **I understand, Failover Group** to begin the reprotect operation.

    ![Reprotect Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-reprotected.png)

## What's next

After creating the recovery group you may want to familiarize yourself with the failover and reprotect operations. These operations are used to (1) **Failover** the primary cluster for the replicated databases from one cluster to the other, and then to later (2) reestablish replication in the opposite direction to **Reprotect** the failed over databases.

- [Failover Databases](/tidb-cloud/recovery-group-failover.md)
- [Reprotect Databases](/tidb-cloud/recovery-group-reprotect.md)

