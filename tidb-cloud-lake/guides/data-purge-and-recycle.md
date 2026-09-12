---
title: 数据清理与回收
summary: 在 {{{ .lake }}} 中，执行 `DROP`、`TRUNCATE` 或 `DELETE` 命令时，数据不会被立即删除。这使得 {{{ .lake }}} 的时间旅行功能得以实现，允许你访问数据的先前状态。不过，这种方式也意味着在执行这些操作后，存储空间不会被自动释放。
---

# 数据清理与回收

## 概述 {#overview}

在 {{{ .lake }}} 中，执行 `DROP`、`TRUNCATE` 或 `DELETE` 命令时，数据不会被立即删除。这使得 {{{ .lake }}} 的时间旅行功能得以实现，允许你访问数据的先前状态。不过，这种方式也意味着在执行这些操作后，存储空间不会被自动释放。

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

## VACUUM 命令与清理范围 {#vacuum-commands-and-cleanup-scope}

{{{ .lake }}} 提供了三种 VACUUM 命令，它们的**清理范围各不相同**。了解每种命令会清理哪些内容，对于数据管理至关重要。

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

> **🚨 关键提示**：只有 `VACUUM DROP TABLE` 会影响 meta service。其他命令只会清理存储文件。

## 使用 VACUUM 命令 {#using-vacuum-commands}

VACUUM 命令族是在 {{{ .lake }}} 中清理数据的主要方法。

### VACUUM DROP TABLE {#vacuum-drop-table}

从存储和元信息中永久移除已删除的表。

```sql
VACUUM DROP TABLE [FROM <database_name>] [DRY RUN [SUMMARY]] [LIMIT <file_count>];
```

**选项：**

- `FROM <database_name>`：限制为特定数据库
- `DRY RUN [SUMMARY]`：预览将要移除的文件，而不实际删除它们
- `LIMIT <file_count>`：限制要执行 vacuum 的文件数量

**示例：**

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

### VACUUM TABLE {#vacuum-table}

移除活动表的历史数据和孤儿文件（仅清理存储）。

```sql
VACUUM TABLE <table_name> [DRY RUN [SUMMARY]];
```

**选项：**

- `DRY RUN [SUMMARY]`：预览将要移除的文件，而不实际删除它们

**示例：**

```sql
-- Preview files that would be removed
VACUUM TABLE my_table DRY RUN;

-- Preview summary of files that would be removed
VACUUM TABLE my_table DRY RUN SUMMARY;

-- Remove historical data from my_table
VACUUM TABLE my_table;
```

### VACUUM TEMPORARY FILES {#vacuum-temporary-files}

移除查询执行期间创建的临时 spill 文件。

```sql
VACUUM TEMPORARY FILES;
```

> **Note:**
>
> 在正常运行期间通常很少需要使用，因为 {{{ .lake }}} 会自动处理清理。通常只有在 {{{ .lake }}} 在查询执行期间发生崩溃时，才需要手动清理。

## 调整数据保留时间 {#adjusting-data-retention-time}

VACUUM 命令会移除早于 `DATA_RETENTION_TIME_IN_DAYS` 设置的数据文件。默认情况下，{{{ .lake }}} 会保留 1 天（24 小时）的历史数据。你可以调整此设置：

```sql
-- Change retention period to 2 days
SET GLOBAL DATA_RETENTION_TIME_IN_DAYS = 2;

-- Check current retention setting
SHOW SETTINGS LIKE 'DATA_RETENTION_TIME_IN_DAYS';
```

| 版本                                  | 默认保留期 | 最大保留期 |
| ---------------------------------------- | ----------------- | ---------------- |
| {{{ .lake }}} 社区版和企业版 | 1 天（24 小时）  | 90 天          |
| {{{ .lake }}}（个人版）                | 1 天（24 小时）  | 1 天（24 小时） |
| {{{ .lake }}}（商业版）                | 1 天（24 小时）  | 90 天          |