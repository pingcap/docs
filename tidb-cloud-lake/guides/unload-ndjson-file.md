---
title: 卸载 NDJSON 文件
summary: 了解如何卸载 NDJSON 文件。
---

# 卸载 NDJSON 文件

## 卸载 TSV 文件 {#unloading-tsv-file}

语法：

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (
    TYPE = NDJSON,
    COMPRESSION = gzip,
    OUTPUT_HEADER = true
)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- 更多 NDJSON 选项，请参见 [NDJSON 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options)
- 使用 [`MAX_FILE_SIZE` Copy 选项](/tidb-cloud-lake/sql/copy-into-location.md#copyoptions) 可将数据卸载到多个文件中
- 有关该语法的更多详细信息，请参见 [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md)

## 教程 {#tutorial}

### 第 1 步：创建 External Stage {#step-1-create-an-external-stage}

```sql
CREATE STAGE ndjson_unload_stage
URL = 's3://unload/ndjson/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 第 2 步：创建自定义 NDJSON 文件格式 {#step-2-create-custom-ndjson-file-format}

```
CREATE FILE FORMAT ndjson_unload_format
    TYPE = NDJSON,
    COMPRESSION = gzip;     -- Unload with gzip compression
```

### 第 3 步：卸载到 NDJSON 文件 {#step-3-unload-into-ndjson-file}

```sql
COPY INTO @ndjson_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'ndjson_unload_format')
DETAILED_OUTPUT = true;
```

结果：

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              file_name                              │ file_size │ row_count │
├─────────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_068976e5-2072-4ad8-9887-16fb9129ed80_0000_00000000.ndjson.gz │       263 │       100 │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 4 步：验证已卸载的 NDJSON 文件 {#step-4-verify-the-unloaded-ndjson-files}

```sql
SELECT COUNT($1)
FROM @ndjson_unload_stage
(
    FILE_FORMAT => 'ndjson_unload_format',
    PATTERN => '.*[.]ndjson[.]gz'
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