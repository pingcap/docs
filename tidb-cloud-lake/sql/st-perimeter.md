---
title: ST_PERIMETER
summary: Returns the perimeter of polygon(s) in a GEOMETRY object, measured in the units of the coordinate system.
---

# ST_PERIMETER

Returns the perimeter of polygon(s) in a GEOMETRY object, measured in the units of the coordinate system.

## Syntax

```sql
ST_PERIMETER(<geometry>)
```

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry>` | A GEOMETRY expression.                               |

> **Note:**
>
> Returns 0 if the input is not a Polygon or MultiPolygon.

## Return Type

Double.

## Examples

```sql
SELECT ST_PERIMETER(TO_GEOMETRY('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'));

┌─────────────────────────────────────────────────────────────────┐
│ st_perimeter(to_geometry('polygon((0 0, 0 1, 1 1, 1 0, 0 0))')) │
├─────────────────────────────────────────────────────────────────┤
│ 4.0                                                              │
└─────────────────────────────────────────────────────────────────┘

SELECT ST_PERIMETER(TO_GEOMETRY('POLYGON((0 0, 0 3, 4 3, 4 0, 0 0))'));

┌─────────────────────────────────────────────────────────────────┐
│ st_perimeter(to_geometry('polygon((0 0, 0 3, 4 3, 4 0, 0 0))')) │
├─────────────────────────────────────────────────────────────────┤
│ 14.0                                                             │
└─────────────────────────────────────────────────────────────────┘

-- Non-polygon types return 0
SELECT ST_PERIMETER(TO_GEOMETRY('POINT(1 1)'));

┌──────────────────────────────────────┐
│ st_perimeter(to_geometry('point(1 1)')) │
├──────────────────────────────────────┤
│ 0.0                                     │
└──────────────────────────────────────┘
```
