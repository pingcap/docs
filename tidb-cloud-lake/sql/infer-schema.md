---
title: INFER_SCHEMA
summary: 自动检测文件元信息 schema 并获取列定义。
---

# INFER_SCHEMA

自动检测文件元信息 schema 并获取列定义。

`infer_schema` 当前支持以下文件格式：

- **Parquet** - 原生支持 schema 推导
- **CSV** - 支持自定义分隔符和表头检测
- **NDJSON** - 以换行符分隔的 JSON 文件

**压缩支持**：所有格式还支持扩展名为 `.zip`、`.xz`、`.zst` 的压缩文件。

> **注意：**
>
> 每个单独文件在进行 schema 推导时的最大大小限制为 **100MB**。

> **注意：**
>
> 处理多个文件时，`infer_schema` 会自动合并不同的 schema：
>
> - **兼容类型**会被提升（例如，INT8 + INT16 → INT16）
> - **不兼容类型**会回退为 **VARCHAR**（例如，INT + FLOAT → VARCHAR）
> - 某些文件中**缺失的列**会被标记为 **nullable**
> - 后续文件中的**新列**会被添加到最终 schema 中
>
> 这可确保所有文件都能使用统一的 schema 进行读取。

## 语法 {#syntax}

```sql
INFER_SCHEMA(
  LOCATION => '{ internalStage | externalStage }'
  [ PATTERN => '<regex_pattern>']
  [ FILE_FORMAT => '<format_name>' ]
  [ MAX_RECORDS_PRE_FILE => <number> ]
  [ MAX_FILE_COUNT => <number> ]
)
```

## 参数 {#parameters}

| 参数 | 描述 | 默认值 | 示例 |
|-----------|-------------|---------|---------|
| `LOCATION` | stage 位置：`@<stage_name>[/<path>]` | 必填 | `'@my_stage/data/'` |
| `PATTERN` | 用于匹配 stage 中文件的正则表达式模式。它匹配 `@<stage_name>[/<path>]` 之后的文件路径部分。参见 [使用 PATTERN 过滤 stage 中的文件](/tidb-cloud-lake/guides/stage-overview.md#filtering-staged-files-with-pattern)。 | 所有文件 | `'.*[.]csv'`, `'.*[.]parquet'` |
| `FILE_FORMAT` | 用于解析的文件格式名称 | stage 的格式 | `'csv_format'`, `'NDJSON'` |
| `MAX_RECORDS_PRE_FILE` | 每个文件采样的最大记录数 | 所有记录 | `100`, `1000` |
| `MAX_FILE_COUNT` | 要处理的最大文件数 | 所有文件 | `5`, `10` |

## 示例 {#examples}

### Parquet 文件 {#parquet-files}

```sql
-- Create stage and export data
CREATE STAGE test_parquet;
COPY INTO @test_parquet FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'PARQUET');

-- Infer schema from parquet files using pattern
SELECT * FROM INFER_SCHEMA(
    location => '@test_parquet',
    pattern => '.*[.]parquet'
);
```

结果：

```
+-------------+-----------------+----------+----------+----------+
| column_name | type            | nullable | filenames| order_id |
+-------------+-----------------+----------+----------+----------+
| number      | BIGINT UNSIGNED |    false | data_... |        0 |
+-------------+-----------------+----------+----------+----------+
```

### CSV 文件 {#csv-files}

```sql
-- Create stage and export CSV data
CREATE STAGE test_csv;
COPY INTO @test_csv FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'CSV');

-- Create a CSV file format
CREATE FILE FORMAT csv_format TYPE = 'CSV';

-- Infer schema using pattern and file format
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv',
    pattern => '.*[.]csv',
    file_format => 'csv_format'
);
```

结果：

```
+-------------+---------+----------+----------+----------+
| column_name | type    | nullable | filenames| order_id |
+-------------+---------+----------+----------+----------+
| column_1    | BIGINT  |     true | data_... |        0 |
+-------------+---------+----------+----------+----------+
```

对于带表头的 CSV 文件：

```sql
-- Create CSV file format with header support
CREATE FILE FORMAT csv_headers_format
TYPE = 'CSV'
field_delimiter = ','
skip_header = 1;

-- Export data with headers
CREATE STAGE test_csv_headers;
COPY INTO @test_csv_headers FROM (
  SELECT number as user_id, 'user_' || number::string as user_name
  FROM numbers(5)
) FILE_FORMAT = (TYPE = 'CSV', output_header = true);

-- Infer schema with headers
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv_headers',
    file_format => 'csv_headers_format'
);
```

限制记录数以加快推导速度：

```sql
-- Sample only first 5 records for schema inference
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv',
    pattern => '.*[.]csv',
    file_format => 'csv_format',
    max_records_pre_file => 5
);
```

### NDJSON 文件 {#ndjson-files}

```sql
-- Create stage and export NDJSON data
CREATE STAGE test_ndjson;
COPY INTO @test_ndjson FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'NDJSON');

-- Infer schema using pattern and NDJSON format
SELECT * FROM INFER_SCHEMA(
    location => '@test_ndjson',
    pattern => '.*[.]ndjson',
    file_format => 'NDJSON'
);
```

结果：

```
+-------------+---------+----------+----------+----------+
| column_name | type    | nullable | filenames| order_id |
+-------------+---------+----------+----------+----------+
| number      | BIGINT  |     true | data_... |        0 |
+-------------+---------+----------+----------+----------+
```

限制记录数以加快推导速度：

```sql
-- Sample only first 5 records for schema inference
SELECT * FROM INFER_SCHEMA(
    location => '@test_ndjson',
    pattern => '.*[.]ndjson',
    file_format => 'NDJSON',
    max_records_pre_file => 5
);
```

### 使用多个文件进行 Schema 合并 {#schema-merging-with-multiple-files}

当文件具有不同的 schema 时，`infer_schema` 会智能地将它们合并：

```sql
-- Suppose you have multiple CSV files with different schemas:
-- file1.csv: id(INT), name(VARCHAR)
-- file2.csv: id(INT), name(VARCHAR), age(INT)
-- file3.csv: id(FLOAT), name(VARCHAR), age(INT)

SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '.*[.]csv',
    file_format => 'csv_format'
);
```

结果会显示合并后的 schema：

```
+-------------+---------+----------+-----------+----------+
| column_name | type    | nullable | filenames | order_id |
+-------------+---------+----------+-----------+----------+
| id          | VARCHAR |     true | file1,... |        0 |  -- INT+FLOAT→VARCHAR
| name        | VARCHAR |     true | file1,... |        1 |
| age         | BIGINT  |     true | file1,... |        2 |  -- Missing in file1→nullable
+-------------+---------+----------+-----------+----------+
```

### 模式匹配和文件数量限制 {#pattern-matching-and-file-limits}

使用模式匹配从多个文件中推导 schema：

```sql
-- Infer schema from all CSV files in the directory
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '.*[.]csv'
);
```

限制处理的文件数量以提升性能：

```sql
-- Process only the first 5 matching files
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '.*[.]csv',
    max_file_count => 5
);
```

### 压缩文件 {#compressed-files}

`infer_schema` 会自动处理压缩文件：

```sql
-- Works with compressed CSV files
SELECT * FROM INFER_SCHEMA(location => '@my_stage/data.csv.zip');

-- Works with compressed NDJSON files
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/data.ndjson.xz',
    file_format => 'NDJSON',
    max_records_pre_file => 50
);
```

### 根据推导出的 Schema 创建表 {#create-table-from-inferred-schema}

`infer_schema` 函数会显示 schema，但不会创建表。要根据推导出的 schema 创建表，请执行以下操作：

```sql
-- Create table structure from file schema
CREATE TABLE my_table AS
SELECT * FROM @my_stage/ (pattern=>'.*[.]parquet')
LIMIT 0;

-- Verify the table structure
DESC my_table;
```