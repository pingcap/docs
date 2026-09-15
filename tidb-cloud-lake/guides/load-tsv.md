---
title: 将 TSV 加载到 TiDB Cloud Lake
summary: TSV（Tab Separated Values）是一种用于存储表格数据的简单文件格式，例如电子表格或数据库。TSV 文件格式与 CSV 非常相似，记录之间以换行符分隔，每个字段之间以制表符分隔。以下示例展示了一个包含两条记录的 TSV 文件。
---

# 将 TSV 加载到 TiDB Cloud Lake

## 什么是 TSV？ {#what-is-tsv}

TSV（Tab Separated Values，在 {{{ .lake }}} `v1.2.890-nightly` 及更高版本中称为 `TEXT`）是一种用于存储表格数据的简单文件格式，例如电子表格或数据库。TSV 文件格式与 CSV 非常相似，记录之间以换行符分隔，每个字段之间以制表符分隔。

以下示例展示了一个包含两条记录的 TSV 文件：

```text
Title_0 Author_0
Title_1 Author_1
```

## 加载 TSV 文件 {#loading-tsv-file}

加载 TSV 文件的通用语法如下：

```sql
COPY INTO [<database>.]<table_name>
FROM { userStage | internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
    TYPE = TSV,
    SKIP_HEADER = <integer>,
    COMPRESSION = AUTO
) ]
```

> **注意：**
>
> 从 {{{ .lake }}} `v1.2.890-nightly` 开始，支持将 `TEXT` 作为 `TSV` 的别名。本指南在示例中仍使用 `TYPE = TSV`，以便它们在较旧的服务器版本上也能正常工作。如果你只面向 `v1.2.890-nightly` 或更高版本，也可以改用 `TYPE = TEXT`。

- 有关更多 TSV 文件格式选项，请参阅 [TSV 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#tsv-options)。
- 有关更多 COPY INTO table 选项，请参阅 [COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md)。

## 教程：从 TSV 文件加载数据 {#tutorial-loading-data-from-tsv-files}

### 第 1 步：创建内部 stage {#step-1-create-an-internal-stage}

创建一个内部 stage 来存储 TSV 文件。

```sql
CREATE STAGE my_tsv_stage;
```

### 第 2 步：创建 TSV 文件 {#step-2-create-tsv-files}

使用以下 SQL 语句生成一个 TSV 文件：

```sql
COPY INTO @my_tsv_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = TSV)
;
```

验证 TSV 文件是否已创建：

```sql
LIST @my_tsv_stage;
```

结果：

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             name                            │   size  │                 md5                │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────┼─────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_7413d5d0-f992-4d92-b28e-0e501d66bdc1_0000_00000000.tsv │ 2477780 │ "a906769144de7aa6a0056a86ddae97d2" │ 2023-12-26 11:56:19.000 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 3 步：创建目标表 {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### 第 4 步：直接从 TSV 复制 {#step-4-copying-directly-from-tsv}

要将 TSV 文件中的数据直接复制到表中，请使用以下 SQL 命令：

```sql
COPY INTO books
FROM @my_tsv_stage
PATTERN = '.*[.]tsv'
FILE_FORMAT = (
    TYPE = TSV,
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = AUTO
);
```

结果：

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             File                            │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├─────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_7413d5d0-f992-4d92-b28e-0e501d66bdc1_0000_00000000.tsv │      100000 │           0 │ NULL             │             NULL │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 4 步（可选）：使用 SELECT 复制数据 {#step-4-option-using-select-to-copy-data}

如果你需要更多控制，例如在复制时转换数据，可以使用 SELECT 语句。更多信息请参阅 [`SELECT from TSV`](/tidb-cloud-lake/guides/query-tsv-files-in-stage.md)。

```sql
COPY INTO books (title, author)
FROM (
    SELECT $1, $2
    FROM @my_tsv_stage
)
PATTERN = '.*[.]tsv'
FILE_FORMAT = (
    TYPE = 'TSV',
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = 'AUTO'
);
```