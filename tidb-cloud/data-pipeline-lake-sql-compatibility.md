---
title: Data Pipeline Support Matrix
summary: Reference for DDL, DML, and column type support in TiDB Cloud Data Pipeline to TiDB Cloud Lake.
---

# Data Pipeline Support Matrix

This document summarizes the DDL, DML, and column type support for TiDB Cloud Data Pipeline based on tested behavior. Use it as a reference when planning your data pipeline setup or troubleshooting replication behavior.

> **Note:**
>
> This compatibility matrix is based on end-to-end testing and is not derived from the Data Pipeline implementation itself. The tested behaviors depend on the TiCDC and TiDB Cloud Lake versions used in the testing. If you observe different behavior, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## DDL support summary

| DDL operation                     | Status |
| ---------------------------------------- | -----: |
| `CREATE TABLE`                           |      ✅ |
| `ADD COLUMN`                             |      ✅ |
| `ADD COLUMN ... NOT NULL DEFAULT ...`    |      ✅ |
| `MODIFY COLUMN` (widening a column type) |      ✅ |
| `DROP COLUMN`                            |      ✅ |
| `RENAME COLUMN`                          |      ✅ |

DDL operations not listed here are not processed by the pipeline and might block subsequent consumption for the affected table. In addition, combining multiple changes in a single `ALTER TABLE` statement is not supported.

## DML support summary

| DML operation | Status |
| -------------------- | -----: |
| `INSERT`             |      ✅ |
| `UPDATE`             |      ✅ |
| `DELETE`             |      ✅ |

DML operations not listed here are not propagated to the destination.

## Type support summary

| Type category                               | Status |
| ------------------------------------------- | -----: |
| `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, and `BIGINT` (including `UNSIGNED` variants) |      ✅ |
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
| `BIT(M)`, where `2 <= M <= 64`              |      ✅ |
| `VECTOR`                                    |      ✅ |

Column types not listed here have not been tested and might not be supported.
