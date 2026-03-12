---
title: Loading Parquet into Databend
sidebar_label: Parquet
---

## What is Parquet?

Parquet is a columnar storage format commonly used in data analytics. It is designed to support complex data structures, and it is efficient for processing large datasets.

Parquet file is most friendly to Databend. It is recommended to use Parquet file as the data source for Databend.

## Loading Parquet File

The common syntax for loading Parquet file is as follows:

```sql
COPY INTO [<database>.]<table_name>
     FROM { internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
FILE_FORMAT = (TYPE = PARQUET)
```

- For more Parquet file format options, refer to [Parquet File Format Options](/sql/sql-reference/file-format-options#parquet-options).
- For more COPY INTO table options, refer to [COPY INTO table](/sql/sql-commands/dml/dml-copy-into-table).

## Tutorial: Loading Data from Parquet Files

### Step 1. Create an Internal Stage

Create an internal stage to store the Parquet files.

```sql
CREATE STAGE my_parquet_stage;
```

### Step 2. Create Parquet files

Generate a Parquet file using these SQL statements:

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

Verify the creation of the Parquet file:

```sql
LIST @my_parquet_stage;
```

Result:

```text

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               name                              │  size  │                 md5                │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_3890e0b1-0233-422c-b506-3a4501602f28_0000_00000000.parquet │  65443 │ "ab4631846ca8a2beed6a48be75d2acac" │ 2023-12-26 10:28:18.000 +0000 │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

More details about unload data to stage can be found in [COPY INTO location](/sql/sql-commands/dml/dml-copy-into-location).

### Step 3: Create Target Table

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### Step 4. Copying Directly from Parquet

To directly copy data into your table from Parquet files, use the following SQL command:

```sql
COPY INTO books
    FROM @my_parquet_stage
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (TYPE = PARQUET);
```

Result:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├─────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_3890e0b1-0233-422c-b506-3a4501602f28_0000_00000000.parquet │      100000 │           0 │ NULL             │             NULL │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4 (Option). Using SELECT to Copy Data

For more control, like transforming data while copying, use the SELECT statement. Learn more at [`SELECT from Parquet`](../04-transform/00-querying-parquet.md)

```sql
COPY INTO books (title, author)
FROM (
    SELECT title, author
    FROM @my_parquet_stage
)
PATTERN = '.*[.]parquet'
FILE_FORMAT = (TYPE = PARQUET);
```
