---
title: Querying TSV Files in Stage
sidebar_label: TSV
---

## Syntax:

- [Query columns by position](./index.md#query-columns-by-position)
- [Query Metadata](./index.md#query-metadata)


## Tutorial

### Step 1. Create an External Stage

Create an external stage with your own S3 bucket and credentials where your TSV files are stored.
```sql
CREATE STAGE tsv_query_stage 
URL = 's3://load/tsv/' 
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>' 
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. Create Custom TSV File Format

```sql
CREATE FILE FORMAT tsv_query_format 
    TYPE = TSV,
    RECORD_DELIMITER = '\n',
    FIELD_DELIMITER = ',',
    COMPRESSION = AUTO;
```

- More TSV file format options refer to [TSV File Format Options](/sql/sql-reference/file-format-options#tsv-options)

### Step 3. Query TSV Files

```sql
SELECT $1, $2, $3
FROM @tsv_query_stage
(
    FILE_FORMAT => 'tsv_query_format',
    PATTERN => '.*[.]tsv'
);
```

If the TSV files is compressed with gzip, we can use the following query:

```sql
SELECT $1, $2, $3
FROM @tsv_query_stage
(
    FILE_FORMAT => 'tsv_query_format',
    PATTERN => '.*[.]tsv[.]gz'
);
```
### Query with Metadata

Query TSV files directly from a stage, including metadata columns like `METADATA$FILENAME` and `METADATA$FILE_ROW_NUMBER`:

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    $1, $2, $3
FROM @tsv_query_stage
(
    FILE_FORMAT => 'tsv_query_format',
    PATTERN => '.*[.]tsv'
);
```