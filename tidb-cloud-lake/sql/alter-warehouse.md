---
title: ALTER WAREHOUSE
sidebar_position: 4
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.687"/>

Suspends, resumes, or modifies settings of an existing warehouse.

## Syntax

```sql
-- Suspend or resume a warehouse
ALTER WAREHOUSE <warehouse_name> { SUSPEND | RESUME }

-- Modify warehouse settings
ALTER WAREHOUSE <warehouse_name>
    SET [ warehouse_size = <size> ]
    [ auto_suspend = <nullable_unsigned_number> ]
    [ auto_resume = <bool> ]
    [ max_cluster_count = <nullable_unsigned_number> ]
    [ min_cluster_count = <nullable_unsigned_number> ]
    [ comment = '<string_literal>' ]

ALTER WAREHOUSE <warehouse_name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER WAREHOUSE <warehouse_name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER WAREHOUSE <warehouse_name> RENAME TO <new_name>
```

| Parameter | Description                                                                  |
| --------- | ---------------------------------------------------------------------------- |
| `SUSPEND` | Immediately suspends the warehouse.                                          |
| `RESUME`  | Immediately resumes the warehouse.                                           |
| `SET`     | Modifies one or more warehouse options. Unspecified fields remain unchanged. |

## Options

The `SET` clause accepts the same options as [CREATE WAREHOUSE](create-warehouse.md):

| Option              | Type / Values                                                       | Description                                                          |
| ------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `WAREHOUSE_SIZE`    | `XSmall`, `Small`, `Medium`, `Large`, `XLarge`, `2XLarge`–`6XLarge` | Changes compute size.                                                |
| `AUTO_SUSPEND`      | `NULL`, `0`, or ≥300 seconds                                        | Idle timeout before automatic suspend. `NULL` disables auto-suspend. |
| `AUTO_RESUME`       | Boolean                                                             | Controls whether incoming queries wake the warehouse automatically.  |
| `MAX_CLUSTER_COUNT` | `NULL` or non-negative integer                                      | Upper bound for auto-scaling clusters.                               |
| `MIN_CLUSTER_COUNT` | `NULL` or non-negative integer                                      | Lower bound for auto-scaling clusters.                               |
| `COMMENT`           | String                                                              | Free-form text description.                                          |

- `NULL` is valid for numeric options to reset them to `0`.
- Supplying `SET` with no options raises an error.
- `SET TAG` adds or updates one or more tags. Multiple tags can be set in a single statement separated by commas.
- `UNSET TAG` removes one or more tags by their keys. Non-existent tag keys are silently ignored.
- `RENAME TO` requires the warehouse to be suspended and uses the same naming rules as `CREATE`.

## Examples

Suspend a warehouse:

```sql
ALTER WAREHOUSE my_wh SUSPEND;
```

Resume a warehouse:

```sql
ALTER WAREHOUSE my_wh RESUME;
```

Modify warehouse settings:

```sql
ALTER WAREHOUSE my_wh
    SET warehouse_size = Large
    auto_resume = TRUE
    comment = 'Serving tier';
```

Disable auto-suspend:

```sql
ALTER WAREHOUSE my_wh SET auto_suspend = NULL;
```

Manage tags:

```sql
ALTER WAREHOUSE wh_hot SET TAG environment = 'production';
ALTER WAREHOUSE wh_hot SET TAG environment = 'staging', owner = 'john', cost_center = 'eng';
ALTER WAREHOUSE wh_hot UNSET TAG environment;
ALTER WAREHOUSE wh_hot UNSET TAG environment, owner, cost_center;
```
