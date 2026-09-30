---
title: Data Pipeline SQL Compatibility for TiDB Cloud Lake
summary: Reference for DDL, DML, and TiDB-to-TiDB Cloud Lake type mapping behavior in TiDB Cloud Data Pipeline.
---

# Data Pipeline SQL Compatibility for TiDB Cloud Lake

This document describes the DDL, DML, and column type support for TiDB Cloud Data Pipeline when replicating data to TiDB Cloud Lake. Use it to plan your pipeline, validate schema compatibility, or troubleshoot type conversions.

> **Note:**
>
> Supported behavior depends on the TiCDC and TiDB Cloud Lake versions in use. If you observe different behavior, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## DDL support summary

| DDL operation | Status | Notes |
| -------------------- | -----: | ----- |
| `CREATE TABLE` | ✅ |  |
| `ADD COLUMN` | ✅ |  |
| `ADD COLUMN ... NOT NULL DEFAULT ...` | ✅ |  |
| `DROP COLUMN` | ✅ |  |
| `RENAME COLUMN` | ✅ |  |
| `MODIFY COLUMN` | ⚠️ Partial support | Supported only for the schema-evolution cases listed below. Other conversions are not guaranteed and can block downstream consumption. |

### Supported `MODIFY COLUMN` conversions

| From | To | Notes |
| ---- | -- | ----- |
| `VARCHAR` | `TEXT` | Common widening conversion during schema evolution. |
| `TINYINT` | `INT` | Promotes integer storage width. |
| `INT` | `BIGINT` | Common widening conversion during schema evolution. |
| `INT` | `VARCHAR` / `TEXT` | Used when the target type is converted to a string representation. |

DDL operations not listed here are not processed by the pipeline and might block subsequent consumption for the affected table. In addition, combining multiple changes in a single `ALTER TABLE` statement is not supported.

## DML support summary

| DML operation | Status |
| ------------ | -----: |
| `INSERT` | ✅ |
| `UPDATE` | ✅ |
| `DELETE` | ✅ |

DML operations not listed here are not propagated to the destination.

## Type mapping reference

### Integer types

| TiDB type | TiDB Cloud Lake type |
| --------- | -------------------- |
| `TINYINT` | `INT8` |
| `TINYINT UNSIGNED` | `UINT8` |
| `SMALLINT` | `INT16` |
| `SMALLINT UNSIGNED` | `UINT16` |
| `MEDIUMINT` | `INT32` |
| `INT` / `INTEGER` | `INT32` |
| `MEDIUMINT UNSIGNED` / `INT UNSIGNED` / `INTEGER UNSIGNED` | `UINT32` |
| `BIGINT` | `INT64` |
| `BIGINT UNSIGNED` | `UINT64` |

### Floating-point types

| TiDB type | TiDB Cloud Lake type |
| --------- | -------------------- |
| `FLOAT` | `FLOAT32` |
| `DOUBLE` / `REAL` | `FLOAT64` |

### Exact numeric types

| TiDB type | TiDB Cloud Lake type | Notes |
| --------- | -------------------- | ----- |
| `DECIMAL(P,S)` | `DECIMAL(P,S)` | Precision and scale are preserved exactly. The same applies to `NUMERIC(P,S)`. |
| `DECIMAL` (no precision) | `DECIMAL(76,30)` | Automatically widened to the maximum valid precision to avoid silent truncation. |
| `NUMERIC` (no precision) | `DECIMAL(76,30)` | Same as above. |

### Date and time types

| TiDB type | TiDB Cloud Lake type | Notes |
| --------- | -------------------- | ----- |
| `DATE` | `DATE` |  |
| `DATETIME` / `DATETIME(n)` | `TIMESTAMP` | Fractional-second precision is supported. |
| `TIMESTAMP` / `TIMESTAMP(n)` | `TIMESTAMP` | Fractional-second precision is supported. |
| `TIME` | `VARCHAR` | TiDB Cloud Lake has no standalone `TIME` type, so it is stored as text. |
| `YEAR` | `INT16` | Mapped as an integer, not a temporal type. |

### String types

| TiDB type | TiDB Cloud Lake type | Notes |
| --------- | -------------------- | ----- |
| `CHAR` / `VARCHAR` | `VARCHAR` | Length is not preserved. |
| `TINYTEXT` / `TEXT` / `MEDIUMTEXT` / `LONGTEXT` | `VARCHAR` |  |
| `ENUM` | `VARCHAR` | Requires a `content-compatible=true` changefeed to preserve the enum text. |
| `SET` | `VARCHAR` | Requires a `content-compatible=true` changefeed to preserve the element text. |

### Binary types

| TiDB type | TiDB Cloud Lake type |
| --------- | -------------------- |
| `BINARY` / `VARBINARY` | `BINARY` |
| `TINYBLOB` / `BLOB` / `MEDIUMBLOB` / `LONGBLOB` | `BINARY` |

### Other types

| TiDB type | TiDB Cloud Lake type | Notes |
| --------- | -------------------- | ----- |
| `BOOLEAN` / `BOOL` | `BOOLEAN` |  |
| `BIT` | `UINT64` | Always mapped as unsigned. All-ones `BIT(64)` exceeds the signed `INT64` range. |
| `JSON` | `VARIANT` |  |
| Unknown / unlisted type | `VARCHAR` | Fallback mapping; typed semantics are lost. |
