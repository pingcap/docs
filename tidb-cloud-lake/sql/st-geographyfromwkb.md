---
title: ST_GEOGRAPHYFROMWKB
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.395"/>

Parses a [WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) or [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) input and returns a value of type GEOGRAPHY.

## Syntax

```sql
ST_GEOGRAPHYFROMWKB(<string>)
ST_GEOGRAPHYFROMWKB(<binary>)
```

## Aliases

- [ST_GEOGFROMWKB](st-geogfromwkb.md)
- [ST_GEOGETRYFROMWKB](st-geogetryfromwkb.md)
- [ST_GEOGFROMEWKB](st-geogfromewkb.md)

## Arguments

| Arguments   | Description                                                                    |
|-------------|--------------------------------------------------------------------------------|
| `<string>`  | The argument must be a string expression in WKB or EWKB in hexadecimal format. |
| `<binary>`  | The argument must be a binary expression in WKB or EWKB format.                |

:::note
Only SRID 4326 is supported for GEOGRAPHY inputs.
:::

## Return Type

Geography.

## Examples

```sql
SELECT
  ST_ASWKT(
    ST_GEOGRAPHYFROMWKB(
      '0101000020E6100000000000000000F03F0000000000000040'
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASWKT(
    ST_GEOGRAPHYFROMWKB(
      FROM_HEX('0101000000000000000000F03F0000000000000040')
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘
```
