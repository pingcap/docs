---
title: ST_TRANSFORM
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.606"/>

Converts a GEOMETRY object from one [spatial reference system (SRS)](https://en.wikipedia.org/wiki/Spatial_reference_system) to another. If you just need to change the SRID without changing the coordinates (e.g. if the SRID was incorrect), use [ST_SETSRID](st-setsrid.md) instead.

## Syntax

```sql
ST_TRANSFORM(<geometry> [, <from_srid>], <to_srid>)
```

## Arguments

| Arguments     | Description                                                                                                                                               |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<geometry>`  | The argument must be an expression of type GEOMETRY object.                                                                                               |
| `<from_srid>` | Optional SRID identifying the current SRS of the input GEOMETRY object, if this argument is omitted, use the SRID specified in the input GEOMETRY object. |
| `<to_srid>`   | The SRID that identifies the SRS to use, transforms the input GEOMETRY object to a new object that uses this SRS.                                         |

## Return Type

Geometry.

## Examples

```sql
SET GEOMETRY_OUTPUT_FORMAT = 'EWKT'

SELECT ST_TRANSFORM(ST_GEOMFROMWKT('POINT(389866.35 5819003.03)', 32633), 3857) AS transformed_geom

┌───────────────────────────────────────────────┐
│                transformed_geom               │
├───────────────────────────────────────────────┤
│ SRID=3857;POINT(1489140.093766 6892872.19868) │
└───────────────────────────────────────────────┘

SELECT ST_TRANSFORM(ST_GEOMFROMWKT('POINT(4.500212 52.161170)'), 4326, 28992) AS transformed_geom

┌──────────────────────────────────────────────┐
│               transformed_geom               │
├──────────────────────────────────────────────┤
│ SRID=28992;POINT(94308.670475 464038.168827) │
└──────────────────────────────────────────────┘

```
