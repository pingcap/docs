---
title: 同步到 TiDB Cloud Lake
summary: 了解如何创建、监控和管理一个数据管道，将数据从 TiDB Cloud 实例复制到 TiDB Cloud Lake。
---

# 同步到 TiDB Cloud Lake

在 TiDB Cloud 中，你可以使用 Data Pipeline 将完整数据和增量变更从你的 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例复制到 TiDB Cloud Lake，而无需使用第三方 ETL 工具。它会先导出所选源数据的完整快照，然后持续复制行变更，从而使 TiDB Cloud Lake 中的数据保持最新。

> **注意：**
>
> - 面向 TiDB Cloud Lake 的 Data Pipeline 当前对 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 处于 **private preview** 阶段，仅可按需申请使用。要申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Support Tickets** 前往 [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals)。创建工单，在 **Description** 字段中输入 "Apply for `Data Pipeline to TiDB Cloud Lake`"，然后点击 **Submit**。
> - Data Pipeline 功能基于 TiCDC 构建，因此具有与 TiCDC 相同的[限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。

## 限制 {#restrictions}

- TiDB Cloud Lake 的计算集群 (Warehouse) 必须与你的 TiDB Cloud 实例位于**同一 Region**。
- 只有带有**主键**的表才能进行增量复制。没有主键的表会在创建管道时显示在 **Filter results** 面板中。如果这些表被包含在同步范围内，其增量复制会被跳过。
- 每个 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例最多可以创建 100 个 changefeed。每个启用增量复制的数据管道会占用一个 changefeed 配额。
- 删除数据管道**不会**删除已经写入 TiDB Cloud Lake 的数据，也不会删除计算集群中的目标数据库和表。

## 前提条件 {#prerequisites}

开始之前，请确保你已具备以下条件：

- 一个 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例。请记下其部署所在的 Region。
- 一个位于 TiDB Cloud Lake 中、且与该实例处于同一 Region 的计算集群。如果你还没有，请先在 [TiDB Cloud Lake 控制台](https://lake.tidbcloud.com/) 中创建。创建数据管道时，只能选择与实例位于同一 Region 的计算集群。
- 一个外部 stage 存储桶：Amazon S3 存储桶或 Alibaba Cloud OSS 存储桶。请在与你的实例相同的 Region 中创建它。
- 一个可读取源表的 TiDB 数据库用户的用户名和密码。

## 创建数据管道 {#create-a-data-pipeline}

要创建数据管道，你需要配置目标端、外部 stage 和复制设置。

### 步骤 1. 配置目标端 {#step-1-configure-the-destination}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，进入目标 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例的概览页面，在左侧导航栏中点击 **Data** > **Data Pipeline**，然后点击右上角的 **Create Data Pipeline**。
2. 在 **Destination** 区域中，配置以下字段：

    - **Destination**：选择 **TiDB Cloud Lake**。
    - **Warehouse**：选择目标计算集群。列表中仅显示与你的实例位于同一 Region 的计算集群。如果没有可用的计算集群，请先在 [TiDB Cloud Lake](https://lake.tidbcloud.com/) 中创建一个，然后刷新列表。

3. （可选）在 **Database Prefix**、**Database Suffix**、**Table Prefix** 和 **Table Suffix** 字段中配置目标命名规则。这四个字段默认都为空，表示在 TiDB Cloud Lake 中创建的数据库和表将保持与源端相同的名称：

    - 数据库名：`<database prefix><source database name><database suffix>`
    - 表名：`<table prefix><source table name><table suffix>`

### 步骤 2. 配置外部 stage {#step-2-configure-the-external-stage}

外部 stage 是连接数据管道两端的对象存储：TiDB Cloud 将导出的快照和捕获到的行变更写入 stage，TiDB Cloud Lake 再从 stage 中将数据加载到目标计算集群。更多信息，请参阅[为什么数据管道需要外部 stage？](/tidb-cloud/data-pipeline-lake-faq.md#why-does-a-data-pipeline-require-an-external-stage)。

TiDB Cloud Data Pipeline 支持使用 Amazon S3 和 Alibaba Cloud OSS 作为外部 stage。请在与你的 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例相同的 Region 中创建存储桶，并先完成云服务提供方侧的配置。具体配置步骤因云服务提供方而异：

<SimpleTab>
<div label="Amazon S3">

1. 在 **External Stage** 区域中，以 `s3://<bucket-name>/<path-to-data>/` 格式填写你的 S3 存储桶 **Bucket URI**。

    先将其他字段留空。完成后续章节所述的任一存储桶访问配置方法后，再填写这些字段。

2. 为了让 TiDB Cloud 能够向外部 stage 写入数据，并让 TiDB Cloud Lake 能够从中读取数据，请在 **Bucket Access** 区域中配置存储桶访问。选择以下任一方法并完成相应授权。

    - 方法 1：使用 AWS Role ARN（推荐）

        TiDB Cloud（向 stage 写入数据）和 TiDB Cloud Lake（从 stage 读取数据）共用同一个 IAM role，因此你只需配置一次授权，且无需存储长期有效的访问密钥。你可以使用 TiDB Cloud 提供的 CloudFormation 模板创建该 role，也可以在 AWS 中手动设置。

        有关 AWS 侧完整配置，请参阅[为 TiDB Cloud Data Pipeline 设置外部 stage（AWS）](/tidb-cloud/data-pipeline-configure-external-stage-aws.md)。创建 role 后，在 TiDB Cloud 控制台中，将 `RoleARN` 输出值粘贴到 **Role ARN** 字段中；如果你还创建了 SQS 队列，请将队列 URL 复制到 **SQS Queue URL** 字段中。

    - 方法 2：使用 AWS access key

        > **注意：**
        >
        > 使用 access key 和 secret key（AK/SK）需要手动管理和轮换凭证，这会增加安全风险。为了获得更强的安全性，建议改用 **AWS Role ARN**。

        有关 AWS 侧完整配置（包括 IAM user、其权限以及可选的 SQS 队列），请参阅[使用 Access Key 访问存储桶](/tidb-cloud/data-pipeline-configure-external-stage-aws.md#option-3-bucket-access-with-access-key-not-recommended)。然后，在 TiDB Cloud 控制台中选择 **AWS Access Key**，并填写 **Access Key ID** 和 **Secret Access Key**。

    在填写完所选方法所需的信息后，点击 **Test Connection** 以验证 TiDB Cloud 是否可以访问该存储桶。如果检查失败，请验证存储桶 Region 以及授予 role 或 access key 的权限，然后再次测试连接。

</div>

<div label="Alibaba Cloud OSS">

有关 OSS 侧完整配置（包括 RAM user、其权限以及访问密钥），请参阅[为 TiDB Cloud Data Pipeline 设置外部 stage（Alibaba Cloud）](/tidb-cloud/data-pipeline-configure-external-stage-alibaba-cloud.md)。

1. 在 **External Stage** 区域中，以 `oss://<bucket-name>/<path-to-data>/` 格式填写你的 OSS 存储桶 **Bucket URI**。
2. 填写以下字段：

    - **Access Key ID**：RAM user 的 AccessKey ID。
    - **Access Key Secret**：RAM user 的 AccessKey Secret。

3. 点击 **Test Connection** 以验证 TiDB Cloud 是否可以访问该存储桶。如果检查失败，请验证存储桶 Region 以及授予 RAM user 的权限，然后再次测试连接。

> **注意：**
>
> 对于 Alibaba Cloud OSS，仅支持 access key 身份验证，不支持使用 SQS 的事件驱动摄取。

</div>

</SimpleTab>

### 步骤 3. 配置复制 {#step-3-configure-replication}

在 **Replication Data** 区域中，配置数据如何复制：

1. **Sync Mode**：选择同步模式。

    - **Full Data + Incremental Data**（默认）：导出所选源数据的完整快照，然后持续复制行变更。这是持续同步的推荐模式。
    - **Full Data**：仅一次性导出所选源数据的完整快照。不复制增量数据，快照生成后源端发生的变更将被忽略。

2. **Sync Interval**：数据管道的端到端延时目标。changefeed 的 flush 周期和 TiDB Cloud Lake 的轮询周期都会影响端到端延时。更短的间隔可以降低数据延时，但会增加对云存储的 API 调用次数。默认值会显示在控制台中。

3. **Changefeed Capacity Units**：为增量复制分配的处理能力，并同时显示其支持的最大复制吞吐。例如，`2 CCUs (the maximum replication throughput is 5,000 rows/s)`。

    > **注意：**
    >
    > Changefeed Capacity Units 用于衡量分配给数据流处理的能力。此设置用于配置增量复制的性能。如果你选择 **Full Data** 作为同步模式，则不会消耗 CCU，因为不会执行增量复制。

4. **TiDB Username** 和 **TiDB Password**：填写 TiDB 数据库用户的用户名和密码。数据管道使用该账户导出完整快照，因此该账户必须具有对源表的读访问权限。增量行变更由 changefeed 单独捕获。

5. **Sync Objects**：选择要复制的对象。

    - **Customize**（默认）：在 **Table Filter Rules** 中指定显式规则。规则语法与 [TiCDC 表过滤规则](https://docs.pingcap.com/tidb/stable/ticdc-filter#table-filter) 相同。默认情况下，单条 `*.*` 规则会复制所有非系统表。**Filter results** 面板会显示与规则匹配的数据库和表。
    - **All**：复制所有数据库中的所有表。此时会隐藏表过滤规则配置。

    你还可以选择 **Case-sensitive**，使过滤规则中数据库名和表名的匹配变为大小写敏感。默认情况下，匹配不区分大小写。

    > **注意：**
    >
    > 只有带有主键的表才能进行增量复制。没有主键的表会单独列在 **Filter results** 面板中，并在增量复制时被跳过。请在创建数据管道前为这些表添加主键，或使用如 `"!test.tbl1"` 之类的过滤规则将其排除。

6. **Pipeline Name**：输入数据管道名称。

7. 点击 **Create**。

    在导出完整快照期间，管道会进入 **Creating** 状态。对于 **Full Data + Incremental Data**，当增量复制开始时，状态会变为 **Running**。

## 管理数据管道 {#manage-the-data-pipeline}

### 编辑数据管道 {#edit-a-data-pipeline}

要编辑数据管道，请进入目标 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例的 **Data Pipeline** 页面，点击该管道所在行中的 **...**，然后点击 **Edit**。

当数据管道处于 `Running` 状态时，无法进行编辑。请先暂停管道，完成编辑后再恢复运行以应用更改。

管道创建后，目标类型和同步模式都不能更改。

> **注意：**
>
> 修改表过滤规则只会影响之后的增量数据：
>
> - 被新规则排除的表将不再接收增量数据。已经写入的数据会被保留。
> - 被新规则新增纳入的表只会接收增量数据。不会为这些表回填历史数据。

### 暂停和恢复数据管道 {#pause-and-resume-a-data-pipeline}

- **Pause**：停止数据复制，并将管道标记为 `Paused`。不会丢失数据，复制进度也会被保留。管道在创建过程中或导出完整快照期间不能暂停。
- **Resume**：从暂停的位置继续复制，包括继续向 TiDB Cloud Lake 摄取数据。

要暂停和恢复数据管道，请进入目标 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例的 **Data Pipeline** 页面，点击该管道所在行中的 **...**，然后点击 **Pause** 或 **Resume**。

### 删除数据管道 {#delete-a-data-pipeline}

要删除数据管道，请执行以下步骤：

1. 进入目标 <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 实例的 **Data Pipeline** 页面，点击该管道所在行中的 **...**，然后点击 **Delete**。
2. 阅读警告并确认操作。删除数据管道会：

    - 立即停止所有数据复制。
    - 尝试移除与该管道关联的 TiDB Cloud Lake 数据源和集成任务。如果移除失败，这些资源可能会保留，并需要手动清理。
    - **不会**删除已经写入 TiDB Cloud Lake 的数据。
    - **不会**删除计算集群中的目标数据库或表。

此操作无法撤销。

## 另请参阅 {#see-also}

- 有关 Data Pipeline 的常见问题，请参阅 [Data Pipeline 常见问题](/tidb-cloud/data-pipeline-lake-faq.md)。
- 有关 DDL、DML 和列类型支持的详细信息，请参阅 [TiDB Cloud Lake 的 Data Pipeline SQL 兼容性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md)。