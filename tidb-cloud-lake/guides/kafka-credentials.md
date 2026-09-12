---
title: Kafka - Credentials（Beta）
summary: 创建一个 “Kafka - Credentials” 数据源，用于存储 Kafka 连接信息，以便在 Kafka Consumer 集成任务中复用。
---

# Kafka - Credentials（Beta）

本页介绍如何创建 `Kafka - Credentials` 数据源。该数据源用于存储访问 Kafka 集群所需的 broker 地址、认证方法和连接凭据。你可以在多个 Kafka Consumer 集成任务中复用这些设置。

`Kafka - Credentials` 仅存储 Kafka 连接信息。它本身不会消费消息。实际读取 Kafka topic 消息并将其写入内部对象存储的过程，由 [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md) 执行。

## 使用场景 {#use-cases}

- 集中管理 Kafka broker 地址和认证设置
- 在多个 Kafka Consumer 任务之间复用相同的 Kafka 连接设置
- 当多个任务引用同一配置时，可在一个位置统一修改 Kafka 地址、认证方法或账户信息

## 创建 Kafka - Credentials {#create-kafka-credentials}

1. 进入 **Data** > **Data Sources**，然后点击 **Create Data Source**。
2. 选择 **Kafka - Credentials** 作为服务类型，然后填写连接详情：

    | 字段 | 必填 | 描述 |
    |-------|----------|-------------|
    | **Name** | 是 | 数据源的描述性名称 |
    | **Brokers** | 是 | Kafka broker 地址列表。多个地址之间使用逗号分隔，例如 `broker-1:9092,broker-2:9093,broker-3:9092` |
    | **Authentication** | 是 | Kafka 认证方法。支持的选项为 **None** 和 **SASL/PLAIN** |
    | **TLS encryption** | 否 | 是否启用 TLS 加密 |
    | **Username** | 适用时必填 | Kafka 用户名。选择 **SASL/PLAIN** 时为必填项 |
    | **Password** | 适用时必填 | Kafka 密码。选择 **SASL/PLAIN** 时为必填项 |

3. 点击 **Test Connectivity** 以验证连接。如果测试成功，点击 **OK** 保存数据源。

## 配置建议 {#configuration-recommendations}

- 建议为平台创建专用的 Kafka 用户，而不是共享应用账户。
- 如果你的 Kafka 集群要求加密连接，请启用 **TLS encryption**。
- 如果你选择 **SASL/PLAIN**，请确保 Kafka 用户具有读取下游任务将要消费的 topic 的权限。
- 在保存数据源之前运行 **Test Connectivity**，以验证 broker 地址、网络访问和认证设置。

## 后续步骤 {#next-steps}

创建数据源后，你可以使用它来创建 [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md)。
