---
title: 在 TiDB Cloud Starter 或 Essential 上备份和恢复数据
summary: 了解如何在 TiDB Cloud Starter 或 TiDB Cloud Essential 集群上备份和恢复你的数据。
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# 在 TiDB Cloud Starter 或 Essential 上备份和恢复数据

本文档介绍如何在 TiDB Cloud Starter 或 TiDB Cloud Essential 集群上备份和恢复你的数据。

> **Tip:**
>
> 如果你想了解如何在 TiDB Cloud Dedicated 集群上备份和恢复数据，请参见 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

## 查看备份页面

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Data** > **Backup**。

## 自动备份

TiDB Cloud 会自动备份你的集群数据，使你能够从备份快照中恢复数据，以最大程度减少灾难发生时的数据丢失。

### 了解备份设置

TiDB Cloud Starter 集群和 TiDB Cloud Essential 集群的自动备份设置有所不同，如下表所示：

| 备份设置         | TiDB Cloud Starter 集群 | TiDB Cloud Essential 集群 |
|------------------|------------------------|--------------------------|
| 备份周期         | 每日                   | 每日                     |
| 备份保留时间     | 1 天                   | 14 天                    |
| 备份时间         | 固定时间               | 可配置                   |

- **Backup Cycle** 表示备份的频率。

- **Backup Retention** 表示备份的保留时长。过期的备份无法恢复。

- **Backup Time** 表示备份开始调度的时间。注意，最终的备份时间可能会滞后于配置的备份时间。

    - TiDB Cloud Starter 集群：备份时间为随机固定时间。
    - TiDB Cloud Essential 集群：你可以将备份时间配置为每半小时一次。默认值为随机固定时间。

### 配置备份设置

要为 TiDB Cloud Essential 集群设置备份时间，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Backup Setting**。此时会打开 **Backup Setting** 窗口，你可以根据需求配置自动备份设置。

3. 在 **Backup Time** 中，安排每日集群备份的开始时间。

4. 点击 **Confirm**。

## 恢复

TiDB Cloud 集群提供恢复功能，帮助你在意外丢失或数据损坏时恢复数据。

### 恢复模式

TiDB Cloud 支持快照恢复和时间点恢复两种方式。

- **Snapshot Restore**：从指定的备份快照恢复你的集群。

- **Point-in-Time Restore (beta)**：将你的集群恢复到指定的时间点。

    - TiDB Cloud Starter 集群：不支持。
    - TiDB Cloud Essential 集群：可恢复到最近 14 天内的任意时间点，但不能早于集群创建时间，也不能晚于当前时间减去 1 分钟。

### 恢复目标

TiDB Cloud 支持原地恢复和恢复到新集群。

**原地恢复**

恢复到当前集群会覆盖现有数据。请注意以下事项：

- 恢复开始后，现有连接会被断开。
- 恢复过程中，集群将不可用，新的连接会被阻止。
- 恢复会影响 `mysql` schema 下的表。任何用户凭证、权限或系统变量的更改都会被还原到备份时的状态。

**恢复到新集群**

创建并恢复到新集群。请注意以下事项：

- 源集群的用户凭证和权限不会恢复到新集群。

### 恢复超时

恢复过程通常会在几分钟内完成。如果恢复超过三小时未完成，将会被自动取消。被取消的恢复操作结果取决于恢复目标：

- **In-place restore**：集群状态会从 **Restoring** 变为 **Available**，集群重新可用。
- **Restore to a new cluster**：新集群会被删除，源集群保持不变。

如果恢复被取消后数据损坏且无法恢复，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 寻求帮助。

### 执行恢复操作

要恢复你的 TiDB Cloud 集群，请按照以下步骤操作：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Restore**。会弹出设置窗口。

3. 在 **Restore Mode** 中，你可以选择从指定备份恢复或恢复到任意时间点。

    <SimpleTab>
    <div label="Snapshot Restore">

    若要从选定的备份快照恢复，请执行以下步骤：

    1. 点击 **Snapshot Restore**。
    2. 选择你要恢复的备份快照。

    </div>
    <div label="Point-in-Time Restore">

    若要将 TiDB Cloud Essential 集群恢复到指定时间点，请执行以下步骤：

    1. 点击 **Point-in-Time Restore**。
    2. 选择你要恢复到的日期和时间。

    </div>
    </SimpleTab>

4. 在 **Destination** 中，你可以选择恢复到新集群或原地恢复。

    <SimpleTab>
    <div label="Restore to a new cluster">

    若要恢复到新集群，请执行以下步骤：

    1. 点击 **Restore to a New Cluster**。
    2. 输入新集群的名称。
    3. 选择新集群的集群方案。

        - 如果你选择 TiDB Cloud Starter 集群且需要超出 [免费额度](/tidb-cloud/select-cluster-tier.md#usage-quota) 的资源，请设置每月消费上限。
        - 如果你选择 TiDB Cloud Essential 集群，请设置最小 RCU 和最大 RCU，并根据需要配置高级设置。

    </div>
    <div label="Restore in-place">

    若要原地恢复，点击 **In-place Restore**。

    </div>
    </SimpleTab>

5. 点击 **Restore** 开始恢复流程。

恢复流程开始后，集群状态会变为 **Restoring**。在恢复完成并状态变为 **Available** 之前，集群将保持不可用。

## 限制

- 如果启用了 TiFlash 副本，恢复后 TiFlash 会有一段时间不可用，因为数据需要在 TiFlash 中重建。
- TiDB Cloud Starter 和 TiDB Cloud Essential 集群不支持手动备份。
- 数据量超过 1 TiB 的集群默认不支持恢复到新集群。如需处理更大数据集，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 寻求帮助。