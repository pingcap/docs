---
title: ST_ENVELOPE_AGG
summary: Aggregates multiple GEOMETRY values and returns the minimum bounding rectangle that covers all non-NULL inputs.
---

# ST_ENVELOPE_AGG

Aggregates multiple GEOMETRY values and returns the minimum bounding rectangle that covers all non-NULL inputs.

This function supports GEOMETRY only.

## Syntax

```sql
ST_ENVELOPE_AGG(<geometry>)
```

## Arguments

| Arguments | Description |
| --------- | ----------- |
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
    SELECT TO_GEOMETRY('POINT(1 1)') AS g
    UNION ALL
    SELECT TO_GEOMETRY('POINT(4 2)')
    UNION ALL
    SELECT TO_GEOMETRY('POINT(2 5)')
)
SELECT ST_ASWKT(ST_ENVELOPE_AGG(g)) FROM data;

╭────────────────────────────────╮
│  st_aswkt(st_envelope_agg(g))  │
├────────────────────────────────┤
│ POLYGON((1 1,4 1,4 5,1 5,1 1)) │
╰────────────────────────────────╯
```
