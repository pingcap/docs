---
title: Delete a TiDB Cloud Premium instance
summary: Learn how to delete a TiDB cluster.
---

# Delete a TiDB Cloud Premium instance

This document describes how to delete a TiDB Cloud Premium instance.

You can delete a instance at any time by performing the following steps:

1. Navigate to the [**TiDBs**](https://tidbcloud.com/tidbs) page of your project.
2. In the row of your target instance to be deleted, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the target instance to go to its overview page, and then click **...** in the upper-right corner.

3. Click **Delete** in the drop-down menu.
4. In the cluster deleting window, confirm the deletion:

    Enter `<organization name>/<cluster name>` to ensure the cluster is deleted correctly.

    If you want to restore the cluster sometime in the future, make sure that you have a backup of the cluster. Otherwise, you cannot restore it anymore. For more information about how to back up TiDB Cloud Dedicated clusters, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore-premium.md).

    > **Note:**
    >
    > [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) and [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) clusters do not support restoring data after the deletion. If you want to delete a {{{ .starter }}} or {{{ .essential }}} cluster and restore its data in the future, see [Export Data from {{{ .starter }}} or Essential](/tidb-cloud/serverless-export.md) to export your data as a backup.

5. Click **I understand, delete it**.

    Once a backed up TiDB Cloud Dedicated cluster is deleted, the existing backup files of the cluster are moved to the recycle bin.

    - Automatic backups will expire and be automatically deleted once the retention period ends. The default retention period is 7 days if you don't modify it.
    - Manual backups will be kept in the Recycle Bin until manually deleted.

    > **Note:**
    >
    > Please be aware that backups will continue to incur charges until deleted.

    If you want to restore a TiDB Cloud Premium cluster from recycle bin, see [Restore a deleted cluster](/tidb-cloud/backup-and-restore-premium.md#restore-a-deleted-cluster).
