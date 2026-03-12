---
title: ST_MAKEPOLYGON
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.413"/>

Constructs a GEOMETRY or GEOGRAPHY object that represents a Polygon without holes. The function uses the specified LineString as the outer loop.

## Syntax

```sql
ST_MAKEPOLYGON(<geometry_or_geography>)
```

## Aliases

- [ST_POLYGON](st-polygon.md)

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

Geometry.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_MAKEPOLYGON(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)'
    )
  ) AS pipeline_polygon;

┌────────────────────────────────┐
│        pipeline_polygon        │
├────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0)) │
└────────────────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_MAKEPOLYGON(
    ST_GEOGFROMWKT(
      'LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)'
    )
  ) AS pipeline_polygon;

╭────────────────────────────────╮
│        pipeline_polygon        │
├────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0)) │
╰────────────────────────────────╯
```
