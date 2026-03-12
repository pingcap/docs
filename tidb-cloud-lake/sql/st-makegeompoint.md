---
title: ST_MAKEGEOMPOINT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.347"/>

Constructs a GEOMETRY object that represents a Point with the specified longitude and latitude.

## Syntax

```sql
ST_MAKEGEOMPOINT(<longitude>, <latitude>)
```

## Aliases

- [ST_GEOM_POINT](st-geom-point.md)

## Arguments

| Arguments     | Description                                   |
|---------------|-----------------------------------------------|
| `<longitude>` | A Double value that represents the longitude. |
| `<latitude>`  | A Double value that represents the latitude.  |

## Return Type

Geometry.

## Examples

```sql
SELECT
  ST_MAKEGEOMPOINT(
    7.0, 8.0
  ) AS pipeline_point;

┌────────────────┐
│ pipeline_point │
├────────────────┤
│ POINT(7 8)     │
└────────────────┘

SELECT
  ST_MAKEGEOMPOINT(
    -122.3061, 37.554162
  ) AS pipeline_point;

┌────────────────────────────┐
│       pipeline_point       │
├────────────────────────────┤
│ POINT(-122.3061 37.554162) │
└────────────────────────────┘
```
