---
title: ST_YMAX
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.512"/>

Returns the maximum latitude (Y coordinate) of all points contained in the specified GEOMETRY or GEOGRAPHY object.

## Syntax

```sql
ST_YMAX(<geometry_or_geography>)
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
  ST_YMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(180 50),LINESTRING(10 10,20 20,10 40),POINT EMPTY)'
    )
  ) AS pipeline_ymax;

┌───────────────┐
│ pipeline_ymax │
├───────────────┤
│            50 │
└───────────────┘

SELECT
  ST_YMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(40 10),LINESTRING(10 10,20 20,10 40),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_ymax;

┌───────────────┐
│ pipeline_ymax │
├───────────────┤
│            45 │
└───────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_YMAX(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 10, 179 22)'
    )
  ) AS pipeline_ymax;

┌───────────────┐
│ pipeline_ymax │
├───────────────┤
│            22 │
└───────────────┘
```
