---
title: Delete Recovery Group
summary: Learn how to delete a Recovery Group when it is no longer needed
---

# Delete Recovery Group

When a Recovery Group is no longer needed it may be deleted.

## Delete a Recovery Group

When a recovery group is no longer needed to manage the replication of a set of databases it may be deleted form the system.

1. In the TiDB Cloud console, click **Project Settings** in the left navigation pane.

2. On the project settings navigation pane, click **Recovery Group**.

3. On the recovery group page, click the name of the recovery group that you wish to delete.

4. Click the action menu for the recovery group, and click **Delete**. The failover dialog will open.

    > **Warning**
    >
    > - Deleting a Recovery Group also removes any of the associated replication relationship that were associated with that Recovery Group. 
    > - The databases associated with the Recovery Group are no longer protected against disaster.

5. Confirm that you understand the impacting of the deletion by typing the name of the recovery group and clicking **I understand, delete it** to delete the recovery group.

