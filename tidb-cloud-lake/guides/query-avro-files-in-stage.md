---
title: 在 Stage 中查询 Avro 文件
summary: "{{{ .lake }}} 提供了对直接从 stage 查询 Avro 文件的全面支持。这使你无需先将数据加载到表中，即可灵活地进行数据探索和转换。"
---

# 在 Stage 中查询 Avro 文件

## 语法 {#syntax}

- [将行作为 Variant 查询](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [查询元信息](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## Avro 查询功能概览 {#avro-querying-features-overview}

{{{ .lake }}} 提供了对直接从 stage 查询 Avro 文件的全面支持。这使你无需先将数据加载到表中，即可灵活地进行数据探索和转换。

* **Variant 表示**：Avro 文件中的每一行都会被视为一个 variant，并通过 `$1` 引用。这使你能够灵活访问 Avro 数据中的嵌套结构。
* **类型映射**：每种 Avro 类型都会映射为 {{{ .lake }}} 中对应的 variant 类型。
* **元信息访问**：你可以访问 `METADATA$FILENAME` 和 `METADATA$FILE_ROW_NUMBER` 等元信息列，以获取有关源文件和行的更多上下文信息。

## 教程 {#tutorial}

本教程演示如何查询存储在 stage 中的 Avro 文件。

### 第 1 步：准备一个 Avro 文件 {#step-1-prepare-an-avro-file}

假设有一个名为 `user` 的 Avro 文件，其 schema 如下：

```json
{
  "type": "record",
  "name": "user",
  "fields": [
    {
      "name": "id",
      "type": "long"
    },
    {
      "name": "name",
      "type": "string"
    }
  ]
}
```

### 第 2 步：创建一个外部 Stage {#step-2-create-an-external-stage}

使用你自己的 S3 存储桶和凭证创建一个外部 stage，其中存储了你的 Avro 文件。

```sql
CREATE STAGE avro_query_stage
URL = 's3://load/avro/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 第 3 步：查询 Avro 文件 {#step-3-query-avro-files}

#### 基本查询 {#basic-query}

直接从 stage 查询 Avro 文件：

```sql
SELECT
    CAST($1:id AS INT) AS id,
    $1:name AS name
FROM @avro_query_stage
(
    FILE_FORMAT => 'AVRO',
    PATTERN => '.*[.]avro'
);
```

### 带元信息的查询 {#query-with-metadata}

直接从 stage 查询 Avro 文件，并包含 `METADATA$FILENAME` 和 `METADATA$FILE_ROW_NUMBER` 等元信息列：

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    CAST($1:id AS INT) AS id,
    $1:name AS name
FROM @avro_query_stage
(
    FILE_FORMAT => 'AVRO',
    PATTERN => '.*[.]avro'
);
```

## 到 Variant 的类型映射 {#type-mapping-to-variant}

{{{ .lake }}} 中的 variant 以 JSONB 形式存储。虽然大多数 Avro 类型都可以直接映射，但仍有一些特殊情况需要注意：

* **时间类型**：`TimeMillis` 和 `TimeMicros` 会映射为 `INT64`，因为 JSONB 没有原生的 Time 类型。用户在处理这些值时应注意其原始类型。
* **Decimal 类型**：Decimal 会被加载为 `DECIMAL128` 或 `DECIMAL256`。如果精度超出支持的限制，可能会报错。
* **Enum 类型**：Avro `ENUM` 类型会映射为 {{{ .lake }}} 中的 `STRING` 值。