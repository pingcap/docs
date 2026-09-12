---
title: 在 Stage 中查询 CSV 文件
summary: 使用你自己的 S3 存储桶和凭证创建一个外部 stage，用于存储你的 CSV 文件。
---

# 在 Stage 中查询 CSV 文件

## 语法 {#syntax}

- [按位置查询列](/tidb-cloud-lake/guides/query-stage.md#query-columns-by-position)
- [查询元信息](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## 教程 {#tutorial}

### 第 1 步：创建外部 Stage {#step-1-create-an-external-stage}

使用你自己的 S3 存储桶和凭证创建一个外部 stage，用于存储你的 CSV 文件。

```sql
CREATE STAGE csv_query_stage
URL = 's3://load/csv/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 第 2 步：创建自定义 CSV 文件格式 {#step-2-create-custom-csv-file-format}

```sql
CREATE FILE FORMAT csv_query_format
    TYPE = CSV,
    RECORD_DELIMITER = '\n',
    FIELD_DELIMITER = ',',
    COMPRESSION = AUTO,
    SKIP_HEADER = 1;        -- Skip first line when querying if the CSV file has header
```

- 更多 CSV 文件格式选项，请参见 [CSV 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#csv-options)

### 第 3 步：查询 CSV 文件 {#step-3-query-csv-files}

```sql
SELECT $1, $2, $3
FROM @csv_query_stage
(
    FILE_FORMAT => 'csv_query_format',
    PATTERN => '.*[.]csv'
);
```

如果 CSV 文件使用 gzip 压缩，可以使用以下查询：

```sql
SELECT $1, $2, $3
FROM @csv_query_stage
(
    FILE_FORMAT => 'csv_query_format',
    PATTERN => '.*[.]csv[.]gz'
);
```

### 使用元信息进行查询 {#query-with-metadata}

直接从 stage 查询 CSV 文件，包括 `METADATA$FILENAME` 和 `METADATA$FILE_ROW_NUMBER` 等元信息列：

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    $1, $2, $3
FROM @csv_query_stage
(
    FILE_FORMAT => 'csv_query_format',
    PATTERN => '.*[.]csv'
);
```