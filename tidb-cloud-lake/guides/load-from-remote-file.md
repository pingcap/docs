---
title: 从远程文件加载
summary: 要将远程文件中的数据加载到 {{{ .lake }}} 中，可以使用 COPY INTO 命令。该命令允许你轻松地将来自多种来源（包括远程文件）的数据复制到 {{{ .lake }}} 中。使用 COPY INTO 时，你可以指定源文件位置、文件格式以及其他相关参数，以根据你的需求定制导入过程。请注意，文件必须采用 {{{ .lake }}} 支持的格式，否则无法导入数据。有关 {{{ .lake }}} 支持的文件格式的更多信息，请参见 Input & Output File Formats。
---

# 从远程文件加载

要将远程文件中的数据加载到 {{{ .lake }}} 中，可以使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令。该命令允许你轻松地将来自多种来源（包括远程文件）的数据复制到 {{{ .lake }}} 中。使用 COPY INTO 时，你可以指定源文件位置、文件格式以及其他相关参数，以根据你的需求定制导入过程。请注意，文件必须采用 {{{ .lake }}} 支持的格式，否则无法导入数据。有关 {{{ .lake }}} 支持的文件格式的更多信息，请参见 [输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

## 使用 Glob 模式加载 {#loading-with-glob-patterns}

{{{ .lake }}} 支持通过 glob 模式从远程文件加载数据。这些模式可用于高效且灵活地从遵循特定命名约定的多个文件中导入数据。{{{ .lake }}} 支持以下 glob 模式：

### 集合模式 {#set-pattern}

glob 表达式中的集合模式可用于匹配集合中的任意一个字符。例如，假设有名为 `data_file_a.csv`、`data_file_b.csv` 和 `data_file_c.csv` 的文件。你可以使用集合模式从这三个文件中加载数据：

```sql
COPY INTO your_table
FROM 'https://your-remote-location/data_file_{a,b,c}.csv' ...
```

### 范围模式 {#range-pattern}

当处理名为 `data_file_001.csv`、`data_file_002.csv` 和 `data_file_003.csv` 的文件时，范围模式会很有用。你可以像下面这样使用范围模式从这一系列文件中加载数据：

```sql
COPY INTO your_table
FROM 'https://your-remote-location/data_file_[001-003].csv' ...
```

## 教程 - 从远程文件加载 {#tutorial-load-from-a-remote-file}

本教程演示如何将远程 CSV 文件中的数据导入到 {{{ .lake }}} 中。示例文件 [books.csv](https://lakesql-bin.tidbcloud.com/datasets/books.csv) 包含两条记录：

```text title='books.csv'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

### 步骤 1. 创建表 {#step-1-create-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);
```

### 步骤 2. 将数据加载到表中 {#step-2-load-data-into-table}

```sql
COPY INTO books
FROM 'https://lakesql-bin.tidbcloud.com/datasets/books.csv'
FILE_FORMAT = (
    TYPE = 'CSV',
    FIELD_DELIMITER = ',',
    RECORD_DELIMITER = '\n',
    SKIP_HEADER = 0
);
```

### 步骤 3. 验证已加载的数据 {#step-3-verify-loaded-data}

```sql
SELECT * FROM books;
```

```text title='Result:'
┌──────────────────────────────────┬─────────────────────┬───────┐
│ title                            │ author              │ date  │
├──────────────────────────────────┼─────────────────────┼───────┤
│ Transaction Processing           │ Jim Gray            │ 1992  │
│ Readings in Database Systems     │ Michael Stonebraker │ 2004  │
└──────────────────────────────────┴─────────────────────┴───────┘
```