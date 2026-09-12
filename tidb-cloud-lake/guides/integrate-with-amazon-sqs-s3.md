---
title: Amazon SQS (S3) 集成任务（Beta）
summary: 了解如何创建 Amazon SQS (S3) 集成任务，该任务从 SQS 队列消费 S3 对象创建事件，并将对应的对象数据写入 {{{ .lake }}}。
---

# Amazon SQS (S3) 集成任务（Beta）

本文介绍如何创建 Amazon SQS (S3) 集成任务。该任务从 SQS 队列消费 S3 对象创建事件，并将对应的对象数据写入 {{{ .lake }}}。

该任务专为 S3 事件驱动的数据摄取而设计。上游系统将对象写入 S3 后，S3 会向 SQS 发送 `ObjectCreated` 事件。{{{ .lake }}} 通过 AssumeRole 消费 SQS 消息，并根据事件中的 bucket 和对象键将数据写入 {{{ .lake }}}。

如果你需要先创建可复用的 SQS (S3) 连接设置，请参见 [Amazon SQS (S3) - IAM Role (Beta)](/tidb-cloud-lake/guides/amazon-sqs-s3-iam-role.md)。

## 使用场景 {#use-cases}

- 基于 S3 `ObjectCreated` 事件自动摄取新写入的 S3 对象
- 使用 S3 事件通知驱动数据摄取，减少新文件到达后的延时
- 避免仅依赖轮询 S3 路径来发现新文件

## 工作流程 {#workflow}

1. 上游系统将对象写入 S3 存储桶。
2. S3 Event Notification 将 `ObjectCreated` 事件发送到一个 SQS 标准队列。
3. {{{ .lake }}} 通过用户配置的 IAM Role 从 SQS 队列读取消息。
4. 任务解析消息中的 S3 事件记录。
5. 任务根据 S3 事件记录中的 bucket、对象键和文件格式，将数据写入 {{{ .lake }}} 目标表。
6. 写入成功后，任务会从队列中删除已处理的 SQS 消息。

> **Note:**
>
> S3 事件通知和 SQS 标准队列都可能产生重复消息。{{{ .lake }}} 会处理失败重试。如果你的业务逻辑要求严格去重，请基于对象信息、事件时间、`sequencer` 或 SQS message ID 设计下游去重逻辑。

## 前提条件 {#prerequisites}

在创建 SQS (S3) 集成任务之前，请确保：

- 已创建 **Amazon SQS (S3) - IAM Role** 数据源
- S3 存储桶已配置 `ObjectCreated` 事件通知，并将事件发送到目标 SQS 队列
- SQS 队列策略允许 Amazon S3 调用 `sqs:SendMessage`
- 用户 IAM Role 允许 {{{ .lake }}} 平台角色通过 `sts:AssumeRole` 访问该角色
- 用户 IAM Role 具有读取目标 S3 对象和消费目标 SQS 队列的权限
- SQS 队列中包含标准 S3 Event Notification 格式的消息
- S3 通知中的 bucket、prefix 和 suffix 与数据源配置一致

## 创建 SQS (S3) 集成任务 {#creating-an-sqs-s3-integration-task}

### 第 1 步：基本信息 {#step-1-basic-info}

1. 进入 **Data** > **Data Integration**，然后点击 **Create Task**。
2. 选择一个 SQS (S3) 数据源，然后配置基本参数：

    | 字段 | 必填 | 描述 |
    |-------|----------|-------------|
    | **Data Source** | 是 | 从下拉列表中选择一个现有的 **Amazon SQS (S3) - IAM Role** 数据源 |
    | **Name** | 是 | 集成任务名称 |
    | **File Format** | 是 | S3 对象的文件格式，例如 CSV、Parquet 或 NDJSON |
    | **Object Key Prefix** | 否 | 仅处理具有指定前缀的对象事件，例如 `raw/events/`。该值应与数据源和 S3 通知过滤器一致 |
    | **Object Key Suffix** | 否 | 仅处理具有指定后缀的对象事件，例如 `.json` 或 `.parquet`。该值应与数据源和 S3 通知过滤器一致 |

    > **Tip:**
    >
    > 建议先在 S3 Event Notification 中配置 prefix 或 suffix 过滤器，并与数据源和任务中的过滤器保持一致。这样可以减少无关消息进入 SQS。

### 第 2 步：预览数据 {#step-2-preview-data}

完成基本设置后，点击 **Next** 预览源数据。

预览结果与 [Amazon S3 集成任务](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) 相同。系统会根据 SQS (S3) 配置定位对应的 S3 对象，读取文件内容，并显示：

- 包含列名和数据类型的样例数据
- 匹配到的 S3 对象列表及对象大小

> **Note:**
>
> 如果当前路径作用域内没有可预览的 S3 对象，预览页面可能不会显示样例数据。请上传一个符合目标 prefix / suffix 的测试对象，然后重试预览。

### 第 3 步：设置目标表 {#step-3-set-target-table}

在 {{{ .lake }}} 中配置目标位置：

| 字段 | 描述 |
|-------|-------------|
| **Warehouse** | 选择用于运行 SQS (S3) 集成任务的 {{{ .lake }}} 计算集群 |
| **Target Database** | 选择 {{{ .lake }}} 中的目标数据库 |
| **Target Table** | 要写入数据的目标表名称 |

系统会根据预览的 S3 对象内容推导列名和数据类型。继续之前，你可以查看并编辑目标表结构。如果要写入现有表，请选择目标表并验证列映射。

点击 **Create** 创建集成任务。

## 任务行为 {#task-behavior}

SQS (S3) 集成任务是一个持续运行的任务。启动后，它会定期从 SQS 队列读取消息，并将数据写入目标表，直到被手动下线。

| 场景 | 行为 |
|----------|----------|
| 队列中存在消息 | 读取消息，解析 S3 事件记录，并根据事件中的对象信息将数据写入目标表 |
| 写入成功 | 删除对应的 SQS 消息，以避免重复处理 |
| 写入失败 | 不删除对应的 SQS 消息，以便后续重试 |
| 消息格式不是有效的 S3 Event Notification | 记录错误，并跳过处理或下线任务 |
| 任务被手动下线 | 下线轮询并保存当前任务状态 |

## 与 Amazon S3 集成任务的区别 {#difference-from-amazon-s3-integration-task}

| 任务类型 | 处理对象 | 写入 {{{ .lake }}} 的数据 | 典型使用场景 |
|-----------|------------------|--------------------------|------------------|
| Amazon S3 Integration Task | S3 file content | CSV、Parquet 或 NDJSON 文件中的业务数据 | 文件数据导入 |
| Amazon SQS (S3) Integration Task | SQS 中的 S3 ObjectCreated 事件 | 与事件对应的 S3 对象数据 | 自动摄取新对象，事件驱动导入 |

如果你的目标是定期扫描某个 S3 路径并导入文件内容，请使用 Amazon S3 Integration Task。如果你的目标是基于 S3 ObjectCreated 事件触发数据摄取，请使用 Amazon SQS (S3) Integration Task。
