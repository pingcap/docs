---
title: Amazon SQS (S3) - IAM Role (Beta)
summary: 了解如何在 {{{ .lake }}} 中创建 `Amazon SQS (S3) - IAM Role` 数据源。
---

# Amazon SQS (S3) - IAM Role (Beta)

本页介绍如何创建 `Amazon SQS (S3) - IAM Role` 数据源。该数据源存储访问 Amazon SQS 队列及其对应 S3 存储桶所需的配置，用于消费从 Amazon S3 投递到 SQS 的 S3 对象创建事件。

`Amazon SQS (S3) - IAM Role` 仅存储 SQS (S3) 导入所需的连接和授权信息。它本身不会消费消息。实际读取 SQS 消息、解析 S3 ObjectCreated 事件并将数据写入 {{{ .lake }}} 的过程，由 [Amazon SQS (S3) 集成任务](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) 执行。

## 使用场景 {#use-cases}

- 集中管理 SQS (S3) 导入所需的队列 URL、Region、IAM Role 和路径作用域
- 消费 S3 `ObjectCreated` 事件，并将对应的对象数据写入 {{{ .lake }}}
- 使用 S3 事件通知驱动数据导入，而不是仅依赖轮询 S3 路径
- 当被多个任务引用时，在一个位置统一修改 IAM Role、队列 URL 或路径作用域

## 创建 Amazon SQS (S3) - IAM Role {#create-amazon-sqs-s3-iam-role}

1. 导航到 **Data** > **Data Sources**，然后点击 **Create Data Source**。
2. 选择 **Amazon SQS (S3) - IAM Role** 作为服务类型，然后填写连接详情：

    | Field | Required | Description |
    |-------|----------|-------------|
    | **Name** | Yes | 数据源的描述性名称 |
    | **Queue URL** | Yes | SQS 标准队列 URL，例如 `https://sqs.us-east-1.amazonaws.com/123456789012/my-queue` |
    | **Queue Region** | Yes | SQS 队列所在的 AWS Region，例如 `us-east-1`。S3 存储桶必须与 SQS 队列位于同一 Region |
    | **Role ARN** | Yes | 你的 AWS 账户中允许 {{{ .lake }}} 扮演的 IAM Role ARN |
    | **External ID** | Yes | 来自 {{{ .lake }}} 控制台的组织 ID，用于 IAM Role 信任策略 |
    | **Bucket** | Yes | 发送 ObjectCreated 事件的 S3 存储桶名称 |
    | **Object Key Prefix** | No | S3 对象键的前缀过滤器。它应与 S3 通知过滤器匹配 |
    | **Object Key Suffix** | No | S3 对象键的后缀过滤器。它应与 S3 通知过滤器匹配 |

3. 点击 **Test Connectivity** 验证连接。如果测试成功，点击 **OK** 保存数据源。

    > **Note:**
    >
    > SQS (S3) 导入使用 AssumeRole 模型。你无需向 {{{ .lake }}} 提供 AWS Access Key 或 Secret Key。相反，你需要在自己的 AWS 账户中创建一个 IAM Role，并在该角色的信任策略中允许 {{{ .lake }}} 平台角色通过 `sts:AssumeRole` 获取临时凭证。

## AWS 侧配置概览 {#aws-side-configuration-overview}

在创建数据源之前，请先在你的 AWS 账户中完成以下配置：

1. 创建或准备一个 SQS 标准队列。
2. 配置 SQS 队列策略，允许指定的 S3 存储桶向该队列发送消息。
3. 配置 S3 存储桶通知，将 `ObjectCreated` 事件发送到 SQS 队列。
4. 创建一个 IAM Role，允许 {{{ .lake }}} 平台角色通过 `sts:AssumeRole` 访问该角色。
5. 为该 IAM Role 附加 S3 读权限和 SQS 消费权限。
6. 上传一个测试对象，并确认 S3 能够将事件投递到 SQS。

请先准备以下变量。`AWS_REGION` 必须是 S3 存储桶和 SQS 队列所在的 Region。`EXTERNAL_ID` 是来自 {{{ .lake }}} 平台控制台的组织 ID。

```bash
export AWS_REGION="<bucket-and-sqs-region>"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

export BUCKET_NAME="<your-bucket-name>"
export BUCKET_ARN="arn:aws:s3:::$BUCKET_NAME"

export QUEUE_NAME="<your-sqs-standard-queue-name>"
export ROLE_NAME="platform-s3-sqs-consumer-role"

export PREFIX="<object-key-prefix>"
export SUFFIX="<object-key-suffix>"

export PLATFORM_SETUP_ROLE_ARN="<platform-setup-role-arn>"
export PLATFORM_LOAD_ROLE_ARN="<platform-load-role-arn>"
export EXTERNAL_ID="<platform-org-id>"
```

> **Tip:**
>
> 使用 Platform 提供的角色 ARN：`PLATFORM_SETUP_ROLE_ARN` 是 **Platform setup and validation role** 的 ARN，`PLATFORM_LOAD_ROLE_ARN` 是 **Platform data loading role** 的 ARN。在大多数情况下，你的 IAM Role 信任策略应同时信任这两个平台角色。

## 第 1 步：创建或获取 SQS 标准队列 {#step-1-create-or-get-an-sqs-standard-queue}

创建一个 SQS 标准队列：

```bash
aws sqs create-queue \
  --region "$AWS_REGION" \
  --queue-name "$QUEUE_NAME"
```

获取后续步骤所需的队列 URL 和队列 ARN：

```bash
export QUEUE_URL=$(
  aws sqs get-queue-url \
    --region "$AWS_REGION" \
    --queue-name "$QUEUE_NAME" \
    --query 'QueueUrl' \
    --output text
)

export QUEUE_ARN=$(
  aws sqs get-queue-attributes \
    --region "$AWS_REGION" \
    --queue-url "$QUEUE_URL" \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text
)
```

我们建议为每个 SQS (S3) 数据源使用专用的 SQS 标准队列。不要将同一个队列复用于其他存储桶、其他前缀/后缀作用域或其他业务事件。

## 第 2 步：配置 SQS 队列策略 {#step-2-configure-the-sqs-queue-policy}

在进行修改前，先备份当前的 SQS 属性：

```bash
aws sqs get-queue-attributes \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --attribute-names Policy QueueArn \
  > "sqs-attributes.backup.$(date +%Y%m%d-%H%M%S).json"
```

生成 `queue-policy.json`，仅允许指定的 S3 存储桶发送消息：

```bash
jq -n \
  --arg policyId "$QUEUE_NAME-policy" \
  --arg queueArn "$QUEUE_ARN" \
  --arg bucketArn "$BUCKET_ARN" \
  --arg accountId "$AWS_ACCOUNT_ID" \
  '{
    Version: "2012-10-17",
    Id: $policyId,
    Statement: [
      {
        Sid: "AllowS3ToSendMessage",
        Effect: "Allow",
        Principal: {
          Service: "s3.amazonaws.com"
        },
        Action: "sqs:SendMessage",
        Resource: $queueArn,
        Condition: {
          ArnLike: {
            "aws:SourceArn": $bucketArn
          },
          StringEquals: {
            "aws:SourceAccount": $accountId
          }
        }
      }
    ]
  }' \
  > queue-policy.json
```

应用该策略：

```bash
jq -n \
  --arg policy "$(jq -c . queue-policy.json)" \
  '{Policy: $policy}' \
  > set-queue-attributes.json

aws sqs set-queue-attributes \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --attributes file://set-queue-attributes.json
```

## Step 3: 配置 S3 Bucket Notification {#step-3-configure-s3-bucket-notification}

在进行修改前，先备份当前的 bucket notification。`put-bucket-notification-configuration` 会替换整个 bucket notification 配置。如果该 bucket 已经有其他通知配置，请先将它们合并，再应用新的配置。

```bash
aws s3api get-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME" \
  > "bucket-notification.backup.$(date +%Y%m%d-%H%M%S).json"
```

生成 `bucket-notification.json`：

```bash
jq -n \
  --arg id "$QUEUE_NAME" \
  --arg queueArn "$QUEUE_ARN" \
  --arg prefix "$PREFIX" \
  --arg suffix "$SUFFIX" \
  '{
    QueueConfigurations: [
      (
        {
          Id: $id,
          QueueArn: $queueArn,
          Events: [
            "s3:ObjectCreated:*"
          ]
        }
        +
        (
          [
            if $prefix != "" then {Name: "prefix", Value: $prefix} else empty end,
            if $suffix != "" then {Name: "suffix", Value: $suffix} else empty end
          ] as $rules
          | if ($rules | length) > 0
            then {Filter: {Key: {FilterRules: $rules}}}
            else {}
            end
        )
      )
    ]
  }' \
  > bucket-notification.json
```

应用该配置：

```bash
aws s3api put-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME" \
  --notification-configuration file://bucket-notification.json
```

检查配置：

```bash
aws s3api get-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME"
```

确认 `QueueArn` 指向目标 SQS 队列，`Events` 包含 `s3:ObjectCreated:*`，并且 `FilterRules` 与 {{{ .lake }}} 数据源中配置的 `Object Key Prefix` / `Object Key Suffix` 一致。

## Step 4: 创建供 {{{ .lake }}} Assume 的 IAM Role {#step-4-create-an-iam-role-for-lake-to-assume}

生成 `trust-policy.json`。`ExternalId` 是来自 {{{ .lake }}}（platform）控制台的组织 ID。

```bash
jq -n \
  --arg platformSetupRoleArn "$PLATFORM_SETUP_ROLE_ARN" \
  --arg platformLoadRoleArn "$PLATFORM_LOAD_ROLE_ARN" \
  --arg externalId "$EXTERNAL_ID" \
  '{
    Version: "2012-10-17",
    Statement: [
      {
        Sid: "AllowPlatformSetupAssumeRole",
        Effect: "Allow",
        Principal: {
          AWS: $platformSetupRoleArn
        },
        Action: "sts:AssumeRole",
        Condition: {
          StringEquals: {
            "sts:ExternalId": $externalId
          }
        }
      },
      {
        Sid: "AllowPlatformLoadAssumeRole",
        Effect: "Allow",
        Principal: {
          AWS: $platformLoadRoleArn
        },
        Action: "sts:AssumeRole",
        Condition: {
          StringEquals: {
            "sts:ExternalId": $externalId
          }
        }
      }
    ]
  }' \
  > trust-policy.json
```

创建 IAM Role：

```bash
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file://trust-policy.json
```

如果该 role 已存在，请备份并修改 trust policy：

```bash
aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json \
  > "trust-policy.backup.$(date +%Y%m%d-%H%M%S).json"

aws iam update-assume-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-document file://trust-policy.json
```

## Step 5: 附加 S3/SQS 权限 {#step-5-attach-s3-sqs-permissions}

生成 `permissions-policy.json`：

```bash
jq -n \
  --arg bucketArn "$BUCKET_ARN" \
  --arg objectArn "$BUCKET_ARN/*" \
  --arg queueArn "$QUEUE_ARN" \
  '{
    Version: "2012-10-17",
    Statement: [
      {
        Sid: "S3BucketMetadataAccess",
        Effect: "Allow",
        Action: [
          "s3:GetBucketLocation",
          "s3:ListBucket"
        ],
        Resource: $bucketArn
      },
      {
        Sid: "S3ObjectReadAccess",
        Effect: "Allow",
        Action: [
          "s3:GetObject"
        ],
        Resource: $objectArn
      },
      {
        Sid: "SQSConsumeAccess",
        Effect: "Allow",
        Action: [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:ChangeMessageVisibility"
        ],
        Resource: $queueArn
      }
    ]
  }' \
  > permissions-policy.json
```

应用权限：

```bash
aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name platform-s3-sqs-access \
  --policy-document file://permissions-policy.json
```

权限检查清单：

- SQS 权限的作用域限定为目标队列 ARN。
- S3 权限的作用域限定为目标 bucket 和对象 ARN。
- 默认情况下，此策略不需要 S3 写入或删除权限。
- 如果未来的 SQS（S3）集成任务启用了 **PURGE** 或 **Clean Up Original Files**，即在成功导入后删除源对象，则需要对目标对象路径授予 `s3:DeleteObject` 权限。

## 第 6 步：验证 S3 到 SQS {#step-6-verify-s3-to-sqs}

上传一个与 `PREFIX` / `SUFFIX` 匹配的测试对象：

```bash
echo 'a,b' > /tmp/sqs-s3-local-test.csv

aws s3 cp /tmp/sqs-s3-local-test.csv \
  "s3://$BUCKET_NAME/${PREFIX}sqs-s3-local-test-$(date +%s)$SUFFIX" \
  --region "$AWS_REGION"
```

从 SQS 接收一条消息：

```bash
aws sqs receive-message \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --max-number-of-messages 1 \
  --wait-time-seconds 10 \
  --visibility-timeout 60
```

确认消息中包含 `Records`，`eventSource` 为 `aws:s3`，`eventName` 为 `ObjectCreated:*`，并且 `Records[].s3.bucket.name` 和 `Records[].s3.object.key` 与测试对象一致。

> **注意：**
>
> `receive-message` 不会自动删除消息。它只会在可见性超时时间内暂时隐藏该消息。如果你希望 {{{ .lake }}} 稍后消费这条测试消息，请不要手动删除它。在测试数据源连通性之前，请等待可见性超时过期。

## 提供给 {{{ .lake }}} 的信息 {#information-to-provide-to-lake}

完成 AWS 侧配置后，在 {{{ .lake }}} 中创建数据源时填写以下信息：

| 参数 | 说明 |
|-----------|-------------|
| `role_arn` | 你的 AWS 账户中允许 {{{ .lake }}} 扮演的 IAM Role ARN |
| `external_id` | 来自 {{{ .lake }}} 控制台的 Organization ID |
| `queue_url` | SQS 标准队列 URL |
| `queue_region` | SQS 队列所在的 Region |
| `bucket` | S3 存储桶名称 |
| `prefix` / `suffix` | 可选。应与 S3 notification filter 匹配 |

获取 `role_arn` 的命令示例：

```bash
aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query 'Role.Arn' \
  --output text
```

## 配置要求 {#configuration-requirements}

- S3 存储桶和 SQS 队列应位于同一个 AWS Region。
- SQS 队列必须是标准队列。不支持 FIFO 队列。
- SQS 队列应专用于一条 S3 notification rule。不要将其复用于其他存储桶、其他 prefix / suffix 作用域或其他业务事件。
- S3 notification 中的 bucket、prefix 和 suffix 应与 {{{ .lake }}} 数据源配置保持一致。
- `put-bucket-notification-configuration` 会替换整个存储桶 notification 配置。应用更改前，请先备份并合并现有配置。
- S3 event notifications 和 SQS 标准队列都采用至少一次投递，因此消息可能会重复。

## 后续步骤 {#next-steps}

创建此数据源后，你可以使用它来创建 [Amazon SQS (S3) 集成任务](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md)。