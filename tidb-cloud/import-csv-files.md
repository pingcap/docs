---
title: 从云存储导入 CSV 文件到 TiDB Cloud Dedicated
summary: 了解如何将 CSV 文件从 Amazon S3、GCS 或 Azure Blob Storage 导入到 TiDB Cloud Dedicated。
aliases: ['/zh/tidbcloud/migrate-from-amazon-s3-or-gcs','/zh/tidbcloud/migrate-from-aurora-bulk-import']
---

# 从云存储导入 CSV 文件到 TiDB Cloud Dedicated

本文档介绍如何将 CSV 文件从 Amazon Simple Storage Service（Amazon S3）、Google Cloud Storage（GCS）或 Azure Blob Storage 导入到 TiDB Cloud Dedicated。

> **提示：**
>
> 对于 TiDB Cloud Starter 或 TiDB Cloud Essential，请参见[从云存储导入 CSV 文件到 TiDB Cloud Starter 或 Essential](/tidb-cloud/import-csv-files-serverless.md)。

## 限制

- 为保证数据一致性，TiDB Cloud 仅允许将 CSV 文件导入到空表中。若需将数据导入已存在且包含数据的表，可以按照本文档的步骤，先将数据导入到一个临时空表，再通过 `INSERT SELECT` 语句将数据复制到目标已存在的表中。

- 如果 TiDB Cloud Dedicated 集群已开启 [changefeed](/tidb-cloud/changefeed-overview.md) 或已启用 [Point-in-time Restore](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)，则无法向该集群导入数据（**Import Data** 按钮会被禁用），因为当前数据导入功能使用的是 [物理导入模式](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)。在该模式下，导入的数据不会生成变更日志，因此 changefeed 和 Point-in-time Restore 无法检测到导入的数据。

## 第 1 步：准备 CSV 文件

1. 如果单个 CSV 文件大于 256 MiB，建议将其切分为更小的文件，每个文件大小约为 256 MiB。

    TiDB Cloud 支持导入非常大的 CSV 文件，但在多个约 256 MiB 的输入文件时性能最佳。这是因为 TiDB Cloud 可以并行处理多个文件，从而大幅提升导入速度。

2. 按如下方式命名 CSV 文件：

    - 如果一个 CSV 文件包含整个表的所有数据，文件名应采用 `${db_name}.${table_name}.csv` 格式，导入时会映射到 `${db_name}.${table_name}` 表。
    - 如果一个表的数据被拆分为多个 CSV 文件，应在这些文件名后添加数字后缀。例如，`${db_name}.${table_name}.000001.csv` 和 `${db_name}.${table_name}.000002.csv`。数字后缀可以不连续，但必须为正序。还需在数字前补零，确保所有后缀长度一致。
    - TiDB Cloud 支持导入以下格式的压缩文件：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。如需导入压缩的 CSV 文件，文件名应采用 `${db_name}.${table_name}.${suffix}.csv.${compress}` 格式，其中 `${suffix}` 可选，可为任意整数（如 '000001'）。例如，若需将 `trips.000001.csv.gz` 文件导入到 `bikeshare.trips` 表，需要将文件重命名为 `bikeshare.trips.000001.csv.gz`。

    > **注意：**
    >
    > - 只需压缩数据文件，无需压缩数据库或表结构文件。
    > - 为获得更好的性能，建议每个压缩文件大小不超过 100 MiB。
    > - Snappy 压缩文件必须为 [官方 Snappy 格式](https://github.com/google/snappy)。不支持其他变体的 Snappy 压缩格式。
    > - 对于未压缩的文件，如果无法按上述规则修改 CSV 文件名（例如，CSV 文件链接也被其他程序使用），可以保持文件名不变，并在[第 4 步](#step-4-import-csv-files-to-tidb-cloud)的 **Destination Mapping** 步骤中取消选中 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping**，然后手动将源文件映射到单个目标表。

## 第 2 步：创建目标表结构

由于 CSV 文件不包含表结构信息，在将 CSV 文件数据导入 TiDB Cloud 前，需要通过以下任一方法创建表结构：

- 方法 1：在 TiDB Cloud 中，为源数据创建目标数据库和表。

- 方法 2：在存放 CSV 文件的 Amazon S3、GCS 或 Azure Blob Storage 目录下，为源数据创建目标表结构文件，具体如下：

    1. 为源数据创建数据库结构文件。

        如果你的 CSV 文件遵循 [第 1 步](#step-1-prepare-the-csv-files) 的命名规则，则数据库结构文件为可选，否则为必需。

        每个数据库结构文件必须采用 `${db_name}-schema-create.sql` 格式，并包含 `CREATE DATABASE` DDL 语句。通过该文件，TiDB Cloud 会在导入数据时创建 `${db_name}` 数据库以存储数据。

        例如，若创建了包含如下语句的 `mydb-schema-create.sql` 文件，TiDB Cloud 会在导入数据时创建 `mydb` 数据库。

        
        ```sql
        CREATE DATABASE mydb;
        ```

    2. 为源数据创建表结构文件。

        如果未在存放 CSV 文件的 Amazon S3、GCS 或 Azure Blob Storage 目录下包含表结构文件，TiDB Cloud 在导入数据时不会为你创建对应的表。

        每个表结构文件必须采用 `${db_name}.${table_name}-schema.sql` 格式，并包含 `CREATE TABLE` DDL 语句。通过该文件，TiDB Cloud 会在 `${db_name}` 数据库中创建 `${db_table}` 表以存储数据。

        例如，若创建了包含如下语句的 `mydb.mytable-schema.sql` 文件，TiDB Cloud 会在导入数据时在 `mydb` 数据库中创建 `mytable` 表。

        
        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注意：**
        >
        > 每个 `${db_name}.${table_name}-schema.sql` 文件只能包含一条 DDL 语句。如果文件中有多条 DDL 语句，仅第一条生效。

## 第 3 步：配置跨账户访问

为允许 TiDB Cloud 访问 Amazon S3 bucket、GCS bucket 或 Azure Blob Storage container 中的 CSV 文件，请按以下方式操作：

- 如果 CSV 文件位于 Amazon S3，请[配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

    你可以使用 AWS 访问密钥或 Role ARN 访问 bucket。完成后，请记录访问密钥（包括 access key ID 和 secret access key）或 Role ARN 值，后续在 [第 4 步](#step-4-import-csv-files-to-tidb-cloud) 中需要用到。

- 如果 CSV 文件位于 GCS，请[配置 GCS 访问](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

- 如果 CSV 文件位于 Azure Blob Storage，请[配置 Azure Blob Storage 访问](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

## 第 4 步：将 CSV 文件导入 TiDB Cloud

要将 CSV 文件导入 TiDB Cloud，请按以下步骤操作：

<SimpleTab>
<div label="Amazon S3">

1. 打开目标 TiDB Cloud Dedicated 集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **提示：**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群名称进入概览页，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，填写以下信息：

    - **Storage Provider**：选择 **Amazon S3**。
    - **Source URI**：
        - 导入单个文件时，输入源文件 URI，格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`s3://mybucket/myfolder/TableName.01.csv`。
        - 导入多个文件时，输入源文件夹 URI，格式为 `s3://[bucket_name]/[data_source_folder]/`。例如，`s3://mybucket/myfolder/`。
    - **Credentials**：你可以使用 AWS Role ARN 或 AWS 访问密钥访问 bucket。详细信息请参见[配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。
        - **AWS Role ARN**（推荐）：输入 AWS Role ARN 值。如果你还没有 Role ARN，可以点击 **Click here to create new one with AWS CloudFormation** 并按照屏幕上的说明操作，或者在对话框中展开 **Having trouble? Create Role ARN manually**，获取集群的 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID**，然后手动创建 IAM role。
        - **AWS Access Key**：输入 AWS access key ID 和 AWS secret access key。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，指定如何将源文件映射到目标表。

    当你在 **Source URI** 中指定目录时，TiDB Cloud 默认选中 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项。

    > **注意：**
    >
    > 当你在 **Source URI** 中指定单个文件时，TiDB Cloud 不会显示 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，并会自动将文件名填入 **Source** 字段。在这种情况下，你只需输入用于导入数据的目标数据库和表。

    - 若要让 TiDB Cloud 自动将所有符合 [TiDB 文件命名规范](/tidb-cloud/naming-conventions-for-data-import.md)的源文件映射到对应的表，请保持选中此选项，并选择 **CSV** 作为数据格式。如果源文件夹中包含 schema 文件（例如 `${db_name}-schema-create.sql` 和 `${db_name}.${table_name}-schema.sql`），TiDB Cloud 会在目标数据库和表不存在时使用这些文件创建它们。

    - 若要手动配置映射规则，将源 CSV 文件关联到目标数据库和表，请取消选中此选项，然后填写以下字段：

        - **Source**：输入文件名模式，格式为 `[file_name].csv`。例如，`TableName.01.csv`。你也可以使用通配符匹配多个文件。TiDB Cloud 仅支持 `*` 和 `?` 通配符。

            - `my-data?.csv`：匹配所有以 `my-data` 开头、后跟单个字符的 CSV 文件，例如 `my-data1.csv` 和 `my-data2.csv`。
            - `my-data*.csv`：匹配所有以 `my-data` 开头的 CSV 文件，例如 `my-data-2023.csv` 和 `my-data-final.csv`。

        - **Target Database** 和 **Target Table**：输入要将数据导入到的目标数据库和表。

    如有需要，点击 **Edit CSV Configuration** 根据你的 CSV 文件配置选项。你可以设置分隔符和定界符字符，指定是否使用反斜杠转义字符，以及文件是否包含表头行。

6. 点击 **Next**。TiDB Cloud 会扫描源文件。

7. 查看扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查已导入的表。

</div>

<div label="Google Cloud">

1. 打开目标 TiDB Cloud Dedicated 集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **提示：**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群名称进入概览页，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，填写以下信息：

    - **Storage Provider**：选择 **Google Cloud Storage**。
    - **Source URI**：
        - 导入单个文件时，输入源文件 URI，格式为 `gs://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`gs://mybucket/myfolder/TableName.01.csv`。
        - 导入多个文件时，输入源文件夹 URI，格式为 `gs://[bucket_name]/[data_source_folder]/`。例如，`gs://mybucket/myfolder/`。
    - **Google Cloud Service Account ID**：TiDB Cloud 会在此页面提供唯一的 Google Cloud Service Account ID（如 `example-service-account@your-project.iam.gserviceaccount.com`）。请在 Google Cloud 项目中为该 Service Account ID 授予 GCS bucket 所需的 IAM 权限（例如 `Storage Object Viewer`）。详细信息请参见[配置 GCS 访问](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，指定如何将源文件映射到目标表。

    当你在 **Source URI** 中指定目录时，TiDB Cloud 默认选中 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项。

    > **注意：**
    >
    > 当你在 **Source URI** 中指定单个文件时，TiDB Cloud 不会显示 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，并会自动将文件名填入 **Source** 字段。在这种情况下，你只需输入用于导入数据的目标数据库和表。

    - 若要让 TiDB Cloud 自动将所有符合 [TiDB 文件命名规范](/tidb-cloud/naming-conventions-for-data-import.md)的源文件映射到对应的表，请保持选中此选项，并选择 **CSV** 作为数据格式。如果源文件夹中包含 schema 文件（例如 `${db_name}-schema-create.sql` 和 `${db_name}.${table_name}-schema.sql`），TiDB Cloud 会在目标数据库和表不存在时使用这些文件创建它们。

    - 若要手动配置映射规则，将源 CSV 文件关联到目标数据库和表，请取消选中此选项，然后填写以下字段：

        - **Source**：输入文件名模式，格式为 `[file_name].csv`。例如，`TableName.01.csv`。你也可以使用通配符匹配多个文件。TiDB Cloud 仅支持 `*` 和 `?` 通配符。

            - `my-data?.csv`：匹配所有以 `my-data` 开头、后跟单个字符的 CSV 文件，例如 `my-data1.csv` 和 `my-data2.csv`。
            - `my-data*.csv`：匹配所有以 `my-data` 开头的 CSV 文件，例如 `my-data-2023.csv` 和 `my-data-final.csv`。

        - **Target Database** 和 **Target Table**：输入要将数据导入到的目标数据库和表。

    如有需要，点击 **Edit CSV Configuration** 根据你的 CSV 文件配置选项。你可以设置分隔符和定界符字符，指定是否使用反斜杠转义字符，以及文件是否包含表头行。

6. 点击 **Next**。TiDB Cloud 会扫描源文件。

7. 查看扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查已导入的表。

</div>

<div label="Azure Blob Storage">

1. 打开目标 TiDB Cloud Dedicated 集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **提示：**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群名称进入概览页，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，填写以下信息：

    - **Storage Provider**：选择 **Azure Blob Storage**。
    - **Source URI**：
        - 导入单个文件时，输入源文件 URI，格式为 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/[file_name].csv`。例如，`https://myaccount.blob.core.windows.net/mycontainer/myfolder/TableName.01.csv`。
        - 导入多个文件时，输入源文件夹 URI，格式为 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/`。例如，`https://myaccount.blob.core.windows.net/mycontainer/myfolder/`。
    - **Connectivity Method**：选择 TiDB Cloud 连接 Azure Blob Storage 的方式：

        - **Public**（默认）：通过公网连接。当存储账户允许公网访问时使用此选项。
        - **Private Link**：通过 Azure 私有终端节点进行网络隔离访问。当存储账户禁止公网访问或安全策略要求私有连接时使用此选项。若选择 **Private Link**，还需填写 **Azure Blob Storage Resource ID**。查找 Resource ID 的方法如下：

            1. 进入 [Azure 门户](https://portal.azure.com/)。
            2. 导航到你的存储账户，点击 **Overview** > **JSON View**。
            3. 复制 `id` 属性的值。Resource ID 格式为 `/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<account_name>`。

    - **SAS Token**：输入账户 SAS token，以允许 TiDB Cloud 访问 Azure Blob Storage container 中的源文件。如果你还没有 SAS token，可以点击 **Click here to create a new one with Azure ARM template** 并按照屏幕上的说明操作，或者手动创建账户 SAS token。详细信息请参见[配置 Azure Blob Storage 访问](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

4. 点击 **Next**。

    如果选择了 **Private Link** 作为连接方式，TiDB Cloud 会为你的存储账户创建私有终端节点。你需要在 Azure 门户中批准该终端节点请求，向导才能继续：

    1. 进入 [Azure 门户](https://portal.azure.com/)，导航到你的存储账户。
    2. 点击 **Networking** > **Private endpoint connections**。
    3. 找到来自 TiDB Cloud 的待处理连接请求，点击 **Approve**。
    4. 返回 [TiDB Cloud 控制台](https://tidbcloud.com/)。终端节点批准后，导入向导会自动继续。

    > **注意：**
    >
    > 若终端节点尚未批准，TiDB Cloud 会显示连接待批准的提示。请在 [Azure 门户](https://portal.azure.com/) 批准请求后重试。

5. 在 **Destination Mapping** 部分，指定如何将源文件映射到目标表。

    当你在 **Source URI** 中指定目录时，TiDB Cloud 默认选中 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项。

    > **注意：**
    >
    > 当你在 **Source URI** 中指定单个文件时，TiDB Cloud 不会显示 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，并会自动将文件名填入 **Source** 字段。在这种情况下，你只需输入用于导入数据的目标数据库和表。

    - 若要让 TiDB Cloud 自动将所有符合 [TiDB 文件命名规范](/tidb-cloud/naming-conventions-for-data-import.md)的源文件映射到对应的表，请保持选中此选项，并选择 **CSV** 作为数据格式。如果源文件夹中包含 schema 文件（例如 `${db_name}-schema-create.sql` 和 `${db_name}.${table_name}-schema.sql`），TiDB Cloud 会在目标数据库和表不存在时使用这些文件创建它们。

    - 若要手动配置映射规则，将源 CSV 文件关联到目标数据库和表，请取消选中此选项，然后填写以下字段：

        - **Source**：输入文件名模式，格式为 `[file_name].csv`。例如，`TableName.01.csv`。你也可以使用通配符匹配多个文件。TiDB Cloud 仅支持 `*` 和 `?` 通配符。

            - `my-data?.csv`：匹配所有以 `my-data` 开头、后跟单个字符的 CSV 文件，例如 `my-data1.csv` 和 `my-data2.csv`。
            - `my-data*.csv`：匹配所有以 `my-data` 开头的 CSV 文件，例如 `my-data-2023.csv` 和 `my-data-final.csv`。

        - **Target Database** 和 **Target Table**：输入要将数据导入到的目标数据库和表。

    如有需要，点击 **Edit CSV Configuration** 根据你的 CSV 文件配置选项。你可以设置分隔符和定界符字符，指定是否使用反斜杠转义字符，以及文件是否包含表头行。

6. 点击 **Next**。TiDB Cloud 会扫描源文件。

7. 查看扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查已导入的表。

</div>

</SimpleTab>

当你运行导入任务时，如果检测到任何不支持或无效的转换，TiDB Cloud 会自动终止导入作业并报告导入错误。你可以在 **Status** 字段查看详细信息。

如果遇到导入错误，请按以下步骤操作：

1. 删除部分导入的表。
2. 检查表结构文件，如有错误请修正。
3. 检查 CSV 文件中的数据类型。
4. 重新尝试导入任务。

## 故障排查

### 解决数据导入过程中的警告

如果在 **Pre-check** 步骤中看到如 `can't find the corresponding source files` 的警告，请通过提供正确的源文件、按 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或返回 **Destination Mapping** 步骤并切换为手动映射规则来解决。

解决这些问题后，返回向导并重新运行导入。

### 导入表中行数为零

当导入进度显示 **Completed** 后，检查已导入的表。如果行数为零，说明没有数据文件匹配你输入的源 URI。此时，请通过提供正确的源文件、按 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或返回 **Destination Mapping** 步骤并切换为手动映射规则来解决。之后重新导入这些表。
