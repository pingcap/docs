---
title: ST_ASEWKB
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.436"/>

Converts a GEOMETRY or GEOGRAPHY object into a [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) format representation.

## Syntax

```sql
ST_ASEWKB(<geometry_or_geography>)
```

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
  ST_ASEWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_ewkb;

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        pipeline_ewkb                                       │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ 0102000020E61000000200000000000000006A18410000000060E3564100000000A07918410000000024ED5641 │
└────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT
  ST_ASEWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkb;

┌────────────────────────────────────────────────────┐
│                    pipeline_ewkb                   │
├────────────────────────────────────────────────────┤
│ 0101000020E61000006666666666965EC06666666666C64240 │
└────────────────────────────────────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_ASEWKB(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkb;

╭────────────────────────────────────────────────────╮
│                    pipeline_ewkb                   │
├────────────────────────────────────────────────────┤
│ 0101000020E61000006666666666965EC06666666666C64240 │
╰────────────────────────────────────────────────────╯
```
