---
title: Schema Evolution
summary: Automatically evolve table schemas when loading data with COPY INTO.
---

# Schema Evolution

Schema evolution allows {{{ .lake }}} to automatically add new columns to a table during `COPY INTO` when the source Parquet files contain columns not yet present in the table.

## How It Works

When enabled, `COPY INTO`:

1. Infers the schema from source Parquet files.
2. Adds any new columns (not in the table) as nullable columns.
3. Loads the data, filling missing values with `NULL`.

## Enabling Schema Evolution

Set the table option `ENABLE_SCHEMA_EVOLUTION` to `true`:

```sql
-- On an existing table
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

-- Or when creating a new table
CREATE TABLE my_table(id INT) ENABLE_SCHEMA_EVOLUTION = true;
```

To disable, set it back to `false`:

```sql
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = false);
```

## Tutorial

This tutorial uses a fully runnable example to demonstrate schema evolution.

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

The table now has three columns — `amount` and `currency` were added automatically:

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

## Column Match Mode

By default, column names are matched case-insensitively. Use `COLUMN_MATCH_MODE` for case-sensitive matching:

```sql
COPY INTO invoices
FROM @my_stage/
FILE_FORMAT = (TYPE = parquet MISSING_FIELD_AS = FIELD_DEFAULT)
COLUMN_MATCH_MODE = CASE_SENSITIVE;
```

## Limitations

- Supported for **Parquet** files only.
- New columns are appended to the end of the table and are always nullable.
- If the same column name appears in multiple files with **different data types**, the load fails.
- No automatic type promotion (e.g., `INT` → `BIGINT`).
- Column drops and renames are not supported through schema evolution.
