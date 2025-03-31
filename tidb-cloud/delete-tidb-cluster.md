---
title: Delete a TiDB Cluster
summary: Learn how to delete a TiDB cluster.
---

# Delete a TiDB Cluster

This document describes how to delete a TiDB cluster on TiDB Cloud.

You can delete a cluster at any time by performing the following steps:

1. Navigate to the [**Clusters**](https://console.tidb.io/clusters) page of your project.
2. In the row of your target cluster to be deleted, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the target cluster to go to its overview page, and then click **...** in the upper-right corner.

3. Click **Delete** in the drop-down menu.
4. In the cluster deleting window, confirm the deletion:

    - If you have at least one manual or automatic backup, you can see the number of backups and the charging policy for backups. Click **Continue** and enter `<organization name>/<project name>/<cluster name>`.
    - If you do not have any backups, just enter `<organization name>/<project name>/<cluster name>`.

    If you want to restore the cluster sometime in the future, make sure that you have a backup of the cluster. Otherwise, you cannot restore it anymore.

    > **Note:**
    >
    > [TiDB Cloud Starter clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-starter) do not support restoring data after the deletion. If you want to delete a TiDB Cloud Starter cluster and restore its data in the future, see [Export Data from TiDB Cloud](/tidb-cloud/serverless-export.md) to export your data as a backup.

5. Click **I understand, delete it**.

    Automatic backups will expire and be automatically deleted once the retention period ends.

    > **Note:**
    >
    > Please be aware that backups will continue to incur charges until deleted.
