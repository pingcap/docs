---
title: Geospatial
sidebar_position: 14
---

Databend stores spatial data through two data types:

- `GEOMETRY` is planar (default SRID 0, or any SRID you assign) and suits local/projected workloads.
- `GEOGRAPHY` is spherical (WGS 84, SRID 4326) with latitude/longitude validation for global workloads.

Both types persist coordinates as IEEE 754 `Float64` values in EWKB, cover every common geometry (Point through GeometryCollection), emit WKT/WKB/GeoJSON, and can be reprojected with functions such as `ST_TRANSFORM`.

## Data Types

### GEOMETRY

- Uses Cartesian coordinates and is ideal for campus-, city-, or province-scale data where planar math is sufficient.
- Default SRID is 0; you can set another SRID when creating the column or writing data.
- Works with most spatial operators and can be reprojected with `ST_TRANSFORM` for downstream consumers.

### GEOGRAPHY

- Stores longitude/latitude pairs on WGS 84 (SRID 4326); values outside [-180°, 180°] / [-90°, 90°] are rejected.
- Recommended for continental or global distance/area calculations that need ellipsoidal formulas.
- Can be converted to GEOMETRY when a planar algorithm is required.

| Feature | GEOMETRY | GEOGRAPHY |
| :--- | :--- | :--- |
| **Coordinate System** | Cartesian (Planar) | Ellipsoidal (Spherical) |
| **SRID** | 0 (default) or Custom | 4326 (WGS 84) only |
| **X / Y Interpretation** | X, Y on a flat plane | Longitude, Latitude on a sphere |
| **Edge Interpretation** | Straight line on a plane | Great circle arc (shortest path on sphere) |
| **Primary Use Case** | Local / Projected data (e.g. city, building) | Global data (e.g. GPS tracks, shipping routes) |

## Precision and Coordinate Control

- **Double precision everywhere**: functions such as `ST_MAKEPOINT` and `ST_GEOMETRYFROMEWKT` ingest `Float64` values and persist them in EWKB, so coordinates keep their original digits.
- **SRID behavior**: GEOMETRY keeps whatever SRID you assign (default 0), while GEOGRAPHY is fixed at SRID 4326 and rejects other SRIDs.
- **Coordinate safety**: GEOGRAPHY inputs run through `check_point`, ensuring longitude/latitude stay within [-180°, 180°] / [-90°, 90°].
- **Projection**: `ST_TRANSFORM` swaps GEOMETRY SRIDs (for example, 4326 → 3857) or converts GEOGRAPHY data to a planar system for downstream processing.

## Supported Object Types

| Object Type | Description & Example | Precision Notes |
| --- | --- | --- |
| Point | Single coordinate, e.g. `POINT(113.98765432109876 23.456789012345678)` | Each coordinate is stored as a `Float64` and keeps ~15–16 digits of precision. |
| LineString | Connected path, e.g. `LINESTRING(10 20, 30 40, 50 60)` | Every vertex uses the same double precision, so derived lengths rely on the original values. |
| Polygon | Closed area, e.g. `POLYGON((10 20, 30 40, 50 60, 10 20))` | All rings share the `Float64` vertices, preserving polygon edges for area/containment tests. |
| MultiPoint | Multiple points, e.g. `MULTIPOINT((10 20), (30 40))` | Each member point inherits the same double-precision storage as a standalone point. |
| MultiLineString | Multiple paths, e.g. `MULTILINESTRING((10 20, 30 40), (50 60, 70 80))` | Precision is maintained per vertex, ensuring accurate length or intersection calculations. |
| MultiPolygon | Multiple areas, e.g. `MULTIPOLYGON(((10 20, 30 40, 50 60, 10 20)), ((15 25, 25 35, 35 45, 15 25)))` | Each polygon’s coordinates remain `Float64`, so combined areas/overlaps retain full precision. |
| GeometryCollection | Mixed objects, e.g. `GEOMETRYCOLLECTION(POINT(10 20), LINESTRING(10 20, 30 40))` | Members keep their native double-precision coordinates regardless of geometry type. |

## Output Formats

Databend persists spatial values as EWKB but exposes several output formats. Set the `geometry_output_format` session setting (default: `WKT`) or call explicit conversion functions:

- **WKT / EWKT** – Text representation; EWKT prefixes an SRID (for example, `SRID=4326;POINT(-44.3 60.1)`).
- **WKB / EWKB** – Compact binary, useful for interop with other GIS runtimes.
- **GeoJSON** – JSON representation for web maps and APIs.

```sql
SET geometry_output_format = 'GeoJSON';
SELECT ST_ASWKB(geo), ST_ASEWKT(geo), ST_ASGEOJSON(geo) FROM ...;
```

## Functions

Browse the catalogued list of spatial functions here:
- [Geospatial Functions](../../20-sql-functions/09-geospatial-functions/index.md)

## Examples

Each example below highlights one object type, the scenario it solves, the SQL to produce it, and a sample result table. `CAST('…' AS GEOMETRY)` parses the inline WKT literal so you can experiment without creating tables.

### Point — pinpoint a single sensor

*Scenario*: store the exact latitude/longitude produced by an IoT device and expose both GeoJSON and numeric coordinates.

```sql
SELECT
    ST_ASGEOJSON(pt) AS sensor_geojson,
    ST_X(pt) AS lon,
    ST_Y(pt) AS lat
FROM (SELECT CAST('POINT(113.98765432109876 23.456789012345678)' AS GEOMETRY) AS pt);
```

```
┌──────────────────────────────────────────────────────────────────────────────┬──────────────────────┬──────────────────────┐
│                              sensor_geojson                                  │         lon          │          lat         │
├──────────────────────────────────────────────────────────────────────────────┼──────────────────────┼──────────────────────┤
│ {"type":"Point","coordinates":[113.98765432109876,23.456789012345677]}       │ 113.98765432109876   │ 23.456789012345677   │
└──────────────────────────────────────────────────────────────────────────────┴──────────────────────┴──────────────────────┘
```

### LineString — describe a route

*Scenario*: record a simple driving route and measure its length in coordinate units.

```sql
SELECT
    ST_ASWKT(route) AS road_segment,
    ST_LENGTH(route) AS segment_length
FROM (SELECT CAST('LINESTRING(10 20, 30 40, 50 60)' AS GEOMETRY) AS route);
```

```
┌──────────────────────────────────────────────────────────────┬────────────────────┐
│                      road_segment                            │  segment_length   │
├──────────────────────────────────────────────────────────────┼────────────────────┤
│ LINESTRING(10 20,30 40,50 60)                                │   56.568542495    │
└──────────────────────────────────────────────────────────────┴────────────────────┘
```

### Polygon — capture an area or geofence

*Scenario*: define a rectangular geofence for a facility, read it back with SRID info, and compute its area.

```sql
SELECT
    ST_ASEWKT(area) AS ewkt_polygon,
    ST_AREA(area) AS area_units
FROM (SELECT CAST('POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))' AS GEOMETRY) AS area);
```

```
┌──────────────────────────────────────────────────────────────┬──────────────┐
│                        ewkt_polygon                          │  area_units  │
├──────────────────────────────────────────────────────────────┼──────────────┤
│ POLYGON((0 0,0 10,10 10,10 0,0 0))                           │     100      │
└──────────────────────────────────────────────────────────────┴──────────────┘
```

### MultiPoint — tag multiple sites together

*Scenario*: keep the coordinates of three kiosks together and report both the GeoJSON payload and the total count.

```sql
SELECT
    ST_ASGEOJSON(places) AS places_geojson,
    ST_NUMPOINTS(places) AS total_sites
FROM (SELECT CAST('MULTIPOINT((10 20), (30 40), (50 60))' AS GEOMETRY) AS places);
```

```
┌──────────────────────────────────────────────────────────────┬──────────────┐
│                      places_geojson                          │ total_sites  │
├──────────────────────────────────────────────────────────────┼──────────────┤
│ {"type":"MultiPoint","coordinates":[[10,20],[30,40],[50,60]]} │      3       │
└──────────────────────────────────────────────────────────────┴──────────────┘
```

### MultiLineString — represent parallel lines

*Scenario*: group two parallel road segments, read them back as WKT, and count the total vertices with `ST_NUMPOINTS`.

```sql
SELECT
    ST_ASWKT(lines) AS multiline_wkt,
    ST_NUMPOINTS(lines) AS vertex_count
FROM (SELECT CAST('MULTILINESTRING((10 20, 30 40), (50 60, 70 80))' AS GEOMETRY) AS lines);
```

```
┌──────────────────────────────────────────────────────────────┬──────────────┐
│                       multiline_wkt                          │ vertex_count │
├──────────────────────────────────────────────────────────────┼──────────────┤
│ MULTILINESTRING((10 20,30 40),(50 60,70 80))                 │      4       │
└──────────────────────────────────────────────────────────────┴──────────────┘
```

### MultiPolygon — cover disjoint districts

*Scenario*: represent two disjoint service zones and calculate the combined area.

```sql
SELECT
    ST_ASGEOJSON(zones) AS zones_geojson,
    ST_AREA(zones) AS total_area
FROM (
    SELECT CAST('MULTIPOLYGON(((0 0, 0 10, 10 10, 10 0, 0 0)), ((20 0, 20 10, 30 10, 30 0, 20 0)))' AS GEOMETRY) AS zones
);
```

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────────┐
│                                                      zones_geojson                                                      │  total_area  │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────┤
│ {"type":"MultiPolygon","coordinates":[[[[0,0],[0,10],[10,10],[10,0],[0,0]]],[[[20,0],[20,10],[30,10],[30,0],[20,0]]]]}  │     200      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────┘
```

### GeometryCollection — mix heterogenous shapes

*Scenario*: keep a landmark marker and its connecting path together, exposing the mixed GeoJSON and the maximum dimension.

```sql
SELECT
    ST_ASGEOJSON(feature) AS feature_geojson,
    ST_DIMENSION(feature) AS max_dimension
FROM (
    SELECT CAST('GEOMETRYCOLLECTION(POINT(10 20), LINESTRING(10 20, 30 40))' AS GEOMETRY) AS feature
);
```

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬───────────────┐
│                                              feature_geojson                                                                               │ max_dimension │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
│ {"type":"GeometryCollection","geometries":[{"type":"Point","coordinates":[10,20]},{"type":"LineString","coordinates":[[10,20],[30,40]]}]}  │       1       │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴───────────────┘
```
