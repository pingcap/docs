---
title: TiDB Cloud Events
summary: Learn how to review the events for TiDB Cloud cluster using the Event page. 
---

# TiDB Cloud Events

TiDB Cloud logs the historical events at the cluster level. An *event* indicates a change in the TiDB Cloud environment. You can review the logged events on the **Events** page, including the event type, status, message, trigger time, and trigger user.

This document describes how to review the events for TiDB Cloud clusters using the **Events** page. 

> **Note:**
>
> The Event page currently is only available for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters.

## View the Events page

To view the events on the Events page, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can switch to the target project from the ☰ hover menu in the upper-left corner.

2. Click the name of the target cluster. The cluster overview page is displayed.
3. Click **Events** in the left navigation pane.

## Logged events

TiDB Cloud logs the following types of cluster events:

| Event Type| Description |  Available since |
|:--- |:--- |:--- |
| CreateCluster |  Events recoded for cluster creation action.  |  2023-03-21   |
| PauseCluster |   Events recoded for cluster pause action. |  2023-03-21   |
| ResumeCluster |   Events recoded for cluster resume action. |  2023-03-21   |
| ModifyClusterSize |   Events recoded for modifying cluster size action. |  2023-03-21   |

For each event, the following information is logged:

- Event Type
- Status
- Message
- Time
- Triggered By

> **Note:**
>
> - If the cluster events happened before 2023-03-21, these events are not visible on the Events page. 

## Event retention policy

- For Dedicated Tier clusters, the event data is kept for 7 days.
- For Serverless Tier clusters, the event data is not available.
