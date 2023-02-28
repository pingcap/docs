---
title: TiDB Cloud Events
summary: Learn how to review the events for TiDB Cloud cluster using the Event page. 
---

# TiDB Cloud Events

The TiDB Cloud Event page provides you with an easy way to review the historical cluster events, including the event type, status, message, trigger time and trigger user.

This document describes how to review the events for TiDB Cloud cluster using the Event page. 

> **Note:**
>
> Event page currently is only available for Dedicated Tier clusters.  It will be available for Serverless Tier cluster in future release. 

## View the Event page

To view the events on the Event page, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

2. Click the name of the target cluster. The cluster overview page is displayed.
3. Click **Events** in the left navigation pane.

## Logged events

The following table lists the cluster events that is logged.

| Event Type| Description |  Added since |
|:--- |:--- |:--- |
| Creating Cluster / Cluster Created |  Events recoded for cluster creation action.  |  2023-3-1   |
| Pausing Cluster  / Cluster Paused  |   Events recoded for cluster pause action. |  2023-3-1   |
| Resuming Cluster / Cluster Resumed  |   Events recoded for cluster resume action. |  2023-3-1   |
| Modifying Cluster Size  / Cluster Size Modified  |   Events recoded for modify cluster size action. |  2023-3-1   |

For each event, the following information is logged.
- Event Type
- Status
- Message
- Time
- Triggered By

> **Note:**
>
> - If the cluster events happened before the event feature added, these event are not visible on Event page. 
> - TiDB Cloud will keep adding more event types in future release. 

## Events retention policy

- For Dedicated Tier clusters, the event data is kept for 7 days.
- For Serverless Tier clusters, the event data is not availabe .
