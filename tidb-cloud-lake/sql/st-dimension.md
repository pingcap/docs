---
title: ST_DIMENSION
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.442"/>

Return the dimension for a geometry object. The dimension of a GEOMETRY or GEOGRAPHY object is:

| Geospatial Object Type       | Dimension  |
|------------------------------|------------|
| Point / MultiPoint           | 0          |
| LineString / MultiLineString | 1          |
| Polygon / MultiPolygon       | 2          |

## Syntax

```sql
ST_DIMENSION(<geometry_or_geography>)
```

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

UInt8.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  0 │
└────────────────────┘

SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(-124.20 42.00, -120.01 41.99)'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  1 │
└────────────────────┘

SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'POLYGON((-124.20 42.00, -120.01 41.99, -121.1 42.01, -124.20 42.00))'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  2 │
└────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_DIMENSION(
    ST_GEOGFROMWKT(
      'LINESTRING(-124.20 42.00, -120.01 41.99)'
    )
  ) AS pipeline_dimension;

╭────────────────────╮
│ pipeline_dimension │
├────────────────────┤
│                  1 │
╰────────────────────╯
```
