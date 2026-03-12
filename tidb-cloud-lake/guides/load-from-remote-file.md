---
title: Loading from Remote File
sidebar_label: Remote
---

To load data from remote files into Databend, the [COPY INTO](/sql/sql-commands/dml/dml-copy-into-table) command can be used. This command allows you to copy data from a variety of sources, including remote files, into Databend with ease. With COPY INTO, you can specify the source file location, file format, and other relevant parameters to tailor the import process to your needs. Please note that the files must be in a format supported by Databend, otherwise the data cannot be imported. For more information on the file formats supported by Databend, see [Input & Output File Formats](/sql/sql-reference/file-format-options).

## Loading with Glob Patterns

Databend facilitates the loading of data from remote files through the use of glob patterns. These patterns allow for efficient and flexible data import from multiple files that follow a specific naming convention. Databend supports the following glob patterns:

### Set Pattern

The set pattern in glob expressions enables matching any one of the characters within a set. For example, consider files named `data_file_a.csv`, `data_file_b.csv`, and `data_file_c.csv`. Utilize the set pattern to load data from all three files:

```sql
COPY INTO your_table 
FROM 'https://your-remote-location/data_file_{a,b,c}.csv' ...
```

### Range Pattern

When dealing with files named `data_file_001.csv`, `data_file_002.csv`, and `data_file_003.csv`, the range pattern becomes useful. Load data from this series of files using the range pattern like this:

```sql
COPY INTO your_table 
FROM 'https://your-remote-location/data_file_[001-003].csv' ...
```

## Tutorial - Load from a Remote File

This tutorial demonstrates how to import data into Databend from a remote CSV file. The sample file [books.csv](https://datafuse-1253727613.cos.ap-hongkong.myqcloud.com/data/books.csv) contains two records:

```text title='books.csv'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

### Step 1. Create Table

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);
```

### Step 2. Load Data into Table

```sql
COPY INTO books
FROM 'https://datafuse-1253727613.cos.ap-hongkong.myqcloud.com/data/books.csv'
FILE_FORMAT = (
    TYPE = 'CSV',
    FIELD_DELIMITER = ',',
    RECORD_DELIMITER = '\n',
    SKIP_HEADER = 0
);
```

### Step 3. Verify Loaded Data

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