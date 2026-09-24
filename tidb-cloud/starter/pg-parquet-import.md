---
title: Import Parquet Data
summary: Learn how to query and import Parquet data into PostgreSQL-compatible TiDB Cloud Starter.
---

# Import Parquet Data

PostgreSQL-compatible {{{ .starter }}} supports the `parquet` extension for reading Parquet data and importing it into SQL tables.

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} is currently in limited public preview.

This document describes Parquet access through HTTP or HTTPS URLs. The source URL must be reachable from TiDB Cloud.

## Enable the `parquet` extension

Enable the extension in the target database:

```sql
CREATE EXTENSION IF NOT EXISTS parquet;
```

## Query a Parquet file

Use the schema-qualified `extensions.read_parquet()` table function to query a Parquet file directly:

```sql
SELECT *
FROM extensions.read_parquet('https://example.com/data.parquet');
```

For example, to count rows:

```sql
SELECT count(*)
FROM extensions.read_parquet('https://example.com/data.parquet');
```

> **Note:**
>
> `read_parquet()` must be schema-qualified as `extensions.read_parquet()`.

## Import Parquet data into a table

Use `COPY ... WITH (FORMAT parquet)` to import Parquet data into an existing table.

For example:

```sql
CREATE TABLE users (
    id BIGINT,
    name TEXT,
    created_at TIMESTAMP
);

COPY users
FROM 'https://example.com/users.parquet'
WITH (FORMAT parquet);
```

Columns are matched by name without case sensitivity.

- Parquet columns that do not have a matching target-table column are ignored.
- Target-table columns that do not have a matching Parquet column are filled with `NULL`, subject to the target column constraints.

## Type mapping

The following common Parquet types are mapped to PostgreSQL-compatible types:

| Parquet type | PostgreSQL type |
| --- | --- |
| `BOOLEAN` | `BOOLEAN` |
| `INT32` | `INTEGER` |
| `INT64` | `BIGINT` |
| `FLOAT` | `REAL` |
| `DOUBLE` | `DOUBLE PRECISION` |
| `BYTE_ARRAY` with UTF-8 annotation | `TEXT` |
| Binary `BYTE_ARRAY` | `BYTEA` |
| `INT96` timestamp | `TIMESTAMP` |
| `DATE` logical type | `DATE` |
| `TIME` logical type | `TIME` |
| `TIMESTAMP` logical type | `TIMESTAMP` |
| `DECIMAL` logical type | `NUMERIC` |

Before importing data, verify that the Parquet schema is compatible with the target table schema.

## Supported Parquet formats

The following Parquet formats are supported:

| Item | Supported value |
| --- | --- |
| Parquet versions | v1 and v2 |
| Compression codecs | Snappy, Gzip, Zstd, and uncompressed |
| Remote URL schemes | HTTP and HTTPS |

## Limitations

The following limitations apply during the limited public preview:

- The target table must exist before you run `COPY ... WITH (FORMAT parquet)`.
- Use an HTTP or HTTPS URL that is reachable from TiDB Cloud.
- Verify the Parquet column types before import. Some incompatible type combinations might not be rejected during import.
- `extensions.read_parquet()` must be called with the `extensions` schema qualifier.
- Remote requests are subject to connection and request timeouts.
