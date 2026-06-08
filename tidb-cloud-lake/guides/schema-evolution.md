---
title: Schema Evolution
summary: Automatically evolve table schemas when loading data with COPY INTO.
---

# Schema Evolution

Schema evolution allows {{{ .lake }}} to automatically add columns that exist in source files but are missing from the target table during `COPY INTO`. It currently supports **Parquet** and **NDJSON** files.

## How It Works

When enabled, {{{ .lake }}} infers the source file schema before loading and appends new columns to the end of the table. New columns are nullable, and missing values are filled with `NULL`.

The workflow differs slightly by file format:

- **Parquet**: After the table option is enabled, `COPY INTO` infers new columns directly from Parquet file schemas.
- **NDJSON**: After the table option is enabled, `COPY INTO` uses `AUTO` sampling values for schema inference. You can optionally add `SCHEMA_EVOLUTION = (...)` to override the file and record sampling limits.

## Enabling Schema Evolution

Set the table option `ENABLE_SCHEMA_EVOLUTION` to `true`:

```sql
-- On an existing table
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

-- Or when creating a new table
CREATE TABLE my_table(id INT) ENABLE_SCHEMA_EVOLUTION = true;
```

To disable schema evolution, set it back to `false`:

```sql
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = false);
```

## Privileges

When `COPY INTO <table>` loads files from a stage or external location and runs schema evolution inference, the loading role must have both `INSERT` and `ALTER` privileges on the target table. `ALTER` is required because {{{ .lake }}} may append new columns before loading.

Query-based COPY is not affected. For example, `COPY INTO <table> FROM (SELECT ... FROM @stage)` keeps the existing privilege requirements.

## Parquet Example

The following example loads Parquet files with different schemas and automatically adds missing columns.

### Step 1: Create a Table and Stage

```sql
CREATE OR REPLACE TABLE invoices(order_id INT);
CREATE OR REPLACE STAGE my_stage;
```

### Step 2: Generate Parquet Files with Different Schemas

```sql
-- File with columns: order_id, amount, currency
COPY INTO @my_stage FROM (
    SELECT 1 AS order_id, 100.50::DOUBLE AS amount, 'USD' AS currency
    UNION ALL
    SELECT 2, 250.50::DOUBLE, 'EUR'
) FILE_FORMAT = (TYPE = parquet);

-- File with columns: order_id, amount (no currency)
COPY INTO @my_stage FROM (
    SELECT 3 AS order_id, 75.50::DOUBLE AS amount
) FILE_FORMAT = (TYPE = parquet);
```

### Step 3: Enable Schema Evolution and Load

```sql
ALTER TABLE invoices SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

COPY INTO invoices
FROM @my_stage/
FILE_FORMAT = (TYPE = parquet MISSING_FIELD_AS = FIELD_DEFAULT);
```

### Step 4: Verify Results

The table now has three columns. `amount` and `currency` were added automatically:

```sql
DESC invoices;
```

```text
┌─────────────────────────────────────────────────────────────┐
│   Field  │      Type      │  Null  │ Default │    Extra     │
├──────────┼────────────────┼────────┼─────────┼──────────────┤
│ order_id │ INT            │ YES    │ NULL    │              │
│ amount   │ DOUBLE         │ YES    │ NULL    │              │
│ currency │ VARCHAR        │ YES    │ NULL    │              │
└─────────────────────────────────────────────────────────────┘
```

```sql
SELECT * FROM invoices ORDER BY order_id;
```

```text
┌──────────────────────────────────────────────────┐
│ order_id │  amount  │ currency                    │
├──────────┼──────────┼─────────────────────────────┤
│        1 │   100.50 │ USD                         │
│        2 │   250.50 │ EUR                         │
│        3 │    75.50 │ NULL                        │
└──────────────────────────────────────────────────┘
```

Row 3 has `currency = NULL` because its source file did not contain that column.

## NDJSON Example

{{{ .lake }}} loads NDJSON files with `TYPE = ndjson`. NDJSON files do not have an embedded columnar schema like Parquet files, so {{{ .lake }}} samples file content, infers fields that are missing from the target table, and appends them as nullable columns.

### Step 1: Create a Table and Stage

```sql
CREATE OR REPLACE TABLE events(id INT);
CREATE OR REPLACE STAGE events_stage;
```

### Step 2: Generate NDJSON Files with Different Fields

```sql
-- File with fields: id, city, score
COPY INTO @events_stage FROM (
    SELECT 1 AS id, 'SF' AS city, 9 AS score
    UNION ALL
    SELECT 2, 'NYC', 8
) FILE_FORMAT = (TYPE = ndjson);

-- File with fields: id, score (no city)
COPY INTO @events_stage FROM (
    SELECT 3 AS id, 7 AS score
) FILE_FORMAT = (TYPE = ndjson);
```

### Step 3: Enable Schema Evolution and Load

```sql
ALTER TABLE events SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

COPY INTO events
FROM @events_stage/
FILE_FORMAT = (TYPE = ndjson MISSING_FIELD_AS = FIELD_DEFAULT)
SCHEMA_EVOLUTION = (
  SAMPLE_FILES = AUTO,
  SAMPLE_RECORDS_PER_FILE = AUTO,
  SAMPLE_TOTAL_RECORDS = AUTO
);
```

The three `SCHEMA_EVOLUTION` sampling options accept either `AUTO` or a positive integer:

| Option | Description |
|------|------|
| `SAMPLE_FILES` | Number of files to sample. |
| `SAMPLE_RECORDS_PER_FILE` | Maximum number of records to sample from each selected file. |
| `SAMPLE_TOTAL_RECORDS` | Maximum number of records to sample across all selected files. |

If `SCHEMA_EVOLUTION` is omitted, {{{ .lake }}} uses `AUTO` for all three sampling options. The current `AUTO` behavior samples up to 64 files, 1,000 records per file, and 10,000 records in total. These internal defaults may change in future versions. If your load is sensitive to the sampling strategy, set `SAMPLE_FILES`, `SAMPLE_RECORDS_PER_FILE`, and `SAMPLE_TOTAL_RECORDS` explicitly.

#### NDJSON Inference Rules

When running Schema Evolution for NDJSON, {{{ .lake }}} infers new columns using these rules:

- Schema is inferred only from sampled NDJSON records. Fields not covered by the sample are not added to the target table ahead of time.
- Each line must be a JSON object. {{{ .lake }}} uses top-level object field names as candidate column names.
- Columns that already exist in the target table are not added again. Only fields missing from the target table are appended.
- New field types are inferred from sampled JSON values, such as integers, floats, strings, and booleans.
- Schema Evolution uses shallow NDJSON inference: if a top-level field value is an object or array, it is appended as a `VARIANT` column instead of being recursively expanded.
- `NULL` samples only mark the field as nullable. They do not force later non-null values to become `VARCHAR` or `VARIANT`.
- Same-name fields across files or records are merged: integer and float conflicts become `DOUBLE`; other scalar conflicts become `VARCHAR`; any conflict involving an object, array, or `VARIANT` becomes `VARIANT`.
- If loading encounters extra fields that were not inferred during sampling, the load fails and reports those field names. Increase `SAMPLE_FILES`, `SAMPLE_RECORDS_PER_FILE`, or `SAMPLE_TOTAL_RECORDS` and retry.

> **Note:**
>
> The `INFER_SCHEMA` table function does not limit NDJSON nesting depth by default. The rules here describe the shallow inference used by `COPY INTO` Schema Evolution.

For example, the following NDJSON records infer six new columns: `name`, `age`, `active`, `score`, `profile`, and `tags`:

```json
{"id":1,"name":"Alice","age":30,"active":true,"score":1,"profile":{"city":"SF"},"tags":["new"]}
{"id":2,"name":"Bob","age":null,"active":false,"score":1.5,"profile":{"city":"NYC"},"tags":["vip"]}
```

If the target table only has `id INT`, {{{ .lake }}} appends:

```text
name    VARCHAR   NULL
age     BIGINT    NULL
active  BOOLEAN   NULL
score   DOUBLE    NULL
profile VARIANT   NULL
tags    VARIANT   NULL
```

The second row has `age = NULL`, which does not change the `BIGINT` type inferred from the first row. `score` contains both an integer and a float, so it becomes `DOUBLE`. `profile` and `tags` are an object and an array, so Schema Evolution appends them as `VARIANT` columns.

### Step 4: Verify Results

The table now has three columns. `city` and `score` were added automatically:

```sql
DESC events;
```

```text
┌─────────────────────────────────────────────────────────┐
│ Field │     Type     │  Null  │ Default │    Extra     │
├───────┼──────────────┼────────┼─────────┼──────────────┤
│ id    │ INT          │ YES    │ NULL    │              │
│ city  │ VARCHAR      │ YES    │ NULL    │              │
│ score │ BIGINT       │ YES    │ NULL    │              │
└─────────────────────────────────────────────────────────┘
```

```sql
SELECT * FROM events ORDER BY id;
```

```text
┌────────────────────────────┐
│ id │ city │ score          │
├────┼──────┼────────────────┤
│  1 │ SF   │              9 │
│  2 │ NYC  │              8 │
│  3 │ NULL │              7 │
└────────────────────────────┘
```

If the sample does not cover a field that appears later in the data, loading fails and returns the extra field name. Increase `SAMPLE_FILES`, `SAMPLE_RECORDS_PER_FILE`, or `SAMPLE_TOTAL_RECORDS` and retry.

## Column Match Mode

By default, column names are matched case-insensitively. Use `COLUMN_MATCH_MODE` for case-sensitive matching:

```sql
COPY INTO invoices
FROM @my_stage/
FILE_FORMAT = (TYPE = parquet MISSING_FIELD_AS = FIELD_DEFAULT)
COLUMN_MATCH_MODE = CASE_SENSITIVE;
```

## Limitations

- Currently supports **Parquet** and **NDJSON** files.
- New columns are appended to the end of the table and are always nullable.
- If the same column name appears in multiple files with **different data types**, the load fails.
- No automatic type promotion, such as `INT` to `BIGINT`.
- Column drops and renames are not supported through schema evolution.
- NDJSON relies on sampling to infer schema. If sampling does not cover all fields, increase the `SCHEMA_EVOLUTION` sampling options.
