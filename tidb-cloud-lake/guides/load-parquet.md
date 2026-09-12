---
title: 将 Parquet 加载到 TiDB Cloud Lake
summary: Parquet 是一种在数据分析中常用的列式存储格式。它旨在支持复杂的数据结构，并且能够高效处理大型数据集。
---

# 将 Parquet 加载到 TiDB Cloud Lake

## 什么是 Parquet？ {#what-is-parquet}

Parquet 是一种在数据分析中常用的列式存储格式。它旨在支持复杂的数据结构，并且能够高效处理大型数据集。

Parquet 文件对 {{{ .lake }}} 最友好。建议使用 Parquet 文件作为 {{{ .lake }}} 的数据源。

## 加载 Parquet 文件 {#loading-parquet-file}

加载 Parquet 文件的常用语法如下：

```sql
COPY INTO [<database>.]<table_name>
     FROM { internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
FILE_FORMAT = (TYPE = PARQUET)
```

- 有关更多 Parquet 文件格式选项，请参见 [Parquet 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#parquet-options)。
- 有关更多 COPY INTO table 选项，请参见 [COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md)。

## 教程：从 Parquet 文件加载数据 {#tutorial-loading-data-from-parquet-files}

### 步骤 1. 创建内部 stage {#step-1-create-an-internal-stage}

创建一个内部 stage 来存储 Parquet 文件。

```sql
CREATE STAGE my_parquet_stage;
```

### 步骤 2. 创建 Parquet 文件 {#step-2-create-parquet-files}

使用以下 SQL 语句生成一个 Parquet 文件：

```sql
COPY INTO @my_parquet_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = PARQUET);
```

验证 Parquet 文件是否已创建：

```sql
LIST @my_parquet_stage;
```

结果：

```text

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               name                              │  size  │                 md5                │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_3890e0b1-0233-422c-b506-3a4501602f28_0000_00000000.parquet │  65443 │ "ab4631846ca8a2beed6a48be75d2acac" │ 2023-12-26 10:28:18.000 +0000 │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

有关将数据 unload 到 stage 的更多信息，请参见 [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md)。

### 步骤 3. 创建目标表 {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### 步骤 4. 直接从 Parquet 复制 {#step-4-copying-directly-from-parquet}

要直接将 Parquet 文件中的数据复制到表中，请使用以下 SQL 命令：

```sql
COPY INTO books
    FROM @my_parquet_stage
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (TYPE = PARQUET);
```

结果：

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├─────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_3890e0b1-0233-422c-b506-3a4501602f28_0000_00000000.parquet │      100000 │           0 │ NULL             │             NULL │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 步骤 5（可选）. 使用 SELECT 复制数据 {#step-5-optional-using-select-to-copy-data}

如果你需要更多控制，例如在复制过程中转换数据，可以使用 SELECT 语句。更多信息请参见 [`SELECT from Parquet`](/tidb-cloud-lake/guides/query-parquet-files-in-stage.md)

```sql
COPY INTO books (title, author)
FROM (
    SELECT title, author
    FROM @my_parquet_stage
)
PATTERN = '.*[.]parquet'
FILE_FORMAT = (TYPE = PARQUET);
```