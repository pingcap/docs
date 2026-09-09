---
title: Events
summary: Learn how to view the events for TiDB Cloud resources using the Events page.
---

# Events

<CustomContent plan="starter,essential,premium">

For {{{ .starter }}}, Essential and Premium instances, TiDB Cloud logs the historical events at the instance level. An *event* indicates a change in your {{{ .starter }}}, Essential or Premium instance. You can view the logged events on the **Events** page, including the event type, status, message, trigger time, and trigger user.

</CustomContent>

<CustomContent plan="dedicated">

For TiDB Cloud Dedicated clusters, TiDB Cloud logs the historical events at the cluster level. An *event* indicates a change in your TiDB Cloud Dedicated cluster. You can view the logged events on the **Events** page, including the event type, status, message, trigger time, and trigger user.

</CustomContent>

This document describes how to view the historical events using the **Events** page and lists the supported event types.

## View the Events page

To view the events on the **Events** page, take the following steps:

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target <CustomContent plan="starter,essential,premium">{{{ .starter }}}, Essential or Premium instance</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicated cluster</CustomContent> to go to its overview page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the left navigation pane, click **Monitoring** > **Events**.

## Logged events

<CustomContent plan="starter,essential,dedicated">

TiDB Cloud logs the following types of events:

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
| UpdateSpendingLimit |   Update spending limit of a {{{ .starter }}} instance |  
| ResourceLimitation |   Update resource limitation of a {{{ .starter }}} or {{{ .essential }}} instance |  

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud Premium logs the following types of events:

| Event Type| Description |
|:--- |:--- |
| CreateInstance |  Create an instance |  
| CreateDataMigration  |  Create a Data Migration Task |
| DeleteDataMigration |  Delete a Data Migration Task |
| PauseDataMigration |  Pause a Data Migration Task  |  
| ResumeDataMigration |  Resume a Data Migration Task |  
| ImportData |  Import Data |  
| CreatePrivateEndpoint |  Create an AWS Private Endpoint for External Services |  
| DeletePrivateEndpoint |  Delete an AWS Private Endpoint for External Services |  
| CreateChangefeed |  Create a changefeed |  
| ScaleChangefeed |  Scale a changefeed |  
| PauseChangefeed |  Pause a changefeed |  
| ResumeChangefeed |  Resume a changefeed |  
| EditChangefeed |  Edit a changefeed |  
| DeleteChangefeed |  Delete a changefeed |  
| BackupCluster |  Back up a cluster |  
| DeleteBackup |  Delete a backup|  
| UpdateBackupSetting |  Update a backup setting |  
| RestoreFromBackup |  Restore from backup |  
| CreateExport |  Create an export |  
| CancelExport |  Cancel an export |  
| DeleteExport |  Delete an export |  
| RestoreInstance |  Restore to an instance |  
| UpdatePublicEndpoint |  Update a public endpoint |  
| UpdateClusterCapacity |  Update an instance capacity |  
| CreatePrivateLink | Create a PrivateLink Endpoint  |

</CustomContent>

For each event, the following information is logged:

- Event Type
- Status
- Message
- Time
- Triggered By

## Event retention policy

Event data is kept for 7 days.
