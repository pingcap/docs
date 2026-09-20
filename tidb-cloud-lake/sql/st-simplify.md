---
title: ST_SIMPLIFY
summary: Returns a simplified version of a GEOMETRY object by removing vertices where the distance to the resulting edge is within the specified tolerance. Uses the Ramer-Douglas-Peucker algorithm.
---

# ST_SIMPLIFY

Returns a simplified version of a GEOMETRY object by removing vertices where the distance to the resulting edge is within the specified tolerance. Uses the Ramer-Douglas-Peucker algorithm.

## Syntax

```sql
ST_SIMPLIFY(<geometry>, <tolerance>)
```

## Arguments

| Arguments     | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `<geometry>`  | A GEOMETRY expression. Works on LineString, MultiLineString, Polygon, and MultiPolygon. No effect on Point or MultiPoint. |
| `<tolerance>` | The maximum distance tolerance for vertex removal.                          |

> **Note:**
>
> GeometryCollection is not supported.

## Return Type

Geometry.

## Examples

```sql
SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('LINESTRING(0 0, 1 0, 1 1, 2 1)'), 0.5
  )
) AS simplified;

┌──────────────────────┐
│      simplified      │
├──────────────────────┤
│ LINESTRING(0 0,2 1)  │
└──────────────────────┘

SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('LINESTRING(1100 1100, 2500 2100, 3100 3100, 4900 1100, 3100 1900)'), 500
  )
) AS simplified;

┌──────────────────────────────────────────────────────┐
│                      simplified                      │
├──────────────────────────────────────────────────────┤
│ LINESTRING(1100 1100,3100 3100,4900 1100,3100 1900)  │
└──────────────────────────────────────────────────────┘

SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0.5 0.5, 0 1, 0 0))'), 0.6
  )
) AS simplified;

┌──────────────────────────────────┐
│            simplified            │
├──────────────────────────────────┤
│ POLYGON((0 0,1 0,1 1,0 1,0 0))  │
└──────────────────────────────────┘
```
