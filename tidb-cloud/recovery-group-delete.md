---
title: Delete a Recovery Group
summary: Learn how to delete a Recovery Group when it is no longer needed.
---

# Delete a Recovery Group

When a recovery group is no longer needed, you can delete it.

## Delete a recovery group

When a recovery group is no longer needed to manage the replication of a set of databases, you can delete it from the system.

1. In the [TiDB Cloud console](https://tidbcloud.com/), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Recovery Group**.
3. On the **Recovery Group** page, locate the name of the recovery group that you wish to delete.
4. Click the **Action** menu for the recovery group, and then click **Delete**. The deletion dialog is displayed.

    > **Warning**
    >
    > - Deleting a recovery group also removes all associated replication relationships associated with that recovery group. 
    > - The databases associated with the recovery group are no longer protected against disasters.

5. Confirm that you understand the impact of the deletion by typing the name of the recovery group and clicking **I understand, delete it**.
