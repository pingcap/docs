---
title: Loading CSV into Databend
sidebar_label: CSV
---

## What is CSV?

CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database. CSV files are plain text files that contain data in a tabular format, where each row is represented on a new line, and columns are separated by a delimiter.

The following example shows a CSV file with two records:

```text
Title_0,Author_0
Title_1,Author_1
```

## Loading CSV File

The common syntax for loading CSV file is as follows:

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

- For more CSV file format options, refer to [CSV File Format Options](/sql/sql-reference/file-format-options#csv-options).
- For more COPY INTO table options, refer to [COPY INTO table](/sql/sql-commands/dml/dml-copy-into-table).

## Tutorial: Loading Data from CSV Files

### Step 1. Create an Internal Stage

Create an internal stage to store the CSV files.

```sql
CREATE STAGE my_csv_stage;
```

### Step 2. Create CSV files

Generate a CSV file using these SQL statements:

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

Verify the creation of the CSV file:

```sql
LIST @my_csv_stage;
```

Result:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │                 md5                │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_4bb7f864-f5f2-41e8-a442-68c2a709be5a_0000_00000000.csv.gz │ 483110 │ "0c8e28daed524468269e44ac13d2f463" │ 2023-12-26 11:37:21.000 +0000 │ NULL             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 3: Create Target Table

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### Step 4. Copying Directly from CSV

To directly copy data into your table from CSV files, use the following SQL command:

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

Result:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_4bb7f864-f5f2-41e8-a442-68c2a709be5a_0000_00000000.csv.gz │      100000 │           0 │ NULL             │             NULL │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4 (Option). Using SELECT to Copy Data

For more control, like transforming data while copying, use the SELECT statement. Learn more at [`SELECT from CSV`](../04-transform/01-querying-csv.md).

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
