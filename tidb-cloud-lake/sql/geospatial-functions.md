---
title: Geospatial Functions
summary: Databend ships with two complementary sets of geospatial capabilities PostGIS-style geometry functions for building and analysing shapes, and H3 utilities for global hexagonal indexing. The tables below group the functions by task so you can quickly locate the right tool, similar to the layout used in the Snowflake documentation.
---

# Geospatial Functions

Databend ships with two complementary sets of geospatial capabilities: PostGIS-style geometry functions for building and analysing shapes, and H3 utilities for global hexagonal indexing. The tables below group the functions by task so you can quickly locate the right tool, similar to the layout used in the Snowflake documentation.

## Geometry Constructors

| Function | Description | Example |
|----------|-------------|---------|
| [ST_MAKEGEOMPOINT](/tidb-cloud-lake/sql/st-makegeompoint.md) / [ST_GEOM_POINT](/tidb-cloud-lake/sql/st-geom-point.md) | Construct a Point geometry | `ST_MAKEGEOMPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKEPOINT](/tidb-cloud-lake/sql/st-makepoint.md) / [ST_POINT](/tidb-cloud-lake/sql/st-point.md) | Construct a Point geography | `ST_MAKEPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKELINE](/tidb-cloud-lake/sql/st-makeline.md) / [ST_MAKE_LINE](/tidb-cloud-lake/sql/st-make-line.md) | Create a LineString from points | `ST_MAKELINE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `LINESTRING(-122.35 37.55, -122.40 37.60)` |
| [ST_MAKEPOLYGON](/tidb-cloud-lake/sql/st-makepolygon.md) | Create a Polygon from a closed LineString | `ST_MAKEPOLYGON(ST_MAKELINE(...))` → `POLYGON(...)` |
| [ST_POLYGON](/tidb-cloud-lake/sql/st-polygon.md) | Create a Polygon from coordinate rings | `ST_POLYGON(...)` → `POLYGON(...)` |

## Geometry Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [ST_GEOMETRYFROMTEXT](/tidb-cloud-lake/sql/st-geometryfromtext.md) / [ST_GEOMFROMTEXT](/tidb-cloud-lake/sql/st-geomfromtext.md) | Convert WKT to geometry | `ST_GEOMETRYFROMTEXT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMWKB](/tidb-cloud-lake/sql/st-geometryfromwkb.md) / [ST_GEOMFROMWKB](/tidb-cloud-lake/sql/st-geomfromwkb.md) | Convert WKB to geometry | `ST_GEOMETRYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMETRYFROMEWKT](/tidb-cloud-lake/sql/st-geometryfromewkt.md) / [ST_GEOMFROMEWKT](/tidb-cloud-lake/sql/st-geomfromewkt.md) | Convert EWKT to geometry | `ST_GEOMETRYFROMEWKT('SRID=4326;POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMEWKB](/tidb-cloud-lake/sql/st-geometryfromewkb.md) / [ST_GEOMFROMEWKB](/tidb-cloud-lake/sql/st-geomfromewkb.md) | Convert EWKB to geometry | `ST_GEOMETRYFROMEWKB(...)` → `POINT(...)` |
| [ST_GEOGRAPHYFROMWKT](/tidb-cloud-lake/sql/st-geographyfromwkt.md) / [ST_GEOGFROMWKT](/tidb-cloud-lake/sql/st-geogfromwkt.md) | Convert WKT/EWKT to geography | `ST_GEOGRAPHYFROMWKT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOGRAPHYFROMWKB](/tidb-cloud-lake/sql/st-geographyfromwkb.md) / [ST_GEOGFROMWKB](/tidb-cloud-lake/sql/st-geogfromwkb.md) | Convert WKB/EWKB to geography | `ST_GEOGRAPHYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMFROMGEOHASH](/tidb-cloud-lake/sql/st-geomfromgeohash.md) | Convert GeoHash to geometry | `ST_GEOMFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOMPOINTFROMGEOHASH](/tidb-cloud-lake/sql/st-geompointfromgeohash.md) | Convert GeoHash to Point geometry | `ST_GEOMPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [ST_GEOGFROMGEOHASH](/tidb-cloud-lake/sql/st-geogfromgeohash.md) | Convert GeoHash to geography polygon | `ST_GEOGFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOGPOINTFROMGEOHASH](/tidb-cloud-lake/sql/st-geogpointfromgeohash.md) | Convert GeoHash to geography point | `ST_GEOGPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [TO_GEOMETRY](/tidb-cloud-lake/sql/geometry.md) | Parse various formats into geometry | `TO_GEOMETRY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [TO_GEOGRAPHY](/tidb-cloud-lake/sql/to-geography.md) / [TRY_TO_GEOGRAPHY](/tidb-cloud-lake/sql/to-geography.md) | Parse various formats into geography | `TO_GEOGRAPHY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |

## Geometry Output

| Function | Description | Example |
|----------|-------------|---------|
| [ST_ASTEXT](/tidb-cloud-lake/sql/st-astext.md) | Convert geometry to WKT | `ST_ASTEXT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASWKT](/tidb-cloud-lake/sql/st-aswkt.md) | Convert geometry to WKT | `ST_ASWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASBINARY](/tidb-cloud-lake/sql/st-asbinary.md) / [ST_ASWKB](/tidb-cloud-lake/sql/st-aswkb.md) | Convert geometry to WKB | `ST_ASBINARY(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `WKB representation` |
| [ST_ASEWKT](/tidb-cloud-lake/sql/st-asewkt.md) | Convert geometry to EWKT | `ST_ASEWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'SRID=4326;POINT(-122.35 37.55)'` |
| [ST_ASEWKB](/tidb-cloud-lake/sql/st-asewkb.md) | Convert geometry to EWKB | `ST_ASEWKB(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `EWKB representation` |
| [ST_ASGEOJSON](/tidb-cloud-lake/sql/st-asgeojson.md) | Convert geometry to GeoJSON | `ST_ASGEOJSON(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'{"type":"Point","coordinates":[-122.35,37.55]}'` |
| [ST_GEOHASH](/tidb-cloud-lake/sql/st-geohash.md) | Convert geometry to GeoHash | `ST_GEOHASH(ST_MAKEGEOMPOINT(-122.35, 37.55), 7)` → `'9q8yyk8'` |
| [TO_STRING](/tidb-cloud-lake/sql/string.md) | Convert geometry to string | `TO_STRING(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |

## Geometry Accessors & Properties

| Function | Description | Example |
|----------|-------------|---------|
| [ST_DIMENSION](/tidb-cloud-lake/sql/st-dimension.md) | Return the topological dimension | `ST_DIMENSION(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `0` |
| [ST_SRID](/tidb-cloud-lake/sql/st-srid.md) | Return the SRID of a geometry | `ST_SRID(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `4326` |
| [ST_SETSRID](/tidb-cloud-lake/sql/st-setsrid.md) | Assign an SRID to a geometry | `ST_SETSRID(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-122.35 37.55)` |
| [ST_TRANSFORM](/tidb-cloud-lake/sql/st-transform.md) | Transform geometry to a new SRID | `ST_TRANSFORM(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-13618288.8 4552395.0)` |
| [ST_NPOINTS](/tidb-cloud-lake/sql/st-npoints.md) / [ST_NUMPOINTS](/tidb-cloud-lake/sql/st-numpoints.md) | Count points in a geometry | `ST_NPOINTS(ST_MAKELINE(...))` → `2` |
| [ST_POINTN](/tidb-cloud-lake/sql/st-pointn.md) | Return a specific point from a LineString | `ST_POINTN(ST_MAKELINE(...), 1)` → `POINT(-122.35 37.55)` |
| [ST_STARTPOINT](/tidb-cloud-lake/sql/st-startpoint.md) | Return the first point in a LineString | `ST_STARTPOINT(ST_MAKELINE(...))` → `POINT(-122.35 37.55)` |
| [ST_ENDPOINT](/tidb-cloud-lake/sql/st-endpoint.md) | Return the last point in a LineString | `ST_ENDPOINT(ST_MAKELINE(...))` → `POINT(-122.40 37.60)` |
| [ST_LENGTH](/tidb-cloud-lake/sql/st-length.md) | Measure the length of a LineString | `ST_LENGTH(ST_MAKELINE(...))` → `5.57` |
| [ST_X](/tidb-cloud-lake/sql/st-x.md) / [ST_Y](/tidb-cloud-lake/sql/st-y.md) | Return the X or Y coordinate of a Point | `ST_X(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `-122.35` |
| [ST_XMIN](/tidb-cloud-lake/sql/st-xmin.md) / [ST_XMAX](/tidb-cloud-lake/sql/st-xmax.md) | Return the min/max X coordinate | `ST_XMIN(ST_MAKELINE(...))` → `-122.40` |
| [ST_YMIN](/tidb-cloud-lake/sql/st-ymin.md) / [ST_YMAX](/tidb-cloud-lake/sql/st-ymax.md) | Return the min/max Y coordinate | `ST_YMAX(ST_MAKELINE(...))` → `37.60` |

## Spatial Relationships

| Function | Description | Example |
|----------|-------------|---------|
| [ST_CONTAINS](/tidb-cloud-lake/sql/st-contains.md) | Test whether one geometry contains another | `ST_CONTAINS(ST_MAKEPOLYGON(...), ST_MAKEGEOMPOINT(...))` → `TRUE` |
| [POINT_IN_POLYGON](/tidb-cloud-lake/sql/point-in-polygon.md) | Check if a point lies inside a polygon | `POINT_IN_POLYGON([lon, lat], [[p1_lon, p1_lat], ...])` → `TRUE` |

## Distance & Measurements

| Function | Description | Example |
|----------|-------------|---------|
| [ST_DISTANCE](/tidb-cloud-lake/sql/st-distance.md) | Measure the distance between geometries | `ST_DISTANCE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `5.57` |
| [HAVERSINE](/tidb-cloud-lake/sql/haversine.md) | Compute great-circle distance between coordinates | `HAVERSINE(37.55, -122.35, 37.60, -122.40)` → `6.12` |

## H3 Indexing & Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [GEO_TO_H3](/tidb-cloud-lake/sql/geo-to-h3.md) | Convert longitude/latitude to an H3 index | `GEO_TO_H3(37.7950, 55.7129, 15)` → `644325524701193974` |
| [H3_TO_GEO](/tidb-cloud-lake/sql/h3-to-geo.md) | Convert an H3 index to longitude/latitude | `H3_TO_GEO(644325524701193974)` → `[37.7950, 55.7129]` |
| [H3_TO_STRING](/tidb-cloud-lake/sql/h3-to-string.md) | Convert an H3 index to its string form | `H3_TO_STRING(644325524701193974)` → `'8f2830828052d25'` |
| [STRING_TO_H3](/tidb-cloud-lake/sql/string-to-h3.md) | Convert an H3 string to an index | `STRING_TO_H3('8f2830828052d25')` → `644325524701193974` |
| [GEOHASH_ENCODE](/tidb-cloud-lake/sql/geohash-encode.md) | Encode longitude/latitude to GeoHash | `GEOHASH_ENCODE(37.7950, 55.7129, 12)` → `'ucfv0nzpt3s7'` |
| [GEOHASH_DECODE](/tidb-cloud-lake/sql/geohash-decode.md) | Decode a GeoHash to longitude/latitude | `GEOHASH_DECODE('ucfv0nzpt3s7')` → `[37.7950, 55.7129]` |

## H3 Cell Properties

| Function | Description | Example |
|----------|-------------|---------|
| [H3_GET_RESOLUTION](/tidb-cloud-lake/sql/h3-get-resolution.md) | Return the resolution of an H3 index | `H3_GET_RESOLUTION(644325524701193974)` → `15` |
| [H3_GET_BASE_CELL](/tidb-cloud-lake/sql/h3-get-base-cell.md) | Return the base cell number | `H3_GET_BASE_CELL(644325524701193974)` → `14` |
| [H3_IS_VALID](/tidb-cloud-lake/sql/h3-is-valid.md) | Check whether an H3 index is valid | `H3_IS_VALID(644325524701193974)` → `TRUE` |
| [H3_IS_PENTAGON](/tidb-cloud-lake/sql/h3-is-pentagon.md) | Check whether an H3 index is a pentagon | `H3_IS_PENTAGON(644325524701193974)` → `FALSE` |
| [H3_IS_RES_CLASS_III](/tidb-cloud-lake/sql/h3-is-res-class-iii.md) | Check whether an H3 index is class III | `H3_IS_RES_CLASS_III(644325524701193974)` → `FALSE` |
| [H3_GET_FACES](/tidb-cloud-lake/sql/h3-get-faces.md) | Return intersecting icosahedron faces | `H3_GET_FACES(644325524701193974)` → `[7]` |
| [H3_TO_PARENT](/tidb-cloud-lake/sql/h3-to-parent.md) | Return the parent index at a lower resolution | `H3_TO_PARENT(644325524701193974, 10)` → `622236721289822207` |
| [H3_TO_CHILDREN](/tidb-cloud-lake/sql/h3-to-children.md) | Return child indexes at a higher resolution | `H3_TO_CHILDREN(622236721289822207, 11)` → `[...]` |
| [H3_TO_CENTER_CHILD](/tidb-cloud-lake/sql/h3-to-center-child.md) | Return the center child for a resolution | `H3_TO_CENTER_CHILD(622236721289822207, 11)` → `625561602857582591` |
| [H3_CELL_AREA_M2](/tidb-cloud-lake/sql/h3-cell-area-m2.md) | Return the area of a cell in square meters | `H3_CELL_AREA_M2(644325524701193974)` → `0.8953` |
| [H3_CELL_AREA_RADS2](/tidb-cloud-lake/sql/h3-cell-area-rads2.md) | Return the area of a cell in square radians | `H3_CELL_AREA_RADS2(644325524701193974)` → `2.2e-14` |
| [H3_HEX_AREA_KM2](/tidb-cloud-lake/sql/h3-hex-area-km2.md) | Return the average hexagon area in km² | `H3_HEX_AREA_KM2(10)` → `0.0152` |
| [H3_HEX_AREA_M2](/tidb-cloud-lake/sql/h3-hex-area-m2.md) | Return the average hexagon area in m² | `H3_HEX_AREA_M2(10)` → `15200` |
| [H3_TO_GEO_BOUNDARY](/tidb-cloud-lake/sql/h3-to-geo-boundary.md) | Return the boundary of a cell | `H3_TO_GEO_BOUNDARY(644325524701193974)` → `[[lon1,lat1], ...]` |
| [H3_NUM_HEXAGONS](/tidb-cloud-lake/sql/h3-num-hexagons.md) | Return the number of hexagons at a resolution | `H3_NUM_HEXAGONS(2)` → `5882` |

## H3 Neighborhoods

| Function | Description | Example |
|----------|-------------|---------|
| [H3_DISTANCE](/tidb-cloud-lake/sql/h3-distance.md) | Return the grid distance between two indexes | `H3_DISTANCE(599119489002373119, 599119491149856767)` → `1` |
| [H3_INDEXES_ARE_NEIGHBORS](/tidb-cloud-lake/sql/h3-indexes-are-neighbors.md) | Test whether two indexes are neighbors | `H3_INDEXES_ARE_NEIGHBORS(599119489002373119, 599119491149856767)` → `TRUE` |
| [H3_K_RING](/tidb-cloud-lake/sql/h3-k-ring.md) | Return all indexes within k distance | `H3_K_RING(599119489002373119, 1)` → `[599119489002373119, ...]` |
| [H3_HEX_RING](/tidb-cloud-lake/sql/h3-hex-ring.md) | Return indexes exactly k steps away | `H3_HEX_RING(599119489002373119, 1)` → `[599119491149856767, ...]` |
| [H3_LINE](/tidb-cloud-lake/sql/h3-line.md) | Return indexes along a path | `H3_LINE(from_h3, to_h3)` → `[from_h3, ..., to_h3]` |

## H3 Edge Operations

| Function | Description | Example |
|----------|-------------|---------|
| [H3_GET_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-unidirectional-edge.md) | Return the edge between two adjacent cells | `H3_GET_UNIDIRECTIONAL_EDGE(from_h3, to_h3)` → `edge_index` |
| [H3_UNIDIRECTIONAL_EDGE_IS_VALID](/tidb-cloud-lake/sql/h3-unidirectional-edge-is-valid.md) | Check whether an edge index is valid | `H3_UNIDIRECTIONAL_EDGE_IS_VALID(edge_index)` → `TRUE` |
| [H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-origin-index-unidirectional-edge.md) | Return the origin cell from an edge | `H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `from_h3` |
| [H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-destination-index-unidirectional-edge.md) | Return the destination cell from an edge | `H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `to_h3` |
| [H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-indexes-unidirectional-edge.md) | Return both cells for an edge | `H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `[from_h3, to_h3]` |
| [H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON](/tidb-cloud-lake/sql/h3-get-unidirectional-edges-hexagon.md) | List edges originating from a cell | `H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON(h3_index)` → `[edge1, edge2, ...]` |
| [H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY](/tidb-cloud-lake/sql/h3-get-unidirectional-edge-boundary.md) | Return the boundary of an edge | `H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY(edge_index)` → `[[lon1,lat1], [lon2,lat2]]` |

## H3 Measurements & Angles

| Function | Description | Example |
|----------|-------------|---------|
| [H3_EDGE_LENGTH_KM](/tidb-cloud-lake/sql/h3-edge-length-km.md) | Return the average edge length in kilometres | `H3_EDGE_LENGTH_KM(10)` → `0.065` |
| [H3_EDGE_LENGTH_M](/tidb-cloud-lake/sql/h3-edge-length-m.md) | Return the average edge length in metres | `H3_EDGE_LENGTH_M(10)` → `65.91` |
| [H3_EXACT_EDGE_LENGTH_KM](/tidb-cloud-lake/sql/h3-exact-edge-length-km.md) | Return the exact edge length in kilometres | `H3_EXACT_EDGE_LENGTH_KM(edge_index)` → `0.066` |
| [H3_EXACT_EDGE_LENGTH_M](/tidb-cloud-lake/sql/h3-exact-edge-length-m.md) | Return the exact edge length in metres | `H3_EXACT_EDGE_LENGTH_M(edge_index)` → `66.12` |
| [H3_EXACT_EDGE_LENGTH_RADS](/tidb-cloud-lake/sql/h3-exact-edge-length-rads.md) | Return the exact edge length in radians | `H3_EXACT_EDGE_LENGTH_RADS(edge_index)` → `0.00001` |
| [H3_EDGE_ANGLE](/tidb-cloud-lake/sql/h3-edge-angle.md) | Return the angle in radians between two edges | `H3_EDGE_ANGLE(edge1, edge2)` → `1.047` |
