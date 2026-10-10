---
title: データのパージとリサイクル
summary: "{{{ .lake }}} では、`DROP`、`TRUNCATE`、または `DELETE` コマンドを実行しても、データはすぐには削除されません。これにより、{{{ .lake }}} のタイムトラベル機能が有効になり、データの過去の状態にアクセスできます。ただし、この方式では、これらの操作の後にストレージ領域が自動的に解放されません。"
---

# データのパージとリサイクル

## 概要 {#overview}

{{{ .lake }}} では、`DROP`、`TRUNCATE`、または `DELETE` コマンドを実行しても、データはすぐには削除されません。これにより、{{{ .lake }}} のタイムトラベル機能が有効になり、データの過去の状態にアクセスできます。ただし、この方式では、これらの操作の後にストレージ領域が自動的に解放されません。

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

## VACUUM コマンドとクリーンアップ範囲 {#vacuum-commands-and-cleanup-scope}

{{{ .lake }}} は、**クリーンアップ範囲が異なる** 3 つの VACUUM コマンドを提供します。各コマンドが何をクリーンアップするのかを理解することは、データ管理において重要です。

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

> **🚨 Critical**: meta service に影響するのは `VACUUM DROP TABLE` のみです。その他のコマンドはストレージファイルのみをクリーンアップします。

## VACUUM コマンドの使用 {#using-vacuum-commands}

VACUUM コマンド群は、{{{ .lake }}} でデータをクリーンアップするための主要な方法です。

### VACUUM DROP TABLE {#vacuum-drop-table}

削除済みテーブルを、ストレージとメタデータの両方から完全に削除します。

```sql
VACUUM DROP TABLE [FROM <database_name>] [DRY RUN [SUMMARY]] [LIMIT <file_count>];
```

**Options:**

- `FROM <database_name>`: 特定のデータベースに限定します
- `DRY RUN [SUMMARY]`: 実際には削除せずに、削除対象となるファイルをプレビューします
- `LIMIT <file_count>`: vacuum 対象のファイル数を制限します

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

### VACUUM TABLE {#vacuum-table}

アクティブなテーブルの履歴データと孤立ファイルを削除します（ストレージのみのクリーンアップ）。

```sql
VACUUM TABLE <table_name> [DRY RUN [SUMMARY]];
```

**Options:**

- `DRY RUN [SUMMARY]`: 実際には削除せずに、削除対象となるファイルをプレビューします

**Examples:**

```sql
-- Preview files that would be removed
VACUUM TABLE my_table DRY RUN;

-- Preview summary of files that would be removed
VACUUM TABLE my_table DRY RUN SUMMARY;

-- Remove historical data from my_table
VACUUM TABLE my_table;
```

### VACUUM TEMPORARY FILES {#vacuum-temporary-files}

クエリ実行中に作成された一時 spill ファイルを削除します。

```sql
VACUUM TEMPORARY FILES;
```

> **Note:**
>
> 通常運用では必要になることはほとんどありません。これは、{{{ .lake }}} が自動的にクリーンアップを処理するためです。手動でのクリーンアップが必要になるのは、通常、クエリ実行中に {{{ .lake }}} がクラッシュした場合のみです。

## データ保持期間の調整 {#adjusting-data-retention-time}

VACUUM コマンドは、`DATA_RETENTION_TIME_IN_DAYS` 設定より古いデータファイルを削除します。デフォルトでは、{{{ .lake }}} は履歴データを 1 日（24 時間）保持します。この設定は調整できます。

```sql
-- Change retention period to 2 days
SET GLOBAL DATA_RETENTION_TIME_IN_DAYS = 2;

-- Check current retention setting
SHOW SETTINGS LIKE 'DATA_RETENTION_TIME_IN_DAYS';
```

| エディション | デフォルトの保持期間 | 最大保持期間 |
| ---------------------------------------- | ----------------- | ---------------- |
| {{{ .lake }}} Community & Enterprise エディション | 1 日 (24 時間)  | 90 日          |
| {{{ .lake }}} (Personal)                | 1 日 (24 時間)  | 1 日 (24 時間) |
| {{{ .lake }}} (Business)                | 1 日 (24 時間)  | 90 日          |