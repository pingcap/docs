---
title: ST_ENDPOINT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.458"/>

Returns the last Point in a LineString.

## Syntax

```sql
ST_ENDPOINT(<geometry_or_geography>)
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
  ST_ENDPOINT(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_endpoint;

┌───────────────────┐
│ pipeline_endpoint │
├───────────────────┤
│ POINT(4 4)        │
└───────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_ENDPOINT(
    ST_GEOGFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_endpoint;

┌───────────────────┐
│ pipeline_endpoint │
├───────────────────┤
│ POINT(4 4)        │
└───────────────────┘
```
