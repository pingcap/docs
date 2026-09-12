---
title: Kafka Consumer Integration Task (Beta)
summary: 创建 Kafka Consumer 任务，持续消费 Kafka topic 中的消息，并将消息内容保存到内部对象存储（租户 Stage）。
---

# Kafka Consumer Integration Task (Beta)

本文介绍如何创建 Kafka Consumer 任务，以持续消费 Kafka topic 中的消息，并将消息内容保存到内部对象存储（租户 Stage）。

与 S3、MySQL 或 PostgreSQL 数据集成任务不同，Kafka Consumer 任务不会直接写入常规目标表。任务创建并启动后，你可以使用 `@kafka_consumer/<task_name>/` stage 路径查看已保存的消息对象，并通过 SQL 查询其内容。

如果你需要先创建可复用的 Kafka 连接设置，请参见 [Kafka - 凭证（Beta）](/tidb-cloud-lake/guides/kafka-credentials.md)。

## 使用场景 {#use-cases}

- 持续从 Kafka topic 中摄取 JSON 消息
- 先将 Kafka 消息落盘到内部对象存储，再通过下游 SQL 进行查询或处理
- 为实时或准实时数据流水线保留原始 Kafka 消息对象

## 工作流 {#workflow}

1. 上游系统将消息写入 Kafka topic。
2. Kafka Consumer 任务从指定的 topic 中读取消息。
3. 任务将消息批量保存到内部对象存储（租户 Stage）。
4. 用户通过 `@kafka_consumer/<task_name>/` 查看生成的对象。
5. 用户从 stage 查询消息内容，并根据需要执行下游加载或转换。

> **注意：**
>
> Kafka Consumer 任务保存的是包含 Kafka 消息内容的对象文件。如果你需要将消息写入业务表，请基于 stage 查询结果执行下游 `INSERT INTO ... SELECT`、`COPY INTO` 或其他处理。

## 前提条件 {#prerequisites}

在创建 Kafka Consumer 任务之前，请确保：

- 已创建 **Kafka - Credentials** 数据源
- 平台可以通过网络访问 Kafka broker
- Kafka 数据源中的认证方法、TLS 设置和账户信息正确
- Kafka 用户具有读取目标 topic 的权限
- 目标 topic 中的消息与任务中选择的 **Data Format** 一致

## 创建 Kafka Consumer 任务 {#creating-a-kafka-consumer-task}

### 第 1 步：基本信息 {#step-1-basic-info}

1. 进入 **Data** > **Data Integration**，然后点击 **Create Task**。
2. 选择一个 Kafka 数据源，然后配置基本参数：

    | 字段 | 必填 | 描述 |
    |-------|----------|-------------|
    | **Data Source** | 是 | 从下拉列表中选择一个已有的 **Kafka - Credentials** 数据源 |
    | **Name** | 是 | Kafka Consumer 任务名称 |
    | **Topics** | 是 | 要消费的 Kafka topic。多个 topic 之间用逗号分隔，例如 `topic-1,topic-2` |
    | **Data Format** | 是 | Kafka 消息的数据格式。目前为 **JSON** |
    | **Start Position** | 是 | 当不存在已提交的偏移时的起始位置。支持 **Latest** 和 **Earliest** |
    | **Max Batch Bytes** | 否 | 每批的最大数据大小。默认值为 **16 MiB** |
    | **Max Batch Wait Interval** | 否 | 每批的最大等待时间。默认值为 **1 Minute** |

    > **注意：**
    >
    > **Latest** 仅消费新消息，而 **Earliest** 从 Kafka 中最早保留的消息开始消费。该设置仅在 Consumer Group 没有已提交偏移时生效，不会重置已有偏移。

### 第 2 步：预览数据 {#step-2-preview-data}

完成基本设置后，点击 **Next** 进入 **Preview Data Info**。

系统会尝试从指定的 Kafka topic 中读取示例消息。如果有可用消息，页面会显示 1 到 2 条 JSON 消息，供你验证 topic、数据格式和消息结构。

如果没有可预览的消息，页面会显示 **No sample data available**。你仍然可以继续创建任务，但建议检查这些 topic 是否已包含消息，以及所选 **Start Position** 是否能够读取到示例数据。

### 第 3 步：查看结果 {#step-3-result-viewing}

在 **Result Viewing** 步骤中，选择用于运行 Kafka Consumer 任务的计算集群 (Warehouse)。

任务启动后，会读取 Kafka 消息并将其保存到内部对象存储（租户 Stage）。页面会提供 SQL 示例。你可以使用 `LIST @kafka_consumer/<task_name>/` 查看生成的对象，并使用 stage 查询读取消息内容。

```sql
-- List stage objects:
LIST @kafka_consumer/<task_name>/;

-- Query object data (replace with the correct PATTERN path):
SELECT $1
FROM @kafka_consumer (
    FILE_FORMAT=>'ndjson',
    PATTERN=>'<task_name>/year=YYYY/month=MM/day=DD/hour=HH/.*[.]ndjson'
);
```

点击 **Create** 创建任务。

## 任务行为 {#task-behavior}

Kafka Consumer 任务会持续运行。启动后，它会从指定的 topic 中消费消息，并将其批量保存为内部对象存储中的对象文件，直到你手动停止该任务。

| 场景 | 行为 |
|----------|----------|
| topics 中存在新消息 | 读取消息并将其写入租户 Stage |
| 批次大小达到 **Max Batch Bytes** | 将当前批次写入对象存储 |
| 等待时间达到 **Max Batch Wait Interval** | 即使当前批次未达到大小限制，也会将其写入对象存储 |
| 写入操作成功 | 保存消费进度，以便后续继续消费 |
| 你手动下线任务 | 停止消费，并保留已保存的消息对象 |

## 查询已保存的消息 {#query-saved-messages}

Kafka Consumer 任务会将消息对象保存在 `@kafka_consumer/<task_name>/` 路径下。任务启动并写入对象后，打开任务详情页并切换到 **Data Browsing** 页签，即可按 UTC 小时查看对象数量和对象列表。

你也可以先使用 SQL 列出对象，再根据实际路径查询其内容：

```sql
LIST @kafka_consumer/<task_name>/;
```

```sql
SELECT $1
FROM @kafka_consumer (
    FILE_FORMAT=>'ndjson',
    PATTERN=>'<task_name>/year=YYYY/month=MM/day=DD/hour=HH/.*[.]ndjson'
);
```

如果你需要将消息写入业务表，请基于查询结果继续执行下游转换或加载。

## 高级配置 {#advanced-configuration}

### 运行时大小 {#runtime-size}

Kafka Consumer 任务支持修改运行时大小。在修改 Runtime Size 之前，请先停止任务，然后通过 **Edit** 菜单打开编辑页面，在 **Runtime Size** 部分选择合适的运行时大小并保存更改。重启任务后，任务将以新的运行时大小运行。

> **注意：**
>
> 可用的运行时大小和价格取决于你的计费方案。请以控制台中显示的选项和定价文档为准。
