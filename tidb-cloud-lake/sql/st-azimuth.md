---
title: ST_AZIMUTH
summary: Returns the azimuth in radians of the line segment from one Point to another, measured clockwise from the positive Y-axis (north). Returns NULL if the two points are identical.
---

# ST_AZIMUTH

Returns the azimuth in radians of the line segment from one Point to another, measured clockwise from the positive Y-axis (north). Returns NULL if the two points are identical.

## Syntax

```sql
ST_AZIMUTH(<point1>, <point2>)
```

## Arguments

| Arguments  | Description                                          |
|------------|------------------------------------------------------|
| `<point1>` | A GEOMETRY expression of type Point (origin).        |
| `<point2>` | A GEOMETRY expression of type Point (target).        |

> **Note:**
>
> Both arguments must be Point geometries. Other types produce an error.

## Return Type

Double (nullable).

## Examples

```sql
-- Due north (along positive Y-axis): 0 radians
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(0 1)'));

┌────────┐
│ result │
├────────┤
│ 0.0    │
└────────┘

-- Due east: π/2 radians
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 0)'));

┌─────────────┐
│    result   │
├─────────────┤
│ 1.570796327 │
└─────────────┘

-- Due south: π radians
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 1)'), TO_GEOMETRY('POINT(0 0)'));

┌─────────────┐
│    result   │
├─────────────┤
│ 3.141592654 │
└─────────────┘

-- Identical points: NULL
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(0 0)'));

┌────────┐
│ result │
├────────┤
│ NULL   │
└────────┘
```
