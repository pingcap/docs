---
title: ST_GEOGRAPHYFROMWKT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.347"/>

Parses a [WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) or [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) input and returns a value of type GEOGRAPHY.

## Syntax

```sql
ST_GEOGRAPHYFROMWKT(<string>)
```

## Aliases

- [ST_GEOGFROMWKT](st-geogfromwkt.md)
- [ST_GEOGRAPHYFROMEWKT](st-geographyfromewkt.md)
- [ST_GEOGRAPHYFROMTEXT](st-geographyfromtext.md)
- [ST_GEOGFROMTEXT](st-geogfromtext.md)

## Arguments

| Arguments   | Description                                                     |
|-------------|-----------------------------------------------------------------|
| `<string>`  | The argument must be a string expression in WKT or EWKT format. |

:::note
Only SRID 4326 is supported for GEOGRAPHY inputs.
:::

## Return Type

Geography.

## Examples

```sql
SELECT
  ST_ASWKT(
    ST_GEOGRAPHYFROMWKT(
      'POINT(1 2)'
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASEWKT(
    ST_GEOGRAPHYFROMWKT(
      'SRID=4326;POINT(1 2)'
    )
  ) AS pipeline_geography;

┌──────────────────────┐
│ pipeline_geography   │
├──────────────────────┤
│ SRID=4326;POINT(1 2) │
└──────────────────────┘
```
