---
title: ST_MAKEPOLYGONORIENTED
summary: Creates a Polygon from a LineString input, preserving the vertex order as given. Unlike ST_MAKEPOLYGON, this function does not reorder vertices to enforce a specific winding direction.
---

# ST_MAKEPOLYGONORIENTED

> **Note:**
>
> Introduced or updated in v1.2.911.

Creates a Polygon from a LineString input, preserving the vertex order as given. Unlike [ST_MAKEPOLYGON](/tidb-cloud-lake/sql/st-makepolygon.md), this function does not reorder vertices to enforce a specific winding direction.

## Syntax

```sql
ST_MAKEPOLYGONORIENTED(<geometry>)
```

## Arguments

| Arguments    | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry>` | A GEOMETRY expression of type LineString. Must have at least 4 points with the first and last point being identical. |

> **Note:**
>
> - Only LineString input is accepted. Other types produce an error.
> - The LineString must form a valid polygon (no self-intersections).

## Return Type

Geometry.

## Examples

```sql
SELECT ST_ASWKT(
  ST_MAKEPOLYGONORIENTED(TO_GEOMETRY('LINESTRING(0 0, 1 0, 1 2, 0 2, 0 0)'))
);

┌──────────────────────────────────┐
│             result               │
├──────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0))  │
└──────────────────────────────────┘

-- Reversed winding order is preserved
SELECT ST_ASWKT(
  ST_MAKEPOLYGONORIENTED(TO_GEOMETRY('LINESTRING(0 0, 0 2, 1 2, 1 0, 0 0)'))
);

┌──────────────────────────────────┐
│             result               │
├──────────────────────────────────┤
│ POLYGON((0 0,0 2,1 2,1 0,0 0))  │
└──────────────────────────────────┘
```
