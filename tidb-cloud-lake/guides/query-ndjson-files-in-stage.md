---
title: Querying NDJSON Files in Stage
sidebar_label: NDJSON
---

In Databend, you can directly query NDJSON files stored in stages without first loading the data into tables. This approach is particularly useful for data exploration, ETL processing, and ad-hoc analysis scenarios.

## What is NDJSON?

NDJSON (Newline Delimited JSON) is a JSON-based file format where each line contains a complete and valid JSON object. This format is especially well-suited for streaming data processing and big data analytics.

**Example NDJSON file content:**
```json
{"id": 1, "title": "Database Fundamentals", "author": "John Doe", "price": 45.50, "category": "Technology"}
{"id": 2, "title": "Machine Learning in Practice", "author": "Jane Smith", "price": 68.00, "category": "AI"}
{"id": 3, "title": "Web Development Guide", "author": "Mike Johnson", "price": 52.30, "category": "Frontend"}
```

**Advantages of NDJSON:**
- **Stream-friendly**: Can be parsed line by line without loading entire file into memory
- **Big data compatible**: Widely used in log files, data exports, and ETL pipelines
- **Easy to process**: Each line is an independent JSON object, enabling parallel processing

## Syntax

- [Query rows as Variants](./index.md#query-rows-as-variants)
- [Query Metadata](./index.md#query-metadata)

## Tutorial

### Step 1. Create an External Stage

Create an external stage with your own S3 bucket and credentials where your NDJSON files are stored.
```sql
CREATE STAGE ndjson_query_stage 
URL = 's3://load/ndjson/' 
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>' 
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. Create Custom NDJSON File Format

```sql
CREATE FILE FORMAT ndjson_query_format 
    TYPE = NDJSON,
    COMPRESSION = AUTO;
```

- More NDJSON file format options refer to [NDJSON File Format Options](/sql/sql-reference/file-format-options#ndjson-options)

### Step 3. Query NDJSON Files

Now you can query the NDJSON files directly from the stage. This example extracts the `title` and `author` fields from each JSON object:

```sql
SELECT $1:title, $1:author
FROM @ndjson_query_stage
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson'
);
```

**Explanation:**
- `$1:title` and `$1:author`: Extract specific fields from the JSON object. The `$1` represents the entire JSON object as a variant, and `:field_name` accesses individual fields
- `@ndjson_query_stage`: References the external stage created in Step 1
- `FILE_FORMAT => 'ndjson_query_format'`: Uses the custom file format defined in Step 2
- `PATTERN => '.*[.]ndjson'`: Regex pattern that matches all files ending with `.ndjson`

### Querying Compressed Files

If the NDJSON files are compressed with gzip, modify the pattern to match compressed files:

```sql
SELECT $1:title, $1:author
FROM @ndjson_query_stage
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson[.]gz'
);
```

**Key difference:** The pattern `.*[.]ndjson[.]gz` matches files ending with `.ndjson.gz`. Databend automatically decompresses gzip files during query execution thanks to the `COMPRESSION = AUTO` setting in the file format.

## Related Documentation

- [Loading NDJSON Files](../03-load-semistructured/03-load-ndjson.md) - How to load NDJSON data into tables
- [NDJSON File Format Options](/sql/sql-reference/file-format-options#ndjson-options) - Complete NDJSON format configuration
- [CREATE STAGE](/sql/sql-commands/ddl/stage/ddl-create-stage) - Managing external and internal stages