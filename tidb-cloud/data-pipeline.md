---
title: Data Pipeline
summary: 了解如何创建和管理 Data Pipeline，将全量和增量数据从 TiDB Cloud 同步到 TiDB Cloud Lake。
---

# Data Pipeline

TiDB Cloud Data Pipeline 可以将全量数据和增量变更从你的 TiDB Cloud 实例同步到 TiDB Cloud Lake，而无需借助第三方 ETL 工具。对于持续同步，它会先导出所选源数据的完整快照，然后持续同步行变更，以便 TiDB Cloud Lake 中的数据保持最新。

你可以在以下场景中使用 Data Pipeline：

- **一次性数据加载**：将完整快照导出到 TiDB Cloud Lake，用于初始数据加载或迁移。
- **持续数据同步**：使 TiDB Cloud Lake 与你的 TiDB Cloud 实例保持同步，以支持分析和报表工作负载。

## 工作原理 {#how-it-works}

启用持续同步的 Data Pipeline 分两个阶段运行：

1. **完整快照导出**：将所选源表一次性导出到外部 stage，TiDB Cloud Lake 再从该 stage 加载快照。
2. **增量同步**：持续捕获并同步行变更（插入、修改和删除），使 TiDB Cloud Lake 与源端保持一致。

你也可以将管道配置为仅导出完整快照，而不进行持续同步。

**外部 stage**（Amazon S3 或 Alibaba Cloud OSS）用作 TiDB Cloud 实例与 TiDB Cloud Lake 之间的中间存储。TiDB Cloud 会将导出的快照和捕获到的行变更写入 stage，而 TiDB Cloud Lake 会将 stage 中的数据加载到目标计算集群 (Warehouse)。这种方式将写入速率与消费速率解耦，从而提高可靠性，并让你能够控制成本和延时。

更多信息，请参阅 [Data Pipeline 常见问题](/tidb-cloud/data-pipeline-lake-faq.md)。

## 可用性 {#availability}

<CustomContent plan="premium">

| 计划 | 状态 |
| ---- | ------ |
| {{{ .premium }}} | Data Pipeline 已在 [TiDB Cloud console](https://tidbcloud.com) 中以私有预览形式提供，可按需申请使用。 |
| {{{ .dedicated }}} | Data Pipeline 尚未在 TiDB Cloud console 中提供。要使用 Data Pipeline，你需要手动进行设置。 |
| {{{ .essential }}} | Data Pipeline 尚未在 TiDB Cloud console 中提供。要使用 Data Pipeline，你需要手动进行设置。 |
</CustomContent>

<CustomContent plan="byoc">

| 计划 | 状态 |
| ---- | ------ |
| {{{ .premium }}} | Data Pipeline 已在 [TiDB Cloud console](https://tidbcloud.com) 中以私有预览形式提供，可按需申请使用。 |
| {{{ .byoc }}} | Data Pipeline 已在 [TiDB Cloud console](https://tidbcloud.com) 中以私有预览形式提供，可按需申请使用。 |
| {{{ .dedicated }}} | Data Pipeline 尚未在 TiDB Cloud console 中提供。要使用 Data Pipeline，你需要手动进行设置。 |
| {{{ .essential }}} | Data Pipeline 尚未在 TiDB Cloud console 中提供。要使用 Data Pipeline，你需要手动进行设置。 |
</CustomContent>

> **注意：**
>
> Data Pipeline 当前支持将 TiDB Cloud Lake 作为目标端。

## 创建 Data Pipeline {#create-a-data-pipeline}

请参考适用于你的计划的指南：

- TiDB Cloud Premium<CustomContent plan="byoc"> 和 {{{ .byoc }}}</CustomContent>：[Set Up a Data Pipeline to TiDB Cloud Lake](/tidb-cloud/data-pipeline-sink-to-lake.md)
- TiDB Cloud Dedicated：[Manually set up a data pipeline to replicate data to TiDB Cloud Lake](/tidb-cloud/data-pipeline-dedicated-sink-to-lake.md)
- TiDB Cloud Essential：[Sink to TiDB Cloud Lake](/tidb-cloud/data-pipeline-essential-sink-to-lake.md)

## 查看 Data Pipeline 页面 {#view-the-data-pipeline-page}

> **注意：**
>
> **Data Pipeline** 页面以及本节中的管理操作仅适用于 {{{ .premium }}}<CustomContent plan="byoc"> 和 {{{ .byoc }}}</CustomContent>。对于 {{{ .dedicated }}} 和 {{{ .essential }}}，你需要手动配置和维护 Data Pipeline。

要查看和管理你的 Data Pipeline，请执行以下步骤：

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 点击目标 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的名称进入其概览页面，然后在左侧导航栏中点击 **Data** > **Data Pipeline**。此时会显示 **Data Pipeline** 页面。

在 **Data Pipeline** 页面中，你可以创建 Data Pipeline、查看现有 Data Pipeline 列表，以及管理现有 Data Pipeline，例如暂停、恢复、编辑和删除管道。

## 管理 Data Pipeline {#manage-a-data-pipeline}

### 暂停和恢复 Data Pipeline {#pause-and-resume-a-data-pipeline}

- **Pause**：停止数据同步，并将管道标记为 `Paused`。不会丢失数据，同步进度也会被保留。管道在创建过程中或导出完整快照期间无法暂停。
- **Resume**：从暂停的位置继续同步，包括继续将数据导入 TiDB Cloud Lake。

要暂停或恢复 Data Pipeline，请进入目标 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的 **Data Pipeline** 页面，点击管道所在行中的 **...**，然后点击 **Pause** 或 **Resume**。

### 编辑 Data Pipeline {#edit-a-data-pipeline}

要编辑 Data Pipeline，请进入目标 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的 **Data Pipeline** 页面，点击管道所在行中的 **...**，然后点击 **Edit**。

当 Data Pipeline 处于 `Running` 状态时，无法进行编辑。请先暂停管道，再进行编辑，之后恢复管道以使更改生效。

管道创建后，目标类型和同步模式都无法更改。

> **注意：**
>
> 修改表过滤规则只会影响之后的增量数据：
>
> - 被新规则排除的表将不再接收增量数据。已经写入的数据会被保留。
> - 被新规则新增的表只会接收增量数据。不会为这些表回填历史数据。

### 删除 Data Pipeline {#delete-a-data-pipeline}

要删除 Data Pipeline，请执行以下步骤：

1. 进入目标 {{{ .premium }}}<CustomContent plan="byoc"> 或 {{{ .byoc }}}</CustomContent> 实例的 **Data Pipeline** 页面，点击管道所在行中的 **...**，然后点击 **Delete**。
2. 阅读警告并确认操作。删除 Data Pipeline 会：

    - 立即停止所有数据同步。
    - 尝试移除与该管道关联的 TiDB Cloud Lake 数据源和集成任务。如果移除失败，这些资源可能会保留，并需要手动清理。
    - **不会** 删除已经写入 TiDB Cloud Lake 的数据。
    - **不会** 删除计算集群中的目标数据库或表。

此操作无法撤销。

## 另请参阅 {#see-also}

- 有关 Data Pipeline 的常见问题，请参阅 [Data Pipeline 常见问题](/tidb-cloud/data-pipeline-lake-faq.md)。
- 有关 DDL、DML 和列类型支持的详细信息，请参阅 [TiDB Cloud Lake 的 Data Pipeline SQL 兼容性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md)。