---
title: Data Pipeline Support Matrix
summary: Reference for DDL, DML, and column type support in TiDB Cloud Data Pipeline to TiDB Cloud Lake.
---

# Data Pipeline Support Matrix

This document summarizes the DDL, DML, and column type support for TiDB Cloud Data Pipeline based on tested behavior. Use it as a reference when planning your data pipeline setup or troubleshooting replication behavior.

> **Note:**
>
> This compatibility matrix is based on end-to-end testing and is not derived from the Data Pipeline implementation itself. The tested behaviors depend on the specific TiCDC and Lake versions deployed. If you observe different behavior, contact TiDB Cloud Support.

## DDL support summary

| DDL pattern                   | Status |
| ----------------------------- | -----: |
| `CREATE TABLE`                |      ✅ |
| `ADD COLUMN`                  |      ✅ |
| `ADD COLUMN NOT NULL DEFAULT` |      ✅ |
| `MODIFY COLUMN (widen)`       |      ✅ |
| `DROP COLUMN`                 |      ✅ |
| `RENAME COLUMN`               |      ✅ |

DDL operations not listed above are not processed by the pipeline and may block subsequent consumption for the affected table. In addition, combining multiple changes in a single `ALTER TABLE` statement is not supported.

## DML support summary

| DML pattern         | Status |
| ------------------- | -----: |
| `INSERT`            |      ✅ |
| `UPDATE`            |      ✅ |
| `DELETE`            |      ✅ |

DML events not listed above are not propagated to the destination.

## Type support summary

| Type category                               | Status |
| ------------------------------------------- | -----: |
| `TINYINT` ~ `BIGINT` (including `UNSIGNED`) |      ✅ |
| `BOOLEAN`                                   |      ✅ |
| `DECIMAL` / `NUMERIC`                       |      ✅ |
| `FLOAT`                                     |      ✅ |
| `DOUBLE`                                    |      ✅ |
| `DATE` / `DATETIME` / `TIMESTAMP`           |      ✅ |
| `TIME`                                      |      ✅ |
| `YEAR`                                      |      ✅ |
| `CHAR` / `VARCHAR` / `TEXT`                 |      ✅ |
| `ENUM`                                      |      ✅ |
| `SET`                                       |      ✅ |
| `JSON`                                      |      ✅ |
| `BINARY` / `VARBINARY`                      |      ✅ |
| `BLOB`                                      |      ✅ |
| `BIT(1)`                                    |      ✅ |
| `BIT(>1)`                                   |      ✅ |
| `VECTOR`                                    |      ✅ |

Column types not listed above are not tested and may not be supported.
