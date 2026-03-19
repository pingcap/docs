---
title: ST_STARTPOINT
summary: Returns the first Point in a LineString.
---

# ST_STARTPOINT

> **Note:**
>
> Introduced or updated in v1.2.458.

Returns the first Point in a LineString.

## Syntax

```sql
ST_STARTPOINT(<geometry_or_geography>)
```

## Arguments

| Arguments    | Description                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY that represents a LineString. |

## Return Type

Geometry.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_STARTPOINT(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_endpoint;

┌───────────────────┐
│ pipeline_endpoint │
├───────────────────┤
│ POINT(1 1)        │
└───────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_STARTPOINT(
    ST_GEOGFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_startpoint;

┌─────────────────────┐
│ pipeline_startpoint │
├─────────────────────┤
│ POINT(1 1)          │
└─────────────────────┘
```
