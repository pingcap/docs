---
title: 为 TiDB Cloud Data Pipeline 设置外部 stage（AWS）
summary: 了解如何将 Amazon S3 存储桶配置为 TiDB Cloud Data Pipeline 的外部 stage，包括存储桶访问和 SQS 摄取。
---

# 为 TiDB Cloud Data Pipeline 设置外部 stage（AWS）

本指南介绍如何将 Amazon S3 存储桶准备为 [数据管道](/tidb-cloud/data-pipeline.md) 的外部 stage。外部 stage 是一个中间存储桶，TiDB Cloud 会将导出的快照和行变更写入其中，而 TiDB Cloud Lake 会从中读取数据，并将数据加载到目标计算集群 (Warehouse) 中。

TiDB Cloud 会将数据写入你的 S3 存储桶，TiDB Cloud Lake 会从中读取数据。

## 前提条件 {#prerequisites}

- 一个具有管理 IAM、S3 以及可选的 SQS 资源权限的 AWS 账户。
- 一个带有 TiDB Cloud Lake 计算集群的 TiDB Cloud 账户。
- 一个与 TiDB Cloud 实例位于同一区域的 S3 存储桶。如果你还没有，可以在[创建 S3 存储桶](#step-1-create-an-s3-bucket)中创建。

## 步骤 1. 创建 S3 存储桶 {#step-1-create-an-s3-bucket}

> **提示：**
>
> 如果你已经准备好了 S3 存储桶，可以跳过此步骤，只需确保存储桶所在区域与 TiDB Cloud 实例所在区域一致。

1. 打开 [AWS S3 Console](https://console.aws.amazon.com/s3/) 并创建一个新的存储桶。
2. 选择一个区域，并确保该区域与 TiDB Cloud 实例所在区域一致。
3. （可选）在存储桶内创建一个文件夹（前缀）来组织 TiDB Cloud 数据（例如，`s3://tidb-cloud-lake-data/my-cluster/`）。

## 步骤 2. 配置存储桶访问 {#step-2-configure-bucket-access}

为存储桶访问选择以下选项之一，然后完成对应章节中的步骤：

* **选项 1：使用 role ARN 访问存储桶（CloudFormation）**（推荐）
* **选项 2：使用 role ARN 访问存储桶（手动设置）**
* **选项 3：使用 access key 访问存储桶（不推荐）**

> **提示：**
>
> **开始之前，请先决定是否启用事件驱动摄取。**
>
> 默认情况下，在创建 data pipeline 后，TiDB Cloud Lake 会定期扫描存储桶中的新数据。如果你需要更低的数据延时，可以选择通过 SQS 队列启用事件驱动摄取。当新数据写入存储桶时，S3 事件通知会发送到 SQS 队列，从而使 TiDB Cloud Lake 无需等待下一次计划扫描即可检测并加载新数据。changefeed 仍会按照其配置的频率将数据刷新到存储桶。由于事件驱动摄取可能会使 TiDB Cloud Lake 更频繁地加载数据，因此可能会增加 TiDB Cloud Lake 服务托管成本。
>
> - 对于**选项 1**，如果你选择启用事件驱动摄取，可以在创建堆栈时让 CloudFormation 堆栈创建 SQS 队列，或者稍后手动添加 SQS 队列。
> - 对于**选项 2 和 3**，如果你选择启用事件驱动摄取，则需要手动创建并配置 SQS 队列。

### 选项 1. 使用 role ARN 访问存储桶（CloudFormation） {#option-1-bucket-access-with-role-arn-cloudformation}

TiDB Cloud（向存储桶写入数据）和 TiDB Cloud Lake（从存储桶读取数据）共用一个 IAM role。该 role 的信任策略允许双方都可以 assume 该 role，并且每一方都由各自的 external ID 进行保护，因此无需存储长期凭证。这是推荐选项，因为 CloudFormation 堆栈可以一次性创建 role、其信任关系、其权限，以及可选的 SQS 队列和对应策略。

#### 1.1 使用 CloudFormation 创建 role {#11-create-the-role-with-cloudformation}

1. 在 TiDB Cloud 控制台中，打开 **Create Data Pipeline** 页面，前往 **External Stage** 区域，并输入你的 **Bucket URI**。
2. 在 **Bucket Access** 下，选择 **AWS Role ARN**，然后点击字段下方的 CloudFormation 链接以打开对话框。
3. 点击 **AWS Console with CloudFormation Template**。浏览器会新打开一个标签页，并进入 AWS CloudFormation 控制台，且所有参数都已预填。
4. 在新标签页中，输入一个**堆栈名称**，如果你需要事件驱动摄取，还可以选择输入一个 **SQS queue name**。CloudFormation 会自动创建该队列及其通知策略。若要跳过，请将 SQS 字段留空。
5. 创建堆栈，并等待状态变为 `CREATE_COMPLETE`。
6. 在堆栈的 **Outputs** 页签中，记录你在 TiDB Cloud 控制台配置 External Stage 时所需的值：

    - **Role ARN**：`RoleARN` 的值。
    - **SQS queue URL**（仅当你启用了 SQS 时）：格式为 `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>` 的队列 URL。

#### 1.2 （可选）配置 S3 存储桶通知 {#12-optional-configure-the-s3-bucket-notification}

如果你在 [1.1](#11-create-the-role-with-cloudformation) 中启用了 SQS，则队列及其策略已经由堆栈创建完成。剩下唯一需要做的就是为你的存储桶配置通知。由于该存储桶已存在，提供的 CloudFormation 堆栈不会配置这一步。请按照 [2.3.2](#232-configure-the-s3-bucket-notification) 中的手动通知步骤进行操作。

### 选项 2. 使用 role ARN 访问存储桶（手动设置） {#option-2-bucket-access-with-role-arn-manual-setup}

如果你无法使用 CloudFormation，或者你的组织要求所有 IAM 资源都必须手动创建并审核，请使用此选项。IAM role 本身与选项 1 相同；不同之处仅在于创建方式。

#### 2.1 收集所需的值 {#21-collect-the-required-values}

1. 在 TiDB Cloud 控制台中，打开 **Create Data Pipeline** 页面，前往 **External Stage** 区域，并输入你的 **Bucket URI**。
2. 在 **Bucket Access** 下，选择 **AWS Role ARN**，然后点击字段下方的 CloudFormation 链接以打开对话框。
3. 从对话框中的 **Having trouble?** 区域复制以下值。你在 [2.2](#22-create-the-role-and-attach-the-policies) 的信任策略中需要用到所有这些值：

    - TiDB Cloud account ID
    - TiDB Cloud external ID
    - Lake external ID
    - Lake platform setup & validation role ARN
    - Lake platform data loading role ARN

#### 2.2 创建 role 并附加策略 {#22-create-the-role-and-attach-the-policies}

1. 打开 [IAM Console](https://console.aws.amazon.com/iam/)，前往 **Roles > Create role**。
2. 在 **Trusted entity type** 下，选择 **Custom trust policy**，并将以下内容粘贴到策略文档中。将占位符值替换为你收集到的实际值：

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowTiDBCloudAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<TiDB Cloud account ID>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<TiDB Cloud external ID>" } }
        },
        {
          "Sid": "AllowLakeSetupAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<Lake platform setup & validation role ARN>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<Lake external ID>" } }
        },
        {
          "Sid": "AllowLakeLoadAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<Lake platform data loading role ARN>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<Lake external ID>" } }
        }
      ]
    }
    ```

3. 输入一个 role 名称（例如，`tidb-cloud-lake-role`），然后点击 **Create role**。
4. 打开你刚创建的 role，前往 **Permissions** 页签，然后点击 **Add permissions > Create inline policy**。
5. 选择 **JSON** 页签，并粘贴以下内容。将 `YOUR_BUCKET_NAME` 和 `your-prefix` 替换为你的实际值；如果你不需要事件驱动摄取，请删除 `SQSConsumeAccess` 语句：

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketMetadata",
          "Effect": "Allow",
          "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
          "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
        },
        {
          "Sid": "S3ObjectReadWrite",
          "Effect": "Allow",
          "Action": ["s3:GetObject", "s3:PutObject"],
          "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/your-prefix/*"
        },
        {
          "Sid": "SQSConsumeAccess",
          "Effect": "Allow",
          "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes", "sqs:ChangeMessageVisibility"],
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME"
        }
      ]
    }
    ```

6. 输入一个策略名称（例如，`tidb-cloud-lake-access`），然后点击 **Create policy**。
7. 从 role 详情页复制 role ARN。你在 TiDB Cloud 控制台配置 External Stage 时需要用到它，例如 `arn:aws:iam::123456789012:role/tidb-cloud-lake-role`。

#### 2.3 （可选）使用 SQS 启用事件驱动摄取 {#23-optional-enable-event-driven-ingestion-with-sqs}

如果定期扫描已能满足你的工作负载需求，请跳过本节。有关何时使用 SQS 的详细信息，请参见[步骤 2. 配置存储桶访问](#step-2-configure-bucket-access)中的提示。

##### 2.3.1 创建 SQS 队列并配置队列策略 {#231-create-the-sqs-queue-and-configure-the-queue-policy}

1. 打开 [SQS Console](https://console.aws.amazon.com/sqs/)，点击 **Create queue**，选择 **Standard** 类型，并输入一个名称（例如，`tidb-cloud-lake-sqs`）。点击 **Create queue**。
2. 打开该队列，前往 **Access policy** 页签，并将策略替换为以下内容。这将允许 S3 向该队列发送通知：

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowS3ToSendMessage",
          "Effect": "Allow",
          "Principal": { "Service": "s3.amazonaws.com" },
          "Action": "sqs:SendMessage",
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME",
          "Condition": {
            "ArnLike": { "aws:SourceArn": "arn:aws:s3:::YOUR_BUCKET_NAME" },
            "StringEquals": { "aws:SourceAccount": "ACCOUNT_ID" }
          }
        }
      ]
    }
    ```

    > **注意：** 将 `REGION`、`ACCOUNT_ID`、`YOUR_QUEUE_NAME` 和 `YOUR_BUCKET_NAME` 替换为你的实际值。

3. 确保 [2.2](#22-create-the-role-and-attach-the-policies) 中的 `SQSConsumeAccess` 语句已包含在 role 的权限策略中。
4. 从 SQS 控制台中的队列详情页记录队列 URL。你在 TiDB Cloud 控制台配置 External Stage 时需要用到它，格式为 `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>`。

##### 2.3.2 配置 S3 存储桶通知 {#232-configure-the-s3-bucket-notification}

配置一个 S3 事件通知，将存储桶中的对象创建事件发送到 SQS 队列：

1. 打开 [AWS S3 Console](https://console.aws.amazon.com/s3/) 并进入你的存储桶。
2. 前往 **Properties > Event notifications > Create event notification**。
3. 配置：
    - **Event types:** 选择 **All object create events**。
    - **Destination:** 选择 **SQS queue**，并选择之前创建的队列。
4. 点击 **Save changes**。

### 选项 3. 使用 access key 访问存储桶（不推荐） {#option-3-bucket-access-with-access-key-not-recommended}

> **注意：**
>
> 使用 Access Key/Secret Key (AK/SK) 意味着你需要手动管理和轮转凭证，并且意外泄露的风险更高。为了更简化的管理和更好的安全性，建议按照[选项 1](#option-1-bucket-access-with-role-arn-cloudformation)或[选项 2](#option-2-bucket-access-with-role-arn-manual-setup)中的步骤创建 Role ARN。

使用此选项时，你需要创建一个 IAM user，并将其 **Access Key ID** 和 **Secret Access Key** 提供给 TiDB Cloud。TiDB Cloud 会使用这些凭证直接访问你的 S3 存储桶。

#### 3.1 创建 IAM 用户和访问密钥 {#31-create-an-iam-user-and-access-key}

1. 打开 [IAM Console](https://console.aws.amazon.com/iam/)，进入 **Users > Create user**。
2. 输入用户名（例如，`tidb-cloud-lake-user`），然后点击 **Next**。
3. 在 **Set permissions** 页面，创建或附加一个策略，为其授予所需的 S3 权限以及可选的 SQS 权限。将 `YOUR_BUCKET_NAME` 和 `your-prefix` 替换为你的实际值；如果不需要事件驱动摄取，请删除 `SQSConsumerAccess` 语句：

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketAccess",
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:ListBucket",
            "s3:GetBucketLocation"
          ],
          "Resource": [
            "arn:aws:s3:::YOUR_BUCKET_NAME",
            "arn:aws:s3:::YOUR_BUCKET_NAME/your-prefix/*"
          ]
        },
        {
          "Sid": "SQSConsumerAccess",
          "Effect": "Allow",
          "Action": [
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes",
            "sqs:ChangeMessageVisibility"
          ],
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME"
        }
      ]
    }
    ```

4. 点击 **Next**。在 **Review and create** 页面，检查用户设置，然后点击 **Create user**。
5. 在 **Users** 页面，点击刚创建的用户名，然后进入 **Security credentials** 标签页。
6. 在 **Access keys** 部分，点击 **Create access key**。在 **Access key best practices & alternatives** 页面，选择 **Other**，点击 **Next**，然后创建访问密钥。
7. 保存 **Access Key ID** 和 **Secret Access Key**。在 TiDB Cloud 控制台中配置 External Stage 时需要用到它们。

    > **注意：**
    >
    > **Secret Access Key** 只会在创建时显示一次。请务必立即保存。

#### 3.2 （可选）使用 SQS 启用事件驱动摄取 {#32-optional-enable-event-driven-ingestion-with-sqs}

如果你的工作负载可以接受周期性扫描，请跳过本节。

1. 打开 [SQS Console](https://console.aws.amazon.com/sqs/)，点击 **Create queue**，选择 **Standard** 类型，并输入名称（例如，`tidb-cloud-lake-sqs`）。点击 **Create queue**。
2. 打开该队列，进入 **Access policy** 标签页，并将策略替换为以下内容，以便 S3 可以向该队列发送通知。将占位符替换为你的实际值：

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowS3ToSendMessage",
          "Effect": "Allow",
          "Principal": { "Service": "s3.amazonaws.com" },
          "Action": "sqs:SendMessage",
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME",
          "Condition": {
            "ArnLike": { "aws:SourceArn": "arn:aws:s3:::YOUR_BUCKET_NAME" },
            "StringEquals": { "aws:SourceAccount": "ACCOUNT_ID" }
          }
        }
      ]
    }
    ```

3. 在你的存储桶上配置通知：

    1. 打开 [AWS S3 Console](https://console.aws.amazon.com/s3/)，并导航到你的存储桶。
    2. 进入 **Properties > Event notifications > Create event notification**。
    3. 配置以下项：
        - **Event types:** 选择 **All object create events**。
        - **Destination:** 选择 **SQS queue**，并选择之前创建的队列。
    4. 点击 **Save changes**。

4. 在 SQS Console 的队列详情页中记录队列 URL。在 TiDB Cloud 控制台中配置 External Stage 时需要用到它，格式为 `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>`。

## 接下来做什么？ {#what-s-next}

完成 AWS 设置后，你已经具备了配置 External Stage 所需的所有值：

- **S3 URI**：来自 **Create an S3 bucket**。
- **Bucket access**：Role ARN（选项 1 和 2），或 Access Key ID 和 Secret Access Key（选项 3）。
- **SQS queue URL**（可选）。

在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你的 TiDB Cloud 实例的 Data Pipeline 配置页面，并在 **External Stage** 设置中填写这些值，以完成数据管道设置。