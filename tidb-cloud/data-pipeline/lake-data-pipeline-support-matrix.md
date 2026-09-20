---
title: Data Pipeline Support Matrix
summary: Reference for DDL, DML, and column type support in TiDB Cloud Data Pipeline to TiDB Cloud Lake.
---

# Data Pipeline Support Matrix

This document summarizes the DDL, DML, and column type support for TiDB Cloud Data Pipeline. Use it as a reference when planning your data pipeline setup or troubleshooting replication behavior.

Legend:
- ✅ = Supported
- N/A = Not processed

---

## DDL support summary

| DDL pattern                   | Status | Behavior / symptom                                                                                      |
| ----------------------------- | -----: | ------------------------------------------------------------------------------------------------------- |
| `CREATE TABLE`                |      ✅ |                                                                                                         |
| `ADD COLUMN`                  |      ✅ |                                                                                                         |
| `ADD COLUMN NOT NULL DEFAULT` |      ✅ |                                                                                                         |
| `MODIFY COLUMN (widen)`       |      ✅ |                                                                                                         |
| `DROP COLUMN`                 |      ✅ |                                                                                                         |
| `ADD INDEX` / `DROP INDEX`    |      ✅ |                                                                                                         |
| `RENAME COLUMN`               |      ✅ |                                                                                                         |
| `DROP TABLE`                  |    N/A | Destination table is kept in Lake.                                                                      |
| `RENAME TABLE`                |    N/A | New table only has rows after rename; old table keeps pre-rename rows. Data is split across two tables. |
| `TRUNCATE`                    |    N/A | Destination retains pre-truncate data.                                                                  |

## DML support summary

| DML pattern           | Status | Behavior / symptom                  |
| --------------------- | -----: | ----------------------------------- |
| `INSERT`              |      ✅ |                                     |
| `UPDATE`              |      ✅ |                                     |
| `DELETE`              |      ✅ |                                     |
| `DELETE + reinsert`   |      ✅ |                                     |
| `TRUNCATE + reinsert` |    N/A | `TRUNCATE` event is not propagated. |

## Type support summary

| Type category                               | Status | Notes / caveat                   |
| ------------------------------------------- | -----: | -------------------------------- |
| `TINYINT` ~ `BIGINT` (including `UNSIGNED`) |      ✅ |                                  |
| `BOOLEAN`                                   |      ✅ |                                  |
| `DECIMAL` / `NUMERIC`                       |      ✅ |                                  |
| `FLOAT`                                     |      ✅ |                                  |
| `DOUBLE`                                    |      ✅ |                                  |
| `DATE` / `DATETIME` / `TIMESTAMP`           |      ✅ |                                  |
| `TIME`                                      |      ✅ |                                  |
| `YEAR`                                      |      ✅ |                                  |
| `CHAR` / `VARCHAR` / `TEXT`                 |      ✅ |                                  |
| `ENUM`                                      |      ✅ |                                  |
| `SET`                                       |      ✅ |                                  |
| `JSON`                                      |      ✅ |                                  |
| `BINARY` / `VARBINARY`                      |      ✅ |                                  |
| `BLOB`                                      |      ✅ |                                  |
| `BIT(1)`                                    |      ✅ |                                  |
| `BIT(>1)`                                   |      ✅ |                                  |
| `VECTOR`                                    |      ✅ |                                  |
| `VARIANT` / `ARRAY` / `OBJECT`              |    N/A | Not applicable to Data Pipeline. |
| `GEOGRAPHY` / `GEOMETRY`                    |    N/A | Not applicable to Data Pipeline. |
