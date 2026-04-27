---
title: ST_INTERSECTION_AGG
summary: Aggregates multiple GEOMETRY values by repeatedly applying ST_INTERSECTION and returns the common overlapping part.
---

# ST_INTERSECTION_AGG

Aggregates multiple GEOMETRY values by repeatedly applying `ST_INTERSECTION` and returns the common overlapping part.

This function supports GEOMETRY only.

## Syntax

```sql
ST_INTERSECTION_AGG(<geometry>)
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `<geometry>` | An expression of type GEOMETRY. |

## Return Type

GEOMETRY.

> **Note:**
>
> - NULL input rows are ignored.
> - If all input rows are NULL, the result is NULL.
> - If the input GEOMETRY values use different SRIDs, the function returns an error.

## Example

```sql
WITH data AS (
    SELECT TO_GEOMETRY('POLYGON((0 0,4 0,4 4,0 4,0 0))') AS g
    UNION ALL
    SELECT TO_GEOMETRY('POLYGON((1 1,3 1,3 3,1 3,1 1))')
)
SELECT ST_ASWKT(ST_INTERSECTION_AGG(g)) FROM data;

╭──────────────────────────────────╮
│ st_aswkt(st_intersection_agg(g)) │
├──────────────────────────────────┤
│ POLYGON((1 3,1 1,3 1,3 3,1 3))   │
╰──────────────────────────────────╯
```
