---
title: CREATE STAGE
summary: 创建内部或外部 stage。
---

# CREATE STAGE

创建内部或外部 stage。

## 语法 {#syntax}

```sql
-- Internal stage
CREATE [ OR REPLACE ] STAGE [ IF NOT EXISTS ] <internal_stage_name>
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO | LANCE } [ formatTypeOptions ]
       ) ]
  [ COMMENT = '<string_literal>' ]

-- External stage
CREATE STAGE [ IF NOT EXISTS ] <external_stage_name>
    externalStageParams
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO | LANCE } [ formatTypeOptions ]
       ) ]
  [ COMMENT = '<string_literal>' ]
```

### externalStageParams {#externalstageparams}

> **Tip:**
>
> 对于外部 stage，建议使用 `CONNECTION` 参数引用预先配置的连接对象，而不是直接内联填写凭证。这种方式可提供更好的安全性和可维护性。

```sql
externalStageParams ::=
  '<protocol>://<location>'
  CONNECTION = (
        <connection_parameters>
  )
|
  CONNECTION = (
        CONNECTION_NAME = '<your-connection-name>'
  );
```

有关不同存储服务可用的连接参数，请参见[连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。

有关 `CONNECTION_NAME` 的更多信息，请参见 [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md)。

### FILE_FORMAT {#file-format}

详情请参见[输入和输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型 | 描述 |
|:----------|:--------------|:--------------------------------------------------------------------------|
| SUPER     | 全局、表 | 对 stage（列出 stage、创建 stage、删除 stage）、catalog 或 share 执行操作。 |

要创建 stage，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 SUPER [权限](/tidb-cloud-lake/guides/privileges.md)。

## 示例 {#examples}

### 示例 1：创建内部 stage {#example-1-create-internal-stage}

以下示例创建一个名为 *my_internal_stage* 的内部 stage：

```sql
CREATE STAGE my_internal_stage;

DESC STAGE my_internal_stage;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│       name        │ stage_type │ storage_type │ url  │ endpoint │ has_credentials │ has_encryption_key │ storage_params │ file_format_options │  creator │         created_on         │ comment │     owner     │
├───────────────────┼────────────┼──────────────┼──────┼──────────┼─────────────────┼────────────────────┼────────────────┼─────────────────────┼──────────┼────────────────────────────┼─────────┼───────────────┤
│ my_internal_stage │ Internal   │ NULL         │ NULL │ NULL     │ false           │ false              │ NULL           │ {"compression":...} │ root@%   │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 示例 2：使用连接创建外部 stage {#example-2-create-external-stage-with-connection}

以下示例在 Amazon S3 上使用连接创建一个名为 *my_s3_stage* 的外部 stage：

```sql
-- First create a connection
CREATE CONNECTION my_s3_connection
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<your-access-key-id>'
  SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Create stage using the connection
CREATE STAGE my_s3_stage
  URL='s3://load/files/'
  CONNECTION = (CONNECTION_NAME = 'my_s3_connection');

DESC STAGE my_s3_stage;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│    name     │ stage_type │ storage_type │       url        │ endpoint │ has_credentials │ has_encryption_key │   storage_params      │ file_format_options │ creator │         created_on         │ comment │     owner     │
├─────────────┼────────────┼──────────────┼──────────────────┼──────────┼─────────────────┼────────────────────┼───────────────────────┼─────────────────────┼─────────┼────────────────────────────┼─────────┼───────────────┤
│ my_s3_stage │ External   │ s3           │ s3://load/files/ │ NULL     │ true            │ false              │ {"bucket":"load",...} │ {"compression":...} │ root@%  │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 示例 3：使用 AWS IAM User 创建外部 stage {#example-3-create-external-stage-with-aws-iam-user}

以下示例在 Amazon S3 上使用 AWS Identity and Access Management (IAM) 用户创建一个名为 *iam_external_stage* 的外部 stage。

#### 步骤 1：为 S3 bucket 创建访问策略 {#step-1-create-access-policy-for-s3-bucket}

以下过程会为 Amazon S3 上的 bucket *lake-toronto* 创建一个名为 *lake-access* 的访问策略：

1. 登录 AWS Management Console，然后选择 **Services** > **Security, Identity, & Compliance** > **IAM**。
2. 在左侧导航栏中选择 **Account settings**，然后前往右侧页面中的 **Security Token Service (STS)** 部分。确保你的账户所属 AWS 区域的状态为 **Active**。
3. 在左侧导航栏中选择 **Policies**，然后在右侧页面选择 **Create policy**。
4. 点击 **JSON** 选项卡，将以下代码复制并粘贴到编辑器中，然后将该策略保存为 *lake_access*。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllObjectActions",
      "Effect": "Allow",
      "Action": ["s3:*Object"],
      "Resource": "arn:aws:s3:::lake-toronto/*"
    },
    {
      "Sid": "ListObjectsInBucket",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::lake-toronto"
    }
  ]
}
```

#### 步骤 2：创建 IAM 用户 {#step-2-create-iam-user}

以下过程会创建一个名为 *lake* 的 IAM 用户，并将访问策略 *lake-access* 附加到该用户。

1. 在左侧导航栏中选择 **Users**，然后在右侧页面选择 **Add users**。
2. 配置用户：
    - 将用户名设置为 *lake*。
    - 为用户设置权限时，点击 **Attach policies directly**，然后搜索并选择访问策略 *lake-access*。
3. 创建用户后，点击用户名打开详情页面，并选择 **Security credentials** 选项卡。
4. 在 **Access keys** 部分，点击 **Create access key**。
5. 在 use case 中选择 **Third-party service**，并勾选下方复选框以确认创建 access key。
6. 复制并保存生成的 access key 和 secret access key 到安全位置。

#### 步骤 3：创建外部 stage {#step-3-create-external-stage}

使用 IAM role 创建外部 stage，可获得更好的安全性。

```sql
-- First create a connection using IAM role
CREATE CONNECTION iam_s3_connection
  STORAGE_TYPE = 's3'
  ROLE_ARN = 'arn:aws:iam::123456789012:role/lake-access'
  EXTERNAL_ID = 'my-external-id-123';

-- Create stage using the connection
CREATE STAGE iam_external_stage
  URL = 's3://lake-toronto'
  CONNECTION = (CONNECTION_NAME = 'iam_s3_connection');
```

### 示例 4：在 Cloudflare R2 上创建外部 stage {#example-4-create-external-stage-on-cloudflare-r2}

[Cloudflare R2](https://www.cloudflare.com/en-ca/products/r2/) 是 Cloudflare 推出的一种对象存储服务，与 Amazon 的 AWS S3 服务完全兼容。以下示例在 Cloudflare R2 上创建一个名为 *r2_stage* 的外部 stage。

#### 步骤 1：创建 bucket {#step-1-create-bucket}

以下过程会在 Cloudflare R2 上创建一个名为 *lake* 的 bucket。

1. 登录 Cloudflare dashboard，并在左侧导航栏中选择 **R2**。
2. 点击 **Create bucket** 创建 bucket，并将 bucket 名称设置为 *lake*。bucket 创建成功后，在查看 bucket 详情页面时，你可以在 bucket 名称正下方找到 bucket endpoint。

#### 步骤 2：创建 R2 API Token {#step-2-create-r2-api-token}

以下过程会创建一个 R2 API token，其中包含 Access Key ID 和 Secret Access Key。

1. 在 **R2** > **Overview** 中点击 **Manage R2 API Tokens**。
2. 点击 **Create API token** 创建一个 API token。
3. 配置 API token 时，选择所需权限，并根据需要设置 **TTL**。
4. 点击 **Create API Token** 以获取 Access Key ID 和 Secret Access Key。复制并将其保存到安全位置。

#### 第 3 步：创建 External Stage {#step-3-create-external-stage}

使用已创建的 Access Key ID 和 Secret Access Key 创建一个名为 *r2_stage* 的 external stage。

```sql
-- First create a connection
CREATE CONNECTION r2_connection
  STORAGE_TYPE = 's3'
  REGION = 'auto'
  ENDPOINT_URL = '<your-bucket-endpoint>'
  ACCESS_KEY_ID = '<your-access-key-id>'
  SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Create stage using the connection
CREATE STAGE r2_stage
  URL='s3://lake/'
  CONNECTION = (CONNECTION_NAME = 'r2_connection');
```