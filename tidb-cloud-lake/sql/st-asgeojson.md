---
title: ST_ASGEOJSON
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.427"/>

Converts a GEOMETRY or GEOGRAPHY object into a [GeoJSON](https://geojson.org/) representation.

## Syntax

```sql
ST_ASGEOJSON(<geometry_or_geography>)
```

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

Variant.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_ASGEOJSON(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_geojson;

┌─────────────────────────────────────────────────────────────────────────┐
│                             pipeline_geojson                            │
├─────────────────────────────────────────────────────────────────────────┤
│ {"coordinates":[[400000,6000000],[401000,6010000]],"type":"LineString"} │
└─────────────────────────────────────────────────────────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_ASGEOJSON(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_geojson;

╭────────────────────────────────────────────────╮
│                pipeline_geojson                │
├────────────────────────────────────────────────┤
│ {"coordinates":[-122.35,37.55],"type":"Point"} │
╰────────────────────────────────────────────────╯```
