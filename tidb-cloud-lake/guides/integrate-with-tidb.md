---
title: TiDB Integration Task (Preview)
summary: Replicate data from a TiDB cluster into TiDB Cloud Lake using full snapshot loads, continuous CDC, or both.
---

# TiDB Integration Task (Preview)

A TiDB integration task replicates data from a TiDB cluster into TiDB Cloud Lake. It supports full `Snapshot` loads from a Dumpling export, continuous `Change Data Capture (CDC)` from a TiCDC changefeed, or a combination of both.

If you need to create reusable staging bucket settings first, see [TiDB Data Source](/tidb-cloud-lake/guides/tidb-data-source.md).

## Use Cases

- Migrate TiDB databases and tables into TiDB Cloud Lake for analytics
- Keep TiDB Cloud Lake continuously in sync with TiDB through TiCDC
- Consolidate sharded databases into per-source target databases in one task
- Run a full load once, or combine a full load with ongoing change capture

## Sync Modes

| Sync Mode | Description |
|-----------|-------------|
| Snapshot | Performs a one-time full data load from a Dumpling export. Ideal for initial migration or periodic bulk refresh. |
| CDC Only | Continuously consumes the TiCDC changefeed and applies real-time changes (inserts, updates, deletes). |
| Snapshot + CDC | Performs a full snapshot first, then transitions to continuous CDC. Recommended for most use cases. |

## Prerequisites

Before creating a TiDB integration task, make sure:

- A **TiDB** data source has already been created.
- The object storage bucket configured in the data source is reachable from TiDB Cloud Lake.
- The TiCDC / Dumpling export for the tables you want to sync has been written to the bucket under the prefixes you will reference in the task.

## Creating a TiDB Integration Task

This section guides you through the steps to create a TiDB integration task in TiDB Cloud Lake.

### Step 1: Configure Basic Settings

1. Navigate to **Data** > **Data Integration** and click **Create Task**.
2. Select a **TiDB** data source, then configure the basic settings:

| Field | Required | Description |
|-------|----------|-------------|
| **Data Source** | Yes | Select an existing **TiDB - Credentials** data source. You can also create one from here |
| **Name** | Yes | A name for this integration task |
| **Sync Mode** | Yes | Choose **Snapshot**, **CDC Only**, or **Snapshot + CDC** |
| **Table Rules** | Yes | Rules that select which source objects to sync. See [Table Rules](#table-rules) |
| **Max Matched Tables** | No | Upper bound on how many tables the rules may match. Leave empty to use the system default (500) |
| **Dumpling S3 Prefix** | Yes (Snapshot modes) | Bucket prefix that holds the Dumpling export, for example `dumpling/export` |
| **Table Parallelism** | No | Number of tables loaded concurrently (default: 4) |
| **Warehouse** | Yes | TiDB Cloud Lake warehouse used to run the task |

### Table Rules

Enter one rule per line. Each rule is `schemaPattern.tablePattern`, optionally prefixed with `!` to exclude:

```text
app.orders             an exact table
shard_*.*              every table of every shard_ database
!*.tmp_*               exclude temporary tables
```

Rules are evaluated from last to first. The first rule whose database and table patterns both match decides the outcome. An object that matches no rule is excluded. A list containing only exclusions gets an implicit leading `*.*`.

Each matched source database is written to its own target database, so same-named tables in different source databases stay separate. This is the only way to sync more than one source database in a single task.

Click **Preview Matched Tables** to evaluate the current rules against the objects actually present under the prefix. The preview lists the matched source database and table together with the derived target database and table.

### Snapshot Options

When the sync mode includes a snapshot, additional options control how the Dumpling export is loaded:

| Field                          | Default | Description                                                                                                              |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Auto Create Table**          | Yes     | Create the target table automatically from the source schema                                                             |
| **Purge After Load**           | No      | Delete source objects from the bucket after a successful load. Requires delete permission                                |
| **On Error**                   | Abort   | **Abort** stops at the first error; **Continue** skips failed rows and keeps loading                                     |
| **CSV Separator**              | `,`     | Field delimiter used by the Dumpling export                                                                              |
| **Skip Header Rows**           | Yes     | Whether the first row contains column names. Choose **YES** when the export has a header row                             |
| **Export Escaped Backslashes** | No      | Must match the Dumpling `--escape-backslash` setting. |

### Target Name Affixes

Target database and table names are derived from the source names, with optional affixes:

```text
target database = targetDatabasePrefix + sourceDatabase + targetDatabaseSuffix
target table    = targetTablePrefix    + sourceTable    + targetTableSuffix
```

Leave the affixes empty to use the source names as-is. Affixes may contain only letters, digits, and underscores.

For example, with a database prefix of `src_`, source database `shard_1` and table `orders` are written to `src_shard_1.orders`.

### Step 2: Create the Task

Review the settings, then click **Create** to create the integration task.

## Task Behavior by Sync Mode

| Sync Mode | Behavior |
|-----------|----------|
| Snapshot | Runs once and automatically stops after the full load completes. |
| CDC Only | Runs continuously, consuming changefeed events until manually stopped. |
| Snapshot + CDC | Completes the full snapshot first, then transitions to continuous CDC until manually stopped. |

For CDC tasks, progress is saved as a checkpoint. When the task is stopped and restarted, it resumes from the saved position instead of reloading from the beginning.

## Advanced Configuration

The following settings are task-level parameters that tune discovery, loading, and merging.

| Parameter | Default | Description |
|-----------|---------|-------------|
| **Table Parallelism** | 4 | Controls how many tables are processed concurrently. Higher values increase throughput but consume more warehouse resources. |
| **Poll Interval** | 60 seconds | How often the task lists the staging bucket (and consumes the optional SQS queue) to discover new changefeed / export objects. A shorter interval reduces latency at the cost of more list requests. For OSS, discovery uses polling only. |
| **Batch File Count** | 100 | Maximum number of CDC event files processed per batch. Adjust to balance memory use and throughput. |
| **Merge Interval** | 30 seconds | How often captured changes are merged into the target table. A shorter interval lowers latency but increases merge activity. |
| **Allow Delete** | Disabled | Whether `DELETE` operations captured from the changefeed are applied to the target table. When disabled, deletes are ignored and historical rows are retained. |
| **Max Matched Tables** | 500 | Upper bound on how many source tables the rules may match. If the rules exceed this limit, the task fails with the offending matches listed. |
