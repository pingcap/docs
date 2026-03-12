---
title: Geospatial Functions
---

Databend ships with two complementary sets of geospatial capabilities: PostGIS-style geometry functions for building and analysing shapes, and H3 utilities for global hexagonal indexing. The tables below group the functions by task so you can quickly locate the right tool, similar to the layout used in the Snowflake documentation.

## Geometry Constructors

| Function | Description | Example |
|----------|-------------|---------|
| [ST_MAKEGEOMPOINT](st-makegeompoint.md) / [ST_GEOM_POINT](st-geom-point.md) | Construct a Point geometry | `ST_MAKEGEOMPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKEPOINT](st-makepoint.md) / [ST_POINT](st-point.md) | Construct a Point geography | `ST_MAKEPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKELINE](st-makeline.md) / [ST_MAKE_LINE](st-make-line.md) | Create a LineString from points | `ST_MAKELINE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `LINESTRING(-122.35 37.55, -122.40 37.60)` |
| [ST_MAKEPOLYGON](st-makepolygon.md) | Create a Polygon from a closed LineString | `ST_MAKEPOLYGON(ST_MAKELINE(...))` → `POLYGON(...)` |
| [ST_POLYGON](st-polygon.md) | Create a Polygon from coordinate rings | `ST_POLYGON(...)` → `POLYGON(...)` |

## Geometry Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [ST_GEOMETRYFROMTEXT](st-geometryfromtext.md) / [ST_GEOMFROMTEXT](st-geomfromtext.md) | Convert WKT to geometry | `ST_GEOMETRYFROMTEXT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMWKB](st-geometryfromwkb.md) / [ST_GEOMFROMWKB](st-geomfromwkb.md) | Convert WKB to geometry | `ST_GEOMETRYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMETRYFROMEWKT](st-geometryfromewkt.md) / [ST_GEOMFROMEWKT](st-geomfromewkt.md) | Convert EWKT to geometry | `ST_GEOMETRYFROMEWKT('SRID=4326;POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMEWKB](st-geometryfromewkb.md) / [ST_GEOMFROMEWKB](st-geomfromewkb.md) | Convert EWKB to geometry | `ST_GEOMETRYFROMEWKB(...)` → `POINT(...)` |
| [ST_GEOGRAPHYFROMWKT](st-geographyfromwkt.md) / [ST_GEOGFROMWKT](st-geogfromwkt.md) | Convert WKT/EWKT to geography | `ST_GEOGRAPHYFROMWKT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOGRAPHYFROMWKB](st-geographyfromwkb.md) / [ST_GEOGFROMWKB](st-geogfromwkb.md) | Convert WKB/EWKB to geography | `ST_GEOGRAPHYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMFROMGEOHASH](st-geomfromgeohash.md) | Convert GeoHash to geometry | `ST_GEOMFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOMPOINTFROMGEOHASH](st-geompointfromgeohash.md) | Convert GeoHash to Point geometry | `ST_GEOMPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [ST_GEOGFROMGEOHASH](st-geogfromgeohash.md) | Convert GeoHash to geography polygon | `ST_GEOGFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOGPOINTFROMGEOHASH](st-geogpointfromgeohash.md) | Convert GeoHash to geography point | `ST_GEOGPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [TO_GEOMETRY](to-geometry.md) | Parse various formats into geometry | `TO_GEOMETRY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [TO_GEOGRAPHY](to-geography.md) / [TRY_TO_GEOGRAPHY](to-geography.md) | Parse various formats into geography | `TO_GEOGRAPHY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |

## Geometry Output

| Function | Description | Example |
|----------|-------------|---------|
| [ST_ASTEXT](st-astext.md) | Convert geometry to WKT | `ST_ASTEXT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASWKT](st-aswkt.md) | Convert geometry to WKT | `ST_ASWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASBINARY](st-asbinary.md) / [ST_ASWKB](st-aswkb.md) | Convert geometry to WKB | `ST_ASBINARY(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `WKB representation` |
| [ST_ASEWKT](st-asewkt.md) | Convert geometry to EWKT | `ST_ASEWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'SRID=4326;POINT(-122.35 37.55)'` |
| [ST_ASEWKB](st-asewkb.md) | Convert geometry to EWKB | `ST_ASEWKB(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `EWKB representation` |
| [ST_ASGEOJSON](st-asgeojson.md) | Convert geometry to GeoJSON | `ST_ASGEOJSON(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'{"type":"Point","coordinates":[-122.35,37.55]}'` |
| [ST_GEOHASH](st-geohash.md) | Convert geometry to GeoHash | `ST_GEOHASH(ST_MAKEGEOMPOINT(-122.35, 37.55), 7)` → `'9q8yyk8'` |
| [TO_STRING](to-string.md) | Convert geometry to string | `TO_STRING(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |

## Geometry Accessors & Properties

| Function | Description | Example |
|----------|-------------|---------|
| [ST_DIMENSION](st-dimension.md) | Return the topological dimension | `ST_DIMENSION(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `0` |
| [ST_SRID](st-srid.md) | Return the SRID of a geometry | `ST_SRID(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `4326` |
| [ST_SETSRID](st-setsrid.md) | Assign an SRID to a geometry | `ST_SETSRID(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-122.35 37.55)` |
| [ST_TRANSFORM](st-transform.md) | Transform geometry to a new SRID | `ST_TRANSFORM(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-13618288.8 4552395.0)` |
| [ST_NPOINTS](st-npoints.md) / [ST_NUMPOINTS](st-numpoints.md) | Count points in a geometry | `ST_NPOINTS(ST_MAKELINE(...))` → `2` |
| [ST_POINTN](st-pointn.md) | Return a specific point from a LineString | `ST_POINTN(ST_MAKELINE(...), 1)` → `POINT(-122.35 37.55)` |
| [ST_STARTPOINT](st-startpoint.md) | Return the first point in a LineString | `ST_STARTPOINT(ST_MAKELINE(...))` → `POINT(-122.35 37.55)` |
| [ST_ENDPOINT](st-endpoint.md) | Return the last point in a LineString | `ST_ENDPOINT(ST_MAKELINE(...))` → `POINT(-122.40 37.60)` |
| [ST_LENGTH](st-length.md) | Measure the length of a LineString | `ST_LENGTH(ST_MAKELINE(...))` → `5.57` |
| [ST_X](st-x.md) / [ST_Y](st-y.md) | Return the X or Y coordinate of a Point | `ST_X(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `-122.35` |
| [ST_XMIN](st-xmin.md) / [ST_XMAX](st-xmax.md) | Return the min/max X coordinate | `ST_XMIN(ST_MAKELINE(...))` → `-122.40` |
| [ST_YMIN](st-ymin.md) / [ST_YMAX](st-ymax.md) | Return the min/max Y coordinate | `ST_YMAX(ST_MAKELINE(...))` → `37.60` |

## Spatial Relationships

| Function | Description | Example |
|----------|-------------|---------|
| [ST_CONTAINS](st-contains.md) | Test whether one geometry contains another | `ST_CONTAINS(ST_MAKEPOLYGON(...), ST_MAKEGEOMPOINT(...))` → `TRUE` |
| [POINT_IN_POLYGON](point-in-polygon.md) | Check if a point lies inside a polygon | `POINT_IN_POLYGON([lon, lat], [[p1_lon, p1_lat], ...])` → `TRUE` |

## Distance & Measurements

| Function | Description | Example |
|----------|-------------|---------|
| [ST_DISTANCE](st-distance.md) | Measure the distance between geometries | `ST_DISTANCE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `5.57` |
| [HAVERSINE](haversine.md) | Compute great-circle distance between coordinates | `HAVERSINE(37.55, -122.35, 37.60, -122.40)` → `6.12` |

## H3 Indexing & Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [GEO_TO_H3](geo-to-h3.md) | Convert longitude/latitude to an H3 index | `GEO_TO_H3(37.7950, 55.7129, 15)` → `644325524701193974` |
| [H3_TO_GEO](h3-to-geo.md) | Convert an H3 index to longitude/latitude | `H3_TO_GEO(644325524701193974)` → `[37.7950, 55.7129]` |
| [H3_TO_STRING](h3-to-string.md) | Convert an H3 index to its string form | `H3_TO_STRING(644325524701193974)` → `'8f2830828052d25'` |
| [STRING_TO_H3](string-to-h3.md) | Convert an H3 string to an index | `STRING_TO_H3('8f2830828052d25')` → `644325524701193974` |
| [GEOHASH_ENCODE](geohash-encode.md) | Encode longitude/latitude to GeoHash | `GEOHASH_ENCODE(37.7950, 55.7129, 12)` → `'ucfv0nzpt3s7'` |
| [GEOHASH_DECODE](geohash-decode.md) | Decode a GeoHash to longitude/latitude | `GEOHASH_DECODE('ucfv0nzpt3s7')` → `[37.7950, 55.7129]` |

## H3 Cell Properties

| Function | Description | Example |
|----------|-------------|---------|
| [H3_GET_RESOLUTION](h3-get-resolution.md) | Return the resolution of an H3 index | `H3_GET_RESOLUTION(644325524701193974)` → `15` |
| [H3_GET_BASE_CELL](h3-get-base-cell.md) | Return the base cell number | `H3_GET_BASE_CELL(644325524701193974)` → `14` |
| [H3_IS_VALID](h3-is-valid.md) | Check whether an H3 index is valid | `H3_IS_VALID(644325524701193974)` → `TRUE` |
| [H3_IS_PENTAGON](h3-is-pentagon.md) | Check whether an H3 index is a pentagon | `H3_IS_PENTAGON(644325524701193974)` → `FALSE` |
| [H3_IS_RES_CLASS_III](h3-is-res-class-iii.md) | Check whether an H3 index is class III | `H3_IS_RES_CLASS_III(644325524701193974)` → `FALSE` |
| [H3_GET_FACES](h3-get-faces.md) | Return intersecting icosahedron faces | `H3_GET_FACES(644325524701193974)` → `[7]` |
| [H3_TO_PARENT](h3-to-parent.md) | Return the parent index at a lower resolution | `H3_TO_PARENT(644325524701193974, 10)` → `622236721289822207` |
| [H3_TO_CHILDREN](h3-to-children.md) | Return child indexes at a higher resolution | `H3_TO_CHILDREN(622236721289822207, 11)` → `[...]` |
| [H3_TO_CENTER_CHILD](h3-to-center-child.md) | Return the center child for a resolution | `H3_TO_CENTER_CHILD(622236721289822207, 11)` → `625561602857582591` |
| [H3_CELL_AREA_M2](h3-cell-area-m2.md) | Return the area of a cell in square meters | `H3_CELL_AREA_M2(644325524701193974)` → `0.8953` |
| [H3_CELL_AREA_RADS2](h3-cell-area-rads2.md) | Return the area of a cell in square radians | `H3_CELL_AREA_RADS2(644325524701193974)` → `2.2e-14` |
| [H3_HEX_AREA_KM2](h3-hex-area-km2.md) | Return the average hexagon area in km² | `H3_HEX_AREA_KM2(10)` → `0.0152` |
| [H3_HEX_AREA_M2](h3-hex-area-m2.md) | Return the average hexagon area in m² | `H3_HEX_AREA_M2(10)` → `15200` |
| [H3_TO_GEO_BOUNDARY](h3-to-geo-boundary.md) | Return the boundary of a cell | `H3_TO_GEO_BOUNDARY(644325524701193974)` → `[[lon1,lat1], ...]` |
| [H3_NUM_HEXAGONS](h3-num-hexagons.md) | Return the number of hexagons at a resolution | `H3_NUM_HEXAGONS(2)` → `5882` |

## H3 Neighborhoods

| Function | Description | Example |
|----------|-------------|---------|
| [H3_DISTANCE](h3-distance.md) | Return the grid distance between two indexes | `H3_DISTANCE(599119489002373119, 599119491149856767)` → `1` |
| [H3_INDEXES_ARE_NEIGHBORS](h3-indexes-are-neighbors.md) | Test whether two indexes are neighbors | `H3_INDEXES_ARE_NEIGHBORS(599119489002373119, 599119491149856767)` → `TRUE` |
| [H3_K_RING](h3-k-ring.md) | Return all indexes within k distance | `H3_K_RING(599119489002373119, 1)` → `[599119489002373119, ...]` |
| [H3_HEX_RING](h3-hex-ring.md) | Return indexes exactly k steps away | `H3_HEX_RING(599119489002373119, 1)` → `[599119491149856767, ...]` |
| [H3_LINE](h3-line.md) | Return indexes along a path | `H3_LINE(from_h3, to_h3)` → `[from_h3, ..., to_h3]` |

## H3 Edge Operations

| Function | Description | Example |
|----------|-------------|---------|
| [H3_GET_UNIDIRECTIONAL_EDGE](h3-get-unidirectional-edge.md) | Return the edge between two adjacent cells | `H3_GET_UNIDIRECTIONAL_EDGE(from_h3, to_h3)` → `edge_index` |
| [H3_UNIDIRECTIONAL_EDGE_IS_VALID](h3-unidirectional-edge-is-valid.md) | Check whether an edge index is valid | `H3_UNIDIRECTIONAL_EDGE_IS_VALID(edge_index)` → `TRUE` |
| [H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE](h3-get-origin-index-from-unidirectional-edge.md) | Return the origin cell from an edge | `H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `from_h3` |
| [H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE](h3-get-destination-index-from-unidirectional-edge.md) | Return the destination cell from an edge | `H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `to_h3` |
| [H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE](h3-get-indexes-from-unidirectional-edge.md) | Return both cells for an edge | `H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `[from_h3, to_h3]` |
| [H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON](h3-get-unidirectional-edges-from-hexagon.md) | List edges originating from a cell | `H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON(h3_index)` → `[edge1, edge2, ...]` |
| [H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY](h3-get-unidirectional-edge-boundary.md) | Return the boundary of an edge | `H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY(edge_index)` → `[[lon1,lat1], [lon2,lat2]]` |

## H3 Measurements & Angles

| Function | Description | Example |
|----------|-------------|---------|
| [H3_EDGE_LENGTH_KM](h3-edge-length-km.md) | Return the average edge length in kilometres | `H3_EDGE_LENGTH_KM(10)` → `0.065` |
| [H3_EDGE_LENGTH_M](h3-edge-length-m.md) | Return the average edge length in metres | `H3_EDGE_LENGTH_M(10)` → `65.91` |
| [H3_EXACT_EDGE_LENGTH_KM](h3-exact-edge-length-km.md) | Return the exact edge length in kilometres | `H3_EXACT_EDGE_LENGTH_KM(edge_index)` → `0.066` |
| [H3_EXACT_EDGE_LENGTH_M](h3-exact-edge-length-m.md) | Return the exact edge length in metres | `H3_EXACT_EDGE_LENGTH_M(edge_index)` → `66.12` |
| [H3_EXACT_EDGE_LENGTH_RADS](h3-exact-edge-length-rads.md) | Return the exact edge length in radians | `H3_EXACT_EDGE_LENGTH_RADS(edge_index)` → `0.00001` |
| [H3_EDGE_ANGLE](h3-edge-angle.md) | Return the angle in radians between two edges | `H3_EDGE_ANGLE(edge1, edge2)` → `1.047` |
