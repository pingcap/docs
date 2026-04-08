---
title: Delete a TiDB Cloud Resource
summary: Learn how to delete a TiDB Cloud Resource.
---

# Delete a TiDB Cloud Resource

This document describes how to delete the following TiDB Cloud resources:

- [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) instance
- [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) instance
- [{{{ .dedicated }}}](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster

You can delete a TiDB Cloud resource at any time by performing the following steps:

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.
2. In the row of your target resource to be deleted, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the target resource to go to its overview page, and then click **...** in the upper-right corner.

3. Click **Delete** in the drop-down menu.
4. In the deletion confirmation window, confirm the deletion:

    - If you have at least one manual or automatic backup, you can see the number of backups and the charging policy for backups. Click **Continue** and enter `<organization name>/<project name>/<resource name>`.
    - If you do not have any backups, just enter `<organization name>/<project name>/<resource name>`.

    If you want to restore a deleted {{{ .essential }}} instance or {{{ .dedicated }}} cluster sometime in the future, make sure that you have a backup of it. Otherwise, you cannot restore it anymore.

    - For more information about how to back up {{{ .essential }}} instances, see [Back Up and Restore {{{ .essential }}} Data](/tidb-cloud/backup-and-restore-serverless.md).
    - For more information about how to back up TiDB Cloud Dedicated clusters, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md).

    > **Note:**
    >
    > [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) instances do not support restoring data after the deletion. If you want to delete a {{{ .starter }}} instance and restore its data in the future, see [Export Data from {{{ .starter }}}](/tidb-cloud/serverless-export.md) to export your data as a backup.

5. Click **I understand, delete it**.

    Once a backed up {{{ .essential }}} instance or TiDB Cloud Dedicated cluster is deleted, the existing backup files of it are moved to the Recycle Bin.

    - Automatic backups will expire and be automatically deleted once the retention period ends, except for the latest one. The default retention period is 7 days if you don't modify it. The latest automatic backup will not be deleted unless you explicitly delete it.
    - Manual backups will be kept in the Recycle Bin until manually deleted.

    > **Note:**
    >
    > Please be aware that backups will continue to incur charges until deleted.

    If you want to restore data from Recycle Bin, see the following documents:

    - [Restore a deleted {{{ .essential }}} instance](/tidb-cloud/backup-and-restore-serverless.md#restore-from-recycle-bin).
    - [Restore a deleted TiDB Cloud Dedicated cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster).
