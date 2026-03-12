---
title: ST_YMIN
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.512"/>

Returns the minimum latitude (Y coordinate) of all points contained in the specified GEOMETRY or GEOGRAPHY object.

## Syntax

```sql
ST_YMIN(<geometry_or_geography>)
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
  ST_YMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(-180 -10),LINESTRING(-179 0, 179 30),POINT EMPTY)'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│           -10 │
└───────────────┘

SELECT
  ST_YMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(180 0),LINESTRING(-60 -30, 60 30),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│           -30 │
└───────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_YMIN(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 10, 179 22)'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│            10 │
└───────────────┘
```
