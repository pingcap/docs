---
title: TiDB Cloud Cluster Events
summary: Learn how to view the events for TiDB Cloud clusters using the Events page.
---

# TiDB Cloud Cluster Events

TiDB Cloud logs the historical events at the cluster level. An *event* indicates a change in your TiDB Cloud cluster. You can view the logged events on the **Events** page, including the event type, status, message, trigger time, and trigger user.

This document describes how to view the events for TiDB Cloud clusters using the **Events** page and lists the supported event types.

## View the Events page

To view the events on the **Events** page, take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. In the left navigation pane, click **Monitoring** > **Events**.

## Logged events

TiDB Cloud logs the following types of cluster events:

| Event Type| Description |
|:--- |:--- |
| CreateCluster |  Create a cluster |  
| PauseCluster |   Pause a cluster |  
| ResumeCluster |   Resume a cluster | 
| ModifyClusterSize |   Modify cluster size | 
| BackupCluster |   Back up a cluster |  
| ExportBackup |   Export a backup |
| RestoreFromCluster |   Restore a cluster |  
| CreateChangefeed |   Create a changefeed |  
| PauseChangefeed |   Pause a changefeed | 
| ResumeChangefeed |   Resume a changefeed | 
| DeleteChangefeed |   Delete a changefeed |  
| EditChangefeed |  Edit a changefeed |  
| ScaleChangefeed |   Scale the specification of a changefeed |  
| FailedChangefeed |   Changefeed failures |  
| ImportData |   Import data to a cluster |  
| UpdateSpendingLimit |   Update spending limit of a TiDB Cloud Serverless scalable cluster |  
| ResourceLimitation |   Update resource limitation of a TiDB Cloud Serverless cluster |  

For each event, the following information is logged:

- Event Type
- Status
- Message
- Time
- Triggered By

## Event retention policy

Event data is kept for 7 days.
