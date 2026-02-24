---
title: 2024-04-11 TiDB Cloud Data Migration (DM) Feature Maintenance Notification
summary: Learn about the details of TiDB Cloud Data Migration (DM) feature maintenance on April 11, 2024, such as the maintenance window and impact.
---

# [2024-04-11] TiDB Cloud Data Migration (DM) Feature Maintenance Notification

This notification describes the details that you need to know about the maintenance for [Data Migration (DM) feature](/tidb-cloud/migrate-from-mysql-using-data-migration.md) of TiDB Cloud Dedicated on April 11, 2024.

## Maintenance window

- Start time: 2024-04-11 08:00 (UTC+0)
- End time: 2024-04-11 09:00 (UTC+0)
- Duration: 1 hour

## Impact

During the maintenance window, the DM feature for TiDB Cloud Dedicated clusters in the following regions will be affected:

- Cloud provider: AWS, region: Oregon (us-west-2)
- Cloud provider: AWS, region: N. Virginia (us-east-1)
- Cloud provider: AWS, region: Singapore (ap-southeast-1)
- Cloud provider: AWS, region: Seoul (ap-northeast-2)
- Cloud provider: AWS, region: Frankfurt (eu-central-1)
- Cloud provider: AWS, region: São Paulo (sa-east-1)
- Cloud provider: AWS, region: Oregon (us-west-2)
- Cloud provider: Google Cloud, region: Oregon (us-west1)
- Cloud provider: Google Cloud, region: Tokyo (asia-northeast1)
- Cloud provider: Google Cloud, region: Singapore (asia-southeast1)

The maintenance only affects the DM feature in the TiDB cluster. All the other functionalities remain unaffected. You can continue to manage the TiDB cluster and perform read/write operations or other operations as usual.

For clusters deployed on AWS:

- During the upgrade, the DM tasks can keep running without disruption. The DM console can be used normally.

For clusters deployed on Google Cloud:

- The DM console will be unavailable for up to 30 minutes. During this period, you cannot create or manage DM tasks.
- If a DM task is in the incremental migration stage, it will be interrupted for up to 30 minutes. During this period, do not purge the binary log of the MySQL database. The DM task will automatically resume after the upgrade is completed.
- If a DM task is in the stage of exporting and importing full data, it will fail during the upgrade, and cannot be resumed after the upgrade. It is recommended not to create any DM task on the day when the upgrade is performed, to ensure that no DM tasks are in the stage of exporting and importing full data when the upgrade starts.

## Completion and resumption

Once the maintenance is successfully completed, the affected functionalities will be reinstated, offering you a better experience.

## Get support

If you have any questions or need assistance, contact our [support team](/tidb-cloud/tidb-cloud-support.md). We are here to address your concerns and provide any necessary guidance.
