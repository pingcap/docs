---
title: SHOW SETTINGS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.314"/>

Databend provides a variety of system settings that enable you to control how Databend works. This command displays the current and default values, as well as the [Setting Levels](#setting-levels), of available system settings. To update a setting, use the [SET](02-set-global.md) or [UNSET](02-unset.md) command.

- Some Databend behaviors cannot be changed through the system settings; you must take them into consideration while working with Databend. For example,
    - Databend encodes strings to the UTF-8 charset.
    - Databend uses a 1-based numbering convention for arrays.
- Databend stores the system settings in the system table [system.settings](../../00-sql-reference/31-system-tables/system-settings.md).

## Syntax

```sql
SHOW SETTINGS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## Setting Levels

Each Databend setting comes with a level that can be Global, Default, or Session. This table illustrates the distinctions between each level:

|   Level    |   Description                                                                                                                                                                                                                                                              |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   Global   |   Settings with this level are written to the meta service and affect all clusters in the same tenant. Changes at this level have a global impact and apply to the entire database environment shared by multiple clusters.                                                |
|   Default  |   Settings with this level are configured through the `databend-query.toml` configuration file. Changes at this level only affect a single query instance and are specific to the configuration file. This level provides a default setting for individual query instances.  |
|   Session  |   Settings with this level are restricted to a single request or session. They have the narrowest scope and apply only to the specific session or request in progress, providing a way to customize settings on a per-session basis.                                       |

## Examples

:::note
As Databend updates the system settings every now and then, this example may not show the most recent results. To view the latest system settings in Databend, please execute `SHOW SETTINGS;` within your Databend instance.
:::

```sql
SHOW SETTINGS LIMIT 5;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                     name                    │  value │ default │   range  │  level  │                                                                     description                                                                    │  type  │
├─────────────────────────────────────────────┼────────┼─────────┼──────────┼─────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┤
│ acquire_lock_timeout                        │ 15     │ 15      │ None     │ DEFAULT │ Sets the maximum timeout in seconds for acquire a lock.                                                                                            │ UInt64 │
│ aggregate_spilling_bytes_threshold_per_proc │ 0      │ 0       │ None     │ DEFAULT │ Sets the maximum amount of memory in bytes that an aggregator can use before spilling data to storage during query execution.                      │ UInt64 │
│ aggregate_spilling_memory_ratio             │ 0      │ 0       │ [0, 100] │ DEFAULT │ Sets the maximum memory ratio in bytes that an aggregator can use before spilling data to storage during query execution.                          │ UInt64 │
│ auto_compaction_imperfect_blocks_threshold  │ 50     │ 50      │ None     │ DEFAULT │ Threshold for triggering auto compaction. This occurs when the number of imperfect blocks in a snapshot exceeds this value after write operations. │ UInt64 │
│ collation                                   │ utf8   │ utf8    │ ["utf8"] │ DEFAULT │ Sets the character collation. Available values include "utf8".                                                                                     │ String │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```