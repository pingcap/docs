---
title: 将 NDJSON 加载到 TiDB Cloud Lake
summary: NDJSON 构建于 JSON 之上，并且是 JSON 的严格子集。每一行都必须包含一个独立且完整的有效 JSON 对象。
---

# 将 NDJSON 加载到 TiDB Cloud Lake

## 什么是 NDJSON？ {#what-is-ndjson}

NDJSON 构建于 JSON 之上，并且是 JSON 的严格子集。每一行都必须包含一个独立且完整的有效 JSON 对象。

以下示例展示了一个包含两个 JSON 对象的 NDJSON 文件：

```text
{"title":"Title_0","author":"Author_0"}
{"title":"Title_1","author":"Author_1"}
```

## 加载 NDJSON 文件 {#loading-ndjson-file}

加载 NDJSON 文件的通用语法如下：

```sql
COPY INTO [<database>.]<table_name>
FROM { userStage | internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
    TYPE = NDJSON,
    COMPRESSION = AUTO
) ]
```

- 有关更多 NDJSON 文件格式选项，请参见 [NDJSON 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options)。
- 有关更多 COPY INTO table 选项，请参见 [COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md)。

## 教程：从 NDJSON 文件加载数据 {#tutorial-loading-data-from-ndjson-files}

### 第 1 步：创建内部 stage {#step-1-create-an-internal-stage}

创建一个内部 stage 来存储 NDJSON 文件。

```sql
CREATE STAGE my_ndjson_stage;
```

### 第 2 步：创建 NDJSON 文件 {#step-2-create-ndjson-files}

使用以下 SQL 语句生成一个 NDJSON 文件：

```sql
COPY INTO @my_ndjson_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = NDJSON)
;
```

验证 NDJSON 文件是否已创建：

```sql
LIST @my_ndjson_stage;
```

结果：

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │   size  │                 md5                │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼─────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_b3d94fad-3052-42e4-b090-26409e88c7b9_0000_00000000.ndjson │ 4777780 │ "d1cc98fefc3e3aa0649cade880d754aa" │ 2023-12-26 12:15:59.000 +0000 │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 3 步：创建目标表 {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### 第 4 步：直接从 NDJSON 复制 {#step-4-copying-directly-from-ndjson}

要将 NDJSON 文件中的数据直接复制到表中，请使用以下 SQL 命令：

```sql
COPY INTO books
FROM @my_ndjson_stage
PATTERN = '.*[.]ndjson'
FILE_FORMAT = (
    TYPE = NDJSON
);
```

结果：

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_b3d94fad-3052-42e4-b090-26409e88c7b9_0000_00000000.ndjson │      100000 │           0 │ NULL             │             NULL │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 4 步（可选）：使用 SELECT 复制数据 {#step-4-option-using-select-to-copy-data}

如果你需要更精细的控制，例如在复制过程中转换数据，请使用 SELECT 语句。更多信息，请参见 [`SELECT from NDJSON`](/tidb-cloud-lake/guides/query-ndjson-files-in-stage.md)。

```sql
COPY INTO books(title, author)
FROM (
    SELECT $1:title, $1:author
    FROM @my_ndjson_stage
)
PATTERN = '.*[.]ndjson'
FILE_FORMAT = (
    TYPE = NDJSON
);
```