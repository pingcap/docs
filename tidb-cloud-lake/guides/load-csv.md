---
title: 将 CSV 加载到 TiDB Cloud Lake
summary: CSV（Comma Separated Values，逗号分隔值）是一种用于存储表格数据的简单文件格式，例如电子表格或数据库中的数据。CSV 文件是纯文本文件，以表格形式包含数据，其中每一行表示一条新记录，各列之间通过分隔符分隔。
---

# 将 CSV 加载到 TiDB Cloud Lake

## 什么是 CSV？ {#what-is-csv}

CSV（Comma Separated Values，逗号分隔值）是一种用于存储表格数据的简单文件格式，例如电子表格或数据库中的数据。CSV 文件是纯文本文件，以表格形式包含数据，其中每一行表示一条新记录，各列之间通过分隔符分隔。

以下示例展示了一个包含两条记录的 CSV 文件：

```text
Title_0,Author_0
Title_1,Author_1
```

## 加载 CSV 文件 {#loading-csv-file}

加载 CSV 文件的常用语法如下：

```sql
COPY INTO [<database>.]<table_name>
FROM { userStage | internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
    TYPE = CSV,
    RECORD_DELIMITER = '<character>',
    FIELD_DELIMITER = '<character>',
    SKIP_HEADER = <integer>,
    COMPRESSION = AUTO
) ]
```

- 有关更多 CSV 文件格式选项，请参见 [CSV 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#csv-options)。
- 有关更多 COPY INTO table 选项，请参见 [COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md)。

## 教程：从 CSV 文件加载数据 {#tutorial-loading-data-from-csv-files}

### 第 1 步：创建 Internal Stage {#step-1-create-an-internal-stage}

创建一个 internal stage 来存储 CSV 文件。

```sql
CREATE STAGE my_csv_stage;
```

### 第 2 步：创建 CSV 文件 {#step-2-create-csv-files}

使用以下 SQL 语句生成一个 CSV 文件：

```sql
COPY INTO @my_csv_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = CSV, COMPRESSION = gzip)
;
```

验证 CSV 文件是否已创建：

```sql
LIST @my_csv_stage;
```

结果：

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │                 md5                │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_4bb7f864-f5f2-41e8-a442-68c2a709be5a_0000_00000000.csv.gz │ 483110 │ "0c8e28daed524468269e44ac13d2f463" │ 2023-12-26 11:37:21.000 +0000 │ NULL             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 3 步：创建目标表 {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### 第 4 步：直接从 CSV 复制 {#step-4-copying-directly-from-csv}

要将 CSV 文件中的数据直接复制到表中，请使用以下 SQL 命令：

```sql
COPY INTO books
FROM @my_csv_stage
PATTERN = '.*[.]csv.gz'
FILE_FORMAT = (
    TYPE = CSV,
    FIELD_DELIMITER = ',',
    RECORD_DELIMITER = '\n',
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = AUTO
);
```

结果：

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_4bb7f864-f5f2-41e8-a442-68c2a709be5a_0000_00000000.csv.gz │      100000 │           0 │ NULL             │             NULL │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 4 步（可选）：使用 SELECT 复制数据 {#step-4-option-using-select-to-copy-data}

如果你需要更精细的控制，例如在复制过程中转换数据，可以使用 SELECT 语句。更多信息请参见 [`SELECT from CSV`](/tidb-cloud-lake/guides/query-csv-files-in-stage.md)。

```sql
COPY INTO books (title, author)
FROM (
    SELECT $1, $2
    FROM @my_csv_stage
)
PATTERN = '.*[.]csv.gz'
FILE_FORMAT = (
    TYPE = 'CSV',
    FIELD_DELIMITER = ',',
    RECORD_DELIMITER = '\n',
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = 'AUTO'
);
```