---
title: 暂停或恢复 TiDB Cloud Dedicated 集群
summary: 了解如何暂停或恢复 TiDB Cloud Dedicated 集群。
---

# 暂停或恢复 TiDB Cloud Dedicated 集群

你可以在 TiDB Cloud 中轻松暂停和恢复并非始终运行的 TiDB Cloud Dedicated 集群。

暂停操作不会影响存储在集群中的数据，只是停止监控信息的收集和计算资源的消耗。暂停后，你可以随时恢复集群。

与备份和恢复相比，暂停和恢复集群所需时间更短，并且会保留你的集群信息（包括集群版本、集群配置和 TiDB 用户账户）。

> **注意：**
>
> 你无法暂停 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。

## 限制

- 只有当集群处于 **Available** 状态时，你才能暂停集群。如果集群处于 **Modifying** 等其他状态，你必须等待当前操作完成后才能暂停集群。
- 当有数据导入任务正在进行时，无法暂停集群。你可以等待导入任务完成或取消导入任务。
- 当有备份任务正在进行时，无法暂停集群。你可以等待当前备份任务完成或[删除正在运行的备份任务](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job)。
- 如果集群存在任何 [changefeeds](/tidb-cloud/changefeed-overview.md)，则无法暂停集群。你需要[删除现有的 changefeed](/tidb-cloud/changefeed-overview.md#delete-a-changefeed) 后才能暂停集群。

## 暂停 TiDB 集群

暂停时长和行为取决于你的组织创建日期：

- 2024 年 11 月 12 日之后创建的组织，采用标准暂停行为，最长暂停时长为 7 天。
- 2024 年 11 月 12 日及之前创建的组织，采用兼容暂停行为，允许更长的暂停时长。这些组织将逐步过渡到标准的 7 天限制。

<SimpleTab>
<div label="Standard pause behavior">

当集群被暂停时，请注意以下事项：

- TiDB Cloud 停止收集该集群的监控信息。
- 你无法从集群中读取或写入数据。
- 你无法导入或备份数据。
- 仅收取以下费用：

    - 节点存储费用
    - 数据备份费用

- TiDB Cloud 停止该集群的[自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。
- 最长暂停时长为 7 天。如果你未在 7 天内手动恢复集群，TiDB Cloud 会自动恢复集群。
- 你可以在集群概览页面查看自动恢复的计划。TiDB Cloud 会在集群自动恢复前 24 小时，向组织所有者和项目所有者发送通知邮件。

</div>
<div label="Compatible pause behavior">

> **注意：**
>
> 如果你的组织是在 2024 年 11 月 12 日之前创建的，集群仍采用兼容暂停行为。TiDB Cloud 会在过渡到新的标准暂停行为前通知你。

当集群被暂停时，请注意以下事项：

- TiDB Cloud 停止收集该集群的监控信息。
- 你无法从集群中读取或写入数据。
- 你无法导入或备份数据。
- TiDB Cloud 不会自动恢复已暂停的集群。
- 仅收取以下费用：

    - 节点存储费用
    - 数据备份费用

- TiDB Cloud 停止该集群的[自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

</div>
</SimpleTab>

暂停集群的步骤如下：

1. 在 TiDB Cloud 控制台，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 在你想要暂停的集群所在行，点击 **...**。

    > **提示：**
    >
    > 你也可以在 **Clusters** 页面点击你想要暂停的集群名称，然后在右上角点击 **...**。

3. 在下拉菜单中点击 **Pause**。

    此时会弹出 **Pause your cluster** 对话框。

4. 在对话框中点击 **Pause** 以确认你的选择。

    点击 **Pause** 后，集群会先进入 **Pausing** 状态。暂停操作完成后，集群会变为 **Paused** 状态。

你也可以通过 TiDB Cloud API 暂停集群。目前，TiDB Cloud API 仍处于 beta 阶段。更多信息请参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。

## 恢复 TiDB 集群

暂停的集群恢复后，请注意以下事项：

- TiDB Cloud 恢复收集该集群的监控信息，你可以从集群中读取或写入数据。
- TiDB Cloud 恢复收取计算和存储费用。
- TiDB Cloud 恢复该集群的[自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

恢复已暂停集群的步骤如下：

1. 在 TiDB Cloud 控制台，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 在你想要恢复的集群所在行，点击 **Resume**。此时会弹出 **Resume your cluster** 对话框。

    > **注意：**
    >
    > 处于 **Pausing** 状态的集群无法恢复。

3. 在对话框中点击 **Resume** 以确认你的选择。集群状态会变为 **Resuming**。

根据你的集群规模，恢复集群可能需要几分钟。集群恢复后，状态会从 **Resuming** 变为 **Available**。

你也可以通过 TiDB Cloud API 恢复集群。目前，TiDB Cloud API 仍处于 beta 阶段。更多信息请参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。