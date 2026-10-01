---
title: Sink to TiDB Cloud Lake
summary: 在 TiDB Cloud Essential 实例上使用 export、changefeed 和 TiDB Cloud Lake 集成构建 TiDB Cloud Lake Data Pipeline 的手动设置指南。
---

# Sink to TiDB Cloud Lake

本指南将带你完成从 TiDB Cloud Essential 实例到 TiDB Cloud Lake 的端到端 Data Pipeline 设置：将完整快照导出到 Amazon S3，创建一个 [Changefeed](/tidb-cloud/changefeed-overview.md) 持续将增量地变化写入同一个 S3 位置，并配置 TiDB Cloud Lake 同时加载快照和增量数据。

## 限制 {#restrictions}

- TiDB Cloud Lake 的计算集群 (Warehouse) 必须与您的 Essential 实例位于**同一 region**。
- 只有带有**主键**的表才能进行增量复制。
- 该管道需要手动设置和维护 AWS IAM 资源与凭证、changefeed 以及 TiDB Cloud Lake 集成。
- 关于 DDL、DML 和列类型支持的详细信息，请参见 [TiDB Cloud Lake 的 Data Pipeline SQL 兼容性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md)。

## 前提条件 {#prerequisites}

开始之前，请确保您具备以下条件：

- 一个已部署在特定 region 的 TiDB Cloud Essential 实例。
- 对该组织的 TiDB Cloud API 的访问权限。您可以在 [TiDB Cloud console](https://tidbcloud.com/) 的 [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) 页面创建 API key。请务必保存 **Public Key** 和 **Private Key**，因为本指南中的所有 API 调用都需要它们。
- 一个与 TiDB Cloud Essential 实例位于同一 region 的 Amazon S3 存储桶（例如，`s3://my-datapipeline-bucket`）。
- 一个与 TiDB Cloud Essential 实例位于同一 region 的 TiDB Cloud Lake 计算集群。

> **Note:**
>
> 本指南假设源 TiDB 数据库中已经存在您希望复制的数据。如果您需要示例数据，请先准备好再继续。

## 步骤 1：准备 S3 存储桶访问 {#step-1-prepare-s3-bucket-access}

Data Pipeline 组件（export、changefeed 和 TiDB Cloud Lake）都需要访问同一个 S3 存储桶。请选择以下任一方法来访问 S3 存储桶：

- **Role ARN**（适用于托管在 AWS 上的 TiDB Cloud Essential 实例）：三个组件共用一个 IAM role。此方法可避免长期凭证，并提供更强的安全性。
- **Access Key**：设置更简单，并且在 Role ARN 不可用时必须使用；但需要手动管理和轮换凭证。

### 方法 1：使用 Role ARN {#method-1-use-a-role-arn}

在此方法中，您首先使用 TiDB Cloud console 中 Export 功能提供的 CloudFormation 堆栈创建一个为 Export 配置的 IAM role。然后，您需要扩展该 role 的信任策略和权限，使 changefeed 和 TiDB Cloud Lake 也能使用它访问 S3 存储桶。

#### 1. 使用 Export CloudFormation 创建 role {#1-create-the-role-with-export-cloudformation}

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入您的 TiDB Cloud Essential 实例的概览页面。
2. 在左侧导航栏中点击 **Data > Import**，然后点击右上角的 **Export Data to**。
3. 选择 **Amazon S3**。当使用 **Role ARN** 身份验证配置 S3 目标时，TiDB Cloud 会提供一个 CloudFormation 链接。使用该链接创建 IAM role。

堆栈创建完成后，记录堆栈 **Outputs** 中的 **Role ARN**（例如，`arn:aws:iam::<account-id>:role/<role-name>`）。

#### 2. 合并信任关系 {#2-consolidate-trust-relationships}

上一步创建的 IAM role 最初仅配置为将数据从 TiDB Cloud Essential 导出到 S3。由于 changefeed 和 TiDB Cloud Lake 也会使用同一个 role 访问 S3 存储桶，因此需要修改其信任策略，以允许这些组件也能 assume 该 role。

收集以下用于附加信任关系的值，然后修改该 role 的信任策略。在 AWS Console 中，进入在 [1. 使用 Export CloudFormation 创建 role](#1-create-the-role-with-export-cloudformation) 中创建的 role，打开 **Trust relationships** 标签页，然后点击 **Edit trust policy**。

- **Export**：在替换信任策略之前，记录现有 Export 的 AWS account ID 和 external ID，以便在合并后的策略中保留该信任关系。
- **Changefeed**：调用 TiDB Cloud API 获取所需的值：

    ```shell
    curl -L -X GET 'https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}/changefeeds:getCloudStorageAuthConfig' \
      -u '<Public Key>:<Private Key>' --digest
    ```

    从响应中记录 `tidbCloudAccountId` 和 `tidbCloudAccountExternalId`。

- **TiDB Cloud Lake**：在 [TiDB Cloud Lake console](https://lake.tidbcloud.com/) 中，进入 **Data > Data Sources > Create**。在 **Basic Info** 部分，选择 **Service: TiDB**，然后在 **Trust Cloud Platform roles** 下记录以下值：
    - Lake Setup & Validation Role ARN
    - Lake Data Loading Role ARN
    - Lake External ID

使用下面的合并策略**替换**该 role 的信任策略：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowExportAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<Export_TiDB_Cloud_Account_ID>:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Export_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowChangefeedAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<Changefeed_TiDB_Cloud_Account_ID>:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Changefeed_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowLakeSetupAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<Lake_Setup_and_Validation_Role_ARN>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Lake_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowLakeLoadAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<Lake_Data_Loading_Role_ARN>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Lake_External_ID>"
        }
      }
    }
  ]
}
```

#### 3. 扩展权限以覆盖整个管道前缀 {#3-expand-permissions-to-cover-the-full-pipeline-prefix}

通过 CloudFormation 创建的权限策略仅限于快照导出路径。changefeed 会写入 `{prefix}/incremental/`，而 TiDB Cloud Lake 会从 `{prefix}/snapshot/` 和 `{prefix}/incremental/` 读取数据，因此该策略必须覆盖父级前缀。

在 AWS Console 中，进入步骤 1 中创建的 role，在 **Permissions** 标签页下点击策略名称，然后修改该策略以替换资源作用域。

使用以下内容**替换**该 role 的内联权限策略：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>"
    },
    {
      "Sid": "S3ObjectAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:GetObjectVersion",
        "s3:DeleteObjectVersion"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>/<your-prefix>/*"
    }
  ]
}
```

> **Note:**
>
> 通过 CloudFormation 创建的策略使用了更窄的资源范围，例如 `arn:aws:s3:::bucket/prefix/snapshot/*`。您必须将其修改为 `arn:aws:s3:::bucket/prefix/*`，这样 changefeed（写入 `prefix/incremental/`）和 TiDB Cloud Lake（从两个子路径读取）才能拥有足够的访问权限。

### 方法 2：使用 Access Key {#method-2-use-an-access-key}

> **注意：**
>
> 使用 Access Key 和 Secret Key（AK/SK）需要手动管理和轮换凭证，这会增加安全风险。为了获得更强的安全性，建议改用 **Role ARN**。

如果你更倾向于使用 Access Key 认证，请创建一个具有以下权限的 IAM 用户，并在配置 Export、changefeed 和 TiDB Cloud Lake 时提供其凭证。

**权限策略：**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>"
    },
    {
      "Sid": "S3ObjectAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:GetObjectVersion",
        "s3:DeleteObjectVersion"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>/<your-prefix>/*"
    }
  ]
}
```

记录 **Access Key ID** 和 **Secret Access Key**，供后续步骤使用。

## 步骤 2. 将完整快照导出到 Amazon S3 {#step-2-export-full-snapshot-to-amazon-s3}

在 TiDB Cloud 控制台中，进入 **Data > Import**，点击右上角的 **Export Data to**，然后选择 **Amazon S3** 以创建新的导出任务。

**配置如下：**

- **Selected Data**：选择要导出的数据库和表。
- **Data Format**：`CSV`
    - 点击 **Edit CSV Configuration** 并设置：
        - **Dialect**：`Snowflake`
        - **Escape backslash**：`false`
- **Compression**：`None`
- **Amazon S3 Settings**：
    - **Bucket URI**：`s3://<bucket>/<prefix>/snapshot/`（使用推荐的 snapshot 子路径）
    - **Role ARN** 或 **Access Key**：使用[准备存储桶访问](#step-1-prepare-s3-bucket-access)中的凭证。

导出任务完成后，打开任务详情并记录 **Snapshot TSO** 的值。创建 changefeed 时需要用到这个 TSO。

## 步骤 3. 为增量数据创建 changefeed {#step-3-create-a-changefeed-for-incremental-data}

目前，TiDB Cloud Essential 不支持通过 TiDB Cloud 控制台创建 cloud-storage sink，因此你需要使用 TiDB Cloud API。

调用 changefeed 创建 API 时，需要包含以下必填字段：

| 字段 | 必填值 |
|-------|---------------|
| `sink.cloudStorage.dataFormat.protocol` | `CANAL_JSON` |
| `sink.cloudStorage.dataFormat.canalJsonConfig.enableTidbExtension` | `true` |
| `sink.cloudStorage.dataFormat.contentCompatible` | `true` |
| `startPosition.mode` | `FROM_TSO` |
| `startPosition.tso` | `<snapshot_tso from the export step>` |

**请求示例：**

```shell
curl -L -X POST 'https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}/changefeeds' \
  -H 'Content-Type: application/json' \
  -u '<Public Key>:<Private Key>' --digest \
  -d '{
    "displayName": "<changefeed-name>",
    "sink": {
      "type": "CLOUD_STORAGE",
      "cloudStorage": {
        "storage": {
          "type": "S3",
          "s3": {
            "uri": "s3://<bucket>/<prefix>/incremental/",
            "authType": "ROLE_ARN",
            "roleArn": "<role-arn>"
          }
        },
        "dataFormat": {
          "protocol": "CANAL_JSON",
          "contentCompatible": true,
          "canalJsonConfig": {
            "enableTidbExtension": true
          }
        }
      }
    },
    "filter": {
      "mode": "IGNORE_NOT_SUPPORT_TABLE",
      "filterRule": ["*.*"]
    },
    "startPosition": {
      "mode": "FROM_TSO",
      "tso": "<snapshot_tso>"
    },
    "rcu": 2
  }'
```

> **注意：**
>
> changefeed 的 URI 必须使用与导出快照相同前缀下的 `incremental/` 子路径。IAM 角色的权限（来自[3. 扩展权限以覆盖整个管道前缀](#3-expand-permissions-to-cover-the-full-pipeline-prefix)）必须覆盖该路径。
>
> 如果你使用的是 **Access Key** 而不是 Role ARN，请将请求体中的 `s3` 代码块替换为：
>
> ```json
> "s3": {
>   "uri": "s3://<bucket>/<prefix>/incremental/",
>   "authType": "ACCESS_KEY",
>   "accessKey": {
>     "id": "<access-key-id>",
>     "secret": "<access-key-secret>"
>   }
> }
> ```
>

## 步骤 4. 配置 TiDB Cloud Lake {#step-4-configure-tidb-cloud-lake}

在 TiDB Cloud Lake 中，你需要创建一个数据源和一个集成，以便从 S3 存储桶加载数据。

### 1. 创建数据源 {#1-create-a-data-source}

1. 在 [TiDB Cloud Lake 控制台](https://lake.tidbcloud.com/) 中，进入 **Data > Data Sources > Create**。
2. 选择 **Service: TiDB**。
3. 选择 **Role ARN** 或 **Access Key** 认证方式，并填写：
    - **Role ARN**：使用[1. 使用 Export CloudFormation 创建 role](#1-create-the-role-with-export-cloudformation)中的 ARN，或者使用[方法 2：使用 Access Key](#method-2-use-an-access-key)中的 **Access Key ID** / **Secret Access Key**。
    - **S3 Bucket Name**：仅填写存储桶名称（例如 `my-datapipeline-bucket`，而不是完整 URI）。
    - **S3 Region**：与你的 Essential 实例相同的 Region。
4. **SQS Queue URL** 为可选项。如果你想启用事件驱动摄取，请先设置 SQS 队列并配置 S3 存储桶通知。详情请参阅 [Amazon SQS and S3 IAM Role for TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/amazon-sqs-s3-iam-role/)。
5. 在 **Trust Cloud Platform roles** 下，验证 TiDB Cloud Lake 平台角色和 external ID 是否与[2. 合并信任关系](#2-consolidate-trust-relationships)中添加到合并信任策略的值一致。

### 2. 创建集成 {#2-create-an-integration}

1. 在 [TiDB Cloud Lake 控制台](https://lake.tidbcloud.com/) 中，进入 **Data > Integration > Create**。
2. 填写以下字段：
    - **Data Source**：选择上面创建的数据源。
    - **Name**：为该集成任务指定一个名称。
    - **Sync Mode**：选择 `Snapshot + CDC`，先加载完整快照，再持续应用增量变更。
    - **Table Rules**：`*.*`，表示同步所有已导出的表。
    - **Changefeed S3 Prefix**：`<prefix>/incremental/`。
    - **Dumpling S3 Prefix**：`<prefix>/snapshot/`。
    - **Poll Interval**：TiDB Cloud Lake 扫描外部 stage 中新数据的间隔时间。默认值为 60 秒。更短的间隔可以降低数据延时，但会增加 TiDB Cloud Lake 托管成本。
    - **Merge Interval**：TiDB Cloud Lake 将增量数据合并到计算集群的间隔时间。默认值为 30 秒。更短的间隔可以降低数据延时，但会增加 TiDB Cloud Lake 托管成本。
    - **Warehouse**：选择目标计算集群。
3. 点击 **Create**。
4. 创建完成后，集成默认处于 **Stopped** 状态。点击集成操作按钮 > **Start** 开始加载数据。

## 另请参阅 {#see-also}

- 有关 DDL、DML 和列类型支持的详细信息，请参阅 [TiDB Cloud Lake 的 Data Pipeline SQL 兼容性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md)。