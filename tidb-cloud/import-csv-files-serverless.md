---
title: 从云存储导入 CSV 文件到 TiDB Cloud Starter 或 Essential
summary: 了解如何将 CSV 文件从 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务（OSS）导入到 TiDB Cloud Starter 或 TiDB Cloud Essential。
---

# 从云存储导入 CSV 文件到 TiDB Cloud Starter 或 Essential

本文档介绍如何将 CSV 文件从 Amazon Simple Storage Service（Amazon S3）、Google Cloud Storage（GCS）、Azure Blob Storage 或阿里云对象存储服务（OSS）导入到 TiDB Cloud Starter 或 TiDB Cloud Essential。

> **Note:**
>
> 关于 TiDB Cloud Dedicated，请参见 [从云存储导入 CSV 文件到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)。

## 限制

- 为保证数据一致性，TiDB Cloud 仅允许将 CSV 文件导入到空表中。若需将数据导入到已存在且包含数据的表中，你可以按照本文档的方式先将数据导入到一个临时空表，然后使用 `INSERT SELECT` 语句将数据复制到目标表。

## 第 1 步：准备 CSV 文件

1. 如果单个 CSV 文件大于 256 MiB，建议将其拆分为多个小文件，每个文件大小约为 256 MiB。

    TiDB Cloud 支持导入非常大的 CSV 文件，但在多个约 256 MiB 的输入文件时性能最佳。这是因为 TiDB Cloud 可以并行处理多个文件，从而大幅提升导入速度。

2. 按如下方式命名 CSV 文件：

    - 如果一个 CSV 文件包含了整个表的所有数据，文件名应采用 `${db_name}.${table_name}.csv` 格式，导入时会映射到 `${db_name}.${table_name}` 表。
    - 如果一个表的数据被拆分为多个 CSV 文件，应在这些文件名后添加数字后缀。例如，`${db_name}.${table_name}.000001.csv` 和 `${db_name}.${table_name}.000002.csv`。数字后缀可以不连续，但必须递增，并且需要在数字前补零以保证所有后缀长度一致。
    - TiDB Cloud 支持导入以下格式的压缩文件：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。如果你需要导入压缩的 CSV 文件，文件名应采用 `${db_name}.${table_name}.${suffix}.csv.${compress}` 格式，其中 `${suffix}` 可选，可以是任意整数如 '000001'。例如，如果你想将 `trips.000001.csv.gz` 文件导入到 `bikeshare.trips` 表，需要将文件重命名为 `bikeshare.trips.000001.csv.gz`。

    > **Note:**
    >
    > - 为获得更好的性能，建议每个压缩文件大小不超过 100 MiB。
    > - Snappy 压缩文件必须为 [官方 Snappy 格式](https://github.com/google/snappy)。不支持其他 Snappy 压缩变体。
    > - 对于未压缩的文件，如果你在某些情况下无法按照上述规则修改 CSV 文件名（例如这些 CSV 文件链接也被其他程序使用），可以保持文件名不变，并在 [第 4 步](#step-4-import-csv-files) 的 **Mapping Settings** 中将源数据导入到单一目标表。

## 第 2 步：创建目标表结构

由于 CSV 文件不包含表结构信息，在将 CSV 文件数据导入 TiDB Cloud 之前，你需要通过以下任一方式创建表结构：

- 方法一：在 TiDB Cloud 中为你的源数据创建目标数据库和数据表。

- 方法二：在存放 CSV 文件的 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务目录下，为你的源数据创建目标表结构文件：

    1. 为你的源数据创建数据库结构文件。

        如果你的 CSV 文件遵循 [第 1 步](#step-1-prepare-the-csv-files) 的命名规则，则导入数据时数据库结构文件为可选项。否则，数据库结构文件为必需项。

        每个数据库结构文件必须采用 `${db_name}-schema-create.sql` 格式，并包含一个 `CREATE DATABASE` DDL 语句。通过该文件，TiDB Cloud 会在导入数据时创建 `${db_name}` 数据库以存储你的数据。

        例如，如果你创建了一个包含如下语句的 `mydb-scehma-create.sql` 文件，TiDB Cloud 会在导入数据时创建 `mydb` 数据库。

        ```sql
        CREATE DATABASE mydb;
        ```

    2. 为你的源数据创建表结构文件。

        如果你没有在存放 CSV 文件的 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务目录下包含表结构文件，TiDB Cloud 在导入数据时不会为你创建相应的数据表。

        每个表结构文件必须采用 `${db_name}.${table_name}-schema.sql` 格式，并包含一个 `CREATE TABLE` DDL 语句。通过该文件，TiDB Cloud 会在 `${db_name}` 数据库中创建 `${db_table}` 表以存储你的数据。

        例如，如果你创建了一个包含如下语句的 `mydb.mytable-schema.sql` 文件，TiDB Cloud 会在 `mydb` 数据库中创建 `mytable` 表。

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **Note:**
        >
        > 每个 `${db_name}.${table_name}-schema.sql` 文件只能包含一个 DDL 语句。如果文件中包含多个 DDL 语句，只有第一个会生效。

## 第 3 步：配置跨账号访问

为了让 TiDB Cloud 能访问 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务桶中的 CSV 文件，请按以下方式操作：

- 如果你的 CSV 文件位于 Amazon S3，请为集群 [配置 Amazon S3 访问权限](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。

    你可以使用 AWS 访问密钥或 Role ARN 访问你的桶。配置完成后，请记录访问密钥（包括访问密钥 ID 和密钥）或 Role ARN 值，后续在 [第 4 步](#step-4-import-csv-files) 中会用到。

- 如果你的 CSV 文件位于 GCS，请为集群 [配置 GCS 访问权限](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)。

- 如果你的 CSV 文件位于 Azure Blob Storage，请为集群 [配置 Azure Blob Storage 访问权限](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)。

- 如果你的 CSV 文件位于阿里云对象存储服务（OSS），请为集群 [配置阿里云对象存储服务（OSS）访问权限](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。

## 第 4 步：导入 CSV 文件

要将 CSV 文件导入到 TiDB Cloud Starter 或 TiDB Cloud Essential，请按照以下步骤操作：

<SimpleTab>
<div label="Amazon S3">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框切换组织、项目和集群。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，填写以下信息：

    - **Storage Provider**：选择 **Amazon S3**。
    - **Source Files URI**：
        - 导入单个文件时，输入源文件 URI，格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`。例如：`s3://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，输入源文件夹 URI，格式为 `s3://[bucket_name]/[data_source_folder]/`。例如：`s3://sampledata/ingest/`。
    - **Credential**：你可以使用 AWS Role ARN 或 AWS 访问密钥访问你的桶。详情请参见 [配置 Amazon S3 访问权限](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。
        - **AWS Role ARN**：输入 AWS Role ARN 值。
        - **AWS Access Key**：输入 AWS 访问密钥 ID 和 AWS 密钥。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，指定源文件与目标表的映射方式。

    当 **Source Files URI** 指定为目录时，**Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项默认被选中。

    > **Note:**
    >
    > 当 **Source Files URI** 指定为单个文件时，不显示 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，TiDB Cloud 会自动将 **Source** 字段填充为文件名。此时你只需选择目标数据库和表即可。

    - 若希望 TiDB Cloud 自动将所有遵循 [文件命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 的源文件映射到对应表，请保持该选项选中，并选择 **CSV** 作为数据格式。

    - 若需手动配置映射规则，将你的源 CSV 文件与目标数据库和表关联，请取消选中该选项，然后填写以下字段：

        - **Source**：输入文件名模式，格式为 `[file_name].csv`。例如：`TableName.01.csv`。你也可以使用通配符匹配多个文件，仅支持 `*` 和 `?` 通配符。

            - `my-data?.csv`：匹配所有以 `my-data` 开头，后跟单个字符的 CSV 文件，如 `my-data1.csv` 和 `my-data2.csv`。
            - `my-data*.csv`：匹配所有以 `my-data` 开头的 CSV 文件，如 `my-data-2023.csv` 和 `my-data-final.csv`。

        - **Target Database** 和 **Target Table**：选择要导入数据的目标数据库和表。

6. 点击 **Next**。TiDB Cloud 会相应扫描源文件。

7. 审核扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查已导入的数据表。

</div>

<div label="Google Cloud">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框切换组织、项目和集群。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，填写以下信息：

    - **Storage Provider**：选择 **Google Cloud Storage**。
    - **Source Files URI**：
        - 导入单个文件时，输入源文件 URI，格式为 `[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv`。例如：`[gcs|gs]://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，输入源文件夹 URI，格式为 `[gcs|gs]://[bucket_name]/[data_source_folder]/`。例如：`[gcs|gs]://sampledata/ingest/`。
    - **Credential**：你可以使用 GCS IAM Role Service Account key 访问你的桶。详情请参见 [配置 GCS 访问权限](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，指定源文件与目标表的映射方式。

    当 **Source Files URI** 指定为目录时，**Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项默认被选中。

    > **Note:**
    >
    > 当 **Source Files URI** 指定为单个文件时，不显示 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，TiDB Cloud 会自动将 **Source** 字段填充为文件名。此时你只需选择目标数据库和表即可。

    - 若希望 TiDB Cloud 自动将所有遵循 [文件命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 的源文件映射到对应表，请保持该选项选中，并选择 **CSV** 作为数据格式。

    - 若需手动配置映射规则，将你的源 CSV 文件与目标数据库和表关联，请取消选中该选项，然后填写以下字段：

        - **Source**：输入文件名模式，格式为 `[file_name].csv`。例如：`TableName.01.csv`。你也可以使用通配符匹配多个文件，仅支持 `*` 和 `?` 通配符。

            - `my-data?.csv`：匹配所有以 `my-data` 开头，后跟单个字符的 CSV 文件，如 `my-data1.csv` 和 `my-data2.csv`。
            - `my-data*.csv`：匹配所有以 `my-data` 开头的 CSV 文件，如 `my-data-2023.csv` 和 `my-data-final.csv`。

        - **Target Database** 和 **Target Table**：选择要导入数据的目标数据库和表。

6. 点击 **Next**。TiDB Cloud 会相应扫描源文件。

7. 审核扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查已导入的数据表。

</div>

<div label="Azure Blob Storage">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框切换组织、项目和集群。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，填写以下信息：

    - **Storage Provider**：选择 **Azure Blob Storage**。
    - **Source Files URI**：
        - 导入单个文件时，输入源文件 URI，格式为 `[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv`。例如：`[azure|https]://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，输入源文件夹 URI，格式为 `[azure|https]://[bucket_name]/[data_source_folder]/`。例如：`[azure|https]://sampledata/ingest/`。
    - **Credential**：你可以使用共享访问签名（SAS）令牌访问你的桶。详情请参见 [配置 Azure Blob Storage 访问权限](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，指定源文件与目标表的映射方式。

    当 **Source Files URI** 指定为目录时，**Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项默认被选中。

    > **Note:**
    >
    > 当 **Source Files URI** 指定为单个文件时，不显示 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，TiDB Cloud 会自动将 **Source** 字段填充为文件名。此时你只需选择目标数据库和表即可。

    - 若希望 TiDB Cloud 自动将所有遵循 [文件命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 的源文件映射到对应表，请保持该选项选中，并选择 **CSV** 作为数据格式。

    - 若需手动配置映射规则，将你的源 CSV 文件与目标数据库和表关联，请取消选中该选项，然后填写以下字段：

        - **Source**：输入文件名模式，格式为 `[file_name].csv`。例如：`TableName.01.csv`。你也可以使用通配符匹配多个文件，仅支持 `*` 和 `?` 通配符。

            - `my-data?.csv`：匹配所有以 `my-data` 开头，后跟单个字符的 CSV 文件，如 `my-data1.csv` 和 `my-data2.csv`。
            - `my-data*.csv`：匹配所有以 `my-data` 开头的 CSV 文件，如 `my-data-2023.csv` 和 `my-data-final.csv`。

        - **Target Database** 和 **Target Table**：选择要导入数据的目标数据库和表。

6. 点击 **Next**。TiDB Cloud 会相应扫描源文件。

7. 审核扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查已导入的数据表。

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框切换组织、项目和集群。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，填写以下信息：

    - **Storage Provider**：选择 **Alibaba Cloud OSS**。
    - **Source Files URI**：
        - 导入单个文件时，输入源文件 URI，格式为 `oss://[bucket_name]/[data_source_folder]/[file_name].csv`。例如：`oss://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，输入源文件夹 URI，格式为 `oss://[bucket_name]/[data_source_folder]/`。例如：`oss://sampledata/ingest/`。
    - **Credential**：你可以使用 AccessKey 对访问你的桶。详情请参见 [配置阿里云对象存储服务（OSS）访问权限](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，指定源文件与目标表的映射方式。

    当 **Source Files URI** 指定为目录时，**Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项默认被选中。

    > **Note:**
    >
    > 当 **Source Files URI** 指定为单个文件时，不显示 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，TiDB Cloud 会自动将 **Source** 字段填充为文件名。此时你只需选择目标数据库和表即可。

    - 若希望 TiDB Cloud 自动将所有遵循 [文件命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 的源文件映射到对应表，请保持该选项选中，并选择 **CSV** 作为数据格式。

    - 若需手动配置映射规则，将你的源 CSV 文件与目标数据库和表关联，请取消选中该选项，然后填写以下字段：

        - **Source**：输入文件名模式，格式为 `[file_name].csv`。例如：`TableName.01.csv`。你也可以使用通配符匹配多个文件，仅支持 `*` 和 `?` 通配符。

            - `my-data?.csv`：匹配所有以 `my-data` 开头，后跟单个字符的 CSV 文件，如 `my-data1.csv` 和 `my-data2.csv`。
            - `my-data*.csv`：匹配所有以 `my-data` 开头的 CSV 文件，如 `my-data-2023.csv` 和 `my-data-final.csv`。

        - **Target Database** 和 **Target Table**：选择要导入数据的目标数据库和表。

6. 点击 **Next**。TiDB Cloud 会相应扫描源文件。

7. 审核扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查已导入的数据表。

</div>

</SimpleTab>

当你运行导入任务时，如果检测到任何不支持或无效的转换，TiDB Cloud 会自动终止导入作业并报告导入错误。

如果你遇到导入错误，请按以下步骤操作：

1. 删除部分导入的表。
2. 检查表结构文件，如有错误请修正。
3. 检查 CSV 文件中的数据类型。
4. 重新尝试导入任务。

## 故障排查

### 解决数据导入过程中的警告

点击 **Start Import** 后，如果你看到类似 `can't find the corresponding source files` 的警告信息，请通过提供正确的源文件、根据 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或使用 **Advanced Settings** 进行调整来解决。

解决这些问题后，你需要重新导入数据。

### 导入表中行数为零

当导入进度显示 **Completed** 后，检查已导入的数据表。如果行数为零，说明没有数据文件匹配你输入的 Bucket URI。此时，请通过提供正确的源文件、根据 [数据导入命名规范](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或使用 **Advanced Settings** 进行调整来解决。之后，重新导入这些表。