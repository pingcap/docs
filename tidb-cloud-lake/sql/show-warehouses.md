---
title: SHOW WAREHOUSES
sidebar_position: 3
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.687"/>

Lists all warehouses visible to the current tenant.

## Syntax

```sql
SHOW WAREHOUSES [ LIKE '<pattern>' ] [ <pattern_without_like> ]
```

| Parameter                | Description                                                                                                                |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `LIKE '<pattern>'`       | Optional. Filters warehouse names using SQL `LIKE` semantics (`%` matches any sequence, `_` matches any single character). |
| `<pattern_without_like>` | Optional. When `LIKE` is omitted but a literal follows, it is treated as `LIKE '<literal>'`.                               |

## Output Columns

| Column              | Description                               |
| ------------------- | ----------------------------------------- |
| `name`              | Warehouse name                            |
| `state`             | Current state (e.g., Running, Suspended)  |
| `size`              | Warehouse size                            |
| `auto_suspend`      | Auto-suspend timeout in seconds           |
| `auto_resume`       | Whether auto-resume is enabled            |
| `min_cluster_count` | Minimum cluster count for auto-scaling    |
| `max_cluster_count` | Maximum cluster count for auto-scaling    |
| `role`              | Warehouse role                            |
| `comment`           | User-defined comment                      |
| `tags`              | Warehouse tags as a JSON-formatted string |
| `created_by`        | Creator                                   |
| `created_on`        | Creation timestamp                        |

## Examples

List all warehouses:

```sql
SHOW WAREHOUSES;
```

List warehouses matching a pattern:

```sql
SHOW WAREHOUSES LIKE '%prod%';
```

Use a literal without `LIKE`:

```sql
SHOW WAREHOUSES nightly_etl;
```
