---
title: ST_ASWKT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.436"/>

Converts a GEOMETRY or GEOGRAPHY object into a [WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format representation.

## Syntax

```sql
ST_ASWKT(<geometry_or_geography>)
```

## Aliases

- [ST_ASTEXT](st-astext.md)

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

String.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_ASWKT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_wkt;

┌───────────────────────────────────────────┐
│                pipeline_wkt               │
├───────────────────────────────────────────┤
│ LINESTRING(400000 6000000,401000 6010000) │
└───────────────────────────────────────────┘

SELECT
  ST_ASTEXT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkt;

┌──────────────────────┐
│     pipeline_wkt     │
├──────────────────────┤
│ POINT(-122.35 37.55) │
└──────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_ASWKT(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkt;

╭──────────────────────╮
│     pipeline_wkt     │
├──────────────────────┤
│ POINT(-122.35 37.55) │
╰──────────────────────╯
```
