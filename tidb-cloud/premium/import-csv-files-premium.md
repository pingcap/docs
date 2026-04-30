---
title: 从云存储将 CSV 文件导入到 {{{ .premium }}}
summary: 了解如何将 Amazon S3 或 Alibaba Cloud Object Storage Service (OSS) 中的 CSV 文件导入到 {{{ .premium }}} 实例。
---

# 从云存储将 CSV 文件导入到 {{{ .premium }}}

本文档介绍如何将 Amazon Simple Storage Service (Amazon S3) 或 Alibaba Cloud Object Storage Service (OSS) 中的 CSV 文件导入到 {{{ .premium }}} 实例。

> **提示：**
>
> - 对于 {{{ .starter }}} 或 Essential，请参见 [从云存储将 CSV 文件导入到 {{{ .starter }}} 或 Essential](/tidb-cloud/import-csv-files-serverless.md)。
> - 对于 {{{ .dedicated }}}，请参见 [从云存储将 CSV 文件导入到 {{{ .dedicated }}}](/tidb-cloud/import-csv-files.md)。

## 限制 {#limitations}

为确保数据一致性，{{{ .premium }}} 仅允许将 CSV 文件导入到空表中。若要将数据导入到已包含数据的现有表中，你可以按照本文档先将数据导入到一个临时空表中，然后使用 `INSERT SELECT` 语句将数据复制到目标现有表。

## 步骤 1. 准备 CSV 文件 {#step-1-prepare-the-csv-files}

1. 如果某个 CSV 文件大于 256 MiB，建议将其拆分为多个较小的文件，每个文件大小约为 256 MiB。

    {{{ .premium }}} 支持导入非常大的 CSV 文件，但在使用多个大小约为 256 MiB 的输入文件时性能最佳。这是因为 {{{ .premium }}} 可以并行处理多个文件，从而显著提升导入速度。

2. 按如下方式命名 CSV 文件：

    - 如果一个 CSV 文件包含整张表的全部数据，请将文件命名为 `${db_name}.${table_name}.csv` 格式。导入数据时，该文件会映射到 `${db_name}.${table_name}` 表。
    - 如果一张表的数据被拆分到多个 CSV 文件中，请为这些 CSV 文件追加数字后缀。例如，`${db_name}.${table_name}.000001.csv` 和 `${db_name}.${table_name}.000002.csv`。数字后缀可以不连续，但必须按升序排列。你还需要在数字前补零，以确保所有后缀长度一致。
    - {{{ .premium }}} 支持导入以下格式的压缩文件：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。如果你想导入压缩的 CSV 文件，请将文件命名为 `${db_name}.${table_name}.${suffix}.csv.${compress}` 格式，其中 `${suffix}` 是可选的，可以是任意整数，例如 '000001'。例如，如果你想将 `trips.000001.csv.gz` 文件导入到 `bikeshare.trips` 表中，则需要将该文件重命名为 `bikeshare.trips.000001.csv.gz`。

    > **注意：**
    >
    > - 为获得更好的性能，建议将每个压缩文件的大小限制在 100 MiB 以内。
    > - Snappy 压缩文件必须采用[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他变体的 Snappy 压缩格式。
    > - 对于未压缩文件，如果在某些情况下你无法按照上述规则更新 CSV 文件名（例如，这些 CSV 文件链接也被你的其他程序使用），你可以保持文件名不变，并在[步骤 4](#step-4-import-csv-files) 中使用 **Mapping Settings** 将源数据导入到单个目标表。

## 步骤 2. 创建目标表结构 {#step-2-create-the-target-table-schemas}

由于 CSV 文件不包含 schema 信息，因此在将 CSV 文件中的数据导入到 {{{ .premium }}} 之前，你需要使用以下任一方法创建表结构：

- 方法 1：在 {{{ .premium }}} 中，为你的源数据创建目标数据库和表。

- 方法 2：在存放 CSV 文件的 Amazon S3 或 Alibaba Cloud Object Storage Service (OSS) 目录中，按如下方式为你的源数据创建目标表结构文件：

    1. 为你的源数据创建数据库结构文件。

        如果你的 CSV 文件遵循[步骤 1](#step-1-prepare-the-csv-files)中的命名规则，则数据库结构文件对于数据导入是可选的。否则，数据库结构文件是必需的。

        每个数据库结构文件必须采用 `${db_name}-schema-create.sql` 格式，并包含一条 `CREATE DATABASE` DDL 语句。导入数据时，借助此文件，{{{ .premium }}} 将创建 `${db_name}` 数据库来存储你的数据。

        例如，如果你创建一个 `mydb-schema-create.sql` 文件，并包含以下语句，则在导入数据时，{{{ .premium }}} 将创建 `mydb` 数据库。

        ```sql
        CREATE DATABASE mydb;
        ```

    2. 为你的源数据创建表结构文件。

        如果你没有在存放 CSV 文件的 Amazon S3 或 Alibaba Cloud Object Storage Service 目录中包含表结构文件，{{{ .premium }}} 在导入数据时将不会为你创建相应的表。

        每个表结构文件必须采用 `${db_name}.${table_name}-schema.sql` 格式，并包含一条 `CREATE TABLE` DDL 语句。导入数据时，借助此文件，{{{ .premium }}} 将在 `${db_name}` 数据库中创建 `${table_name}` 表。

        例如，如果你创建一个 `mydb.mytable-schema.sql` 文件，并包含以下语句，则在导入数据时，{{{ .premium }}} 将在 `mydb` 数据库中创建 `mytable` 表。

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注意：**
        >
        > 每个 `${db_name}.${table_name}-schema.sql` 文件应只包含一条 DDL 语句。如果文件包含多条 DDL 语句，则只有第一条会生效。

## 步骤 3. 配置跨账号访问 {#step-3-configure-cross-account-access}

要允许 {{{ .premium }}} 访问 Amazon S3 或 Alibaba Cloud Object Storage Service (OSS) 中的 CSV 文件，请执行以下任一操作：

- 如果你的 CSV 文件位于 Amazon S3，请为你的 {{{ .premium }}} 实例[配置 Amazon S3 访问](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。

    你可以使用 AWS access key 或 Role ARN 来访问你的 bucket。完成后，请记下 access key（包括 access key ID 和 secret access key）或 Role ARN 的值，因为你将在[步骤 4](#step-4-import-csv-files)中用到它。

- 如果你的 CSV 文件位于 Alibaba Cloud Object Storage Service (OSS)，请为你的 {{{ .premium }}} 实例[配置 Alibaba Cloud Object Storage Service (OSS) 访问](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。
## 第 4 步：导入 CSV 文件 {#step-4-import-csv-files}

要将 CSV 文件导入到 {{{ .premium }}}，请执行以下步骤：

<SimpleTab>
<div label="Amazon S3">

1. 为目标 {{{ .premium }}} 实例打开 **Import** 页面。

    1. 登录 [TiDB Cloud console](https://tidbcloud.com/)，然后进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 {{{ .premium }}} 实例的名称进入其概览页面，然后在左侧导航栏中点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面中，提供以下信息：

    - **Storage Provider**：选择 **Amazon S3**。
    - **Source Files URI**：
        - 导入单个文件时，按以下格式输入源文件 URI：`s3://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`s3://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，按以下格式输入源文件夹 URI：`s3://[bucket_name]/[data_source_folder]/`。例如，`s3://sampledata/ingest/`。
    - **Credential**：你可以使用 AWS Role ARN 或 AWS access key 访问 bucket。更多信息，请参见 [Configure Amazon S3 access](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。
        - **AWS Role ARN**：输入 AWS Role ARN 值。如果你需要创建新角色，点击 **Click here to create a new one with AWS CloudFormation**，然后按照引导步骤启动提供的模板、确认 IAM 警告、创建 stack，并将生成的 ARN 复制回 {{{ .premium }}}。
        - **AWS Access Key**：输入 AWS access key ID 和 AWS secret access key。
    - **Test Bucket Access**：在凭证配置完成后点击此按钮，以确认 {{{ .premium }}} 可以访问该 bucket。
    - **Target Connection**：提供将用于执行导入的 TiDB 用户名和密码。你也可以点击 **Test Connection** 来验证凭证。

4. 点击 **Next**。

5. 在 **Source Files Mapping** 部分，{{{ .premium }}} 会扫描 bucket，并建议源文件与目标表之间的映射关系。

    当在 **Source Files URI** 中指定的是目录时，默认会选中 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项。

    > **Note:**
    >
    > 当在 **Source Files URI** 中指定的是单个文件时，不会显示 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，并且 {{{ .premium }}} 会自动使用文件名填充 **Source** 字段。在这种情况下，你只需要为数据导入选择目标数据库和表。

    - 保持启用自动映射，以将 [file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) 应用于源文件和目标表。数据格式保持选择 **CSV**。

    - **Advanced options**：展开面板以查看 `Ignore compatibility checks (advanced)` 开关。除非你有意绕过 schema 兼容性校验，否则请保持其禁用状态。

    <!-- future feature -->
    > **Note:**
    >
    > 手动映射功能即将推出。当该开关可用时，清除自动映射选项并手动配置映射：
    >
    > - **Source**：输入文件名模式，例如 `TableName.01.csv`。支持通配符 `*` 和 `?`（例如，`my-data*.csv`）。
    > - **Target Database** 和 **Target Table**：为匹配到的文件选择目标对象。

6. {{{ .premium }}} 会自动扫描源路径。检查扫描结果，确认找到的数据文件及其对应的目标表，然后点击 **Start Import**。

7. 当导入进度显示为 **Completed** 时，检查已导入的表。

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1. 为目标 {{{ .premium }}} 实例打开 **Import** 页面。

    1. 登录 [TiDB Cloud console](https://tidbcloud.com/)，然后进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 {{{ .premium }}} 实例的名称进入其概览页面，然后在左侧导航栏中点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面中，提供以下信息：

    - **Storage Provider**：选择 **Alibaba Cloud OSS**。
    - **Source Files URI**：
        - 导入单个文件时，按以下格式输入源文件 URI：`oss://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`oss://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，按以下格式输入源文件夹 URI：`oss://[bucket_name]/[data_source_folder]/`。例如，`oss://sampledata/ingest/`。
    - **Credential**：你可以使用 AccessKey 对访问 bucket。更多信息，请参见 [Configure Alibaba Cloud Object Storage Service (OSS) access](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。
    - **Test Bucket Access**：在凭证配置完成后点击此按钮，以确认 {{{ .premium }}} 可以访问该 bucket。
    - **Target Connection**：提供将用于执行导入的 TiDB 用户名和密码。你也可以点击 **Test Connection** 来验证凭证。

4. 点击 **Next**。

5. 在 **Source Files Mapping** 部分，{{{ .premium }}} 会扫描 bucket，并建议源文件与目标表之间的映射关系。

    当在 **Source Files URI** 中指定的是目录时，默认会选中 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项。

    > **Note:**
    >
    > 当在 **Source Files URI** 中指定的是单个文件时，不会显示 **Use [File naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** 选项，并且 {{{ .premium }}} 会自动使用文件名填充 **Source** 字段。在这种情况下，你只需要为数据导入选择目标数据库和表。

    - 保持启用自动映射，以将 [file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) 应用于源文件和目标表。数据格式保持选择 **CSV**。

    - **Advanced options**：展开面板以查看 `Ignore compatibility checks (advanced)` 开关。除非你有意绕过 schema 兼容性校验，否则请保持其禁用状态。

    <!-- future feature -->
    > **Note:**
    >
    > 手动映射功能即将推出。当该开关可用时，清除自动映射选项并手动配置映射：
    >
    > - **Source**：输入文件名模式，例如 `TableName.01.csv`。支持通配符 `*` 和 `?`（例如，`my-data*.csv`）。
    > - **Target Database** 和 **Target Table**：为匹配到的文件选择目标对象。

6. {{{ .premium }}} 会自动扫描源路径。检查扫描结果，确认找到的数据文件及其对应的目标表，然后点击 **Start Import**。

7. 当导入进度显示为 **Completed** 时，检查已导入的表。

</div>

</SimpleTab>

运行导入任务时，如果检测到任何不受支持或无效的转换，{{{ .premium }}} 会自动终止导入作业并报告导入错误。

如果你遇到导入错误，请执行以下操作：

1. 删除部分已导入的表。
2. 检查表 schema 文件。如果存在任何错误，请更正该表 schema 文件。
3. 检查 CSV 文件中的数据类型。
4. 再次尝试导入任务。

## 故障排查 {#troubleshooting}

### 解决数据导入期间的警告 {#resolve-warnings-during-data-import}

点击 **Start Import** 后，如果你看到类似 `can't find the corresponding source files` 的警告信息，请通过提供正确的源文件、按照 [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或使用 **Advanced Settings** 进行修改来解决此问题。

解决这些问题后，你需要重新导入数据。

### 导入后的表中行数为零 {#zero-rows-in-the-imported-tables}

当导入进度显示为 **Completed** 后，请检查已导入的表。如果行数为零，表示没有数据文件与您输入的 Bucket URI 匹配。在这种情况下，请通过提供正确的源文件、按照 [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md) 重命名现有文件，或使用 **Advanced Settings** 进行修改来解决此问题。之后，重新导入这些表。