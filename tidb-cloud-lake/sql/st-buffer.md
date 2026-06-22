---
title: ST_BUFFER
summary: Returns a GEOMETRY representing all points whose distance from the input geometry is less than or equal to the specified distance. The result is a MultiPolygon or NULL.
---

# ST_BUFFER

Returns a GEOMETRY representing all points whose distance from the input geometry is less than or equal to the specified distance. The result is a MultiPolygon or NULL.

## Syntax

```sql
ST_BUFFER(<geometry>, <distance>)
```

## Arguments

| Arguments    | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry>` | A GEOMETRY expression. GeometryCollection is not supported.                 |
| `<distance>` | Buffer distance. Units match the coordinate system of the input geometry.   |

> **Note:**
>
> - For Point, MultiPoint, LineString, and MultiLineString: the absolute value of distance is used (negative behaves the same as positive).
> - For Polygon and MultiPolygon: positive distance inflates, negative distance deflates.
> - Returns NULL when the result is empty (e.g., zero distance on a Point, or deflating a polygon past zero area).
> - For Polygon with distance 0: returns the polygon wrapped as a MultiPolygon.
> - SRID is preserved in the output.

## Return Type

Geometry (nullable).

## Examples

```sql
-- Buffer a point (produces a polygon approximating a circle)
SELECT ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 1) IS NOT NULL;

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

-- Zero distance on a polygon returns itself as MultiPolygon
SELECT ST_ASWKT(
  ST_BUFFER(TO_GEOMETRY('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'), 0)
);

┌─────────────────────────────────────────────────┐
│                     result                      │
├─────────────────────────────────────────────────┤
│ MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0)))          │
└─────────────────────────────────────────────────┘

-- Zero distance on a point returns NULL
SELECT ST_ASWKT(ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 0));

┌────────┐
│ result │
├────────┤
│ NULL   │
└────────┘

-- SRID is preserved
SELECT ST_SRID(ST_BUFFER(ST_GEOMETRYFROMWKT('POINT(0 0)', 4326), 1));

┌────────┐
│ result │
├────────┤
│ 4326   │
└────────┘
```
