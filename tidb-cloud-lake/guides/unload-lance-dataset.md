---
title: 卸载 Lance Dataset
summary: 了解如何卸载 Lance dataset。
---

## 卸载 Lance Dataset {#unloading-lance-dataset}

Lance 导出面向以 dataset 为中心的使用者，例如机器学习和向量工作流。与 CSV、TSV、NDJSON 或 Parquet 卸载不同，{{{ .lake }}} 会写入一个 Lance **dataset directory**，其中包含 `.lance` 数据文件以及诸如 `_versions/` 之类的元信息。

语法：

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (TYPE = LANCE)
[MAX_FILE_SIZE = <num>]
[USE_RAW_PATH = true | false]
[OVERWRITE = true | false]
[DETAILED_OUTPUT = true | false]
```

- Lance 仅支持用于 `COPY INTO <location>`。
- Lance 不支持 `SINGLE` 和 `PARTITION BY`。
- 当 `USE_RAW_PATH = false`（默认值）时，{{{ .lake }}} 会将查询 ID 追加到目标路径，因此每次导出都会获得各自独立的 dataset 根目录。
- 如果你希望为下游读者（例如 Python `lance`）提供稳定的 dataset URI，请设置 `USE_RAW_PATH = true`。
- 有关语法的更多详细信息，请参见 [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md)。
- 更多 Lance 行为说明列在 [输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md#lance-options) 中。

## 教程 {#tutorial}

本示例将构建一个小型文档分类 dataset。原始文本文件存储在一个 stage 中，`READ_FILE` 会在查询执行期间将它们转换为 `BINARY` 值，而 {{{ .lake }}} 会以 Lance 格式导出最终的 dataset，供 Python 使用者使用。

### 前提条件 {#prerequisites}

准备一个 S3-compatible 存储桶，并确保 {{{ .lake }}} 和你的 Python 环境都可以访问它。

### 第 1 步：创建 External Stage {#step-1-create-an-external-stage}

```sql
CREATE OR REPLACE STAGE ml_assets
URL = 's3://your-bucket/lance-demo/'
CONNECTION = (
    ENDPOINT_URL = '<your-endpoint-url>',
    ACCESS_KEY_ID = '<your-access-key-id>',
    SECRET_ACCESS_KEY = '<your-secret-access-key>',
    REGION = '<your-region>'
);
```

### 第 2 步：创建示例源文件 {#step-2-create-sample-source-files}

在该 stage 中创建三个原始文本文件：

```sql
COPY INTO @ml_assets/raw/ticket_001.txt
FROM (SELECT 'customer asked for a refund after the package arrived damaged')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;

COPY INTO @ml_assets/raw/ticket_002.txt
FROM (SELECT 'customer praised the fast response and confirmed the issue was resolved')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;

COPY INTO @ml_assets/raw/ticket_003.txt
FROM (SELECT 'customer requested escalation because the replacement order was delayed')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;
```

### 第 3 步：创建清单表 {#step-3-create-a-manifest-table}

```sql
CREATE OR REPLACE TABLE support_ticket_manifest (
    ticket_id INT,
    label STRING,
    file_path STRING
);

INSERT INTO support_ticket_manifest VALUES
    (1, 'refund', 'raw/ticket_001.txt'),
    (2, 'resolved', 'raw/ticket_002.txt'),
    (3, 'escalation', 'raw/ticket_003.txt');
```

### 第 4 步：将 dataset 导出为 Lance {#step-4-export-the-dataset-to-lance}

`READ_FILE` 会将 stage 中的文本文件读取为原始字节。然后，`COPY INTO` 会将这些行写入 Lance dataset：

```sql
COPY INTO @ml_assets/datasets/support-ticket-train
FROM (
    SELECT
        ticket_id,
        label,
        file_path,
        READ_FILE('@ml_assets', file_path) AS content
    FROM support_ticket_manifest
    ORDER BY ticket_id
)
FILE_FORMAT = (TYPE = LANCE)
USE_RAW_PATH = TRUE
OVERWRITE = TRUE
DETAILED_OUTPUT = TRUE;
```

结果：

```text
┌───────────────────────────────────────────────────────────────┐
│ file_name                          │ file_size │ row_count   │
├────────────────────────────────────┼───────────┼─────────────┤
│ datasets/support-ticket-train      │ ...       │ 3           │
└───────────────────────────────────────────────────────────────┘
```

### 第 5 步：检查导出的 dataset 布局 {#step-5-inspect-the-exported-dataset-layout}

```sql
LIST @ml_assets/datasets/support-ticket-train;
```

你将看到一个 dataset 目录，其中包含类似以下的路径：

```text
datasets/support-ticket-train/_versions/...
datasets/support-ticket-train/data/... .lance
datasets/support-ticket-train/*.manifest
```

### 第 6 步：使用 Python `lance` 验证 {#step-6-verify-with-python-lance}

安装 Python 包：

```bash
pip install pylance
```

从同一个对象存储位置读取导出的 dataset：

```python
import os
import lance

storage_options = {
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    "region": os.environ.get("AWS_REGION", "us-east-1"),
}

if endpoint := os.environ.get("AWS_ENDPOINT_URL"):
    storage_options["aws_endpoint"] = endpoint
    storage_options["aws_allow_http"] = "true" if endpoint.startswith("http://") else "false"

dataset = lance.dataset(
    "s3://your-bucket/lance-demo/datasets/support-ticket-train",
    storage_options=storage_options,
)

table = dataset.to_table()
print(table.num_rows)
print(table["label"].to_pylist())
print(table["content"].to_pylist()[0].decode("utf-8").strip())
```

预期输出：

```text
3
['refund', 'resolved', 'escalation']
customer asked for a refund after the package arrived damaged
```

至此，你已经拥有一个完整的 Lance dataset，它将标签、原始路径和原始文件字节保存在一起，便于下游 ML 处理。