---
title: 2024-04-09 TiDB Cloud Monitoring Features Maintenance Notification
summary: Learn about the details of the TiDB Cloud monitoring features maintenance on April 9, 2024, such as the maintenance window, reason, and impact.
---

# [2024-04-09] TiDB Cloud Monitoring Features Maintenance Notification

This notification describes the details that you need to know about the TiDB Cloud [monitoring features](/tidb-cloud/monitor-tidb-cluster.md) maintenance on April 9, 2024.

## Maintenance window

- Start time: 2024-04-09 08:00 (UTC+0)
- End time: 2024-04-09 12:00 (UTC+0)
- Duration: 4 hours

## Impact

### Affected regions

During the maintenance window, the monitoring features in the following regions will be affected:

- TiDB Cloud Dedicated clusters：
    - Cloud Provider: AWS, Region: Oregon (us-west-2)
    - Cloud Provider: AWS, Region: Seoul (ap-northeast-2)
    - Cloud Provider: AWS, Region: Frankfurt (eu-central-1)
    - Cloud Provider: AWS, Region: Oregon (us-west-2)
    - Cloud Provider: Google Cloud, Region: Oregon (us-west1)
    - Cloud Provider: Google Cloud, Region: Tokyo (asia-northeast1)
    - Cloud Provider: Google Cloud, Region: Singapore (asia-southeast1)
    - Cloud Provider: Google Cloud, Region: Iowa (us-central1)
    - Cloud Provider: Google Cloud, Region: Taiwan (asia-east1)

- TiDB Cloud Serverless clusters：
    - Cloud Provider: AWS, Region: Frankfurt (eu-central-1)
    - Cloud Provider: AWS, Region: Oregon (us-west-2)

### Affected monitoring features

> **Note:**
>
> The maintenance only affects monitoring features in the TiDB cluster. All the other functionalities remain unaffected. You can continue to manage the TiDB cluster and perform read/write operations or other operations as usual.

- The **Metrics** page will be temporarily unavailable for several short periods (each less than 20 minutes).
- The **Slow Query** page will be temporarily unavailable for several short periods (each less than 5 minutes).
- The metrics integration with Prometheus, DataDog, and NewRelic might have breakpoints.

## Completion and resumption

Once the maintenance is successfully completed, the affected functionalities will be reinstated, offering you an even better experience.

## Get support

If you have any questions or need assistance, contact our [support team](/tidb-cloud/tidb-cloud-support.md). We are here to address your concerns and provide any necessary guidance.
