---
title: Back Up and Restore {{{ .premium }}} Data
summary: Learn how to back up and restore your {{{ .premium }}} instances.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore {{{ .premium }}} Data

This document describes how to back up and restore your data on {{{ .premium }}} instances. {{{ .premium }}} supports automatic backup and lets you restore backup data to a new instance as needed.

Backup files can originate from the following sources:

- Active {{{ .premium }}} instances
- The Recycle Bin for backups from deleted Premium instances

> **Tip:**
>
> - To learn how to back up and restore data on {{{ .dedicated }}} clusters, see [Back Up and Restore {{{ .dedicated }}} Data](/tidb-cloud/backup-and-restore.md).
> - To learn how to back up and restore data on {{{ .starter }}} or {{{ .essential }}} clusters, see [Back Up and Restore {{{ .starter }}} or Essential Data](/tidb-cloud/backup-and-restore-serverless.md).

## View the Backup page

1. On the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and instances.

2. In the left navigation pane, click **Data** > **Backup**.

## Automatic backups

TiDB Cloud automatically backs up your instance data, letting you restore data from a backup snapshot to minimize data loss in the event of a disaster.

### Learn about the backup setting

Compared with {{{ .starter }}} clusters and {{{ .essential }}} clusters, {{{ .premium }}} offers enhanced backup capabilities, including longer retention and hourly backup support.

| Backup setting   | {{{ .starter }}} (free) | {{{ .starter }}} (with spending limit > 0) | {{{ .essential }}} | {{{ .premium }}} |
|------------------|--------------------------|---------------------------------------------|--------------------|------------------|
| Backup Cycle     | Daily                    | Daily                                       | Daily              | Daily + Hourly   |
| Backup Retention | 1 day                    | 30 days                                     | 30 days            | Up to 33 days    |
| Backup Time      | Fixed time               | Configurable                               | Configurable       | Configurable     |

- **Backup Cycle** determines how frequently backups are created.

    - Premium instances support both **daily** and **hourly** backups.
    - The **default** is **hourly backups**.

- **Backup Retention** is the duration for which backups are retained. Expired backups cannot be restored.

    - Premium instances can retain backups for up to **33 days**.

- **Backup Time** is the scheduled start time for backups.

    - For Premium instances, **daily backups** can be configured to start at a preferred time (in 30-minute intervals), while **hourly backups** always run on the hour.

### Configure the backup settings

To configure backups for a {{{ .premium }}} instance, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your TiDB instance.

2. Click **Backup Setting**. This will open the **Backup Setting** window, where you can configure automatic backup options.

3. In **Backup Cycle**, choose between the **Hourly Backup** and **Daily Backup** tabs:

    - **Hourly Backup** (default):
        - Runs **on the hour**.
        - You can configure **Backup Retention** (1–33 days).
    - **Daily Backup**:
        - Runs at a configurable time in **30-minute intervals**.
        - You can configure both **Backup Retention** (1–33 days) and **Backup Time**.

4. Click **Save** to save your settings.

### Delete backup files

To delete an existing backup file for your {{{ .premium }}} instance, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your instance.

2. Locate the corresponding backup file you want to delete, and click **...** > **Delete** in the **Action** column.

## Restore

TiDB Cloud provides restore functionality to help recover data in case of accidental loss or corruption. You can restore from backups of active instances or from deleted instances in the Recycle Bin.

### Restore mode

TiDB Cloud supports snapshot restore and point-in-time restore for your instance.

- **Snapshot Restore**: restores your instance from a specific backup snapshot.

- **Point-in-Time Restore**: restores your instance to a specific point in time.

    - Premium instances: can be restored to any time within the last 33 days, but not earlier than the instance creation time or later than one minute before the current time.

### Restore destination

TiDB Cloud supports restoring data to a new instance.

### Restore to a new instance

To restore your data to a new instance, take the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your instance.

2. Click **Restore**.

3. On the **Select Backup** page, choose the **Restore Mode** you want to use. You can restore from a specific backup snapshot or restore to a specific point in time.

    <SimpleTab>
    <div label="Snapshot Restore">

    To restore from a selected backup snapshot, take the following steps:

    1. Click **Snapshot Restore**.
    2. Select the backup snapshot you want to restore from.

    </div>
    <div label="Point-in-Time Restore">

    To restore to a specific point in time for a Premium instance, take the following steps:

    1. Click **Point-in-Time Restore**.
    2. Select the date and time you want to restore to.

    </div>
    </SimpleTab>

4. Click **Next** to proceed to the **Restore to a New Instance** page.

5. Configure your new TiDB instance for restoration. The steps are the same as [creating a new TiDB instance](/tidb-cloud/premium/create-tidb-instance-premium.md).

    > **Note:**
    >
    > The new instance uses the same cloud provider and region as the backup by default.

6. Click **Restore** to start the restore process.

    When the restore process starts, the instance status first changes to **Creating**. After the creation is complete, it changes to **Restoring**. The instance remains unavailable until the restore finishes and the status changes to **Available**.

### Restore from Recycle Bin

To restore a deleted instance from the Recycle Bin, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com), and then navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page. In the top-right corner, click **Recycle Bin**.

2. On the **Recycle Bin** page, locate the TiDB instance you want to restore:

    - Click the **>** button to expand instance details.
    - Find the desired backup, click **...** in the **Action** column, and then select **Restore**.

3. On the **Restore** page, follow the same steps as [Restore to a new instance](#restore-to-a-new-instance) to restore the backup to a new instance.

### Restore backups from a different plan type

Currently, you can only restore backups from a {{{ .dedicated }}} cluster hosted on AWS to a new {{{ .premium }}} instance.

To restore a backup generated by a {{{ .dedicated }}} cluster, follow these steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com), and then navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page. In the upper-right corner, click **...**, and then click **Restore from Another Plan**.

2. On the **Select Backup** page, select the project that contains the target {{{ .dedicated }}} cluster. Select the cluster, select the backup snapshot that you want to restore, and then click **Next**.

    > **Note:**
    >
    > - Ensure that the cluster that contains the backup snapshot is in either the **Active** or **Deleted** status within the selected project.
    > - The snapshot must be located in a region that {{{ .premium }}} supports. If the region is not supported, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to open a new region for {{{ .premium }}}, or select another backup snapshot.

3. On the **Restore** page, follow the same steps as [Restore to a new instance](#restore-to-a-new-instance) to restore the backup to a new instance.

### Restore backups from cloud storage

{{{ .premium }}} supports restoring backups from cloud storage (such as Amazon S3 and Alibaba Cloud Object Storage Service (OSS)) to a new instance. This feature is compatible with backups generated from {{{ .dedicated }}} clusters or TiDB Self-Managed clusters.

>**Note:**
>
> - Currently, only backups located in **Amazon S3** and **Alibaba Cloud OSS** are supported for restore.
> - You can restore backups only to a new instance hosted by the same cloud provider as your storage bucket.
> - If the instance and the storage bucket are located in different regions, additional cross-region data transfer fees might apply.

#### Steps

Before you begin, ensure that you have an access key and secret key with sufficient permissions to access the backup files.

To restore backups from cloud storage, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com), and then navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page. In the upper-right corner, click **...** , and then click **Restore from Cloud Storage**.

2. On the **Select Backup Storage Location** page, provide the following information:

    - **Cloud Provider**: select the cloud provider where your backup files are stored.
    - **Region**: if your cloud provider is Alibaba Cloud OSS, select a Region.
    - **Backup Files URI**: enter the URI of the top-level folder that contains your backup files.
    - **Access Key ID**: enter your access key ID.
    - **Access Key Secret**: enter your access key secret.

> **Tip:**
>
> To create an access key for your storage bucket, see [Configure Amazon S3 access using an AWS access key](#configure-amazon-s3-access-using-an-aws-access-key) and [Configure Alibaba Cloud OSS access](#configure-alibaba-cloud-oss-access).

3. Click **Verify Backup and Next**.

4. If the verification is successful, the **Restore to a New Instance** page appears. Review the backup information displayed at the top of the page, and then follow the steps in [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md) to restore the backup to a new instance.

    If the backup information is incorrect, click **Previous** to return to the previous page, and then enter the correct information.

5. Click **Restore** to restore the backup.

## Limitations

Currently, manual backups are not supported for {{{ .premium }}} instances.

## References

This section describes how to configure Amazon S3 access using an AWS access key and Alibaba Cloud OSS access.

### Configure Amazon S3 access using an AWS access key

It is recommended that you use an IAM user (instead of the AWS account root user) to create an access key.

Take the following steps to configure an access key:

1. Create an IAM user and access key.

    1. Create an IAM user. For more information, see [Create an IAM user in your AWS account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console).
    2. Use your AWS account ID or account alias, and your IAM user name and password to sign in to [the IAM console](https://console.aws.amazon.com/iam).
    3. Create an access key. For more information, see [creating an access key for an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey).

2. Grant permissions to the IAM user.

    Create a policy and attach it to the IAM user. Ensure that the policy includes the required permissions based on your task. To restore data to a {{{ .premium }}} instance, grant `s3:GetObject`, `s3:GetBucketLocation`, and `s3:ListBucket` permissions.

    The following is an example policy that allows TiDB Cloud to **restore** data from a specific folder in your Amazon S3 bucket.

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowGetBucketLocation",
                "Effect": "Allow",
                "Action": "s3:GetBucketLocation",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>"
            },
            {
                "Sid": "AllowListPrefix",
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>",
                "Condition": {
                    "StringLike": {
                        "s3:prefix": "<Your backup folder>/*"
                    }
                }
                }
            {
                "Sid": "AllowReadObjectsInPrefix",
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>/<Your backup folder>/*"
            }
        ]
    }
    ```

    In the preceding policy, replace `<Your S3 bucket name>` and `<Your backup folder>` with your actual bucket name and backup directory. This configuration follows the principle of least privilege by restricting access to only the necessary backup files.

> **Note:**
>
> TiDB Cloud does not store your access keys. It is recommended that you [delete the access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) after the import or export is complete.

### Configure Alibaba Cloud OSS access

To allow TiDB Cloud to access your Alibaba Cloud OSS bucket, you need to create an AccessKey pair for the bucket.

Take the following steps to configure an AccessKey pair:

1. Create a RAM user and get the AccessKey pair. For more information, see [Create a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user).

    In the **Access Mode** section, select **Using permanent AccessKey to access**.

2. Create a custom policy with the required permissions. For more information, see [Create custom policies](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy).

    - In the **Effect** section, select **Allow**.
    - In the **Service** section, select **Object Storage Service**.
    - In the **Action** section, select the permissions as needed. To restore a backup to a TiDB Cloud instance, grant `oss:ListObjects` and `oss:GetObject` permissions.

        The following is a JSON example for a Restore task. This example restricts access to a specific bucket and backup folder.

        ```json
        {
        "Version": "1",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": "oss:ListObjects",
            "Resource": "acs:oss:*:*:<Your bucket name>",
            "Condition": {
                "StringLike": {
                "oss:Prefix": "<Your backup folder>/*"
                }
            }
            },
            {
            "Effect": "Allow",
            "Action": "oss:GetObject",
            "Resource": "acs:oss:*:*:<Your bucket name>/<Your backup folder>/*"
            }
        ]
        }
        ```

        > **Tip:**
        >
        > For **restore** operations, you can enhance security by restricting access to only the specific folder (prefix) where your backup files are stored, rather than granting access to the entire bucket.

    - In the **Resource** section, select the bucket and the objects in the bucket.

3. Attach the custom policies to the RAM user. For more information, see [Grant permissions to a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user).
