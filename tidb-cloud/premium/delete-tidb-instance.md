---
title: Delete a {{{ .premium }}} instance
summary: Learn how to delete a {{{ .premium }}} instance.
---

# Delete a {{{ .premium }}} instance

This document describes how to delete a {{{ .premium }}} instance.

You can delete an instance at any time by performing the following steps:

1. Navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page.
2. In the row of your target instance to be deleted, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the target instance to go to its overview page, and then click **...** in the upper-right corner.

3. Click **Delete** in the drop-down menu.
4. In the deletion confirmation window, confirm the deletion:

    Enter `<organization name>/<instance name>` to ensure the instance is deleted correctly.

    If you want to restore the instance some time in the future, make sure that you have a backup of the instance. Otherwise, you cannot restore it. For more information about how to back up {{{ .premium }}} instances, see [Back Up and Restore {{{ .premium }}} Data](/tidb-cloud/backup-and-restore-premium.md).

5. Click **I understand, delete it**.

    Once you delete a backed up {{{ .premium }}} instance, the existing backup files of the instance are moved to the recycle bin.

    - Automatic backups will expire and be automatically deleted once the retention period ends. The default retention period is 7 days if you don't modify it.
    - Manual backups will be kept in the Recycle Bin until manually deleted.

    > **Note:**
    >
    > Please be aware that backups will continue to incur charges until deleted.

    If you want to restore a {{{ .premium }}} instance from the recycle bin, see [Restore a deleted instance](/tidb-cloud/backup-and-restore-premium.md#restore-a-deleted-instance).
