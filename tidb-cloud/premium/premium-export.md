---
title: 从 {{{ .premium }}} 导出数据
summary: 了解如何从 {{{ .premium }}} 实例导出数据。
---

# 从 {{{ .premium }}} 导出数据

TiDB Cloud 支持将数据从 {{{ .premium }}} 实例导出到外部存储服务。你可以将导出的数据用于备份、迁移、数据分析或其他用途。

虽然你也可以使用 [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) 和 TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview) 等工具导出数据，但 TiDB Cloud 提供的导出功能为从 {{{ .premium }}} 实例导出数据提供了更便捷、更高效的方式。它具有以下优势：

- 便捷性：导出服务提供了一种简单易用的方式来从 {{{ .premium }}} 实例导出数据，无需额外的工具或资源。
- 隔离性：导出服务使用独立的计算资源，确保与在线服务所使用的资源相隔离。
- 一致性：导出服务可在不加锁的情况下确保导出数据的一致性，因此不会影响你的在线服务。

> **注意：**
>
> - 当前，此功能仅可按需申请使用。要申请此功能，请点击 [TiDB Cloud console](https://tidbcloud.com) 右下角的 **?**，然后点击 **Support Tickets** 进入 [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals)。创建工单，在 **Description** 字段中填写 "Apply for data export for {{{ .premium }}} instance"，然后点击 **Submit**。
> - 最大导出大小为 1 TiB。超过此限制的导出任务可能会失败。如需导出更多数据或申请更高的导出速度，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 导出位置 {#export-locations}

你可以将数据导出到以下外部存储位置：

- [Amazon S3](https://aws.amazon.com/s3/)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
- [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss)

### Amazon S3 {#amazon-s3}

要将数据导出到 Amazon S3，你需要提供以下信息：

- URI：`s3://<bucket-name>/<folder-path>/`
- 以下访问凭证之一：
    - [An access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)：确保该 access key 具有 `s3:PutObject` 权限。
    - [A role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)：确保该 role ARN（Amazon Resource Name）具有 `s3:PutObject` 权限。请注意，只有托管在 AWS 上的 {{{ .premium }}} 实例支持 role ARN。

更多信息，请参见 [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。

### Azure Blob Storage {#azure-blob-storage}

要将数据导出到 Azure Blob Storage，你需要提供以下信息：

- URI：`azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` 或 `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- 访问凭证：你的 Azure Blob Storage 容器的 [shared access signature (SAS) token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。确保该 SAS token 对 `Container` 和 `Object` 资源具有 `Read` 和 `Write` 权限。

更多信息，请参见 [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)。

### Alibaba Cloud OSS {#alibaba-cloud-oss}

要将数据导出到 Alibaba Cloud OSS，你需要提供以下信息：

- URI：`oss://<bucket-name>/<folder-path>/`
- 访问凭证：你的 Alibaba Cloud 账户的 [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)。确保该 AccessKey pair 具有 `oss:PutObject` 和 `oss:GetBucketInfo` 权限。

更多信息，请参见 [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。

## 导出选项 {#export-options}

### 数据过滤 {#data-filtering}

TiDB Cloud console 支持按所选数据库和表导出数据。

### 数据格式 {#data-formats}

你可以按以下格式导出数据：

- `SQL`：以 SQL 格式导出数据。
- `CSV`：以 CSV 格式导出数据。你可以指定以下选项：
    - `delimiter`：指定导出数据中使用的定界符。默认定界符为 `"`。
    - `separator`：指定导出数据中用于分隔字段的字符。默认分隔符为 `,`。
    - `header`：指定是否在导出数据中包含表头行。默认值为 `true`。
    - `null-value`：指定导出数据中表示 NULL 值的字符串。默认值为 `\N`。

Schema 和数据按照以下命名约定导出：

| Item            | Not compressed                | Compressed                                                   |
|-----------------|-------------------------------|--------------------------------------------------------------|
| Database schema | {database}-schema-create.sql  | {database}-schema-create.sql.{compression-type}              |
| Table schema    | {database}.{table}-schema.sql | {database}.{table}-schema.sql.{compression-type}             |
| Data            | {database}.{table}.{0001}.csv | {database}.{table}.{0001}.csv.{compression-type}             |
| Data            | {database}.{table}.{0001}.sql | {database}.{table}.{0001}.sql.{compression-type}             |

### 数据压缩 {#data-compression}

你可以使用以下算法压缩导出的 CSV 和 SQL 数据：

- `gzip`（默认）：使用 `gzip` 压缩导出数据。
- `snappy`：使用 `snappy` 压缩导出数据。
- `zstd`：使用 `zstd` 压缩导出数据。
- `none`：不压缩导出数据。

## 示例 {#examples}

### 将数据导出到 Amazon S3 {#export-data-to-amazon-s3}

1. 登录 [TiDB Cloud console](https://tidbcloud.com/) 并进入 [**TiDB Instances**](https://tidbcloud.com/tidbs) 页面。

   > **提示：**
   >
   > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

2. 点击目标 {{{ .premium }}} 实例的名称进入其概览页面，然后在左侧导航栏中点击 **Data** > **Export**。

3. 在 **Export** 页面右上角点击 **Export Data**。然后配置以下设置：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Source Connection**：输入 {{{ .premium }}} 实例的 **Username** 和 **Password**，然后点击 **Test Connection** 验证凭证。
    - **Target Connection**：
        - **Storage Provider**：选择 Amazon S3。
        - **Folder URI**：输入 Amazon S3 的 URI，格式为 `s3://<bucket-name>/<folder-path>/`。
        - **Bucket Access**：选择以下访问凭证之一，然后填写凭证信息：
            - **AWS Role ARN**：输入具有访问 bucket 权限的 role ARN。建议使用 AWS CloudFormation 创建该 role ARN。更多信息，请参见 [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。
            - **AWS Access Key**：输入具有访问 bucket 权限的 access key ID 和 access key secret。
    - **Exported Data**：选择要导出的数据库或表。
    - **Data Format**：选择 **SQL** 或 **CSV**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。

4. 点击 **Export**。

### 将数据导出到 Azure Blob Storage {#export-data-to-azure-blob-storage}

1. 登录 [TiDB Cloud console](https://tidbcloud.com/) 并进入 [**TiDB Instances**](https://tidbcloud.com/tidbs) 页面。

   > **提示：**
   >
   > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

2. 点击目标 {{{ .premium }}} 实例的名称进入其概览页面，然后在左侧导航栏中点击 **Data** > **Export**。

3. 在 **Export** 页面右上角点击 **Export Data**。然后配置以下设置：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Source Connection**：输入 {{{ .premium }}} 实例的 **Username** 和 **Password**，然后点击 **Test Connection** 验证凭证。
    - **Target Connection**：
        - **Storage Provider**：选择 Azure Blob Storage。
        - **Folder URI**：输入 Azure Blob Storage 的 URI，格式为 `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`。
        - **SAS Token**：输入具有访问 container 权限的 SAS token。建议使用 [Azure ARM template](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/) 创建 SAS token。更多信息，请参见 [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)。
    - **Exported Data**：选择要导出的数据库或表。
    - **Data Format**：选择 **SQL** 或 **CSV**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。

4. 点击 **Export**。

### 将数据导出到 Alibaba Cloud OSS {#export-data-to-alibaba-cloud-oss}

1. 登录 [TiDB Cloud console](https://tidbcloud.com/) 并进入 [**TiDB Instances**](https://tidbcloud.com/tidbs) 页面。

   > **提示：**
   >
   > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

2. 点击目标 {{{ .premium }}} 实例的名称进入其概览页面，然后在左侧导航栏中点击 **Data** > **Export**。

3. 在 **Export** 页面右上角点击 **Export Data**：

    - **Task Name**：输入导出任务名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **Source Connection**：输入 {{{ .premium }}} 实例的 **Username** 和 **Password**，然后点击 **Test Connection** 验证凭证。
    - **Target Connection**：
        - **Storage Provider**：选择 Alibaba Cloud OSS。
        - **Folder URI**：输入要导出数据的 Alibaba Cloud OSS URI，格式为 `oss://<bucket-name>/<folder-path>/`。
        - **AccessKey ID** 和 **AccessKey Secret**：输入具有访问 bucket 权限的 AccessKey ID 和 AccessKey Secret。
    - **Exported Data**：选择要导出的数据库或表。
    - **Data Format**：选择 **SQL** 或 **CSV**。
    - **Compression**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。

4. 点击 **Export**。

### 取消导出任务 {#cancel-an-export-task}

如需取消正在进行的导出任务，请执行以下步骤：

1. 登录 [TiDB Cloud console](https://tidbcloud.com/) 并进入 [**TiDB Instances**](https://tidbcloud.com/tidbs) 页面。

   > **提示：**
   >
   > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

2. 点击目标 {{{ .premium }}} 实例的名称进入其概览页面，然后在左侧导航栏中点击 **Data** > **Export**。

3. 在 **Export** 页面查看导出任务列表。

4. 选择要取消的导出任务，然后点击 **Action**。

5. 在下拉列表中选择 **Cancel**。请注意，你只能取消状态为 **Running** 的导出任务。