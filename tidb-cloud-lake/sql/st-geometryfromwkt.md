---
title: ST_GEOMETRYFROMWKT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.347"/>

Parses a [WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) or [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) input and returns a value of type GEOMETRY.

## Syntax

```sql
ST_GEOMETRYFROMWKT(<string>, [<srid>])
```

## Aliases

- [ST_GEOMFROMWKT](st-geomfromwkt.md)
- [ST_GEOMETRYFROMEWKT](st-geometryfromewkt.md)
- [ST_GEOMFROMEWKT](st-geomfromewkt.md)
- [ST_GEOMFROMTEXT](st-geomfromtext.md)
- [ST_GEOMETRYFROMTEXT](st-geometryfromtext.md)

## Arguments

| Arguments   | Description                                                     |
|-------------|-----------------------------------------------------------------|
| `<string>`  | The argument must be a string expression in WKT or EWKT format. |
| `<srid>`    | The integer value of the SRID to use.                           |

## Return Type

Geometry.

## Examples

```sql
SELECT
  ST_GEOMETRYFROMWKT(
    'POINT(1820.12 890.56)'
  ) AS pipeline_geometry;

┌───────────────────────┐
│   pipeline_geometry   │
├───────────────────────┤
│ POINT(1820.12 890.56) │
└───────────────────────┘

SELECT
  ST_GEOMETRYFROMWKT(
    'POINT(1820.12 890.56)', 4326
  ) AS pipeline_geometry;

┌─────────────────────────────────┐
│        pipeline_geometry        │
│             Geometry            │
├─────────────────────────────────┤
│ SRID=4326;POINT(1820.12 890.56) │
└─────────────────────────────────┘
```
