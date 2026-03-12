---
title: VACUUM TABLE
sidebar_position: 17
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='VACUUM TABLE'/>

The VACUUM TABLE command helps optimize system performance by freeing up storage space through the permanent removal of historical data files from a table. This includes:

- Snapshots associated with the table, as well as their relevant segments and blocks.

- Orphan files. Orphan files in Databend refer to snapshots, segments, and blocks that are no longer associated with the table. Orphan files might be generated from various operations and errors, such as during data backups and restores, and can take up valuable disk space and degrade the system performance over time.

See also: [VACUUM DROP TABLE](91-vacuum-drop-table.md)

### Syntax and Examples

```sql
VACUUM TABLE <table_name> [ DRY RUN [SUMMARY] ]
```

- `DRY RUN [SUMMARY]`: When this parameter is specified, candidate orphan files will not be removed. Instead, a list of up to 1,000 candidate files and their sizes (in bytes) will be returned, showing what would have been removed if the option was not used. When the optional parameter `SUMMARY` is included, the command returns the total number of files to be removed and their combined size in bytes.

### Output

The VACUUM TABLE command (without `DRY RUN`) returns a table summarizing vital statistics of the vacuumed files, containing the following columns:

| Column         | Description                               |
| -------------- | ----------------------------------------- |
| snapshot_files | Number of snapshot files                  |
| snapshot_size  | Total size of snapshot files in bytes     |
| segments_files | Number of segment files                   |
| segments_size  | Total size of segment files in bytes      |
| block_files    | Number of block files                     |
| block_size     | Total size of block files in bytes        |
| index_files    | Number of index files                     |
| index_size     | Total size of index files in bytes        |
| total_files    | Total number of all types of files        |
| total_size     | Total size of all types of files in bytes |

```sql title='Example:'
// highlight-next-line
VACUUM TABLE c;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ snapshot_files │ snapshot_size │ segments_files │ segments_size │ block_files │ block_size │ index_files │ index_size │ total_files │ total_size │
├────────────────┼───────────────┼────────────────┼───────────────┼─────────────┼────────────┼─────────────┼────────────┼─────────────┼────────────┤
│              3 │          1954 │              9 │          4802 │           9 │       1890 │           9 │       3060 │          30 │      11706 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

When the `DRY RUN` parameter is specified with the VACUUM TABLE command, it returns a list of up to 1,000 candidate files and their sizes in bytes. If `DRY RUN SUMMARY` is specified, the command provides the total number of files to be removed and their combined size.

```sql title='Example:'
// highlight-next-line
VACUUM TABLE c DRY RUN;

┌──────────────────────────────────────────────────────────────┐
│                       file                       │ file_size │
├──────────────────────────────────────────────────┼───────────┤
│ 1/67/_ss/61aaf678b9af41568b539099b4b09908_v4.mpk │       543 │
│ 1/67/_ss/dd149d21151c459d8c87076f9412c12c_v4.mpk │       516 │
│ 1/67/_ss/7ba0b2e2f63c4d42897a48830027dcf3_v4.mpk │       462 │
│ 1/67/_ss/db55dac72b29452db976cf0af0f8d962_v4.mpk │       588 │
│ 1/67/_ss/d8055967298f478d97cddaa66cf67e11_v4.mpk │       563 │
│ 1/67/_ss/00c4288dac014760808006f821f1ecbe_v4.mpk │       609 │
└──────────────────────────────────────────────────────────────┘
// highlight-next-line
VACUUM TABLE c DRY RUN SUMMARY;

┌──────────────────────────┐
│ total_files │ total_size │
├─────────────┼────────────┤
│           6 │       3281 │
└──────────────────────────┘
```

### Adjusting Data Retention Time

The VACUUM TABLE command removes data files older than the `data_retention_time_in_days` setting. This retention period can be adjusted as needed, for example, to 2 days:

```sql
SET GLOBAL data_retention_time_in_days = 2;
```

`data_retention_time_in_days` defaults to 1 day (24 hours), and the maximum value varies across Databend editions:

| Edition                                  | Default Retention | Max. Retention   |
| ---------------------------------------- | ----------------- | ---------------- |
| Databend Community & Enterprise Editions | 1 day (24 hours)  | 90 days          |
| Databend Cloud (Personal)                | 1 day (24 hours)  | 1 day (24 hours) |
| Databend Cloud (Business)                | 1 day (24 hours)  | 90 days          |

To check the current value of `data_retention_time_in_days`:

```sql
SHOW SETTINGS LIKE 'data_retention_time_in_days';
```

### VACUUM TABLE vs. OPTIMIZE TABLE

Databend provides two commands for removing historical data files from a table: VACUUM TABLE and [OPTIMIZE TABLE](60-optimize-table.md) (with the PURGE option). Although both commands are capable of permanently deleting data files, they differ in how they handle orphan files: OPTIMIZE TABLE is able to remove orphan snapshots, as well as the corresponding segments and blocks. However, there is a possibility of orphan segments and blocks existing without any associated snapshots. In such a scenario, only VACUUM TABLE can help clean them up.

Both VACUUM TABLE and OPTIMIZE TABLE allow you to specify a period to determine which historical data files to remove. However, OPTIMIZE TABLE requires you to obtain the snapshot ID or timestamp from a query beforehand, whereas VACUUM TABLE allows you to specify the number of hours to retain the data files directly. VACUUM TABLE provides enhanced control over your historical data files both before their removal with the DRY RUN option, which allows you to preview the data files to be removed before applying the command. This provides a safe removal experience and helps you avoid unintended data loss.

|                                                  | VACUUM TABLE | OPTIMIZE TABLE |
| ------------------------------------------------ | ------------ | -------------- |
| Associated snapshots (incl. segments and blocks) | Yes          | Yes            |
| Orphan snapshots (incl. segments and blocks)     | Yes          | Yes            |
| Orphan segments and blocks only                  | Yes          | No             |
| DRY RUN                                          | Yes          | No             |
