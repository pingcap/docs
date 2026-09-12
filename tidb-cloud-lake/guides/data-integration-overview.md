---
title: 数据集成概览
summary: {{{ .lake }}} 中的数据集成功能提供了一个可视化、无代码的接口，用于将外部系统中的数据导入或同步到 {{{ .lake }}}。
---

# 数据集成概览

{{{ .lake }}} 中的数据集成功能提供了一个可视化、无代码的接口，用于将外部系统中的数据导入、同步或消费到 {{{ .lake }}} 中。该功能围绕两个关键概念展开：**数据源** 和 **集成任务**。

## 关键概念 {#key-concepts}

| 概念 | 说明 |
|---------|-------------|
| [数据源](/tidb-cloud-lake/guides/data-sources.md) | 可复用的连接设置或凭证，用于访问外部系统或发送通知，例如 AWS Access Key / Secret Key、MySQL hostname / username / password、SQS (S3) queue URL、Kafka broker addresses，或 FeiShu bot webhook。 |
| [集成任务](/tidb-cloud-lake/guides/integration-tasks.md) | 可执行的任务，用于定义数据来源、任务将数据写入到哪里或如何保存结果、使用哪些运行时参数，以及如何启动和监控任务。 |

数据源本身不会移动数据。它们仅存储访问外部系统所需的信息。集成任务才是实际执行导入、快照、持续同步或消息消费的单元。

> **注意：**
>
> 运行数据集成任务会产生服务托管费用。{{{ .lake }}} 会根据服务的实际运行时间按秒计费。详情请参见[服务托管定价](/tidb-cloud-lake/guides/pricing-billing.md#service-hosting-pricing)。

并非每个数据源都对应一个数据摄取任务。例如，`FeiShuBot` 用于通知，而不是将源数据加载到 {{{ .lake }}} 中。

## 支持的集成任务类型 {#supported-integration-task-types}

| 任务类型 | 说明 |
|-----------|-------------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | 从 Amazon S3 导入 CSV、Parquet 或 NDJSON 文件，支持一次性或持续摄取。 |
| [Amazon SQS (S3) (Beta)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) | 从 SQS 队列中消费 S3 对象创建事件，并将相应的对象数据写入 {{{ .lake }}}。 |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | 使用 `Snapshot`、`CDC Only` 或 `Snapshot + CDC` 模式同步 MySQL 中的表数据。 |
| [PostgreSQL](/tidb-cloud-lake/guides/integrate-with-postgresql.md) | 使用 `Snapshot`、`CDC Only` 或 `Snapshot + CDC` 模式同步 PostgreSQL 中的表数据。 |
| [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md) | 持续消费 Kafka topic 中的消息，并将消息内容保存到内部对象存储中。 |

## 推荐流程 {#recommended-flow}

1. 在[数据源](/tidb-cloud-lake/guides/data-sources.md)页面创建并测试可复用的连接设置。
2. 在[集成任务](/tidb-cloud-lake/guides/integration-tasks.md)页面查看支持的任务类型及其适用场景。
3. 阅读特定任务的指南，配置数据源、预览数据，并配置结果位置或结果查看方法。
4. 使用[任务管理](/tidb-cloud-lake/guides/task-management.md)页面启动任务、检查状态并排查执行问题。