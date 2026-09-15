---
title: 导出 Parquet 文件
summary: 了解如何导出 Parquet 文件。
---

# 导出 Parquet 文件

## 导出 Parquet 文件 {#unloading-parquet-file}

语法：

```sql
COPY INTO {internalStage | externalStage | externalLocation}
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (TYPE = PARQUET)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- 更多 Parquet 选项，请参见 [Parquet 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#parquet-options)
- 如需导出到多个文件，请使用 [`MAX_FILE_SIZE` Copy 选项](/tidb-cloud-lake/sql/copy-into-location.md#copyoptions)
- 有关该语法的更多详细信息，请参见 [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md)

## 教程 {#tutorial}

### 步骤 1. 创建 External Stage {#step-1-create-an-external-stage}

```sql
CREATE STAGE parquet_unload_stage
URL = 's3://unload/parquet/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 步骤 2. 创建自定义 Parquet 文件格式 {#step-2-create-custom-parquet-file-format}

```sql
CREATE FILE FORMAT parquet_unload_format
    TYPE = PARQUET
    ;
```

### 步骤 3. 导出为 Parquet 文件 {#step-3-unload-into-parquet-file}

```sql
COPY INTO @parquet_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'parquet_unload_format')
DETAILED_OUTPUT = true;
```

结果：

```text
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                             file_name                             │ file_size │ row_count │
│                               String                              │   UInt64  │   UInt64  │
├───────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_a3760513-78a8-4a89-8f92-b1a17e0a61b6_0000_00000000.parquet │       445 │       100 │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

### 步骤 4. 验证已导出的 Parquet 文件 {#step-4-verify-the-unloaded-parquet-files}

```sql
SELECT COUNT($1)
FROM @parquet_unload_stage
(
    FILE_FORMAT => 'parquet_unload_format',
    PATTERN => '.*[.]parquet'
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