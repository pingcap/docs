---
title: 在 Stage 中查询 Parquet 文件
summary: 使用你自己的 S3 存储桶和凭证创建一个外部 stage，用于存储你的 Parquet 文件。
---

# 在 Stage 中查询 Parquet 文件

## 语法 {#syntax}

- [将行查询为 Variant](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [按名称查询列](/tidb-cloud-lake/guides/query-stage.md#query-columns-by-name)
- [查询元信息](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## 教程 {#tutorial}

### 第 1 步：创建外部 Stage {#step-1-create-an-external-stage}

使用你自己的 S3 存储桶和凭证创建一个外部 stage，用于存储你的 Parquet 文件。

```sql
CREATE STAGE parquet_query_stage
URL = 's3://load/parquet/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 第 2 步：创建自定义 Parquet 文件格式 {#step-2-create-custom-parquet-file-format}

```sql
CREATE FILE FORMAT parquet_query_format TYPE = PARQUET;
```

- 更多 Parquet 文件格式选项，请参见 [Parquet 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#parquet-options)

### 第 3 步：查询 Parquet 文件 {#step-3-query-parquet-files}

使用列名进行查询：

```sql
SELECT *
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```

使用路径表达式进行查询：

```sql
SELECT $1
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```

### 使用元信息进行查询 {#query-with-metadata}

直接从 stage 查询 Parquet 文件，包括 `METADATA$FILENAME` 和 `METADATA$FILE_ROW_NUMBER` 等元信息列：

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    *
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```