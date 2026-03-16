---
title: CREATE WAREHOUSE
sidebar_position: 1
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.687"/>

Creates a new warehouse for compute resources.

## Syntax

```sql
CREATE WAREHOUSE [ IF NOT EXISTS ] <warehouse_name>
    [ WITH ] warehouse_size = <size>
    [ WITH ] auto_suspend = <nullable_unsigned_number>
    [ WITH ] initially_suspended = <bool>
    [ WITH ] auto_resume = <bool>
    [ WITH ] max_cluster_count = <nullable_unsigned_number>
    [ WITH ] min_cluster_count = <nullable_unsigned_number>
    [ WITH ] comment = '<string_literal>'
    [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] )
```

| Parameter       | Description                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------- |
| `IF NOT EXISTS` | Optional. If specified, the command succeeds without changes if the warehouse already exists. |
| warehouse_name  | 3–63 characters, containing only `A-Z`, `a-z`, `0-9`, and `-`.                                |

## Options

| Option                | Type / Values                                                                          | Default       | Description                                                                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `WAREHOUSE_SIZE`      | `XSmall`, `Small`, `Medium`, `Large`, `XLarge`, `2XLarge`–`6XLarge` (case-insensitive) | `Small`       | Controls compute size.                                                                                                                            |
| `AUTO_SUSPEND`        | `NULL`, `0`, or ≥300 seconds                                                           | `600` seconds | Idle timeout before automatic suspend. `0`/`NULL` means never suspend; values below 300 are rejected.                                             |
| `INITIALLY_SUSPENDED` | Boolean                                                                                | `FALSE`       | If `TRUE`, the warehouse remains suspended after creation until explicitly resumed.                                                               |
| `AUTO_RESUME`         | Boolean                                                                                | `TRUE`        | Controls whether incoming queries wake the warehouse automatically.                                                                               |
| `MAX_CLUSTER_COUNT`   | `NULL` or non-negative integer                                                         | `0`           | Upper bound for auto-scaling clusters. `0` disables auto-scale.                                                                                   |
| `MIN_CLUSTER_COUNT`   | `NULL` or non-negative integer                                                         | `0`           | Lower bound for auto-scaling clusters; should be ≤ `MAX_CLUSTER_COUNT`.                                                                           |
| `COMMENT`             | String                                                                                 | Empty         | Free-form text surfaced by `SHOW WAREHOUSES`.                                                                                                     |
| `TAG`                 | Key-value pairs: `TAG ( key1 = 'value1', key2 = 'value2' )`                            | None          | Resource tags for categorization and organization (similar to AWS tags). Used for cost allocation, environment identification, or team ownership. |

- Options may appear in any order and may repeat (the later value wins).
- `AUTO_SUSPEND`, `MAX_CLUSTER_COUNT`, and `MIN_CLUSTER_COUNT` accept `= NULL` to reset to `0`.

## Examples

This example creates an XLarge warehouse with auto-scaling and custom settings:

```sql
CREATE WAREHOUSE IF NOT EXISTS etl_wh
    WITH warehouse_size = XLarge
    auto_suspend = 600
    initially_suspended = TRUE
    auto_resume = FALSE
    max_cluster_count = 4
    min_cluster_count = 2
    comment = 'Nightly ETL warehouse'
    TAG (environment = 'production', team = 'data-engineering', cost_center = 'analytics');
```

This example creates a basic Small warehouse:

```sql
CREATE WAREHOUSE my_warehouse
    WITH warehouse_size = Small;
```
