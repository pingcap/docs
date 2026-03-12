---
title: Unloading Parquet File
---

## Unloading Parquet File

Syntax:

```sql
COPY INTO {internalStage | externalStage | externalLocation}
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (TYPE = PARQUET)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- More Parquet options refer to [Parquet File Format Options](/sql/sql-reference/file-format-options#parquet-options)
- Unloading into multiple files use the [MAX_FILE_SIZE Copy Option](/sql/sql-commands/dml/dml-copy-into-location#copyoptions)
- More details about the syntax can be found in [COPY INTO location](/sql/sql-commands/dml/dml-copy-into-location)

## Tutorial

### Step 1. Create an External Stage

```sql
CREATE STAGE parquet_unload_stage
URL = 's3://unload/parquet/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. Create Custom Parquet File Format

```sql
CREATE FILE FORMAT parquet_unload_format
    TYPE = PARQUET
    ;
```

### Step 3. Unload into Parquet File

```sql
COPY INTO @parquet_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'parquet_unload_format')
DETAILED_OUTPUT = true;
```

Result:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                             file_name                             │ file_size │ row_count │
│                               String                              │   UInt64  │   UInt64  │
├───────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_a3760513-78a8-4a89-8f92-b1a17e0a61b6_0000_00000000.parquet │       445 │       100 │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4. Verify the Unloaded Parquet Files

```sql
SELECT COUNT($1)
FROM @parquet_unload_stage
(
    FILE_FORMAT => 'parquet_unload_format',
    PATTERN => '.*[.]parquet'
);
```

Result:

```text
┌───────────┐
│ count($1) │
├───────────┤
│       100 │
└───────────┘
```
