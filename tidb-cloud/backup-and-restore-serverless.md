---
title: 备份和恢复 TiDB Cloud Starter 或 Essential 数据
summary: 了解如何备份和恢复你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# 备份和恢复 TiDB Cloud Starter 或 Essential 数据

本文档介绍如何在 TiDB Cloud Starter 或 TiDB Cloud Essential 集群上备份和恢复你的数据。

> **Tip:**
>
> 如果你想了解如何在 TiDB Cloud Dedicated 集群上备份和恢复数据，请参阅 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

## 查看备份页面

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Data** > **Backup**。

## 自动备份

TiDB Cloud 会自动备份你的集群数据，使你能够从备份快照中恢复数据，以最大程度减少灾难发生时的数据丢失。

### 了解备份设置

TiDB Cloud Starter 集群和 TiDB Cloud Essential 集群的自动备份设置有所不同，具体如下表所示：

| Backup setting   | TiDB Cloud Starter (free) | TiDB Cloud Starter (with spending limit > 0) | TiDB Cloud Essential |
|------------------|----------------------------|----------------------------|----------------------------|
| Backup Cycle     | Daily                      | Daily                      | Daily                      |
| Backup Retention | 1 day                      | Up to 30 days              | Up to 30 days              |
| Backup Time      | Fixed time                 | Configurable               | Configurable               |

- **Backup Cycle** 表示备份的频率。

- **Backup Retention** 表示备份的保留时长。过期的备份无法恢复。

    - 对于免费版 TiDB Cloud Starter 集群，备份保留时长为 1 天。
    - 对于 TiDB Cloud Starter（设置了消费上限 > 0）或 TiDB Cloud Essential 集群，你可以将备份保留时长配置为 1 到 30 天之间的任意值。默认保留时长为 14 天。

- **Backup Time** 表示备份开始调度的时间。请注意，最终的备份时间可能会滞后于配置的备份时间。

    - 对于免费版 TiDB Cloud Starter 集群，备份时间为随机固定时间。
    - 对于 TiDB Cloud Starter（设置了消费上限 > 0）或 TiDB Cloud Essential 集群，你可以将备份时间配置为每半小时一次。默认值为随机固定时间。

### 配置备份设置

要为 TiDB Cloud Essential 集群设置备份时间，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Backup Setting**。这将打开 **Backup Setting** 窗口，你可以根据需求配置自动备份设置。

3. 在 **Backup Time** 中，为每日集群备份安排一个开始时间。

4. 点击 **Confirm**。

## 恢复

TiDB Cloud 集群提供恢复功能，帮助你在数据意外丢失或损坏时进行数据恢复。

### 恢复模式

TiDB Cloud 支持快照恢复和时间点恢复两种方式。

- **Snapshot Restore**：从指定的备份快照恢复你的集群。

- **Point-in-Time Restore (beta)**：将你的集群恢复到指定的时间点。

    - TiDB Cloud Starter 集群：不支持。
    - TiDB Cloud Essential 集群：可以恢复到备份保留期内的任意时间，但不能早于集群创建时间，也不能晚于当前时间前 1 分钟。

### 恢复目标

TiDB Cloud 支持将数据恢复到新集群。

### 恢复超时

恢复过程通常会在几分钟内完成。如果恢复时间超过 3 小时，系统会自动取消恢复并删除新集群，源集群不会受到影响。

如果在恢复被取消后数据损坏且无法恢复，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取帮助。

### 执行恢复操作

> **Note:**
>
> 源集群的用户凭证和权限不会被恢复到新集群。

要将你的数据恢复到新集群，请按照以下步骤操作：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Restore**。

3. 在 **Restore Mode** 中，你可以选择从指定备份或任意时间点进行恢复。

    <SimpleTab>
    <div label="Snapshot Restore">

    若要从选定的备份快照恢复，请执行以下步骤：

    1. 点击 **Snapshot Restore**。
    2. 选择你要恢复的备份快照。

    </div>
    <div label="Point-in-Time Restore">

    若要为 TiDB Cloud Essential 集群恢复到指定时间点，请执行以下步骤：

    1. 点击 **Point-in-Time Restore**。
    2. 选择你要恢复到的日期和时间。

    </div>
    </SimpleTab>

4. 输入新集群的名称。
5. 选择新集群的方案，并根据需要调整容量。

    - 如果你选择 TiDB Cloud Starter 集群且需要的资源超出 [免费额度](/tidb-cloud/select-cluster-tier.md#usage-quota)，请设置每月消费上限。
    - 如果你选择 TiDB Cloud Essential 集群，请设置最小 RCU 和最大 RCU，并根据需要配置高级设置。

6. 点击 **Restore** 开始恢复流程。

恢复流程开始后，集群状态会变为 **Restoring**。在恢复完成并且状态变为 **Available** 之前，集群将不可用。

## 限制

- 如果启用了 TiFlash 副本，恢复后的一段时间内 TiFlash 将不可用，因为数据需要在 TiFlash 中重建。
- TiDB Cloud Starter 和 TiDB Cloud Essential 集群不支持手动备份。
- 默认情况下，数据量超过 1 TiB 的集群不支持恢复到新集群。如需处理更大数据集，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取帮助。