---
title: ST_GEOMETRYFROMWKB
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.395"/>

Parses a [WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) or [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) input and returns a value of type GEOMETRY.

## Syntax

```sql
ST_GEOMETRYFROMWKB(<string>, [<srid>])
ST_GEOMETRYFROMWKB(<binary>, [<srid>])
```

## Aliases

- [ST_GEOMFROMWKB](st-geomfromwkb.md)
- [ST_GEOMETRYFROMEWKB](st-geometryfromewkb.md)
- [ST_GEOMFROMEWKB](st-geomfromewkb.md)

## Arguments

| Arguments   | Description                                                                    |
|-------------|--------------------------------------------------------------------------------|
| `<string>`  | The argument must be a string expression in WKB or EWKB in hexadecimal format. |
| `<binary>`  | The argument must be a binary expression in WKB or EWKB format.                |
| `<srid>`    | The integer value of the SRID to use.                                          |

## Return Type

Geometry.

## Examples

```sql
SELECT
  ST_GEOMETRYFROMWKB(
    '0101000020797f000066666666a9cb17411f85ebc19e325641'
  ) AS pipeline_geometry;

┌────────────────────────────────────────┐
│            pipeline_geometry           │
├────────────────────────────────────────┤
│ SRID=32633;POINT(389866.35 5819003.03) │
└────────────────────────────────────────┘

SELECT
  ST_GEOMETRYFROMWKB(
    FROM_HEX('0101000020797f000066666666a9cb17411f85ebc19e325641'), 4326
  ) AS pipeline_geometry;

┌───────────────────────────────────────┐
│           pipeline_geometry           │
├───────────────────────────────────────┤
│ SRID=4326;POINT(389866.35 5819003.03) │
└───────────────────────────────────────┘
```
