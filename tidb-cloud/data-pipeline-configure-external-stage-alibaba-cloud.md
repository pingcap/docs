---
title: 为 TiDB Cloud Data Pipeline 设置外部 stage（Alibaba Cloud）
summary: 了解如何将 Alibaba Cloud OSS 存储桶配置为 TiDB Cloud Data Pipeline 的外部 stage，包括 RAM 用户和访问密钥。
---

# 为 TiDB Cloud Data Pipeline 设置外部 stage（Alibaba Cloud）

本文档介绍如何将 Alibaba Cloud Object Storage Service (OSS) 存储桶准备为 [Data Pipeline](/tidb-cloud/data-pipeline.md) 的外部 stage。外部 stage 是一个中间存储桶，TiDB Cloud 会将导出的快照和行变更写入其中，而 TiDB Cloud Lake 会从中读取数据，并将数据加载到目标计算集群 (Warehouse) 中。

TiDB Cloud 会将增量数据和快照写入你的 OSS 存储桶，TiDB Cloud Lake 会从中读取这些数据。

> **限制：**
>
> - 仅支持 **Access Key** 身份验证。不支持用于 OSS 的 Role ARN。
> - 不支持使用 SQS 的事件驱动摄取。该 Data Pipeline 仅使用轮询。

## 前提条件 {#prerequisites}

- 一个具有管理 OSS 和 RAM 资源权限的 Alibaba Cloud 账户。
- 一个带有 TiDB Cloud Lake 计算集群的 TiDB Cloud 账户。

## 步骤 1：创建 OSS 存储桶 {#step-1-create-an-oss-bucket}

> **提示：**
>
> 如果你已经准备好了 OSS 存储桶，可以跳过此步骤。建议使用与你的 TiDB Cloud 实例相同的 Region，但对于 OSS 来说这并非强制要求。

1. 打开 [OSS Console](https://oss.console.aliyun.com/) 并创建一个新的存储桶。
2. 选择一个 Region。建议使用与你的 TiDB Cloud 实例相同的 Region。
3. 可选：在存储桶内创建一个文件夹（前缀），用于组织 TiDB Cloud 数据（例如，`oss://tidb-cloud-lake-data/my-cluster/`）。
4. 记录以下值，后续步骤中会用到：

    - **Bucket Name：** 例如，`tidb-cloud-lake-data`
    - **OSS URI（带前缀）：** 例如，`oss://tidb-cloud-lake-data/my-cluster/`

## 步骤 2：创建 RAM 用户和 AccessKey 对 {#step-2-create-a-ram-user-and-accesskey-pair}

1. 打开 [RAM Console](https://ram.console.aliyun.com/)，然后进入 **Users > Create user**。
2. 输入显示名称（例如，`tidb-cloud-lake-user`），并选择 **OpenAPI calling** 作为访问方式。
3. 点击 **Next**，然后复制并保存 **AccessKey ID** 和 **AccessKey Secret**。

    > **注意：**
    >
    > AccessKey Secret 仅会在创建时显示一次。请务必立即保存。

4. 返回 **Users** 页面，点击刚刚创建的用户名称，进入 **Permissions** 选项卡，然后点击 **Add permissions**。
5. 选择 **Custom policy**，点击 **Create policy**，然后选择 **Script** 选项卡，使用以下 JSON 创建策略：

    ```json
    {
      "Version": "1",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "oss:HeadBucket",
            "oss:ListObjects",
            "oss:GetObject",
            "oss:PutObject",
            "oss:DeleteObject",
            "oss:GetBucketLocation"
          ],
          "Resource": [
            "acs:oss:*:*:YOUR_BUCKET_NAME",
            "acs:oss:*:*:YOUR_BUCKET_NAME/*"
          ]
        }
      ]
    }
    ```

    > **注意：** 将 `YOUR_BUCKET_NAME` 替换为你的 OSS 存储桶名称。

6. 输入策略名称（例如，`tidb-cloud-lake-access`），然后点击 **OK**。
7. 将该策略附加到 RAM 用户。
8. 记录以下值，配置 TiDB Cloud 时会用到：
    - **Access Key ID：** 例如，`LTAI5t...`
    - **Access Key Secret：** 创建时保存的值

## 下一步是什么？ {#what-s-next}

完成 Alibaba Cloud 设置后，你已经拥有 External Stage 配置所需的全部值：

- **OSS URI**：来自步骤 1。
- **Access Key ID** 和 **Access Key Secret**：来自步骤 2。

在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你的 TiDB Cloud 实例的 Data Pipeline 配置页面，并在 **External Stage** 设置中填写这些值，以完成 Data Pipeline 设置。