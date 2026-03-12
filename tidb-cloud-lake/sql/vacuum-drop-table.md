---
title: VACUUM DROP TABLE
sidebar_position: 18
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='VACUUM DROP TABLE'/>

The VACUUM DROP TABLE command helps save storage space by permanently removing data files of dropped tables, freeing up storage space, and enabling you to manage the process efficiently. It offers optional parameters to target specific databases, preview, and limit the number of data files to be vacuumed. To list the dropped tables of a database, use [SHOW DROP TABLES](show-drop-tables.md).

See also: [VACUUM TABLE](91-vacuum-table.md)

### Syntax

```sql
VACUUM DROP TABLE
    [ FROM <database_name> ]
    [ DRY RUN [SUMMARY] ]
    [ LIMIT <file_count> ]
```

- `FROM <database_name>`: This parameter restricts the search for dropped tables to a specific database. If not specified, the command will scan all databases, including those that have been dropped.

  ```sql title="Example:"
  -- Remove dropped tables from the "default" database
  // highlight-next-line
  VACUUM DROP TABLE FROM default;

  -- Remove dropped tables from all databases
  // highlight-next-line
  VACUUM DROP TABLE;
  ```

- `DRY RUN [SUMMARY]`: When this parameter is specified, data files will not be removed; instead, it returns a result showing which data files would have been removed if this parameter were not specified. See examples in the [Output](#output) section.

- `LIMIT <file_count>`: This parameter can be used with or without the DRY RUN parameter. When used with DRY RUN, it limits the number of data files to be shown in the `DRY RUN` result. When used without `DRY RUN`, it limits the number of data files to be vacuumed.

### Output

The VACUUM DROP TABLE command returns a result when the `DRY RUN` or `DRY RUN SUMMARY` parameter is specified:

- `DRY RUN`: Returns a list of up to 1,000 candidate files and their sizes in bytes for each dropped table.
- `DRY RUN SUMMARY`: Returns the total number of files to be removed and their combined size for each dropped table.

```sql title='Example:'
// highlight-next-line
VACUUM DROP TABLE DRY RUN;

┌──────────────────────────────────────────────────────────────────┐
│  table │                     file                    │ file_size │
├────────┼─────────────────────────────────────────────┼───────────┤
│ b      │ 313ebd4da5cc493f9a7d491da8253ce2_v2.parquet │       210 │
│ b      │ 737f2215b8ac4a268d5b7f2218273358_v2.parquet │       210 │
│ b      │ 737f2215b8ac4a268d5b7f2218273358_v4.parquet │       340 │
│ b      │ 313ebd4da5cc493f9a7d491da8253ce2_v4.parquet │       340 │
│ b      │ last_snapshot_location_hint                 │        72 │
│ b      │ 7e01fa5c2e0a495298942671447dc8cb_v4.mpk     │       515 │
│ b      │ 2bc90e5be55c44258a736d27e5f7ac9e_v4.mpk     │       459 │
│ b      │ 85e73803aabc4eb48774db3d932312dd_v4.mpk     │       534 │
│ b      │ f0e507d0b825428dbfe57c8d8b620a15_v4.mpk     │       533 │
│ c      │ cee790e76f6e4e92bc9dab3b9e873dcf_v2.parquet │       210 │
│ c      │ 4bcb2cef3b6344cb951908ebee5ceb36_v2.parquet │       210 │
│ c      │ cee790e76f6e4e92bc9dab3b9e873dcf_v4.parquet │       340 │
│ c      │ 4bcb2cef3b6344cb951908ebee5ceb36_v4.parquet │       340 │
│ c      │ last_snapshot_location_hint                 │        71 │
│ c      │ 414fc6a8dc6746afbc576cf8fddfcdf3_v4.mpk     │       516 │
│ c      │ 8d0d115c438244c295e3bfd50d556e39_v4.mpk     │       458 │
│ c      │ 28e4f551cc634d3d8d7e648c3baa5f5c_v4.mpk     │       534 │
│ c      │ 007b57e08eda419fbb451a3a3ed71de8_v4.mpk     │       533 │
└──────────────────────────────────────────────────────────────────┘
// highlight-next-line
VACUUM DROP TABLE DRY RUN SUMMARY;

┌───────────────────────────────────┐
│  table │ total_files │ total_size │
├────────┼─────────────┼────────────┤
│ b      │           9 │       3213 │
│ c      │           9 │       3212 │
└───────────────────────────────────┘
```

### Adjusting Data Retention Time

The VACUUM DROP TABLE command removes data files older than the `DATA_RETENTION_TIME_IN_DAYS` setting. This retention period can be adjusted as needed, for example, to 2 days:

```sql
SET GLOBAL DATA_RETENTION_TIME_IN_DAYS = 2;
```

`DATA_RETENTION_TIME_IN_DAYS` defaults to 1 day (24 hours), and the maximum value varies across Databend editions:

| Edition                                  | Default Retention | Max. Retention   |
| ---------------------------------------- | ----------------- | ---------------- |
| Databend Community & Enterprise Editions | 1 day (24 hours)  | 90 days          |
| Databend Cloud (Personal)                | 1 day (24 hours)  | 1 day (24 hours) |
| Databend Cloud (Business)                | 1 day (24 hours)  | 90 days          |

To check the current value of `DATA_RETENTION_TIME_IN_DAYS`:

```sql
SHOW SETTINGS LIKE 'DATA_RETENTION_TIME_IN_DAYS';
```
