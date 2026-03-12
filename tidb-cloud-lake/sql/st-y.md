---
title: ST_Y
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.458"/>

Returns the latitude (Y coordinate) of a Point represented by a GEOMETRY or GEOGRAPHY object.

## Syntax

```sql
ST_Y(<geometry_or_geography>)
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
  ST_Y(
    ST_MAKEGEOMPOINT(
      37.5, 45.5
    )
  ) AS pipeline_y;

┌────────────┐
│ pipeline_y │
├────────────┤
│       45.5 │
└────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_Y(
    ST_GEOGFROMWKT(
      'POINT(37.5 45.5)'
    )
  ) AS pipeline_y;

┌────────────┐
│ pipeline_y │
├────────────┤
│       45.5 │
└────────────┘
```
