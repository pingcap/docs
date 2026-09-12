---
title: Amazon S3 集成任务
summary: Amazon S3 数据集成使你能够将 S3 存储桶中的文件导入到 {{{ .lake }}}。它支持 CSV、Parquet 和 NDJSON 文件格式，并可选择一次性导入或自动轮询新文件的持续摄取。
---

# Amazon S3 集成任务

本页介绍如何创建一个 Amazon S3 集成任务，将 S3 存储桶中的文件导入到 {{{ .lake }}}。支持 CSV、Parquet 和 NDJSON 文件格式，并且该任务可配置为一次性导入或持续摄取。

如果你需要先创建可复用的 AWS 凭证，请参见 [Amazon S3 - 凭证](/tidb-cloud-lake/guides/aws-credentials.md)。

## 支持的文件格式 {#supported-file-formats}

| 格式  | 描述                                                        |
|---------|--------------------------------------------------------------------|
| CSV     | 逗号分隔值，支持可配置的分隔符和表头                               |
| Parquet | 列式存储格式，适用于分析型工作负载，效率较高                       |
| NDJSON  | 按行分隔的 JSON，每行一个 JSON 对象                                |

## 前提条件 {#prerequisites}

- 已创建 **Amazon S3 - Credentials** 数据源
- AWS 凭证对目标 S3 存储桶具有读访问权限
- 如果计划启用 **Clean Up Original Files**，这些凭证还需要写入和删除权限

## 创建 S3 集成任务 {#creating-an-s3-integration-task}

### 步骤 1：基本信息 {#step-1-basic-info}

1. 进入 **Data** > **Data Integration**，然后点击 **Create Task**。

2. 选择一个 S3 数据源，然后配置基本设置：

    | 字段              | 必填     | 描述                                                                                             |
    |--------------------|----------|--------------------------------------------------------------------------------------------------|
    | **Data Source**    | 是      | 从下拉列表中选择一个已有的 **Amazon S3 - Credentials** 数据源                                    |
    | **Name**          | 是      | 此集成任务的名称                                                                                 |
    | **File Path**     | 是      | 带可选通配符模式的 S3 URI（例如：`s3://mybucket/data/2025-*.csv`）                               |
    | **File Type**     | 自动     | 根据文件扩展名自动检测。支持：CSV、Parquet、NDJSON                                               |

#### CSV 选项 {#csv-options}

当文件类型为 CSV 时，可使用以下附加选项：

| 字段                | 默认值 | 描述                                                    |
|----------------------|---------|----------------------------------------------------------------|
| **Record Delimiter** | `\n`    | 行分隔符。可选值：`\n`、`\r`、`\r\n`                           |
| **Field Delimiter**  | `,`     | 列分隔符。支持自定义值                                         |
| **Has Header**       | Yes     | 第一行是否包含列名。如果禁用，列将自动命名为 `c1`、`c2`、`c3` 等。 |

#### 文件路径模式 {#file-path-patterns}

文件路径支持使用通配符模式来匹配多个文件：

```
s3://mybucket/data/2025-*.csv        # All CSV files starting with "2025-"
s3://mybucket/logs/*.parquet         # All Parquet files in the logs directory
s3://mybucket/events/data.ndjson     # A single specific file
```

### 步骤 2：预览数据 {#step-2-preview-data}

配置完基本设置后，点击 **Next** 以预览源数据。

![S3 Preview Data](/media/tidb-cloud-lake/s3-task-preview-step.png)

系统会读取第一个匹配的文件并显示：

- 包含列名和类型的示例数据
- 匹配文件列表（最多 25 个文件）及其大小

> **Note:**
>
> 预览时会跳过大于 10GB 的文件。仅显示前 25 个匹配文件。

### 步骤 3：设置目标表 {#step-3-set-target-table}

在 {{{ .lake }}} 中配置目标位置：

| 字段               | 描述                                                        |
|---------------------|--------------------------------------------------------------------|
| **Warehouse**       | 选择用于运行导入的目标 {{{ .lake }}} 计算集群 (Warehouse)          |
| **Target Database** | 选择 {{{ .lake }}} 中的目标数据库                                  |
| **Target Table**    | {{{ .lake }}} 中的表名                                             |

![S3 Set Target Table](/media/tidb-cloud-lake/s3-task-set-target-table.png)

系统会自动从源文件中检测列。你可以在继续之前查看并编辑列名和类型。

#### 摄取选项 {#ingestion-options}

| 选项                       | 默认值  | 描述                                                                                      |
|------------------------------|----------|--------------------------------------------------------------------------------------------------|
| **Continuous Ingestion**     | On       | 启用后，系统会定期（每 30 秒）轮询 S3 路径并导入新文件                                           |
| **Error Handling**           | Abort    | **Abort**：遇到第一个错误时停止。**Continue**：跳过失败的行并继续导入                            |
| **Clean Up Original Files**  | Off      | 启用后，在成功导入后从 S3 删除源文件                                                             |
| **Allow Duplicate Imports**  | Off      | 启用后，允许重新导入已经导入过的文件                                                             |

> **Tip:**
>
> 当新文件会定期添加到 S3 路径，并且你希望它们自动加载到 {{{ .lake }}} 时，请启用 **Continuous Ingestion**。对于一次性导入，请禁用此选项。

点击 **Create** 完成集成任务创建。

## 任务行为 {#task-behavior}

| 持续摄取 | 行为                                                                                          |
|----------------------|---------------------------------------------------------------------------------------------------|
| On                   | 持续运行，每 30 秒轮询一次 S3 以查找新文件，并自动导入这些文件。                                  |
| Off                  | 仅导入一次匹配的文件后停止。除非启用了 **Allow Duplicate Imports**，否则已导入的文件会被跳过。   |

## 高级配置 {#advanced-configuration}

### 持续摄取 {#continuous-ingestion}

启用后，任务会作为一个长期运行的进程，定期扫描 S3 路径中的新文件。每个周期会执行以下操作：

1. 列出与文件路径模式匹配的对象
2. 识别尚未导入的新文件
3. 使用 `COPY INTO` 将新文件导入目标表
4. 在任务历史中记录导入结果

这对于上游系统持续向 S3 写入新文件的数据管道非常有用。

### 错误处理 {#error-handling}

- **Abort**（默认）：导入在遇到第一个错误时停止。当数据质量至关重要，并且你希望在继续之前先调查问题时，请使用此选项。
- **Continue**：跳过导致错误的行，并继续导入其余数据。当允许部分导入并且你希望最大化数据吞吐时，请使用此选项。

### 清理原始文件（PURGE） {#clean-up-original-files-purge}

启用后，源文件在成功导入到 {{{ .lake }}} 后会从 S3 中删除。这有助于管理存储成本并防止重复处理。请确保你的 AWS 凭证在目标存储桶上具有 `s3:DeleteObject` 权限。

### 允许重复导入（FORCE） {#allow-duplicate-imports-force}

默认情况下，系统会跟踪哪些文件已经导入，并在后续运行中跳过这些文件。启用此选项后，无论这些匹配文件之前是否已被导入，系统都会强制重新导入所有匹配文件。当你需要在 schema 变更或数据修正后重新加载数据时，此功能非常有用。
