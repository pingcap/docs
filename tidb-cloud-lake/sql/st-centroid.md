---
title: ST_CENTROID
summary: Returns the centroid of a GEOMETRY object.
---

# ST_CENTROID

> **Note:**
>
> Introduced or updated in v1.2.895.

Returns the centroid of a GEOMETRY object.

This function only supports GEOMETRY values.

## Syntax

```sql
ST_CENTROID(<geometry>)
```

## Arguments

| Arguments    | Description                                            |
|--------------|--------------------------------------------------------|
| `<geometry>` | The argument must be an expression of type GEOMETRY. |

## Return Type

GEOMETRY.

## Examples

```sql
SELECT ST_ASWKT(ST_CENTROID(TO_GEOMETRY('POINT(1 2)')));

╭──────────────────────────────────────────────────╮
│ st_aswkt(st_centroid(to_geometry('POINT(1 2)'))) │
├──────────────────────────────────────────────────┤
│ POINT(1 2)                                       │
╰──────────────────────────────────────────────────╯
```

```sql
SELECT ST_ASWKT(ST_CENTROID(TO_GEOMETRY('LINESTRING(0 0, 2 0)')));

╭────────────────────────────────────────────────────────────╮
│ st_aswkt(st_centroid(to_geometry('LINESTRING(0 0, 2 0)'))) │
├────────────────────────────────────────────────────────────┤
│ POINT(1 0)                                                 │
╰────────────────────────────────────────────────────────────╯
```
