---
title: 卸载 TSV 文件
summary: 了解如何卸载 TSV 文件。
---

# 卸载 TSV 文件

## 卸载 TSV 文件 {#unloading-tsv-file}

语法：

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (
    TYPE = TSV,
    RECORD_DELIMITER = '<character>',
    FIELD_DELIMITER = '<character>',
    COMPRESSION = gzip,
    OUTPUT_HEADER = true -- Unload with header
)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- 更多 TSV 选项，请参见 [TSV 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#tsv-options)
- 卸载到多个文件时，使用 [`MAX_FILE_SIZE` Copy 选项](/tidb-cloud-lake/sql/copy-into-location.md#copyoptions)
- 有关该语法的更多详细信息，请参见 [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md)

## 教程 {#tutorial}

### 第 1 步：创建 External Stage {#step-1-create-an-external-stage}

```sql
CREATE STAGE tsv_unload_stage
URL = 's3://unload/tsv/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 第 2 步：创建自定义 TSV 文件格式 {#step-2-create-custom-tsv-file-format}

```sql
CREATE FILE FORMAT tsv_unload_format
    TYPE = TSV,
    COMPRESSION = gzip;     -- Unload with gzip compression
```

### 第 3 步：卸载到 TSV 文件 {#step-3-unload-into-tsv-file}

```sql
COPY INTO @tsv_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'tsv_unload_format')
DETAILED_OUTPUT = true;
```

结果：

```text
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             file_name                            │ file_size │ row_count │
├──────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_99e8f5c8-79d6-43d8-80d7-13e3f4c91dd5_0002_00000000.tsv.gz │       160 │       100 │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 4 步：验证已卸载的 TSV 文件 {#step-4-verify-the-unloaded-tsv-files}

```
SELECT COUNT($1)
FROM @tsv_unload_stage
(
    FILE_FORMAT => 'tsv_unload_format',
    PATTERN => '.*[.]tsv[.]gz'
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