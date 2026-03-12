---
title: Fuse Engine Tables
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.736"/>

## Overview

Databend uses the Fuse Engine as its default storage engine, providing a Git-like data management system with:

- **Snapshot-based Architecture**: Query and restore data at any point in time, with history of data changes for recovery
- **High Performance**: Optimized for analytical workloads with automatic indexing and bloom filters
- **Efficient Storage**: Uses Parquet format with high compression for optimal storage efficiency
- **Flexible Configuration**: Customizable compression, indexing, and storage options
- **Data Maintenance**: Automatic data retention, snapshot management, and change tracking capabilities

## When to Use Fuse Engine

Ideal for:
- **Analytics**: OLAP queries with columnar storage
- **Data Warehousing**: Large volumes of historical data
- **Time-Travel**: Access to historical data versions
- **Cloud Storage**: Optimized for object storage

## Syntax

```sql
CREATE TABLE <table_name> (
  <column_definitions>
) [ENGINE = FUSE]
[CLUSTER BY (<expr> [, <expr>, ...] )]
[<Options>];
```

For more details about the `CREATE TABLE` syntax, see [CREATE TABLE](../../10-sql-commands/00-ddl/01-table/10-ddl-create-table.md).

## Parameters

Below are the main parameters for creating a Fuse Engine table:

#### `ENGINE`
- **Description:**
  If an engine is not explicitly specified, Databend will automatically default to using the Fuse Engine to create tables, which is equivalent to `ENGINE = FUSE`.

---

#### `CLUSTER BY`
- **Description:**
  Specifies the sorting method for data that consists of multiple expressions. For more information, see [Cluster Key](/guides/performance/cluster-key).

---

#### `<Options>`
- **Description:**
  The Fuse Engine offers various options (case-insensitive) that allow you to customize the table's properties.
  - See [Fuse Engine Options](#fuse-engine-options) for details.
  - Separate multiple options with a space.
  - Use [ALTER TABLE](../../10-sql-commands/00-ddl/01-table/90-alter-table.md#fuse-engine-options) to modify a table's options.
  - Use [SHOW CREATE TABLE](../../10-sql-commands/00-ddl/01-table/show-create-table.md) to show a table's options.

---

## Fuse Engine Options

Below are the available Fuse Engine options, grouped by their purpose:

---

### `compression`
- **Syntax:**
  `compression = '<compression>'`
- **Description:**
  Specifies the compression method for the engine. Compression options include lz4, zstd, snappy, or none. The compression method defaults to zstd in object storage and lz4 in file system (fs) storage.

---

### `snapshot_loc`
- **Syntax:**
  `snapshot_loc = '<snapshot_loc>'`
- **Description:**
  Specifies a location parameter in string format, allowing easy sharing of a table without data copy.

---


### `block_size_threshold`
- **Syntax:**
  `block_size_threshold = <n>`
- **Description:**
  Specifies the maximum block size in bytes. Defaults to 104,857,600 bytes.

---

### `block_per_segment`
- **Syntax:**
  `block_per_segment = <n>`
- **Description:**
  Specifies the maximum number of blocks in a segment. Defaults to 1,000.

---

### `row_per_block`
- **Syntax:**
  `row_per_block = <n>`
- **Description:**
  Specifies the maximum number of rows in a file. Defaults to 1,000,000.

---

### `bloom_index_columns`
- **Syntax:**
  `bloom_index_columns = '<column> [, <column> ...]'`
- **Description:**
  Specifies the columns to be used for the bloom index. The data type of these columns can be Map, Number, String, Date, or Timestamp. If no specific columns are specified, the bloom index is created by default on all supported columns. `bloom_index_columns=''` disables the bloom indexing.

---

### `change_tracking`
- **Syntax:**
  `change_tracking = True / False`
- **Description:**
  Setting this option to `True` in the Fuse Engine allows for tracking changes for a table. Creating a stream for a table will automatically set `change_tracking` to `True` and introduce additional hidden columns to the table as change tracking metadata. For more information, see [How Stream Works](/guides/load-data/continuous-data-pipelines/stream#how-stream-works).

---

### `data_retention_period_in_hours`
- **Syntax:**
  `data_retention_period_in_hours = <n>`
- **Description:**
  Specifies the number of hours to retain table data. The minimum value is 1 hour. The maximum value is defined by the `data_retention_time_in_days_max` setting in the [databend-query.toml](https://github.com/databendlabs/databend/blob/main/scripts/distribution/configs/databend-query.toml) configuration file, or defaults to 2,160 hours (90 days x 24 hours) if not specified.

---

### `enable_auto_vacuum`
- **Syntax:**
  `enable_auto_vacuum = 0 / 1`
- **Description:**
  Controls whether a table automatically triggers vacuum operations during mutations. This can be set globally as a setting for all tables or configured at the table level. The table-level option has a higher priority than the session/global setting of the same name. When enabled (set to 1), vacuum operations will be automatically triggered after mutations like INSERT or ALTER TABLE, cleaning up the table data according to the configured retention policy.

  **Examples:**
  ```sql
  -- Set enable_auto_vacuum globally for all tables across all sessions
  SET GLOBAL enable_auto_vacuum = 1;
  
  -- Create a table with auto vacuum disabled (overrides global setting)
  CREATE OR REPLACE TABLE t1 (id INT) ENABLE_AUTO_VACUUM = 0;
  INSERT INTO t1 VALUES(1); -- Won't trigger vacuum despite global setting
  
  -- Create another table that inherits the global setting
  CREATE OR REPLACE TABLE t2 (id INT);
  INSERT INTO t2 VALUES(1); -- Will trigger vacuum due to global setting
  
  -- Enable auto vacuum for an existing table
  ALTER TABLE t1 SET OPTIONS(ENABLE_AUTO_VACUUM = 1);
  INSERT INTO t1 VALUES(2); -- Now will trigger vacuum
  
  -- Table option takes precedence over global settings
  SET GLOBAL enable_auto_vacuum = 0; -- Turn off globally
  -- t1 will still vacuum because table setting overrides global
  INSERT INTO t1 VALUES(3); -- Will still trigger vacuum
  INSERT INTO t2 VALUES(2); -- Won't trigger vacuum anymore
  ```

---

### `data_retention_num_snapshots_to_keep`
- **Syntax:**
  `data_retention_num_snapshots_to_keep = <n>`
- **Description:**
  Specifies the number of snapshots to retain during vacuum operations. This can be set globally as a setting for all tables or configured at the table level. The table-level option has a higher priority than the session/global setting of the same name. When set, only the specified number of most recent snapshots will be kept after vacuum operations. Overrides the `data_retention_time_in_days` setting. If set to 0, this setting will be ignored. This option works in conjunction with the `enable_auto_vacuum` setting to provide granular control over snapshot retention policies.
  
  **Examples:**
  ```sql
  -- Set global retention to 10 snapshots for all tables across all sessions
  SET GLOBAL data_retention_num_snapshots_to_keep = 10;
  
  -- Create a table with custom snapshot retention (overrides global setting)
  CREATE OR REPLACE TABLE t1 (id INT) 
    enable_auto_vacuum = 1
    data_retention_num_snapshots_to_keep = 5;
  
  -- Create another table that inherits the global setting
  CREATE OR REPLACE TABLE t2 (id INT) enable_auto_vacuum = 1;
  
  -- When vacuum is triggered:
  -- t1 will keep 5 snapshots (table setting)
  -- t2 will keep 10 snapshots (global setting)
  
  -- Change global setting
  SET GLOBAL data_retention_num_snapshots_to_keep = 20;
  
  -- Table options still take precedence:
  -- t1 will still keep only 5 snapshots
  -- t2 will now keep 20 snapshots
  
  -- Modify snapshot retention for an existing table
  ALTER TABLE t1 SET OPTIONS(data_retention_num_snapshots_to_keep = 3);
  -- Now t1 will keep 3 snapshots when vacuum is triggered
  ```

---
