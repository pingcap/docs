---
title: 从 Amazon S3 将数据导入到 {{{ .premium }}}
summary: 了解如何使用控制台向导将 Amazon S3 中的 CSV 文件导入到 {{{ .premium }}} 实例。
---

# 从 Amazon S3 将数据导入到 {{{ .premium }}}

本文介绍如何将 Amazon Simple Storage Service (Amazon S3) 中的 CSV 文件导入到 {{{ .premium }}} 实例。

> **Tip:**
>
> - 对于 {{{ .starter }}} 或 Essential，请参见[从云存储将 CSV 文件导入到 {{{ .starter }}} 或 Essential](/tidb-cloud/import-csv-files-serverless.md)。
> - 对于 {{{ .dedicated }}}，请参见[从云存储将 CSV 文件导入到 {{{ .dedicated }}}](/tidb-cloud/import-csv-files.md)。

## 限制 {#limitations}

- 为确保数据一致性，{{{ .premium }}} 仅允许将 CSV 文件导入到空表中。如果目标表已包含数据，请先导入到临时表，然后使用 `INSERT ... SELECT` 语句复制行。
- 在公开预览期间，用户界面当前仅支持 Amazon S3 作为存储提供方。对其他提供方的支持将在后续版本中添加。
- 每个导入任务仅将单个源模式映射到一个目标表。

## 步骤 1：准备 CSV 文件 {#step-1-prepare-the-csv-files}

1. 如果某个 CSV 文件大于 256 MiB，建议将其拆分为约 256 MiB 的较小文件，以便 {{{ .premium }}} 能够并行处理它们。
2. 按照 Dumpling 命名约定为 CSV 文件命名：
   - 整表文件：使用 `${db_name}.${table_name}.csv` 格式。
   - 分片文件：追加数字后缀，例如 `${db_name}.${table_name}.000001.csv`。
   - 压缩文件：使用 `${db_name}.${table_name}.${suffix}.csv.${compress}` 格式。
3. 可选的 schema 文件（`${db_name}-schema-create.sql`、`${db_name}.${table_name}-schema.sql`）可帮助 {{{ .premium }}} 自动创建数据库和表。

<!--Todo
These naming conventions are identical to the TiDB Cloud Serverless workflow. Update this section after we validate the Premium defaults.
-->

## 步骤 2：创建目标 schema（可选） {#step-2-create-target-schemas-optional}

如果你希望 {{{ .premium }}} 自动创建数据库和表，请将 Dumpling 生成的 schema 文件放在同一个 S3 目录中。否则，请在运行导入之前，先在 {{{ .premium }}} 中手动创建数据库和表。

## 步骤 3：配置对 Amazon S3 的访问 {#step-3-configure-access-to-amazon-s3}

要允许 {{{ .premium }}} 读取你的 bucket，请使用以下任一方法：

- 提供一个信任 TiDB Cloud 的 AWS Role ARN，并在相关路径上授予 `s3:GetObject` 和 `s3:ListBucket` 权限。
- 提供具有等效权限的 AWS access key（access key ID 和 secret access key）。

向导中包含一个标记为 **Click here to create a new one with AWS CloudFormation** 的帮助链接。如果你需要 {{{ .premium }}} 预填充一个为你创建该角色的 CloudFormation stack，请使用此链接。

## 步骤 4：从 Amazon S3 导入 CSV 文件 {#step-4-import-csv-files-from-amazon-s3}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/tidbs)中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击你的 {{{ .premium }}} 实例名称。
2. 在左侧导航栏中，点击 **Data** > **Import**，然后选择 **Import data from Cloud Storage**。
3. 在 **Source Connection** 对话框中：
    - 将 **Storage Provider** 设置为 **Amazon S3**。
    - 输入单个文件的 **Source Files URI**（`s3://bucket/path/file.csv`）或文件夹的 URI（`s3://bucket/path/`）。
    - 选择 **AWS Role ARN** 或 **AWS Access Key** 并提供凭证。
    - 点击 **Test Bucket Access** 以验证连接性。  <!--Todo-- Known preview issue: the button returns to the idle state without a success toast.-->

4. 点击 **Next**，并为导入任务提供 TiDB SQL 用户名和密码。你也可以选择测试连接。
5. 检查自动生成的源到目标映射。如果你需要定义自定义模式和目标表，请禁用自动映射。
6. 点击 **Next** 运行预检查。解决有关缺失文件或 schema 不兼容的任何警告。
7. 点击 **Start Import** 以启动任务组。
8. 监控任务状态，直到其显示为 **Completed**，然后在 TiDB Cloud 中验证已导入的数据。

## 故障排查 {#troubleshooting}

- 如果预检查报告零个文件，请检查 S3 路径和 IAM 权限。
- 如果任务一直停留在 **Preparing**，请确保目标表为空，并且所需的 schema 文件存在。
- 如果你需要调整映射或凭证，请使用 **Cancel** 操作停止任务组。

## 后续步骤 {#next-steps}

- 如需使用脚本方式导入，请参见[使用 MySQL Command-Line Client 将数据导入到 {{{ .premium }}}](/tidb-cloud/premium/import-with-mysql-cli-premium.md)。
- 有关 IAM 相关问题，请参见[排查从 Amazon S3 导入数据时的 Access Denied 错误](/tidb-cloud/troubleshoot-import-access-denied-error.md)。