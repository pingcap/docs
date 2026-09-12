---
title: 连接参数
summary: 连接参数是你在使用 CREATE CONNECTION 创建可复用连接时提供的键值对。连接创建后，可以通过 CONNECTION = (CONNECTION_NAME = '<connection-name>') 在 stage、COPY 命令以及其他 SQL 功能中引用它。完整语法和用法，请参见 CREATE CONNECTION。
---

# 连接参数

连接参数是在使用 `CREATE CONNECTION` 创建可复用连接时提供的键值对。连接创建后，可以通过 `CONNECTION = (CONNECTION_NAME = '<connection-name>')` 在 stage、COPY 命令以及其他 SQL 功能中引用该连接。完整语法和用法请参见 [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md)。

有关不同存储类型的连接详情，请参见下表。

<SimpleTab groupId="operating-systems">

<div label="Amazon S3" value="Amazon S3">

下表列出了访问 Amazon S3 类存储服务的连接参数：

| 参数                       | 必填？ | 描述                                                         |
|--------------------------- |------- |------------------------------------------------------------ |
| endpoint_url               | 是     | Amazon S3 类存储服务的 endpoint URL。                       |
| access_key_id              | 是     | 用于标识请求方的 access key ID。                            |
| secret_access_key          | 是     | 用于身份验证的 secret access key。                          |
| enable_virtual_host_style  | 否     | 是否使用 virtual host 风格的 URL。默认为 *false*。          |
| master_key                 | 否     | 用于高级数据加密的可选主密钥。                              |
| region                     | 否     | 存储桶所在的 AWS Region。                                   |
| security_token             | 否     | 用于临时凭证的安全令牌。                                    |

> **注意：**
>
> - 如果命令中未指定 **endpoint_url** 参数，{{{ .lake }}} 默认会在 Amazon S3 上创建 stage。因此，当你在兼容 S3 的对象存储或其他对象存储解决方案上创建外部 stage 时，请务必包含 **endpoint_url** 参数。
>
> - **region** 参数不是必需的，因为 {{{ .lake }}} 可以自动检测 Region 信息。通常你不需要手动为该参数指定值。如果自动检测失败，{{{ .lake }}} 将默认使用 `'us-east-1'` 作为 region。使用 MinIO 部署 {{{ .lake }}} 且未配置 Region 信息时，也会自动默认使用 `'us-east-1'`，并且可以正常工作。但是，如果你收到诸如 `"region is missing"` 或 `"The bucket you are trying to access requires a specific endpoint. Please direct all future requests to this particular endpoint"` 之类的错误信息，则需要确认你的 region 名称，并显式将其赋值给 **region** 参数。

```sql title='Examples'
-- Create a reusable connection for Amazon S3
CREATE CONNECTION my_s3_conn
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<your-ak>'
  SECRET_ACCESS_KEY = '<your-sk>';

-- Use the connection when creating a stage
CREATE STAGE my_s3_stage
  URL = 's3://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_s3_conn');

-- Create a reusable connection for an S3-compatible service such as MinIO
CREATE CONNECTION my_minio_conn
  STORAGE_TYPE = 's3'
  ENDPOINT_URL = 'http://localhost:9000'
  ACCESS_KEY_ID = 'ROOTUSER'
  SECRET_ACCESS_KEY = 'CHANGEME123';

CREATE STAGE my_minio_stage
  URL = 's3://lake'
  CONNECTION = (CONNECTION_NAME = 'my_minio_conn');
```

要访问你的 Amazon S3 存储桶，也可以指定 AWS IAM role 和 external ID 进行身份验证。通过指定 AWS IAM role 和 external ID，你可以更细粒度地控制用户可以访问哪些 S3 存储桶。这意味着，如果某个 IAM role 仅被授予访问特定 S3 存储桶的权限，那么用户也只能访问这些存储桶。external ID 还可以通过提供额外的一层验证来进一步增强安全性。更多信息，请参见 <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html>

下表列出了使用 AWS IAM role 身份验证访问 Amazon S3 存储服务的连接参数：

| 参数          | 必填？ | 描述                                                  |
|-------------- |------- |----------------------------------------------------- |
| endpoint_url  | 否     | Amazon S3 的 endpoint URL。                          |
| role_arn      | 是     | 用于授权访问 S3 的 AWS IAM role 的 ARN。             |
| external_id   | 否     | 在承担角色时用于增强安全性的 external ID。           |

```sql title='Examples'
-- Create the connection using IAM role authentication
CREATE CONNECTION my_iam_conn
  STORAGE_TYPE = 's3'
  ROLE_ARN = 'arn:aws:iam::123456789012:role/my-role'
  EXTERNAL_ID = 'my-external-id';

-- Reference the connection when creating a stage
CREATE STAGE my_iam_stage
  URL = 's3://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_iam_conn');
```

</div>

<div label="Azure Blob" value="Azure Blob">

下表列出了访问 Azure Blob Storage 的连接参数：

| 参数           | 必填？ | 描述                                                  |
|----------------|--------|-------------------------------------------------------|
| endpoint_url   | 是     | Azure Blob Storage 的 endpoint URL。                  |
| account_key    | 是     | 用于身份验证的 Azure Blob Storage account key。       |
| account_name   | 是     | 用于标识的 Azure Blob Storage account name。          |

```sql title='Examples'
-- Create a connection for Azure Blob Storage
CREATE CONNECTION my_azure_conn
  STORAGE_TYPE = 'azblob'
  ACCOUNT_NAME = 'myaccount'
  ACCOUNT_KEY = 'myaccountkey'
  ENDPOINT_URL = 'https://<your-storage-account-name>.blob.core.windows.net';

-- Create a stage that uses the connection
CREATE STAGE my_azure_stage
  URL = 'azblob://my-container'
  CONNECTION = (CONNECTION_NAME = 'my_azure_conn');
```

</div>

<div label="Google GCS" value="Google GCS">

下表列出了访问 Google Cloud Storage 的连接参数：

| 参数           | 必填？ | 描述                                                  |
|----------------|--------|-------------------------------------------------------|
| credential     | 是     | 用于身份验证的 Google Cloud Storage credential。      |

要获取 `credential`，你可以参考 Google 文档中的主题 [Create a service account key](https://cloud.google.com/iam/docs/keys-create-delete#creating) 来创建并下载服务账户密钥文件。下载服务账户密钥文件后，可以通过以下命令将其转换为 base64 字符串：

```
base64 -i -o ~/Desktop/base64-encoded-key.txt
```

```sql title='Examples'
-- Create the connection with the base64-encoded credential
CREATE CONNECTION my_gcs_conn
  STORAGE_TYPE = 'gcs'
  CREDENTIAL = '<your-base64-encoded-credential>';

-- Use the connection when creating a stage
CREATE STAGE my_gcs_stage
  URL = 'gcs://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_gcs_conn');
```

</div>

<div label="Alibaba Cloud OSS" value="Alibaba OSS">

下表列出了访问 Alibaba Cloud OSS 的连接参数：

| 参数                   | 必填？ | 描述                                                      |
|---------------------- |------- |--------------------------------------------------------- |
| access_key_id         | 是     | 用于身份验证的 Alibaba Cloud OSS access key ID。         |
| access_key_secret     | 是     | 用于身份验证的 Alibaba Cloud OSS access key secret。     |
| endpoint_url          | 是     | Alibaba Cloud OSS 的 endpoint URL。                      |
| presign_endpoint_url  | 否     | 用于为 Alibaba Cloud OSS URL 预签名的 endpoint URL。     |

```sql title='Examples'
-- Create a connection for Alibaba Cloud OSS
CREATE CONNECTION my_oss_conn
  STORAGE_TYPE = 'oss'
  ACCESS_KEY_ID = '<your-ak>'
  ACCESS_KEY_SECRET = '<your-sk>'
  ENDPOINT_URL = 'https://<bucket-name>.<region-id>[-internal].aliyuncs.com';

-- Create a stage using the connection
CREATE STAGE my_oss_stage
  URL = 'oss://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_oss_conn');
```

</div>

<div label="Tencent COS" value="Tencent COS">

下表列出了访问 Tencent Cloud Object Storage (COS) 的连接参数：

| 参数          | 必填？ | 描述                                                        |
|-------------- |------- |----------------------------------------------------------- |
| endpoint_url  | 是     | Tencent Cloud Object Storage 的 endpoint URL。             |
| secret_id     | 是     | 用于身份验证的 Tencent Cloud Object Storage secret ID。    |
| secret_key    | 是     | 用于身份验证的 Tencent Cloud Object Storage secret key。   |

```sql title='Examples'
-- Create a connection for Tencent COS
CREATE CONNECTION my_cos_conn
  STORAGE_TYPE = 'cos'
  SECRET_ID = '<your-secret-id>'
  SECRET_KEY = '<your-secret-key>'
  ENDPOINT_URL = '<your-endpoint-url>';

-- Create a stage that uses the connection
CREATE STAGE my_cos_stage
  URL = 'cos://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_cos_conn');
```

</div>

<div label="HuggingFace" value="Hugging Face">

下表列出了访问 Hugging Face 的连接参数：

| 参数      | 必填？                | 描述                                                                                           |
|-----------|-----------------------|------------------------------------------------------------------------------------------------|
| repo_type | 否（默认值：dataset） | Hugging Face 仓库的类型。可以是 `dataset` 或 `model`。                                         |
| revision  | 否（默认值：main）    | Hugging Face URI 的 revision。可以是仓库的分支、tag 或 commit。                                |
| token     | 否                    | Hugging Face 的 API token，在访问私有仓库或某些资源时可能需要提供。                            |

```sql title='Examples'
-- Create a connection for Hugging Face
CREATE CONNECTION my_hf_conn
  STORAGE_TYPE = 'hf'
  REPO_TYPE = 'dataset'
  REVISION = 'main';

-- Create a stage that uses the connection
CREATE STAGE my_huggingface_stage
  URL = 'hf://opendal/huggingface-testdata/'
  CONNECTION = (CONNECTION_NAME = 'my_hf_conn');
```

</div>
</SimpleTab>