---
title: Geospatial Functions
summary: "{{{ .lake }}} は、相互補完的な 2 つの地理空間機能セットを提供します。1 つは図形の構築と解析のための PostGIS スタイルの geometry 関数、もう 1 つはグローバルな六角形インデックスのための H3 ユーティリティです。以下の表では、Snowflake のドキュメントと同様のレイアウトで、タスクごとに関数を分類しているため、適切なツールをすばやく見つけることができます。"
---

# Geospatial Functions

{{{ .lake }}} は、相互補完的な 2 つの地理空間機能セットを提供します。1 つは図形の構築と解析のための PostGIS スタイルの geometry 関数、もう 1 つはグローバルな六角形インデックスのための H3 ユーティリティです。以下の表では、Snowflake のドキュメントと同様のレイアウトで、タスクごとに関数を分類しているため、適切なツールをすばやく見つけることができます。

## Constructors {#constructors}

| 関数 | 説明 | 注記 | 例 |
|----------|-------------|------|---------|
| [ST_MAKEGEOMPOINT](/tidb-cloud-lake/sql/st-makegeompoint.md) / [ST_GEOM_POINT](/tidb-cloud-lake/sql/st-geom-point.md) | Point geometry を構築します | GEOGRAPHY のみ | `ST_MAKEGEOMPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKEPOINT](/tidb-cloud-lake/sql/st-makepoint.md) / [ST_POINT](/tidb-cloud-lake/sql/st-point.md) | Point geography を構築します | GEOGRAPHY のみ | `ST_MAKEPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKELINE](/tidb-cloud-lake/sql/st-makeline.md) / [ST_MAKE_LINE](/tidb-cloud-lake/sql/st-make-line.md) | 点から LineString を作成します |  | `ST_MAKELINE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `LINESTRING(-122.35 37.55, -122.40 37.60)` |
| [ST_MAKEPOLYGON](/tidb-cloud-lake/sql/st-makepolygon.md) | 閉じた LineString から Polygon を作成します |  | `ST_MAKEPOLYGON(ST_MAKELINE(...))` → `POLYGON(...)` |
| [ST_POLYGON](/tidb-cloud-lake/sql/st-polygon.md) | 座標リングから Polygon を作成します | GEOGRAPHY のみ | `ST_POLYGON(...)` → `POLYGON(...)` |

## Conversion {#conversion}

| 関数 | 説明 | 注記 | 例 |
|----------|-------------|------|---------|
| [ST_GEOMETRYFROMTEXT](/tidb-cloud-lake/sql/st-geometryfromtext.md) / [ST_GEOMFROMTEXT](/tidb-cloud-lake/sql/st-geomfromtext.md) | WKT を geometry に変換します | GEOGRAPHY のみ | `ST_GEOMETRYFROMTEXT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMWKB](/tidb-cloud-lake/sql/st-geometryfromwkb.md) / [ST_GEOMFROMWKB](/tidb-cloud-lake/sql/st-geomfromwkb.md) | WKB を geometry に変換します | GEOGRAPHY のみ | `ST_GEOMETRYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMETRYFROMEWKT](/tidb-cloud-lake/sql/st-geometryfromewkt.md) / [ST_GEOMFROMEWKT](/tidb-cloud-lake/sql/st-geomfromewkt.md) | EWKT を geometry に変換します | GEOGRAPHY のみ | `ST_GEOMETRYFROMEWKT('SRID=4326;POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMEWKB](/tidb-cloud-lake/sql/st-geometryfromewkb.md) / [ST_GEOMFROMEWKB](/tidb-cloud-lake/sql/st-geomfromewkb.md) | EWKB を geometry に変換します | GEOGRAPHY のみ | `ST_GEOMETRYFROMEWKB(...)` → `POINT(...)` |
| [ST_GEOGRAPHYFROMWKT](/tidb-cloud-lake/sql/st-geographyfromwkt.md) / [ST_GEOGFROMWKT](/tidb-cloud-lake/sql/st-geogfromwkt.md) | WKT/EWKT を geography に変換します | GEOGRAPHY のみ | `ST_GEOGRAPHYFROMWKT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOGRAPHYFROMWKB](/tidb-cloud-lake/sql/st-geographyfromwkb.md) / [ST_GEOGFROMWKB](/tidb-cloud-lake/sql/st-geogfromwkb.md) | WKB/EWKB を geography に変換します | GEOGRAPHY のみ | `ST_GEOGRAPHYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMFROMGEOHASH](/tidb-cloud-lake/sql/st-geomfromgeohash.md) | GeoHash を geometry に変換します | GEOGRAPHY のみ | `ST_GEOMFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOMPOINTFROMGEOHASH](/tidb-cloud-lake/sql/st-geompointfromgeohash.md) | GeoHash を Point geometry に変換します | GEOGRAPHY のみ | `ST_GEOMPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [ST_GEOGFROMGEOHASH](/tidb-cloud-lake/sql/st-geogfromgeohash.md) | GeoHash を geography polygon に変換します | GEOGRAPHY のみ | `ST_GEOGFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOGPOINTFROMGEOHASH](/tidb-cloud-lake/sql/st-geogpointfromgeohash.md) | GeoHash を geography point に変換します | GEOGRAPHY のみ | `ST_GEOGPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [TO_GEOMETRY](/tidb-cloud-lake/sql/geometry.md) | さまざまな形式を geometry として解析します | GEOGRAPHY のみ | `TO_GEOMETRY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [TO_GEOGRAPHY](/tidb-cloud-lake/sql/to-geography.md) / [TRY_TO_GEOGRAPHY](/tidb-cloud-lake/sql/to-geography.md) | さまざまな形式を geography として解析します | GEOGRAPHY のみ | `TO_GEOGRAPHY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |

## Output {#output}

| 関数 | 説明 | 注記 | 例 |
|----------|-------------|------|---------|
| [ST_ASTEXT](/tidb-cloud-lake/sql/st-astext.md) | geometry を WKT に変換します |  | `ST_ASTEXT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASWKT](/tidb-cloud-lake/sql/st-aswkt.md) | geometry を WKT に変換します |  | `ST_ASWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASBINARY](/tidb-cloud-lake/sql/st-asbinary.md) / [ST_ASWKB](/tidb-cloud-lake/sql/st-aswkb.md) | geometry を WKB に変換します |  | `ST_ASBINARY(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `WKB representation` |
| [ST_ASEWKT](/tidb-cloud-lake/sql/st-asewkt.md) | geometry を EWKT に変換します |  | `ST_ASEWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'SRID=4326;POINT(-122.35 37.55)'` |
| [ST_ASEWKB](/tidb-cloud-lake/sql/st-asewkb.md) | geometry を EWKB に変換します |  | `ST_ASEWKB(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `EWKB representation` |
| [ST_ASGEOJSON](/tidb-cloud-lake/sql/st-asgeojson.md) | geometry を GeoJSON に変換します |  | `ST_ASGEOJSON(ST_MAKEGEOMPOINT(-122.35, 37.55))` → '{"type":"Point","coordinates":[-122.35,37.55]}' |
| [ST_GEOHASH](/tidb-cloud-lake/sql/st-geohash.md) | geometry を GeoHash に変換します |  | `ST_GEOHASH(ST_MAKEGEOMPOINT(-122.35, 37.55), 7)` → `'9q8yyk8'` |
| [TO_STRING](/tidb-cloud-lake/sql/string.md) | geometry を文字列に変換します |  | `TO_STRING(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |

## Accessors & Properties {#accessors-properties}

| 関数 | 説明 | 注記 | 例 |
|----------|-------------|------|---------|
| [ST_DIMENSION](/tidb-cloud-lake/sql/st-dimension.md) | トポロジ次元を返します |  | `ST_DIMENSION(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `0` |
| [ST_CENTROID](/tidb-cloud-lake/sql/st-centroid.md) | geometry の重心を返します | GEOMETRY のみ | `ST_CENTROID(TO_GEOMETRY('LINESTRING(0 0, 2 0)'))` → `POINT(1 0)` |
| [ST_ENVELOPE](/tidb-cloud-lake/sql/st-envelope.md) | 最小外接矩形を返します | GEOMETRY のみ | `ST_ENVELOPE(TO_GEOMETRY('LINESTRING(0 0, 2 3)'))` → `POLYGON((0 0,2 0,2 3,0 3,0 0))` |
| [ST_SRID](/tidb-cloud-lake/sql/st-srid.md) | geometry の SRID を返します |  | `ST_SRID(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `4326` |
| [ST_POINTN](/tidb-cloud-lake/sql/st-pointn.md) | LineString から指定した点を返します |  | `ST_POINTN(ST_MAKELINE(...), 1)` → `POINT(-122.35 37.55)` |
| [ST_STARTPOINT](/tidb-cloud-lake/sql/st-startpoint.md) | LineString の最初の点を返します |  | `ST_STARTPOINT(ST_MAKELINE(...))` → `POINT(-122.35 37.55)` |
| [ST_ENDPOINT](/tidb-cloud-lake/sql/st-endpoint.md) | LineString の最後の点を返します |  | `ST_ENDPOINT(ST_MAKELINE(...))` → `POINT(-122.40 37.60)` |
| [ST_X](/tidb-cloud-lake/sql/st-x.md) / [ST_Y](/tidb-cloud-lake/sql/st-y.md) | Point の X または Y 座標を返します |  | `ST_X(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `-122.35` |
| [ST_XMIN](/tidb-cloud-lake/sql/st-xmin.md) / [ST_XMAX](/tidb-cloud-lake/sql/st-xmax.md) | X 座標の最小値/最大値を返します |  | `ST_XMIN(ST_MAKELINE(...))` → `-122.40` |
| [ST_YMIN](/tidb-cloud-lake/sql/st-ymin.md) / [ST_YMAX](/tidb-cloud-lake/sql/st-ymax.md) | Y 座標の最小値/最大値を返します |  | `ST_YMAX(ST_MAKELINE(...))` → `37.60` |

## Relationship and measurement {#relationship-and-measurement}

| 関数 | 説明 | 注記 | 例 |
|----------|-------------|------|---------|
| [HAVERSINE](/tidb-cloud-lake/sql/haversine.md) | 座標間の大円距離を計算します |  | `HAVERSINE(37.55, -122.35, 37.60, -122.40)` → `6.12` |
| [ST_AREA](/tidb-cloud-lake/sql/st-area.md) | geometry または geography オブジェクトの面積を測定します |  | `ST_AREA(TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'))` → `1.0` |
| [ST_CONTAINS](/tidb-cloud-lake/sql/st-contains.md) | ある geometry が別の geometry を含むかどうかを判定します | GEOMETRY のみ | `ST_CONTAINS(ST_MAKEPOLYGON(...), ST_MAKEGEOMPOINT(...))` → `TRUE` |
| [ST_CONVEXHULL](/tidb-cloud-lake/sql/st-convexhull.md) | geometry の凸包を計算します | GEOMETRY のみ | `ST_CONVEXHULL(TO_GEOMETRY('POLYGON((0 0,2 0,2 2,0 2,0 0))'))` → `POLYGON((0 0,2 0,2 2,0 2,0 0))` |
| [ST_NPOINTS](/tidb-cloud-lake/sql/st-npoints.md) | geometry 内の点数を数えます |  | `ST_NPOINTS(ST_MAKELINE(...))` → `2` |
| [ST_NUMPOINTS](/tidb-cloud-lake/sql/st-numpoints.md) | geometry 内の点数を数えます | GEOMETRY のみ | `ST_NUMPOINTS(ST_MAKELINE(...))` → `2` |
| [ST_INTERSECTS](/tidb-cloud-lake/sql/st-intersects.md) | 2 つの geometry が交差するかどうかを判定します | GEOMETRY のみ | `ST_INTERSECTS(TO_GEOMETRY('LINESTRING(0 0, 2 2)'), TO_GEOMETRY('LINESTRING(0 2, 2 0)'))` → `TRUE` |
| [ST_DISJOINT](/tidb-cloud-lake/sql/st-disjoint.md) | 2 つの geometry が互いに素であるかどうかを判定します | GEOMETRY のみ | `ST_DISJOINT(TO_GEOMETRY('POINT(3 3)'), TO_GEOMETRY('POLYGON((0 0,2 0,2 2,0 2,0 0))'))` → `TRUE` |
| [ST_WITHIN](/tidb-cloud-lake/sql/st-within.md) | ある geometry が別の geometry の内部にあるかどうかを判定します | GEOMETRY のみ | `ST_WITHIN(TO_GEOMETRY('POINT(1 1)'), TO_GEOMETRY('POLYGON((0 0,2 0,2 2,0 2,0 0))'))` → `TRUE` |
| [ST_EQUALS](/tidb-cloud-lake/sql/st-equals.md) | 2 つの geometry が空間的に等しいかどうかを判定します | GEOMETRY のみ | `ST_EQUALS(TO_GEOMETRY('POINT(1 1)'), TO_GEOMETRY('POINT(1 1)'))` → `TRUE` |
| [ST_LENGTH](/tidb-cloud-lake/sql/st-length.md) | LineString の長さを測定します |  | `ST_LENGTH(ST_MAKELINE(...))` → `5.57` |
| [ST_DISTANCE](/tidb-cloud-lake/sql/st-distance.md) | geometry 間の距離を測定します |  | `ST_DISTANCE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `5.57` |
| [ST_DWITHIN](/tidb-cloud-lake/sql/st-dwithin.md) | 2 つの geometry が指定距離内にあるかどうかを判定します | GEOMETRY のみ | `ST_DWITHIN(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'), 1.5)` → `TRUE` |
| [ST_UNION](/tidb-cloud-lake/sql/st-union.md) | 2 つの入力を結合した geometry を返します | GEOMETRY のみ | `ST_UNION(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'))` → `MULTIPOINT(0 0,1 1)` |
| [ST_INTERSECTION](/tidb-cloud-lake/sql/st-intersection.md) | 2 つの geometry の共通部分を返します | GEOMETRY のみ | `ST_INTERSECTION(TO_GEOMETRY('LINESTRING(0 0, 1 1)'), TO_GEOMETRY('LINESTRING(0 0, 1 1)'))` → `LINESTRING(0 0,1 1)` |
| [ST_DIFFERENCE](/tidb-cloud-lake/sql/st-difference.md) | 1 つ目の geometry のうち、2 つ目で覆われていない部分を返します | GEOMETRY のみ | `ST_DIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'))` → `POINT(0 0)` |
| [ST_SYMDIFFERENCE](/tidb-cloud-lake/sql/st-symdifference.md) | 2 つの geometry の重ならない部分を返します | GEOMETRY のみ | `ST_SYMDIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'))` → `MULTIPOINT(0 0,1 1)` |

## Transformation {#transformation}

| 関数 | 説明 | 注記 | 例 |
|----------|-------------|------|---------|
| [ST_HILBERT](/tidb-cloud-lake/sql/st-hilbert.md) | geometry または geography を Hilbert curve index にエンコードします |  | `ST_HILBERT(TO_GEOMETRY('POINT(0.5 0.5)'), [0, 0, 1, 1])` → `715827882` |
| [ST_SETSRID](/tidb-cloud-lake/sql/st-setsrid.md) | geometry に SRID を割り当てます | GEOMETRY のみ | `ST_SETSRID(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-122.35 37.55)` |
| [ST_TRANSFORM](/tidb-cloud-lake/sql/st-transform.md) | geometry を新しい SRID に変換します | GEOMETRY のみ | `ST_TRANSFORM(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-13618288.8 4552395.0)` |

## Spatial Relationships {#spatial-relationships}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ST_CONTAINS](/tidb-cloud-lake/sql/st-contains.md) | ある geometry が別の geometry を含むかどうかを判定します | `ST_CONTAINS(ST_MAKEPOLYGON(...), ST_MAKEGEOMPOINT(...))` → `TRUE` |
| [POINT_IN_POLYGON](/tidb-cloud-lake/sql/point-in-polygon.md) | 点が polygon の内側にあるかどうかを確認します | `POINT_IN_POLYGON([lon, lat], [[p1_lon, p1_lat], ...])` → `TRUE` |

## Distance & Measurements {#distance-measurements}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ST_DISTANCE](/tidb-cloud-lake/sql/st-distance.md) | geometry 間の距離を測定します | `ST_DISTANCE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `5.57` |
| [HAVERSINE](/tidb-cloud-lake/sql/haversine.md) | 座標間の大円距離を計算します | `HAVERSINE(37.55, -122.35, 37.60, -122.40)` → `6.12` |

## H3 Indexing & Conversion {#h3-indexing-conversion}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [GEO_TO_H3](/tidb-cloud-lake/sql/geo-to-h3.md) | 経度/緯度を H3 インデックスに変換します | `GEO_TO_H3(37.7950, 55.7129, 15)` → `644325524701193974` |
| [H3_TO_GEO](/tidb-cloud-lake/sql/h3-to-geo.md) | H3 インデックスを経度/緯度に変換します | `H3_TO_GEO(644325524701193974)` → `[37.7950, 55.7129]` |
| [H3_TO_STRING](/tidb-cloud-lake/sql/h3-to-string.md) | H3 インデックスを文字列表現に変換します | `H3_TO_STRING(644325524701193974)` → `'8f2830828052d25'` |
| [STRING_TO_H3](/tidb-cloud-lake/sql/string-to-h3.md) | H3 文字列をインデックスに変換します | `STRING_TO_H3('8f2830828052d25')` → `644325524701193974` |
| [GEOHASH_ENCODE](/tidb-cloud-lake/sql/geohash-encode.md) | 経度/緯度を GeoHash にエンコードします | `GEOHASH_ENCODE(37.7950, 55.7129, 12)` → `'ucfv0nzpt3s7'` |
| [GEOHASH_DECODE](/tidb-cloud-lake/sql/geohash-decode.md) | GeoHash を経度/緯度にデコードします | `GEOHASH_DECODE('ucfv0nzpt3s7')` → `[37.7950, 55.7129]` |

## H3 Cell Properties {#h3-cell-properties}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [H3_GET_RESOLUTION](/tidb-cloud-lake/sql/h3-get-resolution.md) | H3 インデックスの解像度を返します | `H3_GET_RESOLUTION(644325524701193974)` → `15` |
| [H3_GET_BASE_CELL](/tidb-cloud-lake/sql/h3-get-base-cell.md) | ベースセル番号を返します | `H3_GET_BASE_CELL(644325524701193974)` → `14` |
| [H3_IS_VALID](/tidb-cloud-lake/sql/h3-is-valid.md) | H3 インデックスが有効かどうかを確認します | `H3_IS_VALID(644325524701193974)` → `TRUE` |
| [H3_IS_PENTAGON](/tidb-cloud-lake/sql/h3-is-pentagon.md) | H3 インデックスが五角形かどうかを確認します | `H3_IS_PENTAGON(644325524701193974)` → `FALSE` |
| [H3_IS_RES_CLASS_III](/tidb-cloud-lake/sql/h3-is-res-class-iii.md) | H3 インデックスが class III かどうかを確認します | `H3_IS_RES_CLASS_III(644325524701193974)` → `FALSE` |
| [H3_GET_FACES](/tidb-cloud-lake/sql/h3-get-faces.md) | 交差する正二十面体の面を返します | `H3_GET_FACES(644325524701193974)` → `[7]` |
| [H3_TO_PARENT](/tidb-cloud-lake/sql/h3-to-parent.md) | より低い解像度で親インデックスを返します | `H3_TO_PARENT(644325524701193974, 10)` → `622236721289822207` |
| [H3_TO_CHILDREN](/tidb-cloud-lake/sql/h3-to-children.md) | より高い解像度で子インデックスを返します | `H3_TO_CHILDREN(622236721289822207, 11)` → `[...]` |
| [H3_TO_CENTER_CHILD](/tidb-cloud-lake/sql/h3-to-center-child.md) | 指定した解像度の中心子セルを返します | `H3_TO_CENTER_CHILD(622236721289822207, 11)` → `625561602857582591` |
| [H3_CELL_AREA_M2](/tidb-cloud-lake/sql/h3-cell-area-m2.md) | セルの面積を平方メートルで返します | `H3_CELL_AREA_M2(644325524701193974)` → `0.8953` |
| [H3_CELL_AREA_RADS2](/tidb-cloud-lake/sql/h3-cell-area-rads2.md) | セルの面積を平方ラジアンで返します | `H3_CELL_AREA_RADS2(644325524701193974)` → `2.2e-14` |
| [H3_HEX_AREA_KM2](/tidb-cloud-lake/sql/h3-hex-area-km2.md) | 平均六角形面積を km² で返します | `H3_HEX_AREA_KM2(10)` → `0.0152` |
| [H3_HEX_AREA_M2](/tidb-cloud-lake/sql/h3-hex-area-m2.md) | 平均六角形面積を m² で返します | `H3_HEX_AREA_M2(10)` → `15200` |
| [H3_TO_GEO_BOUNDARY](/tidb-cloud-lake/sql/h3-to-geo-boundary.md) | セルの境界を返します | `H3_TO_GEO_BOUNDARY(644325524701193974)` → `[[lon1,lat1], ...]` |
| [H3_NUM_HEXAGONS](/tidb-cloud-lake/sql/h3-num-hexagons.md) | 指定解像度における六角形の数を返します | `H3_NUM_HEXAGONS(2)` → `5882` |
| [GEO_DISTANCE](/tidb-cloud-lake/sql/geo-distance.md) | WGS84 を使用した概算距離をメートルで返します | `GEO_DISTANCE(0, 0, 0, 0)` → `0` |
| [GREAT_CIRCLE_DISTANCE](/tidb-cloud-lake/sql/great-circle-distance.md) | 大円距離をメートルで返します | `GREAT_CIRCLE_DISTANCE(0, 0, 0, 0)` → `0` |
| [GREAT_CIRCLE_ANGLE](/tidb-cloud-lake/sql/great-circle-angle.md) | 大円中心角を度単位で返します | `GREAT_CIRCLE_ANGLE(0, 0, 45, 0)` → `45` |
| [POINT_IN_POLYGON](/tidb-cloud-lake/sql/point-in-polygon.md) | 点が多角形の内側にあるかどうかを確認します | `POINT_IN_POLYGON([lon, lat], [[p1_lon, p1_lat], ...])` → `TRUE` |
| [POINT_IN_ELLIPSES](/tidb-cloud-lake/sql/point-in-ellipses.md) | 点がいずれかの楕円の内側にあるかどうかを確認します | `POINT_IN_ELLIPSES(10, 10, 10, 9.1, 1, 0.9999)` → `1` |

## H3 Neighborhoods {#h3-neighborhoods}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [H3_DISTANCE](/tidb-cloud-lake/sql/h3-distance.md) | 2 つのインデックス間のグリッド距離を返します | `H3_DISTANCE(599119489002373119, 599119491149856767)` → `1` |
| [H3_INDEXES_ARE_NEIGHBORS](/tidb-cloud-lake/sql/h3-indexes-are-neighbors.md) | 2 つのインデックスが隣接しているかどうかを判定します | `H3_INDEXES_ARE_NEIGHBORS(599119489002373119, 599119491149856767)` → `TRUE` |
| [H3_K_RING](/tidb-cloud-lake/sql/h3-k-ring.md) | k 距離以内のすべてのインデックスを返します | `H3_K_RING(599119489002373119, 1)` → `[599119489002373119, ...]` |
| [H3_HEX_RING](/tidb-cloud-lake/sql/h3-hex-ring.md) | ちょうど k ステップ離れたインデックスを返します | `H3_HEX_RING(599119489002373119, 1)` → `[599119491149856767, ...]` |
| [H3_LINE](/tidb-cloud-lake/sql/h3-line.md) | 経路に沿ったインデックスを返します | `H3_LINE(from_h3, to_h3)` → `[from_h3, ..., to_h3]` |

## H3 Edge Operations {#h3-edge-operations}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [H3_GET_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-unidirectional-edge.md) | 隣接する 2 つのセル間のエッジを返します | `H3_GET_UNIDIRECTIONAL_EDGE(from_h3, to_h3)` → `edge_index` |
| [H3_UNIDIRECTIONAL_EDGE_IS_VALID](/tidb-cloud-lake/sql/h3-unidirectional-edge-is-valid.md) | エッジインデックスが有効かどうかを確認します | `H3_UNIDIRECTIONAL_EDGE_IS_VALID(edge_index)` → `TRUE` |
| [H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-origin-index-unidirectional-edge.md) | エッジから始点セルを返します | `H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `from_h3` |
| [H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-destination-index-unidirectional-edge.md) | エッジから終点セルを返します | `H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `to_h3` |
| [H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-indexes-unidirectional-edge.md) | エッジに対応する両方のセルを返します | `H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `[from_h3, to_h3]` |
| [H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON](/tidb-cloud-lake/sql/h3-get-unidirectional-edges-hexagon.md) | セルから出るエッジを一覧表示します | `H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON(h3_index)` → `[edge1, edge2, ...]` |
| [H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY](/tidb-cloud-lake/sql/h3-get-unidirectional-edge-boundary.md) | エッジの境界を返します | `H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY(edge_index)` → `[[lon1,lat1], [lon2,lat2]]` |

## H3 Measurements & Angles {#h3-measurements-angles}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [H3_EDGE_LENGTH_KM](/tidb-cloud-lake/sql/h3-edge-length-km.md) | 平均エッジ長をキロメートルで返します | `H3_EDGE_LENGTH_KM(10)` → `0.065` |
| [H3_EDGE_LENGTH_M](/tidb-cloud-lake/sql/h3-edge-length-m.md) | 平均エッジ長をメートルで返します | `H3_EDGE_LENGTH_M(10)` → `65.91` |
| [H3_EXACT_EDGE_LENGTH_KM](/tidb-cloud-lake/sql/h3-exact-edge-length-km.md) | 正確なエッジ長をキロメートルで返します | `H3_EXACT_EDGE_LENGTH_KM(edge_index)` → `0.066` |
| [H3_EXACT_EDGE_LENGTH_M](/tidb-cloud-lake/sql/h3-exact-edge-length-m.md) | 正確なエッジ長をメートルで返します | `H3_EXACT_EDGE_LENGTH_M(edge_index)` → `66.12` |
| [H3_EXACT_EDGE_LENGTH_RADS](/tidb-cloud-lake/sql/h3-exact-edge-length-rads.md) | 正確なエッジ長をラジアンで返します | `H3_EXACT_EDGE_LENGTH_RADS(edge_index)` → `0.00001` |
| [H3_EDGE_ANGLE](/tidb-cloud-lake/sql/h3-edge-angle.md) | 2 つのエッジ間の角度をラジアンで返します | `H3_EDGE_ANGLE(edge1, edge2)` → `1.047` |