---
title: ST_ASWKB
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.436"/>

Converts a GEOMETRY or GEOGRAPHY object into a [WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) format representation.

## Syntax

```sql
ST_ASWKB(<geometry_or_geography>)
```

## Aliases

- [ST_ASBINARY](st-asbinary.md)

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

Binary.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_ASWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_wkb;

┌────────────────────────────────────────────────────────────────────────────────────┐
│                                    pipeline_wkb                                    │
├────────────────────────────────────────────────────────────────────────────────────┤
│ 01020000000200000000000000006A18410000000060E3564100000000A07918410000000024ED5641 │
└────────────────────────────────────────────────────────────────────────────────────┘

SELECT
  ST_ASBINARY(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkb;

┌────────────────────────────────────────────┐
│                pipeline_wkb                │
├────────────────────────────────────────────┤
│ 01010000006666666666965EC06666666666C64240 │
└────────────────────────────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_ASWKB(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkb;

╭────────────────────────────────────────────╮
│                pipeline_wkb                │
├────────────────────────────────────────────┤
│ 01010000006666666666965EC06666666666C64240 │
╰────────────────────────────────────────────╯
```
