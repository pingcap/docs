---
title: TiDB Cloud Cluster Events
summary: 了解如何使用 Events 页面查看 TiDB Cloud 集群的事件。
---

# TiDB Cloud 集群事件

TiDB Cloud 会在集群层级记录历史事件。一个 *event* 表示你的 TiDB Cloud 集群发生了某种变更。你可以在 **Events** 页面查看已记录的事件，包括事件类型、状态、消息、触发时间和触发用户。

本文档介绍如何使用 **Events** 页面查看 TiDB Cloud 集群的事件，并列出了支持的事件类型。

## 查看 Events 页面

要在 **Events** 页面查看事件，请按照以下步骤操作：

1. 在你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Monitoring** > **Events**。

## 已记录的事件

TiDB Cloud 会记录以下类型的集群事件：

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
| UpdateSpendingLimit |   更新 TiDB Cloud Serverless 弹性集群的消费上限 |  
| ResourceLimitation |   更新 TiDB Cloud Serverless 集群的资源限制 |  

对于每个事件，都会记录以下信息：

- Event Type
- Status
- Message
- Time
- Triggered By

## 事件保留策略

事件数据会保留 7 天。