---
title: ST_GEOHASH
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.436"/>

Return the [geohash](https://en.wikipedia.org/wiki/Geohash) for a GEOMETRY or GEOGRAPHY object. A geohash is a short base32 string that identifies a geodesic rectangle containing a location in the world. The optional precision argument specifies the `precision` of the returned geohash. For example, passing 5 for `precision returns a shorter geohash (5 characters long) that is less precise.

## Syntax

```sql
ST_GEOHASH(<geometry_or_geography> [, <precision>])
```

## Arguments

| Arguments       | Description                                                               |
|-----------------|---------------------------------------------------------------------------|
| `<geometry_or_geography>`    | The argument must be an expression of type GEOMETRY or GEOGRAPHY.                      |
| `[precision]` | Optional. specifies the precision of the returned geohash, default is 12. |

## Return Type

String.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_GEOHASH(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    )
  ) AS pipeline_geohash;

┌──────────────────┐
│ pipeline_geohash │
├──────────────────┤
│ 9q9j8ue2v71y     │
└──────────────────┘

SELECT
  ST_GEOHASH(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    ),
    5
  ) AS pipeline_geohash;

┌──────────────────┐
│ pipeline_geohash │
├──────────────────┤
│ 9q8vx            │
└──────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_GEOHASH(
    ST_GEOGFROMWKT(
      'POINT(-122.306100 37.554162)'
    )
  ) AS pipeline_geohash;

┌──────────────────┐
│ pipeline_geohash │
├──────────────────┤
│ 9q9j8ue2v71y     │
└──────────────────┘
```
