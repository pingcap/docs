---
title: Loading NDJSON into Databend
sidebar_label: NDJSON
---

## What is NDJSON?

NDJSON is built on top of JSON, and it is a strict subset of JSON. Each line must contain a separate, self-contained valid JSON object.

The following example shows a NDJSON file with two JSON objects:

```text
{"title":"Title_0","author":"Author_0"}
{"title":"Title_1","author":"Author_1"}
```

## Loading NDJSON File

The common syntax for loading NDJSON file is as follows:

```sql
COPY INTO [<database>.]<table_name>
FROM { userStage | internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
    TYPE = NDJSON,
    COMPRESSION = AUTO
) ]
```

- For more NDJSON file format options, refer to [NDJSON File Format Options](/sql/sql-reference/file-format-options#ndjson-options).
- For more COPY INTO table options, refer to [COPY INTO table](/sql/sql-commands/dml/dml-copy-into-table).

## Tutorial: Loading Data from NDJSON Files

### Step 1. Create an Internal Stage

Create an internal stage to store the NDJSON files.

```sql
CREATE STAGE my_ndjson_stage;
```

### Step 2. Create NDJSON files

Generate a NDJSON file using these SQL statements:

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

Verify the creation of the NDJSON file:

```sql
LIST @my_ndjson_stage;
```

Result:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │   size  │                 md5                │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼─────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_b3d94fad-3052-42e4-b090-26409e88c7b9_0000_00000000.ndjson │ 4777780 │ "d1cc98fefc3e3aa0649cade880d754aa" │ 2023-12-26 12:15:59.000 +0000 │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 3: Create Target Table

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### Step 4. Copying Directly from NDJSON

To directly copy data into your table from NDJSON files, use the following SQL command:

```sql
COPY INTO books
FROM @my_ndjson_stage
PATTERN = '.*[.]ndjson'
FILE_FORMAT = (
    TYPE = NDJSON
);
```

Result:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_b3d94fad-3052-42e4-b090-26409e88c7b9_0000_00000000.ndjson │      100000 │           0 │ NULL             │             NULL │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4 (Option). Using SELECT to Copy Data

For more control, like transforming data while copying, use the SELECT statement. Learn more at [`SELECT from NDJSON`](../04-transform/03-querying-ndjson.md).

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
