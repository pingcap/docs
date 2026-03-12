---
title: Data Purge and Recycle
sidebar_label: Data Recycle
---

## Overview

In Databend, data is not immediately deleted when you run `DROP`, `TRUNCATE`, or `DELETE` commands. This enables Databend's time travel feature, allowing you to access previous states of your data. However, this approach means that storage space is not automatically freed up after these operations.

```
Before DELETE:                After DELETE:                 After VACUUM:
+----------------+           +----------------+           +----------------+
| Current Data   |           | New Version    |           | Current Data   |
|                |           | (After DELETE) |           | (After DELETE) |
+----------------+           +----------------+           +----------------+
| Historical Data|           | Historical Data|           |                |
| (Time Travel)  |           | (Original Data)|           |                |
+----------------+           +----------------+           +----------------+
                             Storage not freed            Storage freed
```

## VACUUM Commands and Cleanup Scope

Databend provides three VACUUM commands with **different cleanup scopes**. Understanding what each command cleans is crucial for data management.

```
VACUUM DROP TABLE
├── Target: Dropped tables (after DROP TABLE command)
├── S3 Storage: ✅ Removes ALL data (files, segments, blocks, indexes, statistics)  
├── Meta Service: ✅ Removes ALL metadata (schema, permissions, records)
└── Result: Complete table removal - CANNOT be recovered

VACUUM TABLE
├── Target: Historical data and orphan files for active tables
├── S3 Storage: ✅ Removes old snapshots, orphan segments/blocks, indexes/stats
├── Meta Service: ❌ Preserves table structure and current metadata
└── Result: Table stays active, only history cleaned

VACUUM TEMPORARY FILES  
├── Target: Temporary spill files from queries (joins, sorts, aggregates)
├── S3 Storage: ✅ Removes temp files from crashed/interrupted queries
├── Meta Service: ❌ No metadata (temp files don't have any)
└── Result: Storage cleanup only, rarely needed
```

---

> **🚨 Critical**: Only `VACUUM DROP TABLE` affects the meta service. Other commands only clean storage files.

## Using VACUUM Commands

The VACUUM command family is the primary method for cleaning data in Databend ([Enterprise Edition Feature](/guides/self-hosted/editions/enterprise/features)).

### VACUUM DROP TABLE

Permanently removes dropped tables from both storage and metadata.

```sql
VACUUM DROP TABLE [FROM <database_name>] [DRY RUN [SUMMARY]] [LIMIT <file_count>];
```

**Options:**
- `FROM <database_name>`: Restrict to a specific database
- `DRY RUN [SUMMARY]`: Preview files to be removed without actually deleting them
- `LIMIT <file_count>`: Limit the number of files to be vacuumed

**Examples:**

```sql
-- Preview files that would be removed
VACUUM DROP TABLE DRY RUN;

-- Preview summary of files that would be removed
VACUUM DROP TABLE DRY RUN SUMMARY;

-- Remove dropped tables from the "default" database
VACUUM DROP TABLE FROM default;

-- Remove up to 1000 files from dropped tables
VACUUM DROP TABLE LIMIT 1000;
```

### VACUUM TABLE

Removes historical data and orphan files for active tables (storage-only cleanup).

```sql
VACUUM TABLE <table_name> [DRY RUN [SUMMARY]];
```

**Options:**
- `DRY RUN [SUMMARY]`: Preview files to be removed without actually deleting them

**Examples:**

```sql
-- Preview files that would be removed
VACUUM TABLE my_table DRY RUN;

-- Preview summary of files that would be removed
VACUUM TABLE my_table DRY RUN SUMMARY;

-- Remove historical data from my_table
VACUUM TABLE my_table;
```

### VACUUM TEMPORARY FILES

Removes temporary spill files created during query execution.

```sql
VACUUM TEMPORARY FILES;
```

> **Note**: Rarely needed during normal operation since Databend automatically handles cleanup. Manual cleanup is typically only required when Databend crashes during query execution.

## Adjusting Data Retention Time

The VACUUM commands remove data files older than the `DATA_RETENTION_TIME_IN_DAYS` setting. By default, Databend retains historical data for 1 day (24 hours). You can adjust this setting:

```sql
-- Change retention period to 2 days
SET GLOBAL DATA_RETENTION_TIME_IN_DAYS = 2;

-- Check current retention setting
SHOW SETTINGS LIKE 'DATA_RETENTION_TIME_IN_DAYS';
```

| Edition                                  | Default Retention | Maximum Retention |
| ---------------------------------------- | ----------------- | ---------------- |
| Databend Community & Enterprise Editions | 1 day (24 hours)  | 90 days          |
| Databend Cloud (Personal)                | 1 day (24 hours)  | 1 day (24 hours) |
| Databend Cloud (Business)                | 1 day (24 hours)  | 90 days          |
