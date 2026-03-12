---
title: Querying Parquet Files in Stage
sidebar_label: Parquet
---


## Syntax:

- [Query rows as Variants](./index.md#query-rows-as-variants)
- [Query columns by name](./index.md#query-columns-by-name)
- [Query Metadata](./index.md#query-metadata)

## Tutorial

### Step 1. Create an External Stage

Create an external stage with your own S3 bucket and credentials where your Parquet files are stored.
```sql
CREATE STAGE parquet_query_stage 
URL = 's3://load/parquet/' 
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>' 
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. Create Custom Parquet File Format

```sql
CREATE FILE FORMAT parquet_query_format TYPE = PARQUET;
```
- More Parquet file format options refer to [Parquet File Format Options](/sql/sql-reference/file-format-options#parquet-options)

### Step 3. Query Parquet Files

query with colum names:

```sql
SELECT *
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```

query with path expressions:


```sql
SELECT $1
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```


### Query with Metadata

Query Parquet files directly from a stage, including metadata columns like `METADATA$FILENAME` and `METADATA$FILE_ROW_NUMBER`:

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    *
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```
