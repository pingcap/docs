---
title: 从云存储导入 CSV 文件到 TiDB Cloud 专属集群
summary: 了解如何将 CSV 文件从 Amazon S3、GCS 或 Azure Blob Storage 导入到 TiDB Cloud 专属集群。
aliases: ['/tidbcloud/migrate-from-amazon-s3-or-gcs','/tidbcloud/migrate-from-aurora-bulk-import']
---

# 从云存储导入 CSV 文件到 TiDB Cloud 专属集群

本文档介绍如何将 CSV 文件从 Amazon Simple Storage Service（Amazon S3）、Google Cloud Storage（GCS）或 Azure Blob Storage 导入到 TiDB Cloud 专属集群。

## 限制

- 为确保数据一致性，TiDB Cloud 仅允许将 CSV 文件导入到空表中。若需将数据导入已存在且包含数据的表，可以按照本文档将数据导入到一个临时空表中，然后使用 `INSERT SELECT` 语句将数据复制到目标已存在的表中。

- 如果 TiDB Cloud 专属集群已开启 [changefeed](/tidb-cloud/changefeed-overview.md) 或已启用 [Point-in-time Restore](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)，则无法向该集群导入数据（**Import Data** 按钮会被禁用），因为当前数据导入功能使用的是 [物理导入模式](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)。在该模式下，导入的数据不会生成变更日志，因此 changefeed 和 Point-in-time Restore 无法检测到导入的数据。

## 第 1 步：准备 CSV 文件

1. 如果单个 CSV 文件大于 256 MB，建议将其拆分为更小的文件，每个文件大小约为 256 MB。

    TiDB Cloud 支持导入非常大的 CSV 文件，但在多个约 256 MB 的输入文件下性能最佳。这是因为 TiDB Cloud 可以并行处理多个文件，从而大幅提升导入速度。

2. 按如下方式命名 CSV 文件：

    - 如果一个 CSV 文件包含整个表的所有数据，文件名应采用 `${db_name}.${table_name}.csv` 格式，导入时会映射到 `${db_name}.${table_name}` 表。
    - 如果一个表的数据被拆分到多个 CSV 文件中，应为这些文件添加数字后缀。例如，`${db_name}.${table_name}.000001.csv` 和 `${db_name}.${table_name}.000002.csv`。数字后缀可以不连续，但必须递增，并且需要在数字前补零以保证所有后缀长度一致。
    - TiDB Cloud 支持导入以下格式的压缩文件：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。如果需要导入压缩的 CSV 文件，文件名应采用 `${db_name}.${table_name}.${suffix}.csv.${compress}` 格式，其中 `${suffix}` 可选，可以是任意整数如 '000001'。例如，若要将 `trips.000001.csv.gz` 文件导入到 `bikeshare.trips` 表，需要将文件重命名为 `bikeshare.trips.000001.csv.gz`。

    > **注意：**
    >
    > - 只需压缩数据文件，无需压缩数据库或表结构文件。
    > - 为获得更好的性能，建议每个压缩文件大小限制在 100 MiB。
    > - Snappy 压缩文件必须为 [官方 Snappy 格式](https://github.com/google/snappy)，不支持其他变体的 Snappy 压缩格式。
    > - 对于未压缩的文件，如果在某些情况下无法按照上述规则修改 CSV 文件名（例如，CSV 文件链接也被其他程序使用），可以保持文件名不变，并在 [第 4 步](#step-4-import-csv-files-to-tidb-cloud) 的 **Mapping Settings** 中将源数据导入到单个目标表。

## 第 2 步：创建目标表结构

由于 CSV 文件不包含表结构信息，在将 CSV 文件中的数据导入 TiDB Cloud 之前，需要通过以下任一方式创建表结构：

- 方法一：在 TiDB Cloud 中为源数据创建目标数据库和数据表。

- 方法二：在存放 CSV 文件的 Amazon S3、GCS 或 Azure Blob Storage 目录下，为源数据创建目标表结构文件，具体如下：

    1. 为源数据创建数据库结构文件。

        如果你的 CSV 文件遵循 [第 1 步](#step-1-prepare-the-csv-files) 的命名规则，则数据库结构文件为可选项，否则为必需项。

        每个数据库结构文件必须采用 `${db_name}-schema-create.sql` 格式，并包含一个 `CREATE DATABASE` DDL 语句。通过该文件，TiDB Cloud 会在导入数据时创建 `${db_name}` 数据库以存储你的数据。

        例如，若你创建了一个包含如下语句的 `mydb-scehma-create.sql` 文件，TiDB Cloud 会在导入数据时创建 `mydb` 数据库。

        
        ```sql
        CREATE DATABASE mydb;
        ```

    2. 为源数据创建表结构文件。

        如果你未在存放 CSV 文件的 Amazon S3、GCS 或 Azure Blob Storage 目录下包含表结构文件，TiDB Cloud 在导入数据时不会为你创建相应的数据表。

        每个表结构文件必须采用 `${db_name}.${table_name}-schema.sql` 格式，并包含一个 `CREATE TABLE` DDL 语句。通过该文件，TiDB Cloud 会在导入数据时于 `${db_name}` 数据库中创建 `${db_table}` 表。

        例如，若你创建了一个包含如下语句的 `mydb.mytable-schema.sql` 文件，TiDB Cloud 会在导入数据时于 `mydb` 数据库中创建 `mytable` 表。

        
        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注意：**
        >
        > 每个 `${db_name}.${table_name}-schema.sql` 文件只能包含一个 DDL 语句。如果文件中包含多个 DDL 语句，仅第一个生效。

## 第 3 步：配置跨账号访问

为了让 TiDB Cloud 能够访问 Amazon S3、GCS 或 Azure Blob Storage 容器中的 CSV 文件，请按以下方式操作：

- 如果你的 CSV 文件位于 Amazon S3，请[配置 Amazon S3 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

    你可以使用 AWS 访问密钥或 Role ARN 访问你的存储桶。完成后，请记录访问密钥（包括访问密钥 ID 和密钥）或 Role ARN 值，后续在 [第 4 步](#step-4-import-csv-files-to-tidb-cloud) 中会用到。

- 如果你的 CSV 文件位于 GCS，请[配置 GCS 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

- 如果你的 CSV 文件位于 Azure Blob Storage，请[配置 Azure Blob Storage 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

## 第 4 步：将 CSV 文件导入 TiDB Cloud

要将 CSV 文件导入 TiDB Cloud，请按照以下步骤操作：

<SimpleTab>
<div label="Amazon S3">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 选择 **Import data from Cloud Storage**。

3. 在 **Import Data from Amazon S3** 页面，填写以下信息：

    - **Included Schema Files**：如果源文件夹包含目标表结构文件（如 `${db_name}-schema-create.sql`），请选择 **Yes**，否则选择 **No**。
    - **Data Format**：选择 **CSV**。
    - **Edit CSV Configuration**：如有需要，根据你的 CSV 文件配置选项。你可以设置分隔符和定界符字符，指定是否使用反斜杠转义字符，以及文件是否包含表头行。
    - **Folder URI**：以 `s3://[bucket_name]/[data_source_folder]/` 格式输入源文件夹 URI，路径必须以 `/` 结尾。例如，`s3://mybucket/myfolder/`。
    - **Bucket Access**：你可以使用 AWS IAM role ARN 或 AWS 访问密钥访问存储桶。
        - **AWS Role ARN**（推荐）：输入 AWS IAM role ARN。如果还没有为存储桶创建 IAM role，可以点击 **Click here to create new one with AWS CloudFormation**，按照屏幕提示使用提供的 AWS CloudFormation 模板创建。也可以手动为存储桶创建 IAM role ARN。
        - **AWS Access Key**：输入 AWS 访问密钥 ID 和 AWS 密钥。
        - 两种方式的详细说明请参见 [配置 Amazon S3 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

4. 点击 **Connect**。

5. 在 **Destination** 部分，选择目标数据库和数据表。

    当导入多个文件时，可以通过 **Advanced Settings** > **Mapping Settings** 自定义各目标表与其对应 CSV 文件的映射。对于每个目标数据库和表：

    - **Target Database**：从列表中选择对应的数据库名。
    - **Target Table**：从列表中选择对应的表名。
    - **Source File URIs and Names**：输入源文件的完整 URI，包括文件夹和文件名，确保格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`。也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `s3://mybucket/myfolder/my-data1.csv`：`myfolder` 下名为 `my-data1.csv` 的单个 CSV 文件将被导入到目标表。
        - `s3://mybucket/myfolder/my-data?.csv`：`myfolder` 下所有以 `my-data` 开头、后跟一个字符（如 `my-data1.csv` 和 `my-data2.csv`）的 CSV 文件将被导入到同一个目标表。
        - `s3://mybucket/myfolder/my-data*.csv`：`myfolder` 下所有以 `my-data` 开头（如 `my-data10.csv` 和 `my-data100.csv`）的 CSV 文件将被导入到同一个目标表。

6. 点击 **Start Import**。

7. 当导入进度显示 **Completed** 时，检查已导入的数据表。

</div>

<div label="Google Cloud">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 选择 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，为源 CSV 文件填写以下信息：

    - **Included Schema Files**：如果源文件夹包含目标表结构文件（如 `${db_name}-schema-create.sql`），请选择 **Yes**，否则选择 **No**。
    - **Data Format**：选择 **CSV**。
    - **Edit CSV Configuration**：如有需要，根据你的 CSV 文件配置选项。你可以设置分隔符和定界符字符，指定是否使用反斜杠转义字符，以及文件是否包含表头行。
    - **Folder URI**：以 `gs://[bucket_name]/[data_source_folder]/` 格式输入源文件夹 URI，路径必须以 `/` 结尾。例如，`gs://sampledata/ingest/`。
    - **Google Cloud Service Account ID**：TiDB Cloud 会在此页面提供一个唯一的 Service Account ID（如 `example-service-account@your-project.iam.gserviceaccount.com`）。你必须在 Google Cloud 项目中为该 Service Account ID 授予所需的 IAM 权限（如 "Storage Object Viewer"）以访问你的 GCS 存储桶。更多信息请参见 [配置 GCS 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

4. 点击 **Connect**。

5. 在 **Destination** 部分，选择目标数据库和数据表。

    当导入多个文件时，可以通过 **Advanced Settings** > **Mapping Settings** 自定义各目标表与其对应 CSV 文件的映射。对于每个目标数据库和表：

    - **Target Database**：从列表中选择对应的数据库名。
    - **Target Table**：从列表中选择对应的表名。
    - **Source File URIs and Names**：输入源文件的完整 URI，包括文件夹和文件名，确保格式为 `gs://[bucket_name]/[data_source_folder]/[file_name].csv`。也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `gs://mybucket/myfolder/my-data1.csv`：`myfolder` 下名为 `my-data1.csv` 的单个 CSV 文件将被导入到目标表。
        - `gs://mybucket/myfolder/my-data?.csv`：`myfolder` 下所有以 `my-data` 开头、后跟一个字符（如 `my-data1.csv` 和 `my-data2.csv`）的 CSV 文件将被导入到同一个目标表。
        - `gs://mybucket/myfolder/my-data*.csv`：`myfolder` 下所有以 `my-data` 开头（如 `my-data10.csv` 和 `my-data100.csv`）的 CSV 文件将被导入到同一个目标表。

6. 点击 **Start Import**。

7. 当导入进度显示 **Completed** 时，检查已导入的数据表。

</div>

<div label="Azure Blob Storage">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 选择 **Import data from Cloud Storage**。

3. 在 **Import Data from Azure Blob Storage** 页面，填写以下信息：

    - **Included Schema Files**：如果源文件夹包含目标表结构文件（如 `${db_name}-schema-create.sql`），请选择 **Yes**，否则选择 **No**。
    - **Data Format**：选择 **CSV**。
    - **Edit CSV Configuration**：如有需要，根据你的 CSV 文件配置选项。你可以设置分隔符和定界符字符，指定是否使用反斜杠转义字符，以及文件是否包含表头行。
    - **Folder URI**：以 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/` 格式输入存放源文件的 Azure Blob Storage URI，路径必须以 `/` 结尾。例如，`https://myaccount.blob.core.windows.net/mycontainer/myfolder/`。
    - **SAS Token**：输入账户 SAS token，以允许 TiDB Cloud 访问 Azure Blob Storage 容器中的源文件。如果还没有 SAS token，可以点击 **Click here to create a new one with Azure ARM template**，按照屏幕提示使用提供的 Azure ARM 模板创建。也可以手动创建账户 SAS token。更多信息请参见 [配置 Azure Blob Storage 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

4. 点击 **Connect**。

5. 在 **Destination** 部分，选择目标数据库和数据表。

    当导入多个文件时，可以通过 **Advanced Settings** > **Mapping Settings** 自定义各目标表与其对应 CSV 文件的映射。对于每个目标数据库和表：

    - **Target Database**：从列表中选择对应的数据库名。
    - **Target Table**：从列表中选择对应的表名。
    - **Source File URIs and Names**：输入源文件的完整 URI，包括文件夹和文件名，确保格式为 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/[file_name].csv`。也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `https://myaccount.blob.core.windows.net/mycontainer/myfolder/my-data1.csv`：`myfolder` 下名为 `my-data1.csv` 的单个 CSV 文件将被导入到目标表。
        - `https://myaccount.blob.core.windows.net/mycontainer/myfolder/my-data?.csv`：`myfolder` 下所有以 `my-data` 开头、后跟一个字符（如 `my-data1.csv` 和 `my-data2.csv`）的 CSV 文件将被导入到同一个目标表。
        - `https://myaccount.blob.core.windows.net/mycontainer/myfolder/my-data*.csv`：`myfolder` 下所有以 `my-data` 开头（如 `my-data10.csv` 和 `my-data100.csv`）的 CSV 文件将被导入到同一个目标表。

6. 点击 **Start Import**。

7. 当导入进度显示 **Completed** 时，检查已导入的数据表。

</div>

</SimpleTab>

当你运行导入任务时，如果检测到任何不支持或无效的类型转换，TiDB Cloud 会自动终止导入作业并报告导入错误。你可以在 **Status** 字段查看详细信息。

如果遇到导入错误，请按以下步骤操作：

1. 删除部分导入的表。
2. 检查表结构文件，如有错误请修正。
3. 检查 CSV 文件中的数据类型。
4. 重新尝试导入任务。

## 故障排查

### 解决数据导入过程中的警告

点击 **Start Import** 后，如果看到如 `can't find the corresponding source files` 的警告信息，请通过提供正确的源文件、根据 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或使用 **Advanced Settings** 进行调整来解决。

解决后需要重新导入数据。

### 导入表中行数为零

当导入进度显示 **Completed** 后，检查已导入的数据表。如果行数为零，说明没有数据文件匹配你输入的 Bucket URI。此时，请通过提供正确的源文件、根据 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或使用 **Advanced Settings** 进行调整来解决。之后请重新导入这些表。