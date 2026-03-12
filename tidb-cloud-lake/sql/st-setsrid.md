---
title: ST_SETSRID
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.566"/>

Returns a GEOMETRY object that has its [SRID (spatial reference system identifier)](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) set to the specified value. This Function only change the SRID without affecting the coordinates of the object. If you also need to change the coordinates to match the new SRS (spatial reference system), use [ST_TRANSFORM](st-transform.md) instead.

## Syntax

```sql
ST_SETSRID(<geometry>, <srid>)
```

## Arguments

| Arguments    | Description                                                 |
|--------------|-------------------------------------------------------------|
| `<geometry>` | The argument must be an expression of type GEOMETRY object. |
| `<srid>`     | The SRID integer to set in the returned GEOMETRY object.    |

## Return Type

Geometry.

## Examples

```sql
SET GEOMETRY_OUTPUT_FORMAT = 'EWKT'

SELECT ST_SETSRID(TO_GEOMETRY('POINT(13 51)'), 4326) AS geometry

┌────────────────────────┐
│        geometry        │
├────────────────────────┤
│ SRID=4326;POINT(13 51) │
└────────────────────────┘

```
