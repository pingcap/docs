---
title: ST_ASEWKT
summary: Converts a GEOMETRY or GEOGRAPHY object into a EWKT(extended well-known-text) format representation.
---

> **Note:**
>
> Introduced or updated in v1.2.436.

Converts a GEOMETRY or GEOGRAPHY object into a [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) format representation.

## Syntax

```sql
ST_ASEWKT(<geometry_or_geography>)
```

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
  ST_ASEWKT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_ewkt;

┌─────────────────────────────────────────────────────┐
│                    pipeline_ewkt                    │
├─────────────────────────────────────────────────────┤
│ SRID=4326;LINESTRING(400000 6000000,401000 6010000) │
└─────────────────────────────────────────────────────┘

SELECT
  ST_ASEWKT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkt;

┌────────────────────────────────┐
│          pipeline_ewkt         │
├────────────────────────────────┤
│ SRID=4326;POINT(-122.35 37.55) │
└────────────────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_ASEWKT(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkt;

╭────────────────────────────────╮
│          pipeline_ewkt         │
├────────────────────────────────┤
│ SRID=4326;POINT(-122.35 37.55) │
╰────────────────────────────────╯
```
