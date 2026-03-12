---
title: Unloading TSV File
---

## Unloading TSV File

Syntax:

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (
    TYPE = TSV,
    RECORD_DELIMITER = '<character>',
    FIELD_DELIMITER = '<character>',
    COMPRESSION = gzip,
    OUTPUT_HEADER = true -- Unload with header
)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- More TSV options refer to [TSV File Format Options](/sql/sql-reference/file-format-options#tsv-options)
- Unloading into multiple files use the [MAX_FILE_SIZE Copy Option](/sql/sql-commands/dml/dml-copy-into-location#copyoptions)
- More details about the syntax can be found in [COPY INTO location](/sql/sql-commands/dml/dml-copy-into-location)

## Tutorial

### Step 1. Create an External Stage

```sql
CREATE STAGE tsv_unload_stage
URL = 's3://unload/tsv/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. Create Custom TSV File Format

```sql
CREATE FILE FORMAT tsv_unload_format
    TYPE = TSV,
    COMPRESSION = gzip;     -- Unload with gzip compression
```

### Step 3. Unload into TSV File

```sql
COPY INTO @tsv_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'tsv_unload_format')
DETAILED_OUTPUT = true;
```

Result:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             file_name                            │ file_size │ row_count │
├──────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_99e8f5c8-79d6-43d8-80d7-13e3f4c91dd5_0002_00000000.tsv.gz │       160 │       100 │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4. Verify the Unloaded TSV Files

```
SELECT COUNT($1)
FROM @tsv_unload_stage
(
    FILE_FORMAT => 'tsv_unload_format',
    PATTERN => '.*[.]tsv[.]gz'
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
