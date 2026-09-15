---
title: 卸载 CSV 文件
summary: 了解如何卸载 CSV 文件。
---

# 卸载 CSV 文件

本页介绍如何使用 `COPY INTO` 命令卸载 CSV 文件。

## 语法 {#syntax}

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (
    TYPE = CSV,
    RECORD_DELIMITER = '<character>',
    FIELD_DELIMITER = '<character>',
    COMPRESSION = gzip,
    OUTPUT_HEADER = true -- Unload with header
)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- 更多 CSV 选项，请参见 [CSV 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#csv-options)
- 卸载到多个文件时，请使用 [`MAX_FILE_SIZE` Copy 选项](/tidb-cloud-lake/sql/copy-into-location.md#copyoptions)
- 有关该语法的更多详细信息，请参见 [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md)

## 教程 {#tutorial}

### 步骤 1：创建 External Stage {#step-1-create-an-external-stage}

```sql
CREATE STAGE csv_unload_stage
URL = 's3://unload/csv/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 步骤 2：创建自定义 CSV 文件格式 {#step-2-create-custom-csv-file-format}

```sql
CREATE FILE FORMAT csv_unload_format
    TYPE = CSV,
    RECORD_DELIMITER = '\n',
    FIELD_DELIMITER = ',',
    COMPRESSION = gzip,     -- Unload with gzip compression
    OUTPUT_HEADER = true,   -- Unload with header
    SKIP_HEADER = 1;        -- Only for loading, skip first line when querying if the CSV file has header
```

### 步骤 3：卸载到 CSV 文件 {#step-3-unload-into-csv-file}

```sql
COPY INTO @csv_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'csv_unload_format')
DETAILED_OUTPUT = true;
```

结果：

```text
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             file_name                            │ file_size │ row_count │
├──────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_c8382216-0a04-4920-9eca-7b5debe3eed6_0000_00000000.csv.gz │       187 │       100 │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 步骤 4：验证已卸载的 CSV 文件 {#step-4-verify-the-unloaded-csv-files}

```sql
SELECT COUNT($1)
FROM @csv_unload_stage
(
    FILE_FORMAT => 'csv_unload_format',
    PATTERN => '.*[.]csv[.]gz'
);
```

结果：

```text
┌───────────┐
│ count($1) │
├───────────┤
│       100 │
└───────────┘
```