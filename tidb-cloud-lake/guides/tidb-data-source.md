---
title: TiDB 数据源（预览）
summary: 介绍如何在 TiDB Cloud Lake 中设置 TiDB 数据源，包括存储和身份验证配置。
---

# TiDB 数据源（预览）

**TiDB** 数据源用于存储对象存储位置、凭证以及可选的事件队列，TiDB Cloud Lake 会使用这些信息读取由 TiDB 集群暂存的数据。它不会连接到 TiDB 服务器本身。Dumpling 和 TiCDC 会将导出数据和变更事件写入对象存储 bucket，而 TiDB Cloud Lake 则从该 bucket 中读取数据。

## 使用场景 {#use-cases}

- 为多个 TiDB 同步任务集中管理 staging bucket、凭证和可选的 SQS 队列
- 避免在每个任务中重复输入相同的 bucket 和授权设置
- 使用 IAM Role 代替静态密钥，使 TiDB Cloud Lake 获取短期凭证
- 当多个任务引用同一个 bucket、role 或 queue 时，可在一个位置统一更新

## 为集成准备 TiDB {#prepare-tidb-for-integration}

TiDB Cloud 会将全量快照（Dumpling）和增量变更（TiCDC）导出到对象存储 bucket。由于不同 TiDB Cloud 套餐之间存在差异，我们建议针对每种套餐采用特定的设置路径，以尽量减少配置并确保数据兼容。

- **Premium** 或 **BYOC**：使用 [TiDB Cloud console **Data Pipeline**](https://docs.pingcap.com/tidbcloud/data-pipeline-sink-to-lake/?plan=premium) UI 在一个位置设置和管理导出与导入。
- **Essential**：使用 console 的 **Export** 和 **Changefeed** 功能，[手动设置到 TiDB Cloud Lake 的数据管道](https://docs.pingcap.com/tidbcloud/data-pipeline-essential-sink-to-lake/?plan=essential)。
- **Dedicated**：使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 和 console 的 **Changefeed** 功能，[手动设置到 TiDB Cloud Lake 的数据管道](https://docs.pingcap.com/tidbcloud/data-pipeline-dedicated-sink-to-lake/)。

## 创建 TiDB 数据源 {#create-tidb-data-source}

1. 进入 **Data** > **Data Sources**，然后点击 **Create**。
2. 选择 **TiDB** 作为服务，然后填写数据源的 **Name**。
3. 选择 **Storage Provider** 和 **Authentication Method**，然后填写连接详细信息。显示的字段取决于你选择的组合。参见下文的 [Amazon S3](#amazon-s3) 或 [Alibaba Cloud OSS](#alibaba-cloud-oss)。

    > **Note:**
    >
    > 如有可能，请使用与你的 TiDB Cloud Lake 部署相同的存储提供商和 region。

4. 点击 **Test Connectivity** 验证 bucket 和凭证。如果测试成功，点击 **OK** 保存数据源。

## Amazon S3 {#amazon-s3}

当存储提供商为 **Amazon S3** 时，请选择以下其中一种身份验证方法。

### 身份验证方法：Role ARN（推荐） {#authentication-method-role-arn-recommended}

Role ARN 使用 AssumeRole 模型。TiDB Cloud Lake 会假设你 AWS 账户中的 IAM Role 并获取临时凭证，因此你无需将静态密钥交给 TiDB Cloud Lake。

在保存数据源之前，你的 IAM Role 信任策略必须信任这两个平台角色（TiDB Cloud Lake 设置与验证角色，以及 TiDB Cloud Lake 数据加载角色），并在 `sts:ExternalId` 条件中指定对应的 External ID。有关完整的信任策略配置，请参见 [Authenticate with AWS IAM Role](https://docs.pingcap.com/tidbcloudlake/authenticate-with-aws-iam-role/)。

| 字段 | 必填 | 说明 |
| ------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**                  | 是      | 此数据源的描述性名称                                                                                                      |
| **Storage Provider**      | 是      | 选择 **Amazon S3**                                                                                                                         |
| **Authentication Method** | 是      | 选择 **Role ARN**                                                                                                                          |
| **Role ARN**              | 是      | 你 AWS 账户中的 IAM Role ARN，TiDB Cloud Lake 被允许假设该角色，例如 `arn:aws:iam::123456789012:role/tidbcloud-lake-tidb` |
| **S3 Bucket Name**        | 是      | TiCDC / Dumpling 暂存数据、供 TiDB Cloud Lake 加载的 bucket                                                                     |
| **S3 Region**             | 是      | bucket 所在的 AWS Region，例如 `us-east-1`                                                                                            |
| **S3 Endpoint**           | 否       | 仅用于 MinIO 等兼容 S3 的存储，例如 `http://localhost:9000`。对于 Amazon S3 请留空                                 |
| **SQS Queue URL**         | 否       | 用于事件驱动模式的可选标准 SQS 队列 URL。参见 [可选 SQS 队列](#optional-sqs-queue)                                         |

### 身份验证方法：Access Key / Secret Key {#authentication-method-access-key-secret-key}

当你更倾向于使用静态凭证时，可使用此方法，例如用于不支持角色假设的兼容 S3 存储。

更多信息，请参见 [Amazon S3 - Credentials](https://docs.pingcap.com/tidbcloudlake/aws-credentials/)。

| 字段 | 必填 | 说明 |
|-------|----------|-------------|
| **Name** | 是 | 此数据源的描述性名称 |
| **Storage Provider** | 是 | 选择 **Amazon S3** |
| **Authentication Method** | 是 | 选择 **Access Key / Secret Key** |
| **S3 Access Key** | 是 | 具有对 staging 存储桶访问权限的 Access key ID |
| **S3 Secret Key** | 是 | 与 access key ID 配对的 Secret access key |
| **S3 Bucket Name** | 是 | TiCDC / Dumpling 暂存数据、供 TiDB Cloud Lake 加载的存储桶 |
| **S3 Region** | 是 | 存储桶所在的 AWS Region |
| **S3 Endpoint** | 否 | 仅用于兼容 S3 的存储。对于 Amazon S3 请留空 |
| **SQS Queue URL** | 否 | 用于事件驱动模式的可选标准 SQS 队列 URL |

## Alibaba Cloud OSS {#alibaba-cloud-oss}

当存储提供商为 **Alibaba Cloud OSS** 时，TiDB Cloud Lake 会从 Alibaba Cloud 读取 staging bucket。OSS 仅支持 **Access Key / Secret Key** 身份验证。

| 字段 | 必填 | 说明 |
|-------|----------|-------------|
| **Name** | 是 | 此数据源的描述性名称 |
| **Storage Provider** | 是 | 选择 **Alibaba Cloud OSS** |
| **OSS Access Key ID** | 是 | OSS AccessKey ID |
| **OSS AccessKey Secret** | 是 | OSS AccessKey Secret |
| **OSS Bucket** | 是 | TiCDC / Dumpling 暂存数据的 OSS 存储桶 |
| **OSS Region** | 只读 | Lake 的部署 Region。该值会自动显示，且无法修改 |

## 可选 SQS 队列 {#optional-sqs-queue}

**SQS Queue URL** 字段是可选的，并且仅适用于 Amazon S3。当你提供一个接收 staging bucket 的 S3 `ObjectCreated` 事件的标准 SQS 队列时，TiDB Cloud Lake 可以从该队列中发现新写入的 changefeed / export 对象，而不必等待下一次轮询。

- 该队列必须是 **standard** 队列。不支持 FIFO 队列，因为 S3 事件通知无法投递到这类队列。
- S3 bucket 和 SQS 队列应位于同一个 Region。
- 轮询 bucket 仍然是权威的发现路径，SQS 只是用于优化延时，而不是替代方案。
- 如果将此字段留空，任务将通过轮询来发现对象。

有关队列、bucket 通知和信任策略设置，请参见 [Amazon SQS (S3) - IAM Role (Preview)](/tidb-cloud-lake/guides/amazon-sqs-s3-iam-role.md)。

## 后续步骤 {#next-steps}

创建此数据源后，你可以使用它来创建 [TiDB 集成任务（预览版）](/tidb-cloud-lake/guides/integrate-with-tidb.md)。