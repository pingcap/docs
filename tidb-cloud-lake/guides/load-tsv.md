---
title: Loading TSV into Databend
sidebar_label: TSV
---

## What is TSV?

TSV (Tab Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database. The TSV file format is very similar to CSV, the records are separated by newlines, and each field is separated by a tab.
The following example shows a TSV file with two records:

```text
Title_0	Author_0
Title_1	Author_1
```

## Loading TSV File

The common syntax for loading TSV file is as follows:

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

- For more TSV file format options, refer to [TSV File Format Options](/sql/sql-reference/file-format-options#tsv-options).
- For more COPY INTO table options, refer to [COPY INTO table](/sql/sql-commands/dml/dml-copy-into-table).

## Tutorial: Loading Data from TSV Files

### Step 1. Create an Internal Stage

Create an internal stage to store the TSV files.

```sql
CREATE STAGE my_tsv_stage;
```

### Step 2. Create TSV files

Generate a TSV file using these SQL statements:

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

Verify the creation of the TSV file:

```sql
LIST @my_tsv_stage;
```

Result:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             name                            │   size  │                 md5                │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────┼─────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_7413d5d0-f992-4d92-b28e-0e501d66bdc1_0000_00000000.tsv │ 2477780 │ "a906769144de7aa6a0056a86ddae97d2" │ 2023-12-26 11:56:19.000 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 3: Create Target Table

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### Step 4. Copying Directly from TSV

To directly copy data into your table from TSV files, use the following SQL command:

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

Result:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             File                            │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├─────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_7413d5d0-f992-4d92-b28e-0e501d66bdc1_0000_00000000.tsv │      100000 │           0 │ NULL             │             NULL │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4 (Option). Using SELECT to Copy Data

For more control, like transforming data while copying, use the SELECT statement. Learn more at [`SELECT from TSV`](../04-transform/02-querying-tsv.md).

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
