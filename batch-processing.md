---
title: Batch Processing
summary: Introduces batch processing features in TiDB, including Pipelined DML, non-transactional DML, the `IMPORT INTO` statement, and the deprecated batch-dml feature.
---

# Batch Processing

Batch processing is a common and essential operation in real-world scenarios. It enables efficient handling of large datasets for tasks such as data migration, bulk imports, archiving, and large-scale updates.

To optimize performance for batch operations, TiDB introduces various features over its version evolution:

- Data import
    - `IMPORT INTO` statement (introduced in TiDB v7.2.0 and GA in v7.5.0)
- Data inserts, updates, and deletions
    - Pipelined DML (experimental, introduced in TiDB v8.0.0)
    - Non-transactional DML (introduced in TiDB v6.1.0)
    - Batch-dml (deprecated)

This document outlines the key benefits, limitations, and use cases of these features to help you choose the most suitable solution for efficient batch processing.

## Data import

The `IMPORT INTO` statement is designed for data import tasks. It allows you to quickly import data in formats such as CSV, SQL, or PARQUET into an empty TiDB table, without the need to deploy [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) separately.

### Key benefits

- Extremely fast import speed
- Easier to use compared to TiDB Lightning

### Limitations

- No transactional [ACID](/glossary.md#acid) guarantees
- Subject to various usage restrictions

### Use cases

- Suitable for data import scenarios such as data migration or recovery. It is recommended to use `IMPORT INTO` instead of TiDB Lightning where applicable.

For more information, see [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md).

## Data inserts, updates, and deletions

### Pipelined DML

Pipelined DML is an experimental feature introduced in TiDB v8.0.0. In v8.5.0, the feature is enhanced with significant performance improvements.

#### Key benefits

- Streams data to the storage layer during transaction execution instead of buffering it entirely in memory, allowing transaction size no longer limited by TiDB memory and supporting ultra-large-scale data processing
- Achieves faster performance compared to standard DML
- Can be enabled through system variables without SQL modifications

#### Limitations

- Only supports [autocommit](/transaction-overview.md#autocommit) `INSERT`, `REPLACE`, `UPDATE`, and `DELETE` statements.

#### Use cases

- Suitable for general batch processing tasks, such as bulk data inserts, updates, and deletions.

For more information, see [Pipelined DML](/pipelined-dml.md).

### Non-transactional DML statements

Non-transactional DML is introduced in TiDB v6.1.0. Initially, only the `DELETE` statement supports this feature. Starting from v6.5.0, `INSERT`, `REPLACE`, and `UPDATE` statements also supports this feature.

#### Key benefits

- Splits a single SQL statement into multiple smaller statements, bypassing memory limitations.
- Achieves performance that is slightly faster or comparable to standard DML.

#### Limitations

- Only supports [autocommit](/transaction-overview.md#autocommit) statements
- Requires modifications to SQL statements
- Imposes strict requirements on SQL syntax; some statements might need rewriting
- Lacks full transactional ACID guarantees; in case of failures, partial execution of a statement might occur

#### Use cases

- Suitable for scenarios involving bulk data inserts, updates, and deletions. Due to its limitations, it is recommended to consider non-transactional DML only when Pipelined DML is not applicable.

For more information, see [Non-transactional DML](/non-transactional-dml.md).

### Deprecated batch-dml feature

The batch-dml feature, available in TiDB versions prior to v4.0, is now deprecated and no longer recommended. This feature is controlled by the following system variables:

- `tidb_batch_insert`
- `tidb_batch_delete`
- `tidb_batch_commit`
- `tidb_enable_batch_dml`
- `tidb_dml_batch_size`

Due to the risk of data corruption or loss caused by inconsistent data and indexes, these variables have been deprecated and are planned for removal in future releases.

It is **NOT RECOMMENDED** to use the deprecated batch-dml feature under any circumstances. Instead, consider other alternative features outlined in this document.