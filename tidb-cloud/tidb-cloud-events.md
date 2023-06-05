---
title: TiDB Cloud Cluster Events
summary: Learn how to view the events for TiDB Cloud clusters using the Events page.
---

# TiDB Cloud Cluster Events

TiDB Cloud logs the historical events at the cluster level. An *event* indicates a change in your TiDB Cloud cluster. You can view the logged events on the **Events** page, including the event type, status, message, trigger time, and trigger user.

This document describes how to view the events for TiDB Cloud clusters using the **Events** page and lists the supported event types.

> **Note:**
>
> Currently, the Events page is only available for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

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

| Event Type| Description |
|:--- |:--- |
| CreateCluster |  Create a cluster |  
| PauseCluster |   Pause a cluster |  
| ResumeCluster |   Resume a cluster | 
| ModifyClusterSize |   Modify cluster size | 
| BackupCluster |   Back up a cluster |  
| RestoreFromCluster |   Restore a cluster |  
| CreateChangefeed |   Create a changefeed |  
| PauseChangefeed |   Pause a changefeed | 
| ResumeChangefeed |   Resume a changefeed | 
| DeleteChangefeed |   Delete a changefeed |  
| EditChangefeed |  Edit a changefeed |  
| ScaleChangefeed |   Scale the specification of a changefeed |  
| FailedChangefeed |   Changefeed failures |  
| ImportData |   Import data to a cluster |  

For each event, the following information is logged:

- Event Type
- Status
- Message
- Time
- Triggered By

> **Note:**
>
> Cluster events started before 2023-03-22 are not visible on the Events page.

## Event retention policy

For TiDB Dedicated clusters, the event data is kept for 7 days.
