---
title: INFER_SCHEMA
---

Automatically detects the file metadata schema and retrieves the column definitions.

`infer_schema` currently supports the following file formats:
- **Parquet** - Native support for schema inference
- **CSV** - With customizable delimiters and header detection
- **NDJSON** - Newline-delimited JSON files

**Compression Support**: All formats also support compressed files with extensions `.zip`, `.xz`, `.zst`.

:::info File Size Limit
Each individual file has a maximum size limit of **100MB** for schema inference.
:::

:::info Schema Merging
When processing multiple files, `infer_schema` automatically merges different schemas:

- **Compatible types** are promoted (e.g., INT8 + INT16 → INT16)
- **Incompatible types** fall back to **VARCHAR** (e.g., INT + FLOAT → VARCHAR)
- **Missing columns** in some files are marked as **nullable**
- **New columns** from later files are added to the final schema

This ensures all files can be read using the unified schema.
:::

## Syntax

```sql
INFER_SCHEMA(
  LOCATION => '{ internalStage | externalStage }'
  [ PATTERN => '<regex_pattern>']
  [ FILE_FORMAT => '<format_name>' ]
  [ MAX_RECORDS_PRE_FILE => <number> ]
  [ MAX_FILE_COUNT => <number> ]
)
```

## Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `LOCATION` | Stage location: `@<stage_name>[/<path>]` | Required | `'@my_stage/data/'` |
| `PATTERN` | File name pattern to match | All files | `'*.csv'`, `'*.parquet'` |
| `FILE_FORMAT` | File format name for parsing | Stage's format | `'csv_format'`, `'NDJSON'` |
| `MAX_RECORDS_PRE_FILE` | Max records to sample per file | All records | `100`, `1000` |
| `MAX_FILE_COUNT` | Max number of files to process | All files | `5`, `10` |

## Examples

### Parquet Files

```sql
-- Create stage and export data
CREATE STAGE test_parquet;
COPY INTO @test_parquet FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'PARQUET');

-- Infer schema from parquet files using pattern
SELECT * FROM INFER_SCHEMA(
    location => '@test_parquet',
    pattern => '*.parquet'
);
```

Result:
```
+-------------+-----------------+----------+----------+----------+
| column_name | type            | nullable | filenames| order_id |
+-------------+-----------------+----------+----------+----------+
| number      | BIGINT UNSIGNED |    false | data_... |        0 |
+-------------+-----------------+----------+----------+----------+
```

### CSV Files

```sql
-- Create stage and export CSV data
CREATE STAGE test_csv;
COPY INTO @test_csv FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'CSV');

-- Create a CSV file format
CREATE FILE FORMAT csv_format TYPE = 'CSV';

-- Infer schema using pattern and file format
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv',
    pattern => '*.csv',
    file_format => 'csv_format'
);
```

Result:
```
+-------------+---------+----------+----------+----------+
| column_name | type    | nullable | filenames| order_id |
+-------------+---------+----------+----------+----------+
| column_1    | BIGINT  |     true | data_... |        0 |
+-------------+---------+----------+----------+----------+
```

For CSV files with headers:

```sql
-- Create CSV file format with header support
CREATE FILE FORMAT csv_headers_format
TYPE = 'CSV'
field_delimiter = ','
skip_header = 1;

-- Export data with headers
CREATE STAGE test_csv_headers;
COPY INTO @test_csv_headers FROM (
  SELECT number as user_id, 'user_' || number::string as user_name
  FROM numbers(5)
) FILE_FORMAT = (TYPE = 'CSV', output_header = true);

-- Infer schema with headers
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv_headers',
    file_format => 'csv_headers_format'
);
```

Limit records for faster inference:

```sql
-- Sample only first 5 records for schema inference
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv',
    pattern => '*.csv',
    file_format => 'csv_format',
    max_records_pre_file => 5
);
```

### NDJSON Files

```sql
-- Create stage and export NDJSON data
CREATE STAGE test_ndjson;
COPY INTO @test_ndjson FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'NDJSON');

-- Infer schema using pattern and NDJSON format
SELECT * FROM INFER_SCHEMA(
    location => '@test_ndjson',
    pattern => '*.ndjson',
    file_format => 'NDJSON'
);
```

Result:
```
+-------------+---------+----------+----------+----------+
| column_name | type    | nullable | filenames| order_id |
+-------------+---------+----------+----------+----------+
| number      | BIGINT  |     true | data_... |        0 |
+-------------+---------+----------+----------+----------+
```

Limit records for faster inference:

```sql
-- Sample only first 5 records for schema inference
SELECT * FROM INFER_SCHEMA(
    location => '@test_ndjson',
    pattern => '*.ndjson',
    file_format => 'NDJSON',
    max_records_pre_file => 5
);
```

### Schema Merging with Multiple Files

When files have different schemas, `infer_schema` merges them intelligently:

```sql
-- Suppose you have multiple CSV files with different schemas:
-- file1.csv: id(INT), name(VARCHAR)
-- file2.csv: id(INT), name(VARCHAR), age(INT)
-- file3.csv: id(FLOAT), name(VARCHAR), age(INT)

SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '*.csv',
    file_format => 'csv_format'
);
```

Result shows merged schema:
```
+-------------+---------+----------+-----------+----------+
| column_name | type    | nullable | filenames | order_id |
+-------------+---------+----------+-----------+----------+
| id          | VARCHAR |     true | file1,... |        0 |  -- INT+FLOAT→VARCHAR
| name        | VARCHAR |     true | file1,... |        1 |
| age         | BIGINT  |     true | file1,... |        2 |  -- Missing in file1→nullable
+-------------+---------+----------+-----------+----------+
```

### Pattern Matching and File Limits

Use pattern matching to infer schema from multiple files:

```sql
-- Infer schema from all CSV files in the directory
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '*.csv'
);
```

Limit the number of files processed to improve performance:

```sql
-- Process only the first 5 matching files
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '*.csv',
    max_file_count => 5
);
```

### Compressed Files

`infer_schema` automatically handles compressed files:

```sql
-- Works with compressed CSV files
SELECT * FROM INFER_SCHEMA(location => '@my_stage/data.csv.zip');

-- Works with compressed NDJSON files
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/data.ndjson.xz',
    file_format => 'NDJSON',
    max_records_pre_file => 50
);
```

### Create Table from Inferred Schema

The `infer_schema` function displays the schema but doesn't create tables. To create a table from the inferred schema:

```sql
-- Create table structure from file schema
CREATE TABLE my_table AS
SELECT * FROM @my_stage/ (pattern=>'*.parquet')
LIMIT 0;

-- Verify the table structure
DESC my_table;
```
