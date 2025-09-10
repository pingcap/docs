---
title: 备份和恢复 TiDB Cloud 专属集群数据
summary: 了解如何备份和恢复你的 TiDB Cloud 专属集群。
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# 备份和恢复 TiDB Cloud 专属集群数据

本文档介绍了如何在 TiDB Cloud 上备份和恢复你的 TiDB Cloud 专属集群数据。TiDB Cloud 专属集群支持自动备份和手动备份。你还可以将备份数据恢复到新集群，或从回收站恢复已删除的集群。

> **提示**
>
> 如需了解如何在 TiDB Cloud Starter 或 TiDB Cloud Essential 集群上备份和恢复数据，请参见 [在 TiDB Cloud Starter 或 Essential 上备份和恢复数据](/tidb-cloud/backup-and-restore-serverless.md)。

## 限制

- 对于 v6.2.0 及以上版本的集群，TiDB Cloud 专属集群默认支持从备份中恢复用户账户和 SQL 绑定。
- TiDB Cloud 专属集群不支持恢复存储在 `mysql` schema 中的系统变量。
- 建议你先导入数据，然后执行一次**手动**快照备份，最后开启 Point-in-time Restore（时间点恢复）。因为通过 TiDB Cloud 控制台导入的数据**不会**生成变更日志，无法被自动检测和备份。更多信息请参见 [从云存储导入 CSV 文件到 TiDB Cloud 专属集群](/tidb-cloud/import-csv-files.md)。
- 如果你多次开启和关闭 Point-in-time Restore，只能选择最近一次开启 Point-in-time Restore 后的可恢复范围内的时间点，之前的可恢复范围将无法访问。
- **不要**同时修改 **Point-in-time Restore** 和 **Dual Region Backup** 的开关。

## 备份

### 查看备份页面

1. 在你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入其概览页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Data** > **Backup**。

### 开启自动备份

TiDB Cloud 专属集群支持 [快照备份](https://docs.pingcap.com/tidb/stable/br-snapshot-guide) 和 [日志备份](https://docs.pingcap.com/tidb/stable/br-pitr-guide)。快照备份可以让你将数据恢复到备份时的状态。默认情况下，快照备份会自动执行，并根据你的备份保留策略进行存储。你可以随时关闭自动备份。

#### 开启 Point-in-time Restore

> **注意**
>
> Point-in-time Restore（时间点恢复）功能仅支持 v6.4.0 及以上版本的 TiDB Cloud 专属集群。

该功能支持将任意时间点的数据恢复到新集群。你可以用它来：

- 降低灾备场景下的 RPO。
- 通过恢复到错误事件发生前的时间点，解决数据写入错误问题。
- 审计业务的历史数据。

强烈建议开启此功能。其费用与快照备份相同。更多信息请参见 [数据备份费用](https://www.pingcap.com/tidb-dedicated-pricing-details#backup-storage-cost)。

要为你的 TiDB Cloud 专属集群开启此功能，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Backup Setting**。

3. 将 **Auto Backup** 开关切换为 **On**。

4. 将 **Point-in-time Restore** 开关切换为 **On**。

    > **警告**
    >
    > Point-in-Time Restore 仅在下一个备份任务完成后生效。若需提前生效，可以在开启后[手动执行一次备份](#perform-a-manual-backup)。

5. 点击 **Save** 保存更改。

#### 配置备份计划

TiDB Cloud 专属集群支持每日和每周备份计划。默认情况下，备份计划为每日。你可以选择一天或一周中的特定时间启动快照备份。

要为你的 TiDB Cloud 专属集群配置备份计划，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Backup Setting**。

3. 将 **Auto Backup** 开关切换为 **On**。

4. 按如下方式配置备份计划：

    - 在 **Backup Cycle** 中，点击 **Daily Backup** 或 **Weekly Backup** 标签。若选择 **Weekly Backup**，需指定每周的备份日期。

        > **警告**
        >
        > - 启用每周备份时，Point-in-time Restore 功能默认开启，你可以手动关闭。
        > - 如果将备份周期从每周切换为每日，Point-in-time Restore 功能会保持原有设置。如有需要可手动关闭。

    - 在 **Backup Time** 中，为每日或每周集群备份安排开始时间。

        如果你未指定首选备份时间，TiDB Cloud 会分配默认备份时间，即集群所在区域时区的凌晨 2:00。

        > **注意**
        >
        > - 当数据导入任务进行中时，备份任务会自动延迟。**不要**在数据导入或集群扩容期间执行手动备份。

    - 在 **Backup Retention** 中，配置最小备份数据保留周期。默认周期为 7 天。为尽量减少对业务的影响，建议在业务低峰期安排自动备份。

        > **注意**
        >
        > - 除最新备份外，所有超出保留周期的自动备份将被删除。最新的自动备份不会被删除，除非你手动删除它。这样可以确保在误删情况下仍可恢复集群数据。
        > - 删除集群后，保留周期内的自动备份会被移入回收站。

### 开启双区域备份

> **注意：**
>
> - 目前，双区域备份功能仅适用于托管在 AWS 和 Google Cloud 上的集群。
> - 托管在 Google Cloud 上的 TiDB Cloud 专属集群可无缝对接 Google Cloud Storage。与 Google Cloud Storage 类似，**TiDB Cloud 专属集群仅支持在同一 multi-region code 下的 Google 双区域存储配对**。例如，在亚洲，目前必须将东京和大阪配对为双区域存储。更多信息请参见 [Dual-regions](https://cloud.google.com/storage/docs/locations#location-dr)。

TiDB Cloud 专属集群支持双区域备份，通过将集群所在区域的备份复制到另一个不同区域。开启该功能后，所有备份会自动复制到指定区域，实现跨区域数据保护和灾备能力。预计约 99% 的数据可在一小时内复制到次级区域。

双区域备份费用包括备份存储用量和跨区域数据传输费用。更多信息请参见 [数据备份费用](https://www.pingcap.com/tidb-dedicated-pricing-details#backup-storage-cost)。

要为你的 TiDB Cloud 专属集群开启双区域备份，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Backup Setting**。

3. 将 **Dual Region Backup** 开关切换为 **On**。

4. 在 **Secondary Region** 下拉列表中，选择用于存储备份文件的区域。

5. 点击 **Save** 保存更改。

### 关闭自动备份

> **注意**
>
> 关闭自动备份会默认关闭 point-in-time restore。

要关闭 TiDB Cloud 专属集群的自动备份，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Backup Setting**。

3. 将 **Auto Backup** 开关切换为 **Off**。

4. 点击 **Save** 保存更改。

### 关闭双区域备份

> **提示**
>
> 禁用双区域备份不会立即删除次级区域的备份。这些备份会根据备份保留计划稍后清理。如需立即移除，可手动[删除备份](#delete-backups)。

要关闭 TiDB Cloud 专属集群的双区域备份，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Backup Setting**。

3. 将 **Dual Region Backup** 开关切换为 **Off**。

4. 点击 **Save** 保存更改。

### 执行手动备份

手动备份是由用户发起的备份，允许你根据需要将数据备份到已知状态，并可随时恢复到该状态。

> **注意**
>
> - 手动备份会被无限期保留，直到你手动删除或账户关闭。
> - 删除 TiDB Cloud 专属集群后，现有的手动备份会被移入回收站，直至手动删除或账户关闭。

要为你的 TiDB Cloud 专属集群执行手动备份，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 在右上角点击 **...** > **Manual Backup**。

3. 在弹出的对话框中输入 **Name**。

4. 点击 **Confirm**，集群数据即会被备份。

### 删除备份

#### 删除备份文件

要删除 TiDB Cloud 专属集群的现有备份文件，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 找到你要删除的备份文件，在 **Action** 列点击 **...** > **Delete**。

#### 删除正在运行的备份任务

要删除 TiDB Cloud 专属集群正在运行的备份任务，操作方式与 [**删除备份文件**](#delete-backup-files) 类似。

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 找到处于 **Pending** 或 **Running** 状态的备份任务，在 **Action** 列点击 **...** > **Delete**。

## 恢复

### 恢复数据到新集群

> **注意**
>
> 当你从备份恢复 TiDB 集群时，恢复过程会保留原有的时区设置，不会覆盖。

要将 TiDB Cloud 专属集群的数据从备份恢复到新集群，请执行以下步骤：

1. 进入集群的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Restore**，弹出设置窗口。

3. 在 **Restore Mode** 中，选择 **Restore From Region**，即备份存储的区域。

    > **注意**
    >
    > - **Restore From Region** 的默认值与备份集群相同。

4. 在 **Restore Mode** 中，选择将任意时间点的数据或选定备份恢复到新集群。

    <SimpleTab>
    <div label="Select Time Point">

    若要将备份保留期内任意时间点的数据恢复到新集群，请确保 **Backup Setting** 中已开启 **Point-in-time Restore**，然后执行以下步骤：

    - 点击 **Select Time Point**。
    - 选择你要恢复的 **Date** 和 **Time**。

    </div>

    <div label="Select Backup Name">

    若要将选定的备份恢复到新集群，请执行以下步骤：

    - 点击 **Select Backup Name**。
    - 选择你要恢复的备份。

    </div>
    </SimpleTab>

5. 在 **Restore to Region** 中，选择与 **Backup Setting** 中配置的 **Primary Region** 相同的区域。

6. 在 **Restore** 窗口中，如有需要你还可以进行如下更改：

    - 设置集群名称。
    - 更新集群端口号。
    - 增加集群节点数、vCPU 和内存、存储空间。

7. 点击 **Restore**。

   集群恢复流程启动，并弹出 **Password Settings** 对话框。

8. 在 **Password Settings** 对话框中，设置连接集群的 root 密码，然后点击 **Save**。

### 恢复已删除的集群

> **注意：**
>
> 已删除集群无法恢复到任意时间点，只能选择自动或手动备份进行恢复。

要从回收站恢复已删除的集群，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Recycle Bin**。
3. 在 **Recycle Bin** 页面，找到你要恢复的集群，在 **Action** 列点击 **...**，然后点击 **Backups**。
4. 在 **Backups** 页面，找到你想要的备份时间，在 **Action** 列点击 **...**，然后点击 **Restore**。
5. 在 **Restore** 页面，为新集群指定名称，并根据需要进行如下更改：

    - 更新集群端口号。
    - 增加集群节点数、vCPU 和内存、存储空间。

6. 在 **Summary** 部分，检查恢复信息，然后点击 **Restore**。

   集群恢复流程启动，并弹出 **Password Settings** 对话框。

7. 在 **Password Settings** 对话框中，设置连接集群的 root 密码，然后点击 **Save**。