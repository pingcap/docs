---
title: ST_XMAX
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.458"/>

Returns the maximum longitude (X coordinate) of all points contained in the specified GEOMETRY or GEOGRAPHY object.

## Syntax

```sql
ST_XMAX(<geometry_or_geography>)
```

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

Double.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_XMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(40 10),LINESTRING(10 10,20 20,10 40),POINT EMPTY)'
    )
  ) AS pipeline_xmax;

┌───────────────┐
│ pipeline_xmax │
├───────────────┤
│            40 │
└───────────────┘

SELECT
  ST_XMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(40 10),LINESTRING(10 10,20 20,10 40),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_xmax;

┌───────────────┐
│ pipeline_xmax │
├───────────────┤
│            45 │
└───────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_XMAX(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 0, 179 0)'
    )
  ) AS pipeline_xmax;

┌───────────────┐
│ pipeline_xmax │
├───────────────┤
│           179 │
└───────────────┘
```
