---
title: Back Up and Restore {{{ .starter }}} or Essential Data
summary: Learn how to back up and restore your {{{ .starter }}} or {{{ .essential }}} instances.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore {{{ .starter }}} or Essential Data

This document describes how to back up and restore your data on {{{ .starter }}} or {{{ .essential }}} instances.

> **Tip:**
>
> To learn how to back up and restore data on TiDB Cloud Dedicated clusters, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md).

## View the Backup page

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target {{{ .starter }}} or Essential instance to go to its overview page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the left navigation pane, click **Data** > **Backup**.

## Automatic backups

TiDB Cloud automatically backs up your data, allowing you to restore data from a backup snapshot to minimize data loss in the event of a disaster.

### Learn about the backup setting

Automatic backup settings vary between {{{ .starter }}} instances and {{{ .essential }}} instances, as shown in the following table:

| Backup setting   | {{{ .starter }}} (free) | {{{ .starter }}} (with spending limit > 0) | {{{ .essential }}} |
|------------------|----------------------------|----------------------------|----------------------------|
| Backup Cycle     | Daily                      | Daily                      | Daily                      |
| Backup Retention | 1 day                      | Up to 30 days              | Up to 30 days              |
| Backup Time      | Fixed time                 | Configurable               | Configurable               |

- **Backup Cycle** is the frequency at which backups are taken.

- **Backup Retention** is the duration for which backups are retained. Expired backups cannot be restored.

    - For a free {{{ .starter }}} instance, the backup retention is 1 day.
    - For a {{{ .starter }}} (with spending limit > 0) or {{{ .essential }}} instance, you can configure the backup retention to any value between 1 and 30 days. The default retention is 14 days.

- **Backup Time** is the time when the backup starts to be scheduled. Note that the final backup time might fall behind the configured backup time.

    - For a free {{{ .starter }}} instance, the backup time is a randomly fixed time.
    - For a {{{ .starter }}} (with spending limit > 0) or {{{ .essential }}} instance, you can configure the backup time to every half an hour. The default value is a randomly fixed time.

### Configure the backup setting

To set the backup time for a {{{ .essential }}} instance, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your {{{ .starter }}} or Essential instance.

2. Click **Backup Setting**. This will open the **Backup Setting** window, where you can configure the automatic backup settings according to your requirements.

3. In **Backup Time**, schedule a start time for the daily backup.

4. Click **Confirm**.

## Manual backups

Manual backups are supported for {{{ .essential }}} instances created on or after July 1, 2026. You can create a manual backup before high-risk operations, such as critical data deletion or irreversible schema changes.

### Retention and deletion

Manual backups are retained until you explicitly delete them. The automatic backup retention setting does not apply to manual backups. If you delete the instance, its manual backups move to the Recycle Bin and remain there until you manually delete them. Backups in the Recycle Bin continue to incur charges until deleted. For more information, see [Delete a TiDB Cloud Resource](/tidb-cloud/delete-tidb-cluster.md).

### Create a manual backup in the console

1. Navigate to the [**Backup**](#view-the-backup-page) page of your {{{ .essential }}} instance.

2. In the upper-right corner, click **...**, and then click **Manual Backup**.

3. Confirm the operation. The backup appears in the **Backup List**.

4. Wait until the backup completes successfully before using it for a [snapshot restore](#restore-to-a-new-instance).

### Create a manual backup using the API

You can create a manual backup using the [TiDB Cloud API v1beta2](/api/tidb-cloud-api-v1beta2.md#essential-manual-backups). Before you begin, [create an API key](/api/tidb-cloud-api-overview.md) and set the `PUBLIC_KEY`, `PRIVATE_KEY`, and `TIDB_ID` environment variables to your API public key, private key, and instance ID, respectively.

1. Send a request to create a manual backup. Replace `before-schema-change` with your desired backup name.

    ```shell
    curl --request POST \
      --url "https://cloud.tidbapi.com/v1beta2/tidbs/${TIDB_ID}/backups" \
      --digest --user "${PUBLIC_KEY}:${PRIVATE_KEY}" \
      --header 'Content-Type: application/json' \
      --data '{"name":"before-schema-change"}'
    ```

    The response contains the `backupId` of the backup. A successful response means that the backup request was accepted, not that the backup has completed.

2. List the instance's backups to check the state of the backup with the returned `backupId`:

    ```shell
    curl --request GET \
      --url "https://cloud.tidbapi.com/v1beta2/tidbs/${TIDB_ID}/backups?pageSize=100" \
      --digest --user "${PUBLIC_KEY}:${PRIVATE_KEY}"
    ```

    Match the returned `backupId` to the `id` field of a backup in the list. If the response includes a `nextPageToken`, use it as the `pageToken` query parameter to retrieve additional results.

3. Wait until the backup state is `SUCCEEDED` before using it for a [snapshot restore](#restore-to-a-new-instance).

### Delete a manual backup

1. Navigate to the [**Backup**](#view-the-backup-page) page of your {{{ .essential }}} instance. If the instance has been deleted, locate its backups in the [Recycle Bin](#restore-from-recycle-bin).

2. Locate the manual backup you want to delete, click **...** in its row, and then click **Delete**.

3. Confirm the deletion. The deleted backup can no longer be used to restore your data.

## Restore

TiDB Cloud offer restore functionality to help recover data in case of accidental loss or corruption.

### Restore mode

TiDB Cloud supports snapshot restore and point-in-time restore for your {{{ .starter }}} or Essential instance.

- **Snapshot Restore**: restores your {{{ .starter }}} or Essential instance from a specific backup snapshot. For {{{ .essential }}} instances created on or after July 1, 2026, you can restore from either an automatic or a manual backup.

- **Point-in-Time Restore (PREVIEW)**: restores your {{{ .essential }}} instance to a specific time.

    - {{{ .starter }}} instances: not supported.
    - {{{ .essential }}} instances: restores to any time within the backup retention, but not earlier than the {{{ .essential }}} instance creation time or later than one minute before the current time.

    Point-in-time restore applies to automatic backups and is not supported for manual backups.

### Restore destination

TiDB Cloud supports restoring data to a new {{{ .starter }}} or Essential instance.

### Restore timeout

The restore process typically completes within a few minutes. If the restore takes longer than three hours, it is automatically canceled and the new {{{ .starter }}} or Essential instance is deleted, while the source instance remains unchanged.

If the data is corrupted after a canceled restore and cannot be recovered, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance.

### Restore to a new {{{ .starter }}} or Essential instance {#restore-to-a-new-instance}

> **Note:**
>
> User credentials and permissions from the source {{{ .starter }}} or Essential instance will not be restored to the new {{{ .starter }}} or Essential instance.

To restore your data to a new {{{ .starter }}} or Essential instance, take the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your {{{ .starter }}} or Essential instance.

2. Click **Restore**.

3. In **Restore Mode**, you can choose to restore from a specific backup or any point in time.

    <SimpleTab>
    <div label="Snapshot Restore">

    To restore from a selected backup snapshot, take the following steps:

    1. Click **Snapshot Restore**.
    2. Select the backup snapshot you want to restore from. To restore a manual backup of an {{{ .essential }}} instance, select the completed manual backup.

    </div>
    <div label="Point-in-Time Restore">

    To restore to a specific point in time for a {{{ .essential }}} instance, take the following steps:

    1. Click **Point-in-Time Restore**.
    2. Select the date and time you want to restore to.

    </div>
    </SimpleTab>

4. Enter a name for the new instance.
5. Update the capacity as needed.

    - For a {{{ .starter }}} instance, if you need more resources than the [free quota](/tidb-cloud/select-cluster-tier.md#usage-quota), set a monthly spending limit.
    - For a {{{ .essential }}} instance, set the minimum RCU and maximum RCU, and then configure advanced settings as needed.

6. Click **Restore** to begin the restore process.

Once the restore process begins, the {{{ .starter }}} or Essential instance status changes to **Restoring**. The {{{ .starter }}} or Essential instance will remain unavailable until the restore is complete and the status changes to **Available**.

### Restore from Recycle Bin

> **Note:**
>
> {{{ .starter }}} does not support restoring from Recycle Bin.

To restore a deleted {{{ .essential }}} instance from the Recycle Bin, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, click **...** in the upper-right corner, and then click **Recycle Bin**.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. On the **Recycle Bin** page, click the **Essential** tab to go to the recycle bin of {{{ .essential }}} instances.

3. Locate the {{{ .essential }}} instance you want to restore, and then click the **>** button to expand the available backups of the instance. For instances created on or after July 1, 2026, this list can include manual backups. Manual backups remain available until you explicitly delete them.

    > **Note:**
    >
    > If a {{{ .essential }}} instance **has no backup**, the deleted instance is not displayed in the Recycle Bin.

4. In the row of your desired backup, click **...**, and then select **Restore**.

5. On the **Restore** page, follow the same steps as [Restore to a new instance](#restore-to-a-new-instance) to restore the backup to a new instance.

## Limitations

- If a TiFlash replica is enabled, it will be unavailable for a period after the restore, because the data needs to be rebuilt in TiFlash.
- Manual backups are not supported for {{{ .starter }}} instances or {{{ .essential }}} instances created before July 1, 2026.
- Manual backups do not support point-in-time restore or partial backups, such as table-level or database-level backups. Each restore creates a new instance; restoring a manual backup to an existing instance is not supported.
- A {{{ .starter }}} or {{{ .essential }}} instance with more than 1 TiB of data does not support restoring to a new instance by default. Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance with larger datasets.
