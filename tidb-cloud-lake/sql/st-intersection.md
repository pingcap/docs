---
title: ST_INTERSECTION
summary: Returns the shared part of two GEOMETRY objects.
---

# ST_INTERSECTION

> **Note:**
>
> Introduced or updated in v1.2.895.

Returns the shared part of two GEOMETRY objects.

This function only supports GEOMETRY values.

## Syntax

```sql
ST_INTERSECTION(<geometry1>, <geometry2>)
```

## Arguments

| Arguments     | Description                                            |
|---------------|--------------------------------------------------------|
| `<geometry1>` | The argument must be an expression of type GEOMETRY. |
| `<geometry2>` | The argument must be an expression of type GEOMETRY. |

> **Note:**
>
> The function reports an error if the two input GEOMETRY objects have different SRIDs.

## Return Type

GEOMETRY.

## Examples

```sql
SELECT ST_ASWKT(ST_INTERSECTION(TO_GEOMETRY('LINESTRING(0 0, 1 1)'), TO_GEOMETRY('LINESTRING(0 0, 1 1)')));

╭─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_intersection(to_geometry('LINESTRING(0 0, 1 1)'), to_geometry('LINESTRING(0 0, 1 1)'))) │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LINESTRING(0 0,1 1)                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
