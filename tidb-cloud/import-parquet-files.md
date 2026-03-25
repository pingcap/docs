---
title: 从云存储导入 Apache Parquet 文件到 TiDB Cloud Dedicated
summary: 了解如何将 Apache Parquet 文件从 Amazon S3、GCS 或 Azure Blob Storage 导入到 TiDB Cloud Dedicated。
---

# 从云存储导入 Apache Parquet 文件到 TiDB Cloud Dedicated

本文档介绍如何将 Apache Parquet 文件从 Amazon Simple Storage Service（Amazon S3）、Google Cloud Storage（GCS）或 Azure Blob Storage 导入到 TiDB Cloud Dedicated。你可以导入未压缩的 Parquet 文件，或使用 [Google Snappy](https://github.com/google/snappy) 压缩的 Parquet 文件。不支持其他 Parquet 压缩编码。

## 限制

- 为保证数据一致性，TiDB Cloud 仅允许将 Parquet 文件导入到空表中。若需将数据导入到已存在数据的表中，你可以按照本文档的步骤，先将数据导入到一个临时空表，再通过 `INSERT SELECT` 语句将数据复制到目标表。

- 如果 TiDB Cloud Dedicated 集群已开启 [changefeed](/tidb-cloud/changefeed-overview.md) 或已启用 [Point-in-time Restore](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)，则无法向该集群导入数据（**Import Data** 按钮会被禁用），因为当前数据导入功能使用的是 [物理导入模式](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)。在该模式下，导入的数据不会生成变更日志，因此 changefeed 和 Point-in-time Restore 无法检测到导入的数据。

## 步骤 1. 准备 Parquet 文件

> **注意：**
>
> 当前，TiDB Cloud 不支持导入包含以下任意数据类型的 Parquet 文件。如果待导入的 Parquet 文件包含这些数据类型，你需要先使用 [支持的数据类型](#supported-data-types)（例如 `STRING`）重新生成 Parquet 文件。或者，你也可以使用 AWS Glue 等服务轻松转换数据类型。
>
> - `LIST`
> - `NEST STRUCT`
> - `BOOL`
> - `ARRAY`
> - `MAP`

1. 如果单个 Parquet 文件大于 256 MB，建议将其切分为多个小文件，每个文件大小约为 256 MB。

    TiDB Cloud 支持导入非常大的 Parquet 文件，但以多个约 256 MB 的输入文件导入时性能最佳。这是因为 TiDB Cloud 可以并行处理多个文件，从而大幅提升导入速度。

2. 按如下方式命名 Parquet 文件：

    - 如果一个 Parquet 文件包含整个表的所有数据，文件名应采用 `${db_name}.${table_name}.parquet` 格式，导入时会映射到 `${db_name}.${table_name}` 表。
    - 如果一个表的数据被拆分为多个 Parquet 文件，应为这些文件添加数字后缀。例如，`${db_name}.${table_name}.000001.parquet` 和 `${db_name}.${table_name}.000002.parquet`。数字后缀可以不连续，但必须为正序，并且需要在数字前补零以保证所有后缀长度一致。

    > **注意：**
    >
    > - 如果在某些场景下无法按照上述规则修改 Parquet 文件名（例如这些文件链接也被其他程序使用），你可以保持文件名不变，并在 [步骤 4](#step-4-import-parquet-files-to-tidb-cloud) 的 **Mapping Settings** 中将源数据导入到单一目标表。
    > - Snappy 压缩文件必须采用 [官方 Snappy 格式](https://github.com/google/snappy)。不支持其他 Snappy 压缩变体。

## 步骤 2. 创建目标表结构

由于 Parquet 文件不包含表结构信息，在将 Parquet 文件数据导入 TiDB Cloud 之前，你需要通过以下任一方法创建表结构：

- 方法 1：在 TiDB Cloud 中为源数据创建目标数据库和表。

- 方法 2：在存放 Parquet 文件的 Amazon S3、GCS 或 Azure Blob Storage 目录下，为源数据创建目标表结构文件，具体如下：

    1. 为源数据创建数据库结构文件。

        如果你的 Parquet 文件遵循 [步骤 1](#step-1-prepare-the-parquet-files) 的命名规则，则数据库结构文件对于数据导入来说是可选的。否则，数据库结构文件是必需的。

        每个数据库结构文件必须采用 `${db_name}-schema-create.sql` 格式，并包含一个 `CREATE DATABASE` DDL 语句。通过该文件，TiDB Cloud 会在导入数据时创建 `${db_name}` 数据库以存储你的数据。

        例如，如果你创建了一个包含如下语句的 `mydb-schema-create.sql` 文件，TiDB Cloud 会在导入数据时创建 `mydb` 数据库。

        ```sql
        CREATE DATABASE mydb;
        ```

    2. 为源数据创建表结构文件。

        如果你没有在 Parquet 文件所在的 Amazon S3、GCS 或 Azure Blob Storage 目录下包含表结构文件，TiDB Cloud 在导入数据时不会为你创建对应的表。

        每个表结构文件必须采用 `${db_name}.${table_name}-schema.sql` 格式，并包含一个 `CREATE TABLE` DDL 语句。通过该文件，TiDB Cloud 会在 `${db_name}` 数据库中创建 `${db_table}` 表以存储你的数据。

        例如，如果你创建了一个包含如下语句的 `mydb.mytable-schema.sql` 文件，TiDB Cloud 会在导入数据时在 `mydb` 数据库中创建 `mytable` 表。

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注意：**
        >
        > 每个 `${db_name}.${table_name}-schema.sql` 文件只能包含一个 DDL 语句。如果文件中包含多个 DDL 语句，只有第一个会生效。

## 步骤 3. 配置跨账户访问

为了让 TiDB Cloud 能够访问 Amazon S3、GCS 或 Azure Blob Storage 中的 Parquet 文件，请按如下方式操作：

- 如果你的 Parquet 文件位于 Amazon S3，请[配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

    你可以使用 AWS 访问密钥或 Role ARN 访问你的 bucket。完成后，请记录访问密钥（包括访问密钥 ID 和密钥）或 Role ARN 值，后续在 [步骤 4](#step-4-import-parquet-files-to-tidb-cloud) 中会用到。

- 如果你的 Parquet 文件位于 GCS，请[配置 GCS 访问](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

- 如果你的 Parquet 文件位于 Azure Blob Storage，请[配置 Azure Blob Storage 访问](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

## 步骤 4. 将 Parquet 文件导入 TiDB Cloud

要将 Parquet 文件导入 TiDB Cloud，请按以下步骤操作：

<SimpleTab>
<div label="Amazon S3">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入概览页面，然后点击左侧导航栏的 **Data** > **Import**。

2. 选择 **Import data from Cloud Storage**。

3. 在 **Import Data from Amazon S3** 页面，填写以下信息：

    - **Included Schema Files**：如果源文件夹包含目标表结构文件（如 `${db_name}-schema-create.sql`），请选择 **Yes**，否则选择 **No**。
    - **Data Format**：选择 **Parquet**。
    - **Folder URI**：输入源文件夹的 URI，格式为 `s3://[bucket_name]/[data_source_folder]/`，路径必须以 `/` 结尾。例如：`s3://sampledata/ingest/`。
    - **Bucket Access**：你可以使用 AWS IAM role ARN 或 AWS 访问密钥访问你的 bucket。
        - **AWS Role ARN**（推荐）：输入 AWS IAM role ARN。如果你还没有为 bucket 创建 IAM role，可以点击 **Click here to create new one with AWS CloudFormation**，按照屏幕上的指引使用 AWS CloudFormation 模板创建。你也可以手动为 bucket 创建 IAM role ARN。
        - **AWS Access Key**：输入 AWS 访问密钥 ID 和 AWS 密钥。
        - 两种方式的详细说明见 [配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

4. 点击 **Connect**。

5. 在 **Destination** 部分，选择目标数据库和表。

    导入多个文件时，你可以通过 **Advanced Settings** > **Mapping Settings** 自定义每个目标表与其对应 Parquet 文件的映射。对于每个目标数据库和表：

    - **Target Database**：从列表中选择对应的数据库名。
    - **Target Table**：从列表中选择对应的表名。
    - **Source File URIs and Names**：输入源文件的完整 URI，包括文件夹和文件名，格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].parquet`。例如：`s3://sampledata/ingest/TableName.01.parquet`。你也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `s3://[bucket_name]/[data_source_folder]/my-data1.parquet`：`[data_source_folder]` 下名为 `my-data1.parquet` 的单个 Parquet 文件将被导入到目标表。
        - `s3://[bucket_name]/[data_source_folder]/my-data?.parquet`：`[data_source_folder]` 下所有以 `my-data` 开头、后跟一个字符（如 `my-data1.parquet` 和 `my-data2.parquet`）的 Parquet 文件将被导入到同一个目标表。
        - `s3://[bucket_name]/[data_source_folder]/my-data*.parquet`：`[data_source_folder]` 下所有以 `my-data` 开头（如 `my-data10.parquet` 和 `my-data100.parquet`）的 Parquet 文件将被导入到同一个目标表。

6. 点击 **Start Import**。

7. 当导入进度显示 **Completed** 时，检查已导入的表。

</div>

<div label="Google Cloud">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入概览页面，然后点击左侧导航栏的 **Data** > **Import**。

2. 选择 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，为源 Parquet 文件填写以下信息：

    - **Included Schema Files**：如果源文件夹包含目标表结构文件（如 `${db_name}-schema-create.sql`），请选择 **Yes**，否则选择 **No**。
    - **Data Format**：选择 **Parquet**。
    - **Folder URI**：输入源文件夹的 URI，格式为 `gs://[bucket_name]/[data_source_folder]/`，路径必须以 `/` 结尾。例如：`gs://sampledata/ingest/`。
    - **Google Cloud Service Account ID**：TiDB Cloud 会在该页面提供一个唯一的 Service Account ID（如 `example-service-account@your-project.iam.gserviceaccount.com`）。你必须在 Google Cloud 项目中为该 Service Account ID 授予必要的 IAM 权限（如 “Storage Object Viewer”）以访问你的 GCS bucket。更多信息见 [配置 GCS 访问](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

4. 点击 **Connect**。

5. 在 **Destination** 部分，选择目标数据库和表。

    导入多个文件时，你可以通过 **Advanced Settings** > **Mapping Settings** 自定义每个目标表与其对应 Parquet 文件的映射。对于每个目标数据库和表：

    - **Target Database**：从列表中选择对应的数据库名。
    - **Target Table**：从列表中选择对应的表名。
    - **Source File URIs and Names**：输入源文件的完整 URI，包括文件夹和文件名，格式为 `gs://[bucket_name]/[data_source_folder]/[file_name].parquet`。例如：`gs://sampledata/ingest/TableName.01.parquet`。你也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `gs://[bucket_name]/[data_source_folder]/my-data1.parquet`：`[data_source_folder]` 下名为 `my-data1.parquet` 的单个 Parquet 文件将被导入到目标表。
        - `gs://[bucket_name]/[data_source_folder]/my-data?.parquet`：`[data_source_folder]` 下所有以 `my-data` 开头、后跟一个字符（如 `my-data1.parquet` 和 `my-data2.parquet`）的 Parquet 文件将被导入到同一个目标表。
        - `gs://[bucket_name]/[data_source_folder]/my-data*.parquet`：`[data_source_folder]` 下所有以 `my-data` 开头（如 `my-data10.parquet` 和 `my-data100.parquet`）的 Parquet 文件将被导入到同一个目标表。

6. 点击 **Start Import**。

7. 当导入进度显示 **Completed** 时，检查已导入的表。

</div>

<div label="Azure Blob Storage">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入概览页面，然后点击左侧导航栏的 **Data** > **Import**。

2. 选择 **Import data from Cloud Storage**。

3. 在 **Import Data from Azure Blob Storage** 页面，填写以下信息：

    - **Included Schema Files**：如果源文件夹包含目标表结构文件（如 `${db_name}-schema-create.sql`），请选择 **Yes**，否则选择 **No**。
    - **Data Format**：选择 **Parquet**。
    - **Connectivity Method**：选择 TiDB Cloud 连接 Azure Blob Storage 的方式：

        - **Public**（默认）：通过公网连接。当存储账户允许公网访问时使用此选项。
        - **Private Link**：通过 Azure 私有终端节点进行网络隔离访问。当存储账户禁止公网访问或安全策略要求私有连接时使用此选项。如果选择 **Private Link**，还需填写 **Azure Blob Storage Resource ID**。查找 Resource ID 的方法如下：
            
            1. 进入 [Azure 门户](https://portal.azure.com/)。
            2. 导航到你的存储账户，点击 **Overview** > **JSON View**。
            3. 复制 `id` 属性的值。Resource ID 格式为 `/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<account_name>`。

    - **Folder URI**：输入源文件所在的 Azure Blob Storage URI，格式为 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/`，路径必须以 `/` 结尾。例如：`https://myaccount.blob.core.windows.net/mycontainer/data-ingestion/`。
    - **SAS Token**：输入账户 SAS token，以允许 TiDB Cloud 访问 Azure Blob Storage 容器中的源文件。如果还没有 SAS token，可以点击 **Click here to create a new one with Azure ARM template**，按照屏幕上的指引使用 Azure ARM 模板创建。你也可以手动创建账户 SAS token。更多信息见 [配置 Azure Blob Storage 访问](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

4. 点击 **Connect**。

    如果你选择了 **Private Link** 作为连接方式，TiDB Cloud 会为你的存储账户创建一个私有终端节点。你需要在 Azure 门户中批准该终端节点请求，连接才能继续：

    1. 进入 [Azure 门户](https://portal.azure.com/)，导航到你的存储账户。
    2. 点击 **Networking** > **Private endpoint connections**。
    3. 找到来自 TiDB Cloud 的待审批连接请求，点击 **Approve**。
    4. 返回 [TiDB Cloud 控制台](https://tidbcloud.com/)。终端节点审批通过后，导入向导会自动继续。

    > **注意：**
    >
    > 如果终端节点尚未审批，TiDB Cloud 会显示连接待审批的提示。请在 [Azure 门户](https://portal.azure.com/) 审批请求后重试连接。

5. 在 **Destination** 部分，选择目标数据库和表。

    导入多个文件时，你可以通过 **Advanced Settings** > **Mapping Settings** 自定义每个目标表与其对应 Parquet 文件的映射。对于每个目标数据库和表：

    - **Target Database**：从列表中选择对应的数据库名。
    - **Target Table**：从列表中选择对应的表名。
    - **Source File URIs and Names**：输入源文件的完整 URI，包括文件夹和文件名，格式为 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/[file_name].parquet`。例如：`https://myaccount.blob.core.windows.net/mycontainer/data-ingestion/TableName.01.parquet`。你也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data1.parquet`：`[data_source_folder]` 下名为 `my-data1.parquet` 的单个 Parquet 文件将被导入到目标表。
        - `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data?.parquet`：`[data_source_folder]` 下所有以 `my-data` 开头、后跟一个字符（如 `my-data1.parquet` 和 `my-data2.parquet`）的 Parquet 文件将被导入到同一个目标表。
        - `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data*.parquet`：`[data_source_folder]` 下所有以 `my-data` 开头（如 `my-data10.parquet` 和 `my-data100.parquet`）的 Parquet 文件将被导入到同一个目标表。

6. 点击 **Start Import**。

7. 当导入进度显示 **Completed** 时，检查已导入的表。

</div>

</SimpleTab>

当你运行导入任务时，如果检测到任何不支持或无效的类型转换，TiDB Cloud 会自动终止导入作业并报告导入错误。你可以在 **Status** 字段查看详细信息。

如果遇到导入错误，请按以下步骤操作：

1. 删除部分导入的表。
2. 检查表结构文件，如有错误请修正。
3. 检查 Parquet 文件中的数据类型。

    如果 Parquet 文件包含任何不支持的数据类型（如 `NEST STRUCT`、`ARRAY` 或 `MAP`），你需要使用 [支持的数据类型](#supported-data-types)（如 `STRING`）重新生成 Parquet 文件。

4. 重新尝试导入任务。

## 支持的数据类型

下表列出了可导入到 TiDB Cloud 的 Parquet 支持数据类型。

| Parquet Primitive Type | Parquet Logical Type | Types in TiDB or MySQL |
|---|---|---|
| DOUBLE | DOUBLE | DOUBLE<br />FLOAT |
| FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0) | BIGINT UNSIGNED |
| FIXED_LEN_BYTE_ARRAY(N) | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | N/A | INT<br />MEDIUMINT<br />YEAR |
| INT64 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT64 | N/A | BIGINT<br />INT UNSIGNED<br />MEDIUMINT UNSIGNED |
| INT64 | TIMESTAMP_MICROS | DATETIME<br />TIMESTAMP |
| BYTE_ARRAY | N/A | BINARY<br />BIT<br />BLOB<br />CHAR<br />LINESTRING<br />LONGBLOB<br />MEDIUMBLOB<br />MULTILINESTRING<br />TINYBLOB<br />VARBINARY |
| BYTE_ARRAY | STRING | ENUM<br />DATE<br />DECIMAL<br />GEOMETRY<br />GEOMETRYCOLLECTION<br />JSON<br />LONGTEXT<br />MEDIUMTEXT<br />MULTIPOINT<br />MULTIPOLYGON<br />NUMERIC<br />POINT<br />POLYGON<br />SET<br />TEXT<br />TIME<br />TINYTEXT<br />VARCHAR |
| SMALLINT | N/A | INT32 |
| SMALLINT UNSIGNED | N/A | INT32 |
| TINYINT | N/A | INT32 |
| TINYINT UNSIGNED | N/A | INT32 |

## 故障排查

### 解决数据导入过程中的警告

点击 **Start Import** 后，如果看到类似 `can't find the corresponding source files` 的警告信息，请通过提供正确的源文件、按照 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md)重命名现有文件，或使用 **Advanced Settings** 进行调整来解决。

解决后需要重新导入数据。

### 导入表中行数为零

当导入进度显示 **Completed** 后，检查已导入的表。如果行数为零，说明没有数据文件匹配你输入的 Bucket URI。此时，请通过提供正确的源文件、按照 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md)重命名现有文件，或使用 **Advanced Settings** 进行调整来解决。之后重新导入这些表。