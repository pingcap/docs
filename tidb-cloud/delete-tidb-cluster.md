---
title: Delete a TiDB Cluster
summary: Learn how to delete a TiDB cluster.
---

# Delete a TiDB Cluster

This document describes how to delete a TiDB cluster on TiDB Cloud.

You can delete a cluster at any time by performing the following steps:

1. Navigate to the TiDB Clusters page and click the name of a cluster that you want to delete. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Delete** in the drop-down menu.
4. In the cluster deleting window, enter the cluster name to confirm.
5. Click **I understand the consequences, delete this cluster**.

When you delete a TiDB cluster, TiDB Cloud automatically creates a backup of the deleted cluster in the recycle bin and retains the backup for 7 days. If you want to restore a deleted cluster from recycle bin, see [Restore a deleted cluster](backup-and-restore.md#restore-a-deleted-cluster).