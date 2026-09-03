---
title: Events
summary: 了解如何使用 Events 页面查看 TiDB Cloud 资源的事件。
---

# Events

<CustomContent plan="starter,essential,premium">

对于 {{{ .starter }}}、Essential 和 Premium 实例，TiDB Cloud 会在实例层级记录历史事件。一个 *event* 表示你的 {{{ .starter }}}、Essential 或 Premium 实例发生了一次变更。你可以在 **Events** 页面查看已记录的事件，包括事件类型、状态、消息、触发时间和触发用户。

</CustomContent>

<CustomContent plan="dedicated">

对于 TiDB Cloud Dedicated 集群，TiDB Cloud 会在集群层级记录历史事件。一个 *event* 表示你的 TiDB Cloud Dedicated 集群发生了一次变更。你可以在 **Events** 页面查看已记录的事件，包括事件类型、状态、消息、触发时间和触发用户。

</CustomContent>

本文档介绍如何使用 **Events** 页面查看历史事件，并列出了支持的事件类型。

## 查看 Events 页面

要在 **Events** 页面查看事件，请按照以下步骤操作：

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标 <CustomContent plan="starter,essential,premium">{{{ .starter }}}、Essential 或 Premium 实例</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicated 集群</CustomContent> 的名称，进入其概览页面。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏，点击 **Monitoring** > **Events**。

## 已记录的事件

<CustomContent plan="starter,essential,dedicated">

TiDB Cloud 会记录以下类型的事件：

| Event Type| Description |
|:--- |:--- |
| CreateCluster |  创建集群 |  
| PauseCluster |   暂停集群 |  
| ResumeCluster |   恢复集群 | 
| ModifyClusterSize |   修改集群规格 | 
| BackupCluster |   备份集群 |  
| ExportBackup |   导出备份 |
| RestoreFromCluster |   恢复集群 |  
| CreateChangefeed |   创建 changefeed |  
| PauseChangefeed |   暂停 changefeed | 
| ResumeChangefeed |   恢复 changefeed | 
| DeleteChangefeed |   删除 changefeed |  
| EditChangefeed |  编辑 changefeed |  
| ScaleChangefeed |   扩容 changefeed 规格 |  
| FailedChangefeed |   changefeed 失败 |  
| ImportData |   向集群导入数据 |  
| UpdateSpendingLimit |   更新 TiDB Cloud Starter 实例的消费额度 |  
| ResourceLimitation |   更新 TiDB Cloud Starter 或 TiDB Cloud Essential 实例的资源限制 |  

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud Premium 会记录以下类型的事件：

| Event Type| Description |
|:--- |:--- |
| CreateInstance |  创建实例 |  
| CreateDataMigration  |  创建数据迁移任务 |
| DeleteDataMigration |  删除数据迁移任务 |
| PauseDataMigration |  暂停数据迁移任务  |  
| ResumeDataMigration |  恢复数据迁移任务 |  
| ImportData |  导入数据 |  
| CreatePrivateEndpoint |  为外部服务创建 AWS Private Endpoint |  
| DeletePrivateEndpoint |  删除外部服务的 AWS Private Endpoint |  
| CreateChangefeed |  创建 changefeed |  
| ScaleChangefeed |  扩展 changefeed |  
| PauseChangefeed |  暂停 changefeed |  
| ResumeChangefeed |  恢复 changefeed |  
| EditChangefeed |  编辑 changefeed |  
| DeleteChangefeed |  删除 changefeed |  
| BackupCluster |  备份集群 |  
| DeleteBackup |  删除备份|  
| UpdateBackupSetting |  修改备份设置 |  
| RestoreFromBackup |  从备份恢复 |  
| CreateExport |  创建导出 |  
| CancelExport |  取消导出 |  
| DeleteExport |  删除导出 |  
| RestoreInstance |  恢复到实例 |  
| UpdatePublicEndpoint |  修改公共端点 |  
| UpdateClusterCapacity |  修改实例容量 |  
| CreatePrivateLink | 创建 PrivateLink Endpoint  |

</CustomContent>

对于每个事件，都会记录以下信息：

- Event Type
- Status
- Message
- Time
- Triggered By

## 事件保留策略

事件数据会保留 7 天。
