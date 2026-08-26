---
title: 备份和恢复 {{{ .premium }}} 数据
summary: 了解如何备份和恢复你的 {{{ .premium }}} 实例。
aliases: ['/zh/tidbcloud/restore-deleted-tidb-cluster']
---

# 备份和恢复 {{{ .premium }}} 数据

<CustomContent plan="premium">

本文档介绍如何在 {{{ .premium }}} 实例上备份和恢复数据。{{{ .premium }}} 同时支持自动备份和手动备份，并允许你根据需要将备份数据恢复到新的实例。

</CustomContent>

<CustomContent plan="byoc">

本文档介绍如何在 {{{ .premium }}} 或 {{{ .byoc }}} 实例上备份和恢复数据。{{{ .premium }}} 和 {{{ .byoc }}} 同时支持自动备份和手动备份，并允许你根据需要将备份数据恢复到新的实例。

</CustomContent>

备份文件可以来自以下来源：

- 活跃的 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例
- 回收站中已删除 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的备份

> **Tip:**
>
> - 如需了解如何在 {{{ .dedicated }}} 集群上备份和恢复数据，请参见 [备份和恢复 {{{ .dedicated }}} 数据](/tidb-cloud/backup-and-restore.md)。
> - 如需了解如何在 {{{ .starter }}} 或 {{{ .essential }}} 实例上备份和恢复数据，请参见 [备份和恢复 {{{ .starter }}} 或 Essential 数据](/tidb-cloud/backup-and-restore-serverless.md)。

## 查看 Backup 页面 {#view-the-backup-page}

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面上，点击目标 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的名称，进入其实例概览页面。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Data** > **Backup**。

## 自动备份 {#automatic-backups}

<CustomContent plan="premium">

{{{ .premium }}} 为生产环境提供增强的自动备份能力。它结合高频快照和日志备份，以确保数据可靠性。

</CustomContent>

<CustomContent plan="byoc">

{{{ .premium }}} 和 {{{ .byoc }}} 为生产环境提供增强的自动备份能力。它们结合高频快照和日志备份，以确保数据可靠性。

</CustomContent>

### 自动备份模式 {#automatic-backup-modes}

你可以在 **Backup Settings** 中选择自动备份模式。可用的备份类型、保留时间和计费模式取决于所选模式。

<CustomContent plan="premium">

| 备份模式 | 支持的备份类型 | 保留和恢复选项 | 计费模式 |
| --- | --- | --- | --- |
| **Standard Bundle Mode** | <ul><li>PITR</li><li>每小时备份快照</li><li>每日备份快照</li></ul> | <ul><li>PITR：7 天</li><li>每小时快照：7 天</li><li>每日快照：33 天</li><li>每日快照在 UTC 00:00 创建。</li></ul> | 基于增量数据量。 |
| **Custom Retention Mode** | <ul><li>PITR</li><li>每日备份快照</li></ul> | 你可以将保留时间设置为 3 到 33 天。PITR 和每日快照使用所配置的保留时间。 | 基于快照大小乘以保留时长。每个备份作为单独对象计费。 |

</CustomContent>

<CustomContent plan="byoc">

| 备份模式 | 支持的备份类型 | 保留时间和恢复选项 |
| --- | --- | --- |
| **Standard Bundle Mode** | <ul><li>PITR</li><li>每小时备份快照</li><li>每日备份快照</li></ul> | <ul><li>PITR：7 天</li><li>每小时快照：7 天</li><li>每日快照：33 天</li><li>每日快照在 UTC 00:00 创建。</li></ul> |
| **Custom Retention Mode** | <ul><li>PITR</li><li>每日备份快照</li></ul> | 你可以将保留时间设置为 3 到 33 天。PITR 和每日快照使用已配置的保留时间。 |

</CustomContent>

PITR 允许你将数据恢复到保留时间内的任意时间点。快照允许你从仍在保留时间内的特定每小时或每日快照恢复数据。

### 配置自动备份 {#configure-automatic-backups}

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面上，点击目标 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的名称。

2. 在左侧导航窗格中，点击 **Data** > **Backup**。

3. 在右上角，点击 **...**，然后点击 **Backup Settings**。

4. 选择一种自动备份模式：

    - **Standard Bundle Mode** 使用预定义设置来配置 PITR、每小时快照和每日快照。
    - **Custom Retention Mode** 允许你指定自动备份的保留时间和每日备份时间。

5. 如果你选择了 **Custom Retention Mode**，请配置以下设置。否则，跳过此步骤。

    - **Backup Retention**：选择 3 到 33 天的保留时间。默认值为 7 天。
    - **Daily Backup Time**：选择每日快照的时间。该设置旁边会显示时区。

6. 查看 **Overview** 部分，然后点击 **Save**。

    概览会显示所选备份模式启用的备份类型、对应的保留时间以及可用的恢复选项。

<CustomContent plan="byoc">

> **注意：**
>
> 如果你[切换备份模式](#switch-between-automatic-backup-modes)或缩短保留时间，TiDB Cloud 可能会永久删除早于新保留时间的现有自动备份。此操作无法撤销。

</CustomContent>

<CustomContent plan="premium">

> **注意：**
>
> - Custom Retention Mode 的定价基于快照大小和保留时长。PITR 在公开预览期间暂时免费。更多信息，请参见 [TiDB Cloud pricing](https://www.pingcap.com/tidb-cloud-premium-pricing-details)。
> - 如果你[切换备份模式](#switch-between-automatic-backup-modes)或缩短保留时间，TiDB Cloud 可能会永久删除早于新保留时间的现有自动备份。此操作无法撤销。

</CustomContent>

### 在自动备份模式之间切换 {#switch-between-automatic-backup-modes}

要在 **Standard Bundle Mode** 和 **Custom Retention Mode** 之间切换，请执行以下步骤：

1. 进入实例的 [**Backup**](#view-the-backup-page) 页面。
2. 在右上角，点击 **...**，然后点击 **Backup Settings**。
3. 在显示的对话框中，选择一种新模式。

    - 如果切换到 **Custom Retention Mode**，则需要配置备份保留时间和每日备份时间。
    - 如果切换到 **Standard Bundle Mode**，保留时间和每日备份时间将重置为标准套餐的默认值。

4. 在 **Overview** 部分检查保留设置，然后点击 **Save**。

<CustomContent plan="premium">

保存更改后，后续自动备份将按照所选模式的计费模型进行计费。

</CustomContent>

如果新的保留时间短于当前保留时间，确认对话框会列出早于新保留时间的自动备份，这些备份将被永久删除。仅在验证你不再需要这些备份后，再确认此操作。

### 备份保护 {#backup-protection}

为帮助防止数据丢失并保留一个恢复点，TiDB Cloud 会保护实例的**最近一次成功的自动备份**，直到其保留时间过期。因此，即使实例已被删除，你也无法手动删除这个受保护的最新备份。如果你尝试删除它，控制台会显示一条消息，说明该备份受保护，且在过期前无法删除。

### 删除备份文件 {#delete-backup-files}

如需删除 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的现有备份文件，请执行以下步骤：

1. 进入实例的 [**Backup**](#view-the-backup-page) 页面。

2. 找到要删除的对应备份文件，然后在 **Action** 列中点击 **...** > **Delete**。

    > **注意：**
    >
    > TiDB Cloud 会保护实例的**最近一次成功的自动备份**，以帮助防止数据丢失。如果你尝试删除该备份，控制台会显示一条消息，说明该备份受保护，在过期前无法删除。
    > 如果你在 TiDB Cloud 中拥有 `Organization Owner` 或 `Project Owner` 角色，则可以删除除最近一次成功备份之外的自动备份，或者删除手动备份。

## 手动备份 {#manual-backups}

<CustomContent plan="premium">

除了自动备份外，{{{ .premium }}} 还支持手动备份。手动备份可提供一个可控且有保障的恢复点。强烈建议你在执行高风险操作之前创建手动备份，例如系统升级、关键数据删除，或不可逆的 schema 或配置变更。

</CustomContent>

<CustomContent plan="byoc">

除了自动备份外，{{{ .premium }}} 和 {{{ .byoc }}} 还支持手动备份。手动备份可提供一个可控且有保障的恢复点。强烈建议你在执行高风险操作之前创建手动备份，例如系统升级、关键数据删除，或不可逆的 schema 或配置变更。

</CustomContent>

### 关键特性 {#key-characteristics}

- **保留和删除**：与自动备份不同，手动备份不会根据保留策略自动删除。它们会一直保留，直到你显式删除它们。如果你删除实例，其手动备份会移动到回收站，并一直保留在那里，直到你手动删除。

- **存储位置**：手动备份存储在由 TiDB 管理的云存储中。

- **成本**：由于手动备份会一直保留，直到你将其删除，因此会产生额外费用。

- **限制**：手动备份不支持 point-in-time recovery (PITR) 或部分备份（例如表级或数据库级备份）。你不能将手动备份恢复到现有实例。每次恢复操作都会创建一个新实例。

- **权限**：`Organization Owner` 和 `Instance Manager` 都可以创建手动备份。只有 `Organization Owner` 可以恢复系统管理的手动备份。

### 创建手动备份 {#create-a-manual-backup}

1. 进入实例的 [**Backup**](#view-the-backup-page) 页面。

2. 在右上角，点击 **...**，然后点击 **Manual Backup**。

3. 确认操作。备份将存储在 TiDB Cloud 中，并显示在 **Backup List** 中。 

你可以直接在 TiDB Cloud 控制台中恢复手动备份，而无需提供外部存储凭证。

## 恢复 {#restore}

TiDB Cloud 提供恢复功能，以帮助你在数据意外丢失或损坏时恢复数据。你可以从活跃实例的备份中恢复，也可以从回收站中已删除实例的备份中恢复。

### 恢复模式 {#restore-mode}

TiDB Cloud 支持对你的实例进行快照恢复和 point-in-time 恢复。

- **Snapshot Restore**：从特定备份快照恢复你的实例。你可以使用此方法恢复自动备份和手动备份。在 **Backup List** 中，手动备份会标记为 **Manual** 类型，过期状态为 **Permanent**。

- **Point-in-Time Restore**：将你的实例恢复到特定时间点。

    - Premium<CustomContent plan="byoc"> 或 BYOC</CustomContent> 实例：可以恢复到最近 7 天内的任意时间，但不能早于实例创建时间，也不能晚于当前时间前 1 分钟。请注意，手动备份不支持 PITR。

### 恢复目标 {#restore-destination}

TiDB Cloud 支持将数据恢复到新实例。

### 恢复到新的 {{{ .premium }}} 实例 {#restore-to-a-new-instance}

如需将数据恢复到新的 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例，请执行以下步骤：

1. 进入实例的 [**Backup**](#view-the-backup-page) 页面。

2. 点击 **Restore**。

3. 在 **Select Backup** 页面，选择你要使用的 **Restore Mode**。你可以从特定备份快照恢复，或恢复到特定时间点。

    <SimpleTab>
    <div label="Snapshot Restore">

    如需从选定的备份快照恢复，请执行以下步骤：

    1. 点击 **Snapshot Restore**。
    2. 选择你要恢复的备份快照。

    </div>
    <div label="Point-in-Time Restore">

    如需将 Premium<CustomContent plan="byoc"> 或 BYOC</CustomContent> 实例恢复到特定时间点，请执行以下步骤：

    1. 点击 **Point-in-Time Restore**。
    2. 选择你要恢复到的日期和时间。

    </div>
    </SimpleTab>

4. 点击 **Next** 进入 **Restore to a New Instance** 页面。

5. 为恢复配置新的 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例。请按照 <CustomContent plan="premium">[Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)</CustomContent><CustomContent plan="byoc">[Create a {{{ .byoc }}} Instance](/tidb-cloud/byoc/create-tidb-instance-byoc.md)</CustomContent> 中的步骤进行操作。

    <CustomContent plan="byoc">

    对于 {{{ .byoc }}}，请选择与备份位于同一云服务提供商和 region 的活跃资源池。恢复后的实例会继承所选资源池的高可用模式。你可以将同一备份恢复到单可用区或多可用区资源池。如果没有可用的合适资源池，`Organization Owner` 可以在恢复实例前创建一个。其他角色无法创建资源池。更多信息，请参见 [Create a Resource Pool](/tidb-cloud/byoc/create-resource-pool-byoc.md)。

    如果所选资源池设置了 Pool vCPU Limit，且其当前已配置的 vCPU 大于或等于该限制，TiDB Cloud 会显示警告，并且你无法将实例恢复到该资源池。要继续，请前往 Resource Pool 详情页面，提高或关闭 Pool vCPU Limit，或选择另一个资源池。

    > **Note:**
    >
    > 即使当前已配置的 vCPU 低于 Pool vCPU Limit，恢复实例也可能导致总已配置 vCPU 超过该限制。这可能会限制资源扩缩容并降低资源池中所有实例的性能。在恢复实例之前，请确保资源池具有足够的 vCPU 容量。如有必要，请提高或关闭 Pool vCPU Limit，或选择另一个资源池。

    </CustomContent>

    > **Note:**
    >
    > 默认情况下，新实例使用与备份相同的云服务提供商和 region。

6. 点击 **Restore** 开始恢复过程。

    当恢复过程开始时，实例状态会先变为 **Creating**。创建完成后，状态会变为 **Restoring**。在恢复完成且状态变为 **Available** 之前，实例始终不可用。

### 从回收站恢复 {#restore-from-recycle-bin}

如需从回收站恢复已删除的 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例，请执行以下步骤：

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击右上角的 **...**，然后点击 **Recycle Bin**。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在 **Recycle Bin** 页面，点击 <CustomContent plan="premium">**Premium**</CustomContent><CustomContent plan="byoc">**BYOC**</CustomContent> 页签，进入 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例的回收站。

3. 找到你要恢复的 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例，然后点击 **>** 按钮以展开该实例的可用备份。

4. 在目标备份所在行中，点击 **...**，然后选择 **Restore**。

5. 在 **Restore** 页面，按照[恢复到新实例](#restore-to-a-new-instance)中的相同步骤，将备份恢复到新实例。

<CustomContent plan="premium">

### 从不同套餐类型恢复备份 {#restore-backups-from-a-different-plan-type}

当前，你只能将托管在 AWS 上的 {{{ .dedicated }}} 集群备份恢复到新的 {{{ .premium }}} 实例。

如需恢复由 {{{ .dedicated }}} 集群生成的备份，请执行以下步骤：

1. 登录 [TiDB Cloud console](https://tidbcloud.com)，然后进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。在右上角，点击 **...**，然后点击 **Restore from Another Plan**。

2. 在 **Select Backup** 页面，选择包含目标 {{{ .dedicated }}} 集群的项目。选择该 {{{ .dedicated }}} 集群，选择你要恢复的备份快照，然后点击 **Next**。

    > **Note:**
    >
    > - 确保包含该备份快照的 {{{ .dedicated }}} 集群在所选项目中处于 **Active** 或 **Deleted** 状态。
    > - 该快照必须位于 {{{ .premium }}} 支持的 region 中。如果该 region 不受支持，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 为 {{{ .premium }}} 开通新的 region，或选择其他备份快照。

3. 在 **Restore** 页面，按照[恢复到新实例](#restore-to-a-new-instance)中的相同步骤，将备份恢复到新实例。

</CustomContent>

### 从云存储恢复备份 {#restore-backups-from-cloud-storage}

<CustomContent plan="premium">

{{{ .premium }}} 支持将云存储（例如 Amazon S3 和 Alibaba Cloud Object Storage Service (OSS)）中的备份恢复到新实例。此功能兼容从 {{{ .dedicated }}} 集群或 TiDB Self-Managed 集群生成的备份。

</CustomContent>

<CustomContent plan="byoc">

{{{ .premium }}} 和 {{{ .byoc }}} 支持将云存储（例如 Amazon S3）中的备份恢复到新实例。此功能兼容从 {{{ .dedicated }}} 集群或 TiDB Self-Managed 集群生成的备份。

</CustomContent>

<CustomContent plan="premium">

> **Note:**
>
> - 当前仅支持恢复位于 **Amazon S3** 和 **Alibaba Cloud OSS** 中的备份。
> - 你只能将备份恢复到由与你的存储 bucket 相同云服务提供商托管的新实例。
> - 如果实例和存储 bucket 位于不同 region，可能会产生额外的跨 region 数据传输费用。

</CustomContent>

<CustomContent plan="byoc">

> **Note:**
>
> - 当前仅支持恢复位于 **Amazon S3** 中的备份。
> - 你只能将备份恢复到由与你的存储 bucket 相同云服务提供商托管的新实例。
> - 如果实例和存储 bucket 位于不同 region，可能会产生额外的跨 region 数据传输费用。

</CustomContent>

#### 步骤 {#steps}

开始之前，请确保你拥有具有足够权限以访问备份文件的 access key 和 secret key。

要从云存储恢复备份，请执行以下操作：

1. 登录 [TiDB Cloud console](https://tidbcloud.com)，然后进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。在右上角，点击 **...** ，然后点击 **Restore from Cloud Storage**。

2. 在 **Select Backup Storage Location** 页面，提供以下信息：

    <CustomContent plan="premium">

    - **Cloud Provider**：选择存储备份文件的云服务提供商。
    - **Region**：如果你的云服务提供商是 Alibaba Cloud OSS，请选择一个 region。
    - **Backup Files URI**：输入包含备份文件的顶层文件夹的 URI。
    - **Access Key ID**：输入你的 access key ID。
    - **Access Key Secret**：输入你的 access key secret。

    </CustomContent>

    <CustomContent plan="byoc">

    - **Cloud Provider**：选择存储备份文件的云服务提供商。
    - **Backup Files URI**：输入包含备份文件的顶层文件夹的 URI。
    - **Access Key ID**：输入你的 access key ID。
    - **Access Key Secret**：输入你的 access key secret。

    </CustomContent>

    > **Tip:**
    >
    > 要为你的存储 bucket 创建 access key，请参见 [Configure Amazon S3 access using an AWS access key](#configure-amazon-s3-access-using-an-aws-access-key)<CustomContent plan="premium"> 和 [Configure Alibaba Cloud OSS access](#configure-alibaba-cloud-oss-access)</CustomContent>。

3. 点击 **Verify Backup and Next**。

4. 如果验证成功，将显示 **Restore to a New Instance** 页面。查看页面顶部显示的备份信息，然后按照 <CustomContent plan="premium">[Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)</CustomContent><CustomContent plan="byoc">[Create a {{{ .byoc }}} Instance](/tidb-cloud/byoc/create-tidb-instance-byoc.md)</CustomContent> 中的步骤将备份恢复到一个新的实例。

    <CustomContent plan="byoc">

    对于 {{{ .byoc }}}，请选择一个与目标云服务提供商和 region 匹配的活跃资源池。恢复后的实例会继承所选资源池的高可用模式。你可以将同一备份恢复到单可用区或多可用区资源池。如果没有可用的合适资源池，`Organization Owner` 可以在恢复实例之前创建一个。其他角色无法创建资源池。更多信息，请参见 [Create a Resource Pool](/tidb-cloud/byoc/create-resource-pool-byoc.md)。

    如果所选资源池设置了 Pool vCPU Limit，且其当前已配置的 vCPU 大于或等于该限制，TiDB Cloud 会显示警告，并且你无法将实例恢复到该资源池。要继续，请前往 Resource Pool 详情页面，提高或关闭 Pool vCPU Limit，或选择另一个资源池。

    > **Note:**
    >
    > 即使当前已配置的 vCPU 低于 Pool vCPU Limit，恢复实例也可能导致总已配置 vCPU 超过该限制。这可能会限制资源扩缩容并影响资源池中所有实例的性能。在恢复实例之前，请确保资源池具有足够的 vCPU 容量。如有必要，请提高或关闭 Pool vCPU Limit，或选择另一个资源池。

    </CustomContent>

    如果备份信息不正确，点击 **Previous** 返回上一页，然后输入正确的信息。

5. 点击 **Restore** 以恢复备份。

## 参考 {#references}

本节介绍如何为 Amazon S3<CustomContent plan="premium"> 和 Alibaba Cloud OSS</CustomContent> 配置访问。

### 使用 AWS access key 配置 Amazon S3 访问 {#configure-amazon-s3-access-using-an-aws-access-key}

建议你使用 IAM user，而不是 AWS account root user，来创建 access key。

请按照以下步骤配置 access key：

1. 创建 IAM user 和 access key。

    1. 创建一个 IAM user。更多信息，请参见 [Create an IAM user in your AWS account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)。
    2. 使用你的 AWS account ID 或 account alias，以及 IAM user name 和 password，登录 [IAM console](https://console.aws.amazon.com/iam)。
    3. 创建 access key。更多信息，请参见 [Manage access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

2. 向 IAM user 授予权限。

    创建一个仅包含你的任务所需权限的 policy，并将其附加到 IAM user。要将数据恢复到 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例，请授予 `s3:GetObject`、`s3:GetBucketLocation` 和 `s3:ListBucket` 权限。

    以下是一个示例 policy，允许 TiDB Cloud 从你的 Amazon S3 bucket 中的特定文件夹恢复数据。

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowGetBucketLocation",
                "Effect": "Allow",
                "Action": "s3:GetBucketLocation",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>"
            },
            {
                "Sid": "AllowListPrefix",
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>",
                "Condition": {
                    "StringLike": {
                        "s3:prefix": "<Your backup folder>/*"
                    }
                }
            },
            {
                "Sid": "AllowReadObjectsInPrefix",
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>/<Your backup folder>/*"
            }
        ]
    }
    ```

    在上述 policy 中，将 `<Your S3 bucket name>` 和 `<Your backup folder>` 替换为你的实际 bucket 名称和备份目录。此配置遵循最小权限原则，将访问限制为仅必要的备份文件。

> **Note:**
>
> TiDB Cloud 不会存储你的 access keys。为保持安全，请在导入或导出任务完成后[删除 access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

<CustomContent plan="premium">

### 配置 Alibaba Cloud OSS 访问 {#configure-alibaba-cloud-oss-access}

要授予 TiDB Cloud 对你的 Alibaba Cloud OSS bucket 的访问权限，你需要为该 bucket 创建一个 AccessKey 对。

请按照以下步骤配置 AccessKey 对：

1. 创建一个 RAM user 并获取 AccessKey 对。更多信息，请参见 [Create a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)。

    在 **Access Mode** 部分，选择 **Using permanent AccessKey to access**。

2. 创建一个具有所需权限的自定义 policy。更多信息，请参见 [Create custom policies](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)。

    - 在 **Effect** 部分，选择 **Allow**。
    - 在 **Service** 部分，选择 **Object Storage Service**。
    - 在 **Action** 部分，选择所需权限。要将备份恢复到 {{{ .premium }}} 实例，请授予 `oss:ListObjects` 和 `oss:GetObject` 权限。

        > **Tip:**
        >
        > 为了增强恢复操作的安全性，你可以将访问限制为存储备份文件的特定文件夹（`oss:Prefix`），而不是授予对整个 bucket 的访问权限。

        以下 JSON 示例展示了一个用于恢复任务的 policy。此 policy 将访问限制为特定 bucket 和备份文件夹。

        ```json
        {
        "Version": "1",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": "oss:ListObjects",
            "Resource": "acs:oss:*:*:<Your bucket name>",
            "Condition": {
                "StringLike": {
                "oss:Prefix": "<Your backup folder>/*"
                }
            }
            },
            {
            "Effect": "Allow",
            "Action": "oss:GetObject",
            "Resource": "acs:oss:*:*:<Your bucket name>/<Your backup folder>/*"
            }
        ]
        }
        ```

    - 在 **Resource** 部分，选择该 bucket 以及 bucket 中的特定对象。

3. 将自定义 policy 附加到 RAM user。

    更多信息，请参见 [Grant permissions to a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)。

</CustomContent>
