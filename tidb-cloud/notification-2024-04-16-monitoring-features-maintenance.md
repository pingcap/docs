---
title: 2024-04-16 TiDB Cloud Monitoring Features Maintenance Notification
summary: Learn about the details of the TiDB Cloud Monitoring features maintenance on April 16, 2024, such as the maintenance window, reason, and impact.
---

# [2023-08-31] TiDB Cloud Console Maintenance Notification

This notification describes the details that you need to know about the [TiDB Cloud console](https://tidbcloud.com/) maintenance on April 16, 2024.

## Maintenance window

- Start time: 2024-04-16 08:00 (UTC+0)
- End time: 2024-04-16 12:00 (UTC+0)
- Duration: 4 hours

## Impact

### Impacted region scope:  
- Monitoring features for TiDB Dedicated clusters in the following regions：
    - Cloud Provider: AWS, Region: Tokyo (ap-northeast-1)
    - Cloud Provider: AWS, Region: N. Virginia (us-east-1)

- Monitoring features for Serverless clusters in the following regions：
    - Cloud Provider: AWS, Region: Tokyo (ap-northeast-1)
    - Cloud Provider: AWS, Region: N. Virginia (us-east-1)

### Affected Monitoring features ：

> **Note:**
>
> The maintenance only affects the Monitoring features in the TiDB cluster. All the other functionalities remain unaffected. You can continue to manage the TiDB cluster and perform read/write operations or other operations as usual.

- Metrics page will be temporarily unavailable for several short periods（less than 20 mins）.
- Slow Query page will be temporarily unavailable for several short periods （less than 5 mins）.
- Metrics Integration with Prometheus, DataDog and NewRelic may have breakpoints

## Completion and resumption

Once the maintenance is successfully completed, the affected functionalities will be reinstated, offering you an even better experience.

## Get support

If you have any questions or need assistance, contact our [support team](/tidb-cloud/tidb-cloud-support.md). We are here to address your concerns and provide any necessary guidance.
