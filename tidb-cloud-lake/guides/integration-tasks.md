---
title: 集成任务
summary: 本页概述 {{{ .lake }}} 中的集成任务。集成任务定义了数据如何从外部源流入 {{{ .lake }}}，包括源设置、目标表和运行时参数。
---

# 集成任务

{{{ .lake }}} 中的集成任务定义了数据如何从源流入 {{{ .lake }}}。每个任务都会引用一个现有数据源，并指定源设置、目标位置或结果查看方法，以及特定于任务类型的运行时参数。

与数据源不同，集成任务是实际执行数据移动、同步或消息消费的可执行单元。数据源存储访问设置，而任务负责调度、摄取、同步、消费、下线、恢复和监控。

## 支持的任务类型 {#supported-task-types}

| Task Type | Description |
|-----------|-------------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | 从 Amazon S3 导入 CSV、Parquet 或 NDJSON 文件，支持一次性或持续摄取。 |
| [Amazon SQS (S3) (Beta)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) | 从 SQS 队列消费 S3 对象创建事件，并将相应的对象数据写入 {{{ .lake }}}。 |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | 使用 `Snapshot`、`CDC Only` 或 `Snapshot + CDC` 同步 MySQL 的表数据。 |
| [PostgreSQL](/tidb-cloud-lake/guides/integrate-with-postgresql.md) | 使用 `Snapshot`、`CDC Only` 或 `Snapshot + CDC` 同步 PostgreSQL 的表数据。 |
| [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md) | 持续消费 Kafka topic 中的消息，并将消息内容保存到内部对象存储。 |

## 阅读指南 {#reading-guide}

建议按以下顺序阅读：

1. 先阅读 [任务管理](/tidb-cloud-lake/guides/task-management.md)，了解任务创建流程、启动 / 下线行为、状态和运行历史。
2. 然后阅读与你要配置的源类型对应的任务专用指南。

## 任务类型差异 {#task-type-differences}

- S3 任务适用于文件导入场景，主要关注文件路径模式、文件格式和摄取行为。
- SQS (S3) 任务适用于由 S3 事件驱动的数据摄取场景，主要关注 SQS 队列、S3 事件过滤器、IAM Role 和目标表。
- MySQL 和 PostgreSQL 任务适用于表同步场景，主要关注同步模式、主键、增量捕获和归档调度。
- Kafka Consumer 任务适用于消息消费场景，主要关注 topic、起始位置、批大小、批等待间隔以及租户 Stage 查询。