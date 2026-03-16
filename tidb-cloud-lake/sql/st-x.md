---
title: ST_X
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.458"/>

Returns the longitude (X coordinate) of a Point represented by a GEOMETRY or GEOGRAPHY object.

## Syntax

```sql
ST_X(<geometry_or_geography>)
```

## Arguments

| Arguments    | Description                                                                   |
|--------------|-------------------------------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY and must contain a Point. |

## Return Type

Double.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_X(
    ST_MAKEGEOMPOINT(
      37.5, 45.5
    )
  ) AS pipeline_x;

┌────────────┐
│ pipeline_x │
├────────────┤
│       37.5 │
└────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_X(
    ST_GEOGFROMWKT(
      'POINT(37.5 45.5)'
    )
  ) AS pipeline_x;

┌────────────┐
│ pipeline_x │
├────────────┤
│       37.5 │
└────────────┘
```
