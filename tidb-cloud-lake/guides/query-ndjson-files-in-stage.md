---
title: 在 Stage 中查询 NDJSON 文件
summary: 在 {{{ .lake }}} 中，你可以直接查询存储在 stage 中的 NDJSON 文件，而无需先将数据加载到表中。这种方式特别适用于数据探索、ETL 处理和临时分析场景。
---

# 在 Stage 中查询 NDJSON 文件

在 {{{ .lake }}} 中，你可以直接查询存储在 stage 中的 NDJSON 文件，而无需先将数据加载到表中。这种方式特别适用于数据探索、ETL 处理和临时分析场景。

## 什么是 NDJSON？ {#what-is-ndjson}

NDJSON（Newline Delimited JSON）是一种基于 JSON 的文件格式，其中每一行都包含一个完整且有效的 JSON 对象。这种格式特别适合流式数据处理和大数据分析。

**NDJSON 文件内容示例：**

```json
{"id": 1, "title": "Database Fundamentals", "author": "John Doe", "price": 45.50, "category": "Technology"}
{"id": 2, "title": "Machine Learning in Practice", "author": "Jane Smith", "price": 68.00, "category": "AI"}
{"id": 3, "title": "Web Development Guide", "author": "Mike Johnson", "price": 52.30, "category": "Frontend"}
```

**NDJSON 的优势：**

- **适合流式处理**：可以逐行解析，而无需将整个文件加载到内存中
- **兼容大数据**：广泛用于日志文件、数据导出和 ETL 管道
- **易于处理**：每一行都是一个独立的 JSON 对象，便于并行处理

## 语法 {#syntax}

- [将行查询为 Variants](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [查询元信息](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## 教程 {#tutorial}

### 第 1 步：创建外部 Stage {#step-1-create-an-external-stage}

使用你自己的 S3 存储桶和凭证创建一个外部 stage，用于存储 NDJSON 文件。

```sql
CREATE STAGE ndjson_query_stage
URL = 's3://load/ndjson/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### 第 2 步：创建自定义 NDJSON 文件格式 {#step-2-create-custom-ndjson-file-format}

```sql
CREATE FILE FORMAT ndjson_query_format
    TYPE = NDJSON,
    COMPRESSION = AUTO;
```

- 更多 NDJSON 文件格式选项，请参见 [NDJSON 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options)

### 第 3 步：查询 NDJSON 文件 {#step-3-query-ndjson-files}

现在，你可以直接从 stage 中查询 NDJSON 文件。以下示例从每个 JSON 对象中提取 `title` 和 `author` 字段：

```sql
SELECT $1:title, $1:author
FROM @ndjson_query_stage
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson'
);
```

**说明：**

- `$1:title` 和 `$1:author`：从 JSON 对象中提取特定字段。`$1` 表示整个 JSON 对象（作为 variant），而 `:field_name` 用于访问各个字段
- `@ndjson_query_stage`：引用在第 1 步中创建的外部 stage
- `FILE_FORMAT => 'ndjson_query_format'`：使用在第 2 步中定义的自定义文件格式
- `PATTERN => '.*[.]ndjson'`：匹配所有以 `.ndjson` 结尾文件的正则表达式模式

### 查询压缩文件 {#querying-compressed-files}

如果 NDJSON 文件使用 gzip 压缩，请修改模式以匹配压缩文件：

```sql
SELECT $1:title, $1:author
FROM @ndjson_query_stage
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson[.]gz'
);
```

**关键区别：** 模式 `.*[.]ndjson[.]gz` 匹配所有以 `.ndjson.gz` 结尾的文件。由于文件格式中设置了 `COMPRESSION = AUTO`，{{{ .lake }}} 会在查询执行期间自动解压缩 gzip 文件。

## 相关文档 {#related-documentation}

- [加载 NDJSON 文件](/tidb-cloud-lake/guides/load-ndjson.md) - 如何将 NDJSON 数据加载到表中
- [NDJSON 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options) - 完整的 NDJSON 格式配置
- [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) - 管理外部和内部 stage