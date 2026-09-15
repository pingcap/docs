---
title: 任务管理
summary: 本页介绍数据集成任务的常见操作，包括任务创建流程、启动和下线行为、任务状态以及运行历史。有关特定数据源的配置，请参阅详细的任务指南。
---

# 任务管理

本页介绍数据集成任务的常见操作，包括任务创建流程、启动和下线行为、任务状态以及运行历史。有关特定数据源的配置，请参阅详细的任务指南。

## 通用任务创建流程 {#general-task-creation-flow}

1. 导航到 **Data** > **Data Integration**，然后点击 **Create Task**。
2. 选择一个现有的数据源。
3. 根据任务类型填写源端参数，例如文件路径、源表、同步模式、topic 或过滤条件。
4. 预览源数据并验证 schema、字段类型或消息内容。
5. 根据任务类型，选择目标计算集群和目标数据库 / 表，或配置结果查看方式。
6. 创建任务，并在需要时启动任务。

## 启动和下线任务 {#starting-and-stopping-tasks}

任务创建后，其初始状态为 **Stopped**。要开始同步、导入或消费，请在任务上点击 **Start**。

要下线正在运行的任务，请点击 **Stop**。任务将优雅地下线并保存当前进度。

## 任务状态 {#task-status}

数据集成页面会显示所有任务及其当前状态：

| 状态 | 描述 |
|--------|-------------|
| Running | 任务正在主动同步、导入或消费数据 |
| Stopped | 任务当前未运行 |
| Failed | 任务在执行期间遇到错误 |

## 查看运行历史 {#viewing-run-history}

点击某个任务可查看其执行历史。运行历史包括：

- 执行开始或结束时间
- 已导入或同步的行数，或已写入的消息对象数量
- 错误详情（如有）

## 按任务类型划分的运行时行为 {#runtime-behavior-by-task-type}

- S3 任务可以运行一次，也可以持续轮询新文件。
- MySQL `Snapshot` 任务通常会在全量负载完成后自动下线。
- MySQL `CDC Only` 和 `Snapshot + CDC` 任务会持续运行，直到手动下线。
- PostgreSQL `Snapshot` 任务通常会在全量负载完成后自动下线。
- PostgreSQL `CDC Only` 和 `Snapshot + CDC` 任务会持续运行，直到手动下线。
- SQS (S3) 任务会持续轮询 SQS 队列，消费 S3 对象创建事件，并将数据写入目标表，直到手动下线。
- Kafka Consumer 任务会持续消费 Kafka topic，并将消息内容保存到内部对象存储中，直到手动下线。

有关字段级配置和详细行为，请继续阅读相应的任务指南：

- [Amazon S3 集成任务](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md)
- [Amazon SQS (S3) 集成任务（Beta）](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md)
- [MySQL Integration Task](/tidb-cloud-lake/guides/integrate-with-mysql.md)
- [PostgreSQL 集成任务](/tidb-cloud-lake/guides/integrate-with-postgresql.md)
- [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md)
