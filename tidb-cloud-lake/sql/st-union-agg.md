---
title: ST_UNION_AGG
summary: Aggregates multiple GEOMETRY values by repeatedly applying ST_UNION and returns the merged GEOMETRY result.
---

# ST_UNION_AGG

Aggregates multiple GEOMETRY values by repeatedly applying `ST_UNION` and returns the merged GEOMETRY result.

This function supports GEOMETRY only.

## Syntax

```sql
ST_UNION_AGG(<geometry>)
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
    SELECT TO_GEOMETRY('POINT(0 0)') AS g
    UNION ALL
    SELECT TO_GEOMETRY('POINT(1 1)')
)
SELECT ST_ASWKT(ST_UNION_AGG(g)) FROM data;

╭───────────────────────────╮
│ st_aswkt(st_union_agg(g)) │
├───────────────────────────┤
│ MULTIPOINT(0 0,1 1)       │
╰───────────────────────────╯
```
