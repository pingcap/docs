---
title: 数据源
summary: {{{ .lake }}} 中的数据源表示与外部系统的连接。它存储访问外部系统所需的凭证和连接详细信息，并可在多个集成任务或通知场景中复用。
---

# 数据源

{{{ .lake }}} 中的数据源表示与外部系统的连接。它存储访问外部系统所需的凭证和连接详细信息，并可在多个集成任务或通知场景中复用。

数据源本身不会执行同步。它的作用是集中管理访问设置，这样你就不需要在每个任务中重复输入账户、密码、密钥或通知端点。

## 支持的数据源类型 {#supported-data-source-types}

| 类型 | 用途 |
|------|---------|
| [Amazon S3 - 凭证](/tidb-cloud-lake/guides/aws-credentials.md) | 存储访问 Amazon S3 所需的 Access Key 和 Secret Key。这些凭证可在多个 S3 导入任务中复用。 |
| [Amazon SQS (S3) - IAM Role (Beta)](/tidb-cloud-lake/guides/amazon-sqs-s3-iam-role.md) | 存储 SQS (S3) 摄取所需的 queue URL、Region、IAM Role 和 S3 path scope。它可用于消费 S3 对象创建事件。 |
| [MySQL - Credentials](/tidb-cloud-lake/guides/mysql-credentials.md) | 存储访问 MySQL 所需的主机、端口、用户名、密码和数据库信息。这些设置可在多个 MySQL 同步任务中复用。 |
| [PostgreSQL - Credentials](/tidb-cloud-lake/guides/postgresql-credentials.md) | 存储访问 PostgreSQL 所需的主机、端口、用户名、密码和数据库信息。这些设置可在多个 PostgreSQL 同步任务中复用。 |
| [FeiShuBot](/tidb-cloud-lake/guides/feishubot.md) | 存储用于任务失败通知及类似场景的飞书机器人 webhook 和消息模板。 |
| [Kafka - 凭证（Beta）](/tidb-cloud-lake/guides/kafka-credentials.md) | 存储访问 Kafka 所需的 broker 地址、认证方法和连接凭证。这些设置可供 Kafka Consumer 任务复用。 |

并非每个数据源都对应一个集成任务。例如，`FeiShuBot` 用于通知配置，而 `Amazon S3 - Credentials`、`Amazon SQS (S3) - IAM Role`、`MySQL - Credentials`、`PostgreSQL - Credentials` 和 `Kafka - Credentials` 则由实际的导入、同步或事件消费任务引用。

## 管理数据源 {#managing-data-sources}

导航到 **Data** > **Data Sources**。在此页面中，你可以：

- 查看所有已配置的数据源
- 创建新数据源
- 编辑或删除现有数据源
- 测试连接以验证凭证

> **Tip:**
>
> 在保存数据源之前运行 **Test Connectivity**，以尽早发现无效凭证、权限缺失或网络限制等问题。

## 后续步骤 {#next-steps}

创建数据源后，你可以根据其用途，在[集成任务](/tidb-cloud-lake/guides/integration-tasks.md)或通知配置中引用它。