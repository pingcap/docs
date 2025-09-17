---
title: 从 TiDB Cloud Starter 或 Essential 导出数据
summary: 了解如何从 TiDB Cloud Starter 或 TiDB Cloud Essential 集群导出数据。
---

# 从 TiDB Cloud Starter 或 Essential 导出数据

TiDB Cloud 支持你将数据从 TiDB Cloud Starter 或 Essential 集群导出到本地文件或外部存储服务。你可以将导出的数据用于备份、迁移、数据分析或其他用途。

虽然你也可以使用 [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) 和 TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview) 等工具导出数据，但 TiDB Cloud 提供的导出功能为你从集群导出数据带来了更便捷、高效的方式。其优势包括：

- 便捷性：导出服务提供了简单易用的方式从集群导出数据，无需额外的工具或资源。
- 隔离性：导出服务使用独立的计算资源，确保与在线服务资源的隔离。
- 一致性：导出服务保证导出数据的一致性且不会加锁，不会影响你的在线服务。

> **注意：**
>
> 当前最大导出数据量为 1 TiB。如需导出更多数据或申请更高的导出速度，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 导出位置

你可以将数据导出到以下位置：

- 本地文件
- 外部存储，包括：

    - [Amazon S3](https://aws.amazon.com/s3/)
    - [Google Cloud Storage](https://cloud.google.com/storage)
    - [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
    - [阿里云对象存储 OSS](https://www.alibabacloud.com/product/oss)

> **注意：**
>
> 如果导出数据量较大（超过 100 GiB），建议导出到外部存储。

### 本地文件

要将数据从 TiDB Cloud 集群导出到本地文件，你需要 [使用 TiDB Cloud 控制台导出数据](#export-data-to-a-local-file) 或 [使用 TiDB Cloud CLI 导出数据](/tidb-cloud/ticloud-serverless-export-create.md)，然后通过 TiDB Cloud CLI 下载导出的数据。

导出到本地文件有以下限制：

- 不支持通过 TiDB Cloud 控制台下载导出数据。
- 导出数据会保存在 TiDB Cloud 的暂存区，且将在两天后过期。你需要及时下载导出数据。
- 如果暂存区存储空间已满，将无法导出数据到本地文件。

### Amazon S3

要导出数据到 Amazon S3，你需要提供以下信息：

- URI：`s3://<bucket-name>/<folder-path>/`
- 以下访问凭证之一：
    - [访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)：确保该访问密钥拥有 `s3:PutObject` 和 `s3:ListBucket` 权限。
    - [角色 ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)：确保该角色 ARN（Amazon Resource Name）拥有 `s3:PutObject` 和 `s3:ListBucket` 权限。注意，只有托管在 AWS 上的集群支持角色 ARN。

更多信息，参见 [配置 Amazon S3 访问](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)。

### Google Cloud Storage

要导出数据到 Google Cloud Storage，你需要提供以下信息：

- URI：`gs://<bucket-name>/<folder-path>/`
- 访问凭证：你的 bucket 的 **base64 编码** [服务账号密钥](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)。确保该服务账号密钥拥有 `storage.objects.create` 权限。

更多信息，参见 [配置 GCS 访问](/tidb-cloud/serverless-external-storage.md#configure-gcs-access)。

### Azure Blob Storage

要导出数据到 Azure Blob Storage，你需要提供以下信息：

- URI：`azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` 或 `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- 访问凭证：你的 Azure Blob Storage 容器的 [共享访问签名（SAS）令牌](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。确保该 SAS 令牌对 `Container` 和 `Object` 资源拥有 `Read` 和 `Write` 权限。

更多信息，参见 [配置 Azure Blob Storage 访问](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)。

### 阿里云 OSS

要导出数据到阿里云 OSS，你需要提供以下信息：

- URI：`oss://<bucket-name>/<folder-path>/`
- 访问凭证：你的阿里云账号的 [AccessKey 对](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)。确保该 AccessKey 对拥有 `oss:PutObject`、`oss:ListBuckets` 和 `oss:GetBucketInfo` 权限，以允许数据导出到 OSS bucket。

更多信息，参见 [配置阿里云对象存储 OSS 访问](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access)。

## 导出选项

### 数据过滤

- TiDB Cloud 控制台支持按所选数据库和数据表导出数据。
- TiDB Cloud CLI 支持通过 SQL 语句和 [表过滤器](/table-filter.md) 导出数据。

### 数据格式

你可以将数据导出为以下格式：

- `SQL`：以 SQL 格式导出数据。
- `CSV`：以 CSV 格式导出数据。你可以指定以下选项：
    - `delimiter`：指定导出数据中使用的定界符。默认定界符为 `"`。
    - `separator`：指定导出数据中用于分隔字段的字符。默认分隔符为 `,`。
    - `header`：指定是否在导出数据中包含表头行。默认值为 `true`。
    - `null-value`：指定导出数据中表示 NULL 值的字符串。默认值为 `\N`。
- `Parquet`：以 Parquet 格式导出数据。

导出的 schema 和数据文件遵循以下命名规范：

| 项目            | 未压缩文件名                                        | 压缩后文件名                                                                                                          |
|-----------------|----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| 数据库 schema   | {database}-schema-create.sql                       | {database}-schema-create.sql.{compression-type}                                                                      |
| 表 schema      | {database}.{table}-schema.sql                       | {database}.{table}-schema.sql.{compression-type}                                                                     |
| 数据            | {database}.{table}.{0001}.{csv&#124;parquet&#124;sql} | {database}.{table}.{0001}.{csv&#124;sql}.{compression-type}<br/>{database}.{table}.{0001}.{compression-type}.parquet |

### 数据压缩

你可以使用以下算法压缩导出的 CSV 和 SQL 数据：

- `gzip`（默认）：使用 `gzip` 压缩导出数据。
- `snappy`：使用 `snappy` 压缩导出数据。
- `zstd`：使用 `zstd` 压缩导出数据。
- `none`：不对导出数据进行压缩。

你可以使用以下算法压缩导出的 Parquet 数据：

- `zstd`（默认）：使用 `zstd` 压缩 Parquet 文件。
- `gzip`：使用 `gzip` 压缩 Parquet 文件。
- `snappy`：使用 `snappy` 压缩 Parquet 文件。
- `none`：不对 Parquet 文件进行压缩。

### 数据类型转换

当导出数据为 Parquet 格式时，TiDB 与 Parquet 之间的数据类型转换如下：

| TiDB 数据类型 | Parquet 基础类型 | Parquet 逻辑类型                         |
|----------------------------|-------------------------|------------------------------------------|
| VARCHAR                    | BYTE_ARRAY              | String(UTF8)                             |
| TIME                       | BYTE_ARRAY              | String(UTF8)                             |
| TINYTEXT                   | BYTE_ARRAY              | String(UTF8)                             |
| MEDIUMTEXT                 | BYTE_ARRAY              | String(UTF8)                             |
| TEXT                       | BYTE_ARRAY              | String(UTF8)                             |
| LONGTEXT                   | BYTE_ARRAY              | String(UTF8)                             |
| SET                        | BYTE_ARRAY              | String(UTF8)                             |
| JSON                       | BYTE_ARRAY              | String(UTF8)                             |
| DATE                       | BYTE_ARRAY              | String(UTF8)                             |
| CHAR                       | BYTE_ARRAY              | String(UTF8)                             |
| VECTOR                     | BYTE_ARRAY              | String(UTF8)                             |
| DECIMAL(1<=p<=9)           | INT32                   | DECIMAL(p,s)                             |
| DECIMAL(10<=p<=18)         | INT64                   | DECIMAL(p,s)                             |
| DECIMAL(p>=19)             | BYTE_ARRAY              | String(UTF8)                             |
| ENUM                       | BYTE_ARRAY              | String(UTF8)                             |
| TIMESTAMP                  | INT64                   | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| DATETIME                   | INT64                   | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| YEAR                       | INT32                   | /                                        |
| TINYINT                    | INT32                   | /                                        |
| UNSIGNED TINYINT           | INT32                   | /                                        |
| SMALLINT                   | INT32                   | /                                        |
| UNSIGNED SMALLINT          | INT32                   | /                                        |
| MEDIUMINT                  | INT32                   | /                                        |
| UNSIGNED MEDIUMINT         | INT32                   | /                                        |
| INT                        | INT32                   | /                                        |
| UNSIGNED INT               | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                            |
| BIGINT                     | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                            |
| UNSIGNED BIGINT            | BYTE_ARRAY              | String(UTF8)                             |
| FLOAT                      | FLOAT                   | /                                        |
| DOUBLE                     | DOUBLE                  | /                                        |
| BLOB                       | BYTE_ARRAY              | /                                        |
| TINYBLOB                   | BYTE_ARRAY              | /                                        |
| MEDIUMBLOB                 | BYTE_ARRAY              | /                                        |
| LONGBLOB                   | BYTE_ARRAY              | /                                        |
| BINARY                     | BYTE_ARRAY              | /                                        |
| VARBINARY                  | BYTE_ARRAY              | /                                        |
| BIT                        | BYTE_ARRAY              | /                                        |

## 示例

### 导出数据到本地文件

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

   > **提示：**
   >
   > 你可以使用左上角的下拉框切换组织、项目和集群。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

3. 在 **Import** 页面，点击右上角的 **Export Data to**，选择 **Local File**。填写以下参数：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Exported Data**：选择你要导出的数据库和数据表。
    - **Data Format**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。

   > **提示：**
   >
   > 如果你的集群之前未导入或导出过数据，需要在页面底部点击 **Click here to export data to...** 进行导出。

4. 点击 **Export**。

5. 导出任务成功后，你可以复制导出任务详情中显示的下载命令，并在 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 中运行该命令下载导出数据。

</div>

<div label="CLI">

1. 创建导出任务：

    ```shell
    ticloud serverless export create -c <cluster-id>
    ```

    你将在输出中获得一个导出 ID。

2. 导出任务成功后，将导出数据下载到本地文件：

    ```shell
    ticloud serverless export download -c <cluster-id> -e <export-id>
    ```

    有关下载命令的更多信息，参见 [ticloud serverless export download](/tidb-cloud/ticloud-serverless-export-download.md)。
 
</div>
</SimpleTab>

### 导出数据到 Amazon S3

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

   > **提示：**
   >
   > 你可以使用左上角的下拉框切换组织、项目和集群。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

3. 在 **Import** 页面，点击右上角的 **Export Data to**，选择 **Amazon S3**。填写以下参数：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Exported Data**：选择你要导出的数据库和数据表。
    - **Data Format**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **Folder URI**：输入 Amazon S3 的 URI，格式为 `s3://<bucket-name>/<folder-path>/`。
    - **Bucket Access**：选择以下访问凭证之一并填写凭证信息：
        - **AWS Role ARN**：输入有权限访问 bucket 的角色 ARN。推荐使用 AWS CloudFormation 创建角色 ARN。更多信息参见 [配置 Amazon S3 访问](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)。
        - **AWS Access Key**：输入有权限访问 bucket 的 Access Key ID 和 Access Key Secret。

4. 点击 **Export**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter "database.table"

ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.role-arn <role-arn> --filter "database.table"
```

- `s3.uri`：Amazon S3 的 URI，格式为 `s3://<bucket-name>/<folder-path>/`。
- `s3.access-key-id`：有权限访问 bucket 的用户的 Access Key ID。
- `s3.secret-access-key`：有权限访问 bucket 的用户的 Access Key Secret。
- `s3.role-arn`：有权限访问 bucket 的角色 ARN。

</div>
</SimpleTab>

### 导出数据到 Google Cloud Storage

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

   > **提示：**
   >
   > 你可以使用左上角的下拉框切换组织、项目和集群。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

3. 在 **Import** 页面，点击右上角的 **Export Data to**，选择 **Google Cloud Storage**。填写以下参数：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Exported Data**：选择你要导出的数据库和数据表。
    - **Data Format**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **Folder URI**：输入 Google Cloud Storage 的 URI，格式为 `gs://<bucket-name>/<folder-path>/`。
    - **Bucket Access**：上传有权限访问 bucket 的 Google Cloud 凭证文件。

4. 点击 **Export**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type GCS --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter "database.table"
```

- `gcs.uri`：Google Cloud Storage bucket 的 URI，格式为 `gs://<bucket-name>/<folder-path>/`。
- `gcs.service-account-key`：base64 编码的服务账号密钥。

</div>
</SimpleTab>

### 导出数据到 Azure Blob Storage

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

   > **提示：**
   >
   > 你可以使用左上角的下拉框切换组织、项目和集群。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

3. 在 **Import** 页面，点击右上角的 **Export Data to**，选择 **Azure Blob Storage**。填写以下参数：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Exported Data**：选择你要导出的数据库和数据表。
    - **Data Format**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **Folder URI**：输入 Azure Blob Storage 的 URI，格式为 `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`。
    - **SAS Token**：输入有权限访问容器的 SAS 令牌。推荐使用 [Azure ARM 模板](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/) 创建 SAS 令牌。更多信息参见 [配置 Azure Blob Storage 访问](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)。

4. 点击 **Export**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type AZURE_BLOB --azblob.uri <uri> --azblob.sas-token <sas-token> --filter "database.table"
```

- `azblob.uri`：Azure Blob Storage 的 URI，格式为 `(azure|https)://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`。
- `azblob.sas-token`：Azure Blob Storage 的账户 SAS 令牌。

</div>
</SimpleTab>

### 导出数据到阿里云 OSS

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

   > **提示：**
   >
   > 你可以使用左上角的下拉框切换组织、项目和集群。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

3. 在 **Import** 页面，点击右上角的 **Export Data to**，选择 **Alibaba Cloud OSS**。

4. 填写以下参数：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Exported Data**：选择你要导出的数据库和数据表。
    - **Data Format**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **Folder URI**：输入你希望导出数据的阿里云 OSS URI，格式为 `oss://<bucket-name>/<folder-path>/`。
    - **AccessKey ID** 和 **AccessKey Secret**：输入有权限访问 bucket 的 AccessKey ID 和 AccessKey Secret。

5. 点击 **Export**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type OSS --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter "database.table"
```

- `oss.uri`：你希望导出数据的阿里云 OSS URI，格式为 `oss://<bucket-name>/<folder-path>/`。
- `oss.access-key-id`：有权限访问 bucket 的用户的 AccessKey ID。
- `oss.access-key-secret`：有权限访问 bucket 的用户的 AccessKey Secret。

</div>
</SimpleTab>

### 取消导出任务

要取消正在进行的导出任务，请按以下步骤操作：

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

   > **提示：**
   >
   > 你可以使用左上角的下拉框切换组织、项目和集群。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

3. 在 **Import** 页面，点击 **Export** 查看导出任务列表。

4. 选择你要取消的导出任务，然后点击 **Action**。

5. 在下拉列表中选择 **Cancel**。注意，你只能取消状态为 **Running** 的导出任务。

</div>

<div label="CLI">

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

</div>
</SimpleTab>

## 导出速度

导出速度取决于你的 [集群套餐](/tidb-cloud/select-cluster-tier.md)：

- **TiDB Cloud Starter**：

    - 如果消费上限设置为 0，导出速度最高为 25 MiB/s。
    - 如果消费上限大于 0，导出速度最高为 100 MiB/s。

- **TiDB Cloud Essential**：最高 100 MiB/s。

## 计费

导出服务在测试期间免费。你只需为成功或已取消任务的导出过程产生的 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 支付费用。对于失败的导出任务，不会收取费用。