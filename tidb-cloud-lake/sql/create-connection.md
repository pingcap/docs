---
title: CREATE CONNECTION
summary: 创建到外部存储的连接。
---

# CREATE CONNECTION

创建到外部存储的连接。

> **Warning:**
>
> 重要提示：当对象（stage、表等）使用某个连接时，它们会永久复制并存储该连接的参数。如果你之后使用 CREATE OR REPLACE CONNECTION 修改该连接，现有对象仍将继续使用旧参数。若要让对象使用新的连接参数，必须删除并重新创建这些对象。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] CONNECTION [ IF NOT EXISTS ] <connection_name>
    STORAGE_TYPE = '<type>'
    [ <storage_params> ]
```

| 参数 | 描述 |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| STORAGE_TYPE     | 存储服务的类型。可能的值包括：`s3`、`azblob`、`gcs`、`oss` 和 `cos`。                                                         |
| storage_params   | 根据存储类型和认证方法而变化。完整列表请参见 [连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。 |

## 连接参数 {#connection-parameters}

连接封装了特定存储后端的凭证和配置。创建连接时，请选择合适的 `STORAGE_TYPE` 并提供所需参数。下表列出了常见选项：

| STORAGE_TYPE | 常见参数 | 描述 |
|--------------|-------------------|-------------|
| `s3`         | `ACCESS_KEY_ID`/`SECRET_ACCESS_KEY`，或 `ROLE_ARN`/`EXTERNAL_ID`，可选 `ENDPOINT_URL`、`REGION` | Amazon S3 和兼容 S3 的服务（MinIO、Cloudflare R2 等）。 |
| `azblob`     | `ACCOUNT_NAME`、`ACCOUNT_KEY`、`ENDPOINT_URL` | Azure Blob Storage。 |
| `gcs`        | `CREDENTIAL`（base64 编码的服务账户密钥） | Google Cloud Storage。 |
| `oss`        | `ACCESS_KEY_ID`、`ACCESS_KEY_SECRET`、`ENDPOINT_URL` | 阿里云对象存储服务。 |
| `cos`        | `SECRET_ID`、`SECRET_KEY`、`ENDPOINT_URL` | 腾讯云对象存储。 |
| `hf`         | `REPO_TYPE`、`REVISION`，可选 `TOKEN` | Hugging Face Hub 数据集和模型。 |

有关参数含义、可选（命令行）标记/参数以及其他存储类型，请参见 [连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。展开下面的标签页可查看各存储类型的示例：

<SimpleTab groupId="connection-storage-types">

<div label="Amazon S3" value="s3">

为 Amazon S3 和兼容 S3 的服务选择一种认证方法：

<SimpleTab groupId="s3-auth-methods">

<div label="Access Keys" value="access-keys">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';
```

| 参数 | 描述 |
|-----------|-------------|
| ACCESS_KEY_ID | 你的 AWS access key ID。 |
| SECRET_ACCESS_KEY | 你的 AWS secret access key。 |

</div>

<div label="IAM Role" value="iam-role">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 's3'
    ROLE_ARN = '<your-role-arn>';
```

| 参数 | 描述 |
|-----------|-------------|
| ROLE_ARN  | {{{ .lake }}} 将用于访问你的 S3 资源的 IAM 角色的 Amazon Resource Name (ARN)。 |

</div>
</SimpleTab>

</div>

<div label="Azure Blob" value="azblob">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'azblob'
    ACCOUNT_NAME = '<account-name>'
    ACCOUNT_KEY = '<account-key>'
    ENDPOINT_URL = 'https://<account-name>.blob.core.windows.net';
```

</div>

<div label="Google Cloud Storage" value="gcs">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'gcs'
    CREDENTIAL = '<base64-encoded-service-account>';
```

</div>

<div label="Alibaba Cloud OSS" value="oss">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'oss'
    ACCESS_KEY_ID = '<your-ak>'
    ACCESS_KEY_SECRET = '<your-sk>'
    ENDPOINT_URL = 'https://<region-id>[-internal].aliyuncs.com';
```

</div>

<div label="Tencent COS" value="cos">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'cos'
    SECRET_ID = '<your-secret-id>'
    SECRET_KEY = '<your-secret-key>'
    ENDPOINT_URL = '<your-endpoint-url>';
```

</div>

<div label="Hugging Face" value="hf">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'hf'
    REPO_TYPE = 'dataset'
    REVISION = 'main'
    TOKEN = '<optional-access-token>';
```

对于公共仓库，可省略 `TOKEN`；对于私有仓库或受速率限制的资源，请包含该参数。

</div>
</SimpleTab>

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型 | 描述 |
|:------------------|:------------|:----------------------|
| CREATE CONNECTION | 全局      | 创建连接。 |

要创建连接，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 CREATE CONNECTION [权限](/tidb-cloud-lake/guides/privileges.md)。

## 修改表连接 {#update-table-connections}

要将现有表切换到新连接，请使用 [`ALTER TABLE ... CONNECTION`](/tidb-cloud-lake/sql/alter-table.md#external-table-connection)。该命令可以将外部表重新绑定到不同的连接，而无需重新创建表。

## 示例 {#examples}

### 使用 Access Keys {#using-access-keys}

本示例创建了一个名为 `toronto` 的 Amazon S3 连接，并使用该 `toronto` 连接创建了一个名为 `my_s3_stage` 的外部 stage，该 stage 关联到 `s3://lake-toronto` URL。有关连接的更多实际示例，请参见 [使用示例](/tidb-cloud-lake/sql/connection.md#usage-examples)。

```sql
CREATE CONNECTION toronto
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE STAGE my_s3_stage
    URL = 's3://lake-toronto'
    CONNECTION = (CONNECTION_NAME = 'toronto');
```

### 使用 AWS IAM Role {#using-aws-iam-role}

本示例使用 IAM 角色创建一个 Amazon S3 连接，然后创建一个使用该连接的 stage。这种方式更安全，因为它不需要在 {{{ .lake }}} 中存储 access keys。

```sql
CREATE CONNECTION lake_test
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::987654321987:role/lake-test';

CREATE STAGE lake_test
    URL = 's3://test-bucket-123'
    CONNECTION = (CONNECTION_NAME = 'lake_test');

-- You can now query data from your S3 bucket
SELECT * FROM @lake_test/test.parquet LIMIT 1;
```

> **Note:**
>
> 要在 {{{ .lake }}} 中使用 IAM 角色，你需要在你的 AWS 账户与 {{{ .lake }}} 之间建立信任关系。详细说明请参见 [使用 AWS IAM Role 进行认证](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md)。