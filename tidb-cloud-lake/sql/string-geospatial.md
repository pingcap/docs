---
title: TO_STRING
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.330"/>

Converts a GEOMETRY object into a String representation. The display format of the output data is controlled by the `geometry_output_format` setting, which contains the following types:

| Parameter         | Description                                                         |
|-------------------|---------------------------------------------------------------------|
| GeoJSON (default) | The GEOMETRY result is rendered as a JSON object in GeoJSON format. |
| WKT               | The GEOMETRY result is rendered as a String in WKT format.          |
| WKB               | The GEOMETRY result is rendered as a Binary in WKB format.          |
| EWKT              | The GEOMETRY result is rendered as a String in EWKT format.         |
| EWKB              | The GEOMETRY result is rendered as a Binary in EWKB format.         |

## Syntax

```sql
TO_STRING(<geometry>)
```

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry>` | The argument must be an expression of type GEOMETRY. |

## Return Type

String.

## Examples

```sql
SET geometry_output_format='GeoJSON';

SELECT
  TO_GEOMETRY(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_geometry;

┌────────────────────────────────────────────────────────────────────────────┐
│                              pipeline_geometry                             │
├────────────────────────────────────────────────────────────────────────────┤
│ {"type": "LineString", "coordinates": [[400000,6000000],[401000,6010000]]} │
└────────────────────────────────────────────────────────────────────────────┘

SET geometry_output_format='WKT';

SELECT
  TO_GEOMETRY(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_geometry;

┌───────────────────────────────────────────┐
│             pipeline_geometry             │
├───────────────────────────────────────────┤
│ LINESTRING(400000 6000000,401000 6010000) │
└───────────────────────────────────────────┘

SET geometry_output_format='EWKT';

SELECT
  TO_GEOMETRY(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_geometry;

┌─────────────────────────────────────────────────────┐
│                  pipeline_geometry                  │
├─────────────────────────────────────────────────────┤
│ SRID=4326;LINESTRING(400000 6000000,401000 6010000) │
└─────────────────────────────────────────────────────┘

SET geometry_output_format='WKB';

SELECT
  TO_GEOMETRY(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_geometry;

┌────────────────────────────────────────────────────────────────────────────────────┐
│                                  pipeline_geometry                                 │
├────────────────────────────────────────────────────────────────────────────────────┤
│ 01020000000200000000000000006A18410000000060E3564100000000A07918410000000024ED5641 │
└────────────────────────────────────────────────────────────────────────────────────┘

SET geometry_output_format='EWKB';

SELECT
  TO_GEOMETRY(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_geometry;

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      pipeline_geometry                                     │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ 0102000020E61000000200000000000000006A18410000000060E3564100000000A07918410000000024ED5641 │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```
