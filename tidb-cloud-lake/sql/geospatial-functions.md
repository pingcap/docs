---
title: Geospatial Functions
summary: "{{{ .lake }}} 提供两组互补的地理空间能力：用于构建和分析形状的 PostGIS 风格几何函数，以及用于全局六边形索引的 H3 工具。下表按任务对这些函数进行了分组，便于你快速找到合适的工具，布局方式类似于 Snowflake 文档。"
---

# Geospatial Functions

{{{ .lake }}} 提供两组互补的地理空间能力：用于构建和分析形状的 PostGIS 风格几何函数，以及用于全局六边形索引的 H3 工具。下表按任务对这些函数进行了分组，便于你快速找到合适的工具，布局方式类似于 Snowflake 文档。

## 构造函数 {#constructors}

| 函数 | 描述 | 说明 | 示例 |
|----------|-------------|------|---------|
| [ST_MAKEGEOMPOINT](/tidb-cloud-lake/sql/st-makegeompoint.md) / [ST_GEOM_POINT](/tidb-cloud-lake/sql/st-geom-point.md) | 构造 Point 几何对象 | 仅 GEOGRAPHY | `ST_MAKEGEOMPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKEPOINT](/tidb-cloud-lake/sql/st-makepoint.md) / [ST_POINT](/tidb-cloud-lake/sql/st-point.md) | 构造 Point geography 对象 | 仅 GEOGRAPHY | `ST_MAKEPOINT(-122.35, 37.55)` → `POINT(-122.35 37.55)` |
| [ST_MAKELINE](/tidb-cloud-lake/sql/st-makeline.md) / [ST_MAKE_LINE](/tidb-cloud-lake/sql/st-make-line.md) | 由点创建 LineString |  | `ST_MAKELINE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `LINESTRING(-122.35 37.55, -122.40 37.60)` |
| [ST_MAKEPOLYGON](/tidb-cloud-lake/sql/st-makepolygon.md) | 由闭合的 LineString 创建 Polygon |  | `ST_MAKEPOLYGON(ST_MAKELINE(...))` → `POLYGON(...)` |
| [ST_POLYGON](/tidb-cloud-lake/sql/st-polygon.md) | 由坐标环创建 Polygon | 仅 GEOGRAPHY | `ST_POLYGON(...)` → `POLYGON(...)` |

## 转换 {#conversion}

| 函数 | 描述 | 说明 | 示例 |
|----------|-------------|------|---------|
| [ST_GEOMETRYFROMTEXT](/tidb-cloud-lake/sql/st-geometryfromtext.md) / [ST_GEOMFROMTEXT](/tidb-cloud-lake/sql/st-geomfromtext.md) | 将 WKT 转换为 geometry | 仅 GEOGRAPHY | `ST_GEOMETRYFROMTEXT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMWKB](/tidb-cloud-lake/sql/st-geometryfromwkb.md) / [ST_GEOMFROMWKB](/tidb-cloud-lake/sql/st-geomfromwkb.md) | 将 WKB 转换为 geometry | 仅 GEOGRAPHY | `ST_GEOMETRYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMETRYFROMEWKT](/tidb-cloud-lake/sql/st-geometryfromewkt.md) / [ST_GEOMFROMEWKT](/tidb-cloud-lake/sql/st-geomfromewkt.md) | 将 EWKT 转换为 geometry | 仅 GEOGRAPHY | `ST_GEOMETRYFROMEWKT('SRID=4326;POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOMETRYFROMEWKB](/tidb-cloud-lake/sql/st-geometryfromewkb.md) / [ST_GEOMFROMEWKB](/tidb-cloud-lake/sql/st-geomfromewkb.md) | 将 EWKB 转换为 geometry | 仅 GEOGRAPHY | `ST_GEOMETRYFROMEWKB(...)` → `POINT(...)` |
| [ST_GEOGRAPHYFROMWKT](/tidb-cloud-lake/sql/st-geographyfromwkt.md) / [ST_GEOGFROMWKT](/tidb-cloud-lake/sql/st-geogfromwkt.md) | 将 WKT/EWKT 转换为 geography | 仅 GEOGRAPHY | `ST_GEOGRAPHYFROMWKT('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [ST_GEOGRAPHYFROMWKB](/tidb-cloud-lake/sql/st-geographyfromwkb.md) / [ST_GEOGFROMWKB](/tidb-cloud-lake/sql/st-geogfromwkb.md) | 将 WKB/EWKB 转换为 geography | 仅 GEOGRAPHY | `ST_GEOGRAPHYFROMWKB(...)` → `POINT(...)` |
| [ST_GEOMFROMGEOHASH](/tidb-cloud-lake/sql/st-geomfromgeohash.md) | 将 GeoHash 转换为 geometry | 仅 GEOGRAPHY | `ST_GEOMFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOMPOINTFROMGEOHASH](/tidb-cloud-lake/sql/st-geompointfromgeohash.md) | 将 GeoHash 转换为 Point 几何对象 | 仅 GEOGRAPHY | `ST_GEOMPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [ST_GEOGFROMGEOHASH](/tidb-cloud-lake/sql/st-geogfromgeohash.md) | 将 GeoHash 转换为 geography 多边形 | 仅 GEOGRAPHY | `ST_GEOGFROMGEOHASH('9q8yyk8')` → `POLYGON(...)` |
| [ST_GEOGPOINTFROMGEOHASH](/tidb-cloud-lake/sql/st-geogpointfromgeohash.md) | 将 GeoHash 转换为 geography 点 | 仅 GEOGRAPHY | `ST_GEOGPOINTFROMGEOHASH('9q8yyk8')` → `POINT(...)` |
| [TO_GEOMETRY](/tidb-cloud-lake/sql/geometry.md) | 将多种格式解析为 geometry | 仅 GEOGRAPHY | `TO_GEOMETRY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |
| [TO_GEOGRAPHY](/tidb-cloud-lake/sql/to-geography.md) / [TRY_TO_GEOGRAPHY](/tidb-cloud-lake/sql/to-geography.md) | 将多种格式解析为 geography | 仅 GEOGRAPHY | `TO_GEOGRAPHY('POINT(-122.35 37.55)')` → `POINT(-122.35 37.55)` |

## 输出 {#output}

| 函数 | 描述 | 说明 | 示例 |
|----------|-------------|------|---------|
| [ST_ASTEXT](/tidb-cloud-lake/sql/st-astext.md) | 将 geometry 转换为 WKT |  | `ST_ASTEXT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASWKT](/tidb-cloud-lake/sql/st-aswkt.md) | 将 geometry 转换为 WKT |  | `ST_ASWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |
| [ST_ASBINARY](/tidb-cloud-lake/sql/st-asbinary.md) / [ST_ASWKB](/tidb-cloud-lake/sql/st-aswkb.md) | 将 geometry 转换为 WKB |  | `ST_ASBINARY(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `WKB representation` |
| [ST_ASEWKT](/tidb-cloud-lake/sql/st-asewkt.md) | 将 geometry 转换为 EWKT |  | `ST_ASEWKT(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'SRID=4326;POINT(-122.35 37.55)'` |
| [ST_ASEWKB](/tidb-cloud-lake/sql/st-asewkb.md) | 将 geometry 转换为 EWKB |  | `ST_ASEWKB(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `EWKB representation` |
| [ST_ASGEOJSON](/tidb-cloud-lake/sql/st-asgeojson.md) | 将 geometry 转换为 GeoJSON |  | `ST_ASGEOJSON(ST_MAKEGEOMPOINT(-122.35, 37.55))` → '{"type":"Point","coordinates":[-122.35,37.55]}' |
| [ST_GEOHASH](/tidb-cloud-lake/sql/st-geohash.md) | 将 geometry 转换为 GeoHash |  | `ST_GEOHASH(ST_MAKEGEOMPOINT(-122.35, 37.55), 7)` → `'9q8yyk8'` |
| [TO_STRING](/tidb-cloud-lake/sql/string.md) | 将 geometry 转换为字符串 |  | `TO_STRING(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `'POINT(-122.35 37.55)'` |

## 访问器和属性 {#accessors-properties}

| 函数 | 描述 | 说明 | 示例 |
|----------|-------------|------|---------|
| [ST_DIMENSION](/tidb-cloud-lake/sql/st-dimension.md) | 返回拓扑维度 |  | `ST_DIMENSION(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `0` |
| [ST_CENTROID](/tidb-cloud-lake/sql/st-centroid.md) | 返回 geometry 的质心 | 仅 GEOMETRY | `ST_CENTROID(TO_GEOMETRY('LINESTRING(0 0, 2 0)'))` → `POINT(1 0)` |
| [ST_ENVELOPE](/tidb-cloud-lake/sql/st-envelope.md) | 返回最小外接矩形 | 仅 GEOMETRY | `ST_ENVELOPE(TO_GEOMETRY('LINESTRING(0 0, 2 3)'))` → `POLYGON((0 0,2 0,2 3,0 3,0 0))` |
| [ST_SRID](/tidb-cloud-lake/sql/st-srid.md) | 返回 geometry 的 SRID |  | `ST_SRID(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `4326` |
| [ST_POINTN](/tidb-cloud-lake/sql/st-pointn.md) | 返回 LineString 中指定位置的点 |  | `ST_POINTN(ST_MAKELINE(...), 1)` → `POINT(-122.35 37.55)` |
| [ST_STARTPOINT](/tidb-cloud-lake/sql/st-startpoint.md) | 返回 LineString 中的第一个点 |  | `ST_STARTPOINT(ST_MAKELINE(...))` → `POINT(-122.35 37.55)` |
| [ST_ENDPOINT](/tidb-cloud-lake/sql/st-endpoint.md) | 返回 LineString 中的最后一个点 |  | `ST_ENDPOINT(ST_MAKELINE(...))` → `POINT(-122.40 37.60)` |
| [ST_X](/tidb-cloud-lake/sql/st-x.md) / [ST_Y](/tidb-cloud-lake/sql/st-y.md) | 返回 Point 的 X 或 Y 坐标 |  | `ST_X(ST_MAKEGEOMPOINT(-122.35, 37.55))` → `-122.35` |
| [ST_XMIN](/tidb-cloud-lake/sql/st-xmin.md) / [ST_XMAX](/tidb-cloud-lake/sql/st-xmax.md) | 返回最小/最大 X 坐标 |  | `ST_XMIN(ST_MAKELINE(...))` → `-122.40` |
| [ST_YMIN](/tidb-cloud-lake/sql/st-ymin.md) / [ST_YMAX](/tidb-cloud-lake/sql/st-ymax.md) | 返回最小/最大 Y 坐标 |  | `ST_YMAX(ST_MAKELINE(...))` → `37.60` |

## 关系与度量 {#relationship-and-measurement}

| 函数 | 描述 | 说明 | 示例 |
|----------|-------------|------|---------|
| [HAVERSINE](/tidb-cloud-lake/sql/haversine.md) | 计算坐标之间的大圆距离 |  | `HAVERSINE(37.55, -122.35, 37.60, -122.40)` → `6.12` |
| [ST_AREA](/tidb-cloud-lake/sql/st-area.md) | 测量 geometry 或 geography 对象的面积 |  | `ST_AREA(TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'))` → `1.0` |
| [ST_CONTAINS](/tidb-cloud-lake/sql/st-contains.md) | 测试一个 geometry 是否包含另一个 geometry | 仅 GEOMETRY | `ST_CONTAINS(ST_MAKEPOLYGON(...), ST_MAKEGEOMPOINT(...))` → `TRUE` |
| [ST_CONVEXHULL](/tidb-cloud-lake/sql/st-convexhull.md) | 计算 geometry 的凸包 | 仅 GEOMETRY | `ST_CONVEXHULL(TO_GEOMETRY('POLYGON((0 0,2 0,2 2,0 2,0 0))'))` → `POLYGON((0 0,2 0,2 2,0 2,0 0))` |
| [ST_NPOINTS](/tidb-cloud-lake/sql/st-npoints.md) | 统计 geometry 中的点数 |  | `ST_NPOINTS(ST_MAKELINE(...))` → `2` |
| [ST_NUMPOINTS](/tidb-cloud-lake/sql/st-numpoints.md) | 统计 geometry 中的点数 | 仅 GEOMETRY | `ST_NUMPOINTS(ST_MAKELINE(...))` → `2` |
| [ST_INTERSECTS](/tidb-cloud-lake/sql/st-intersects.md) | 测试两个 geometry 是否相交 | 仅 GEOMETRY | `ST_INTERSECTS(TO_GEOMETRY('LINESTRING(0 0, 2 2)'), TO_GEOMETRY('LINESTRING(0 2, 2 0)'))` → `TRUE` |
| [ST_DISJOINT](/tidb-cloud-lake/sql/st-disjoint.md) | 测试两个 geometry 是否不相交 | 仅 GEOMETRY | `ST_DISJOINT(TO_GEOMETRY('POINT(3 3)'), TO_GEOMETRY('POLYGON((0 0,2 0,2 2,0 2,0 0))'))` → `TRUE` |
| [ST_WITHIN](/tidb-cloud-lake/sql/st-within.md) | 测试一个 geometry 是否位于另一个 geometry 内部 | 仅 GEOMETRY | `ST_WITHIN(TO_GEOMETRY('POINT(1 1)'), TO_GEOMETRY('POLYGON((0 0,2 0,2 2,0 2,0 0))'))` → `TRUE` |
| [ST_EQUALS](/tidb-cloud-lake/sql/st-equals.md) | 测试两个 geometry 在空间上是否相等 | 仅 GEOMETRY | `ST_EQUALS(TO_GEOMETRY('POINT(1 1)'), TO_GEOMETRY('POINT(1 1)'))` → `TRUE` |
| [ST_LENGTH](/tidb-cloud-lake/sql/st-length.md) | 测量 LineString 的长度 |  | `ST_LENGTH(ST_MAKELINE(...))` → `5.57` |
| [ST_DISTANCE](/tidb-cloud-lake/sql/st-distance.md) | 测量 geometry 之间的距离 |  | `ST_DISTANCE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `5.57` |
| [ST_DWITHIN](/tidb-cloud-lake/sql/st-dwithin.md) | 测试两个 geometry 是否在给定距离内 | 仅 GEOMETRY | `ST_DWITHIN(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'), 1.5)` → `TRUE` |
| [ST_UNION](/tidb-cloud-lake/sql/st-union.md) | 返回两个输入合并后的 geometry | 仅 GEOMETRY | `ST_UNION(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'))` → `MULTIPOINT(0 0,1 1)` |
| [ST_INTERSECTION](/tidb-cloud-lake/sql/st-intersection.md) | 返回两个 geometry 的共享部分 | 仅 GEOMETRY | `ST_INTERSECTION(TO_GEOMETRY('LINESTRING(0 0, 1 1)'), TO_GEOMETRY('LINESTRING(0 0, 1 1)'))` → `LINESTRING(0 0,1 1)` |
| [ST_DIFFERENCE](/tidb-cloud-lake/sql/st-difference.md) | 返回第一个 geometry 中未被第二个覆盖的部分 | 仅 GEOMETRY | `ST_DIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'))` → `POINT(0 0)` |
| [ST_SYMDIFFERENCE](/tidb-cloud-lake/sql/st-symdifference.md) | 返回两个 geometry 中不重叠的部分 | 仅 GEOMETRY | `ST_SYMDIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'))` → `MULTIPOINT(0 0,1 1)` |

## 变换 {#transformation}

| 函数 | 描述 | 说明 | 示例 |
|----------|-------------|------|---------|
| [ST_HILBERT](/tidb-cloud-lake/sql/st-hilbert.md) | 将 geometry 或 geography 编码为 Hilbert 曲线索引 |  | `ST_HILBERT(TO_GEOMETRY('POINT(0.5 0.5)'), [0, 0, 1, 1])` → `715827882` |
| [ST_SETSRID](/tidb-cloud-lake/sql/st-setsrid.md) | 为 geometry 指定 SRID | 仅 GEOMETRY | `ST_SETSRID(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-122.35 37.55)` |
| [ST_TRANSFORM](/tidb-cloud-lake/sql/st-transform.md) | 将 geometry 转换到新的 SRID | 仅 GEOMETRY | `ST_TRANSFORM(ST_MAKEGEOMPOINT(-122.35, 37.55), 3857)` → `POINT(-13618288.8 4552395.0)` |

## 空间关系 {#spatial-relationships}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ST_CONTAINS](/tidb-cloud-lake/sql/st-contains.md) | 测试一个 geometry 是否包含另一个 geometry | `ST_CONTAINS(ST_MAKEPOLYGON(...), ST_MAKEGEOMPOINT(...))` → `TRUE` |
| [POINT_IN_POLYGON](/tidb-cloud-lake/sql/point-in-polygon.md) | 检查点是否位于多边形内部 | `POINT_IN_POLYGON([lon, lat], [[p1_lon, p1_lat], ...])` → `TRUE` |

## 距离与度量 {#distance-measurements}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ST_DISTANCE](/tidb-cloud-lake/sql/st-distance.md) | 测量几何图形之间的距离 | `ST_DISTANCE(ST_MAKEGEOMPOINT(-122.35, 37.55), ST_MAKEGEOMPOINT(-122.40, 37.60))` → `5.57` |
| [HAVERSINE](/tidb-cloud-lake/sql/haversine.md) | 计算坐标之间的大圆距离 | `HAVERSINE(37.55, -122.35, 37.60, -122.40)` → `6.12` |

## H3 索引与转换 {#h3-indexing-conversion}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [GEO_TO_H3](/tidb-cloud-lake/sql/geo-to-h3.md) | 将经度/纬度转换为 H3 索引 | `GEO_TO_H3(37.7950, 55.7129, 15)` → `644325524701193974` |
| [H3_TO_GEO](/tidb-cloud-lake/sql/h3-to-geo.md) | 将 H3 索引转换为经度/纬度 | `H3_TO_GEO(644325524701193974)` → `[37.7950, 55.7129]` |
| [H3_TO_STRING](/tidb-cloud-lake/sql/h3-to-string.md) | 将 H3 索引转换为其字符串形式 | `H3_TO_STRING(644325524701193974)` → `'8f2830828052d25'` |
| [STRING_TO_H3](/tidb-cloud-lake/sql/string-to-h3.md) | 将 H3 字符串转换为索引 | `STRING_TO_H3('8f2830828052d25')` → `644325524701193974` |
| [GEOHASH_ENCODE](/tidb-cloud-lake/sql/geohash-encode.md) | 将经度/纬度编码为 GeoHash | `GEOHASH_ENCODE(37.7950, 55.7129, 12)` → `'ucfv0nzpt3s7'` |
| [GEOHASH_DECODE](/tidb-cloud-lake/sql/geohash-decode.md) | 将 GeoHash 解码为经度/纬度 | `GEOHASH_DECODE('ucfv0nzpt3s7')` → `[37.7950, 55.7129]` |

## H3 单元属性 {#h3-cell-properties}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [H3_GET_RESOLUTION](/tidb-cloud-lake/sql/h3-get-resolution.md) | 返回 H3 索引的分辨率 | `H3_GET_RESOLUTION(644325524701193974)` → `15` |
| [H3_GET_BASE_CELL](/tidb-cloud-lake/sql/h3-get-base-cell.md) | 返回基础单元编号 | `H3_GET_BASE_CELL(644325524701193974)` → `14` |
| [H3_IS_VALID](/tidb-cloud-lake/sql/h3-is-valid.md) | 检查 H3 索引是否有效 | `H3_IS_VALID(644325524701193974)` → `TRUE` |
| [H3_IS_PENTAGON](/tidb-cloud-lake/sql/h3-is-pentagon.md) | 检查 H3 索引是否为五边形 | `H3_IS_PENTAGON(644325524701193974)` → `FALSE` |
| [H3_IS_RES_CLASS_III](/tidb-cloud-lake/sql/h3-is-res-class-iii.md) | 检查 H3 索引是否为 III 类 | `H3_IS_RES_CLASS_III(644325524701193974)` → `FALSE` |
| [H3_GET_FACES](/tidb-cloud-lake/sql/h3-get-faces.md) | 返回相交的二十面体面 | `H3_GET_FACES(644325524701193974)` → `[7]` |
| [H3_TO_PARENT](/tidb-cloud-lake/sql/h3-to-parent.md) | 返回较低分辨率下的父索引 | `H3_TO_PARENT(644325524701193974, 10)` → `622236721289822207` |
| [H3_TO_CHILDREN](/tidb-cloud-lake/sql/h3-to-children.md) | 返回较高分辨率下的子索引 | `H3_TO_CHILDREN(622236721289822207, 11)` → `[...]` |
| [H3_TO_CENTER_CHILD](/tidb-cloud-lake/sql/h3-to-center-child.md) | 返回指定分辨率下的中心子索引 | `H3_TO_CENTER_CHILD(622236721289822207, 11)` → `625561602857582591` |
| [H3_CELL_AREA_M2](/tidb-cloud-lake/sql/h3-cell-area-m2.md) | 返回单元面积（平方米） | `H3_CELL_AREA_M2(644325524701193974)` → `0.8953` |
| [H3_CELL_AREA_RADS2](/tidb-cloud-lake/sql/h3-cell-area-rads2.md) | 返回单元面积（平方弧度） | `H3_CELL_AREA_RADS2(644325524701193974)` → `2.2e-14` |
| [H3_HEX_AREA_KM2](/tidb-cloud-lake/sql/h3-hex-area-km2.md) | 返回平均六边形面积（km²） | `H3_HEX_AREA_KM2(10)` → `0.0152` |
| [H3_HEX_AREA_M2](/tidb-cloud-lake/sql/h3-hex-area-m2.md) | 返回平均六边形面积（m²） | `H3_HEX_AREA_M2(10)` → `15200` |
| [H3_TO_GEO_BOUNDARY](/tidb-cloud-lake/sql/h3-to-geo-boundary.md) | 返回单元边界 | `H3_TO_GEO_BOUNDARY(644325524701193974)` → `[[lon1,lat1], ...]` |
| [H3_NUM_HEXAGONS](/tidb-cloud-lake/sql/h3-num-hexagons.md) | 返回指定分辨率下的六边形数量 | `H3_NUM_HEXAGONS(2)` → `5882` |
| [GEO_DISTANCE](/tidb-cloud-lake/sql/geo-distance.md) | 使用 WGS84 返回近似距离（米） | `GEO_DISTANCE(0, 0, 0, 0)` → `0` |
| [GREAT_CIRCLE_DISTANCE](/tidb-cloud-lake/sql/great-circle-distance.md) | 返回大圆距离（米） | `GREAT_CIRCLE_DISTANCE(0, 0, 0, 0)` → `0` |
| [GREAT_CIRCLE_ANGLE](/tidb-cloud-lake/sql/great-circle-angle.md) | 返回大圆中心角（度） | `GREAT_CIRCLE_ANGLE(0, 0, 45, 0)` → `45` |
| [POINT_IN_POLYGON](/tidb-cloud-lake/sql/point-in-polygon.md) | 检查点是否位于多边形内部 | `POINT_IN_POLYGON([lon, lat], [[p1_lon, p1_lat], ...])` → `TRUE` |
| [POINT_IN_ELLIPSES](/tidb-cloud-lake/sql/point-in-ellipses.md) | 检查点是否位于任一椭圆内部 | `POINT_IN_ELLIPSES(10, 10, 10, 9.1, 1, 0.9999)` → `1` |

## H3 邻域 {#h3-neighborhoods}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [H3_DISTANCE](/tidb-cloud-lake/sql/h3-distance.md) | 返回两个索引之间的网格距离 | `H3_DISTANCE(599119489002373119, 599119491149856767)` → `1` |
| [H3_INDEXES_ARE_NEIGHBORS](/tidb-cloud-lake/sql/h3-indexes-are-neighbors.md) | 测试两个索引是否为邻居 | `H3_INDEXES_ARE_NEIGHBORS(599119489002373119, 599119491149856767)` → `TRUE` |
| [H3_K_RING](/tidb-cloud-lake/sql/h3-k-ring.md) | 返回距离不超过 k 的所有索引 | `H3_K_RING(599119489002373119, 1)` → `[599119489002373119, ...]` |
| [H3_HEX_RING](/tidb-cloud-lake/sql/h3-hex-ring.md) | 返回恰好距离 k 步的索引 | `H3_HEX_RING(599119489002373119, 1)` → `[599119491149856767, ...]` |
| [H3_LINE](/tidb-cloud-lake/sql/h3-line.md) | 返回路径上的索引 | `H3_LINE(from_h3, to_h3)` → `[from_h3, ..., to_h3]` |

## H3 边操作 {#h3-edge-operations}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [H3_GET_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-unidirectional-edge.md) | 返回两个相邻单元之间的边 | `H3_GET_UNIDIRECTIONAL_EDGE(from_h3, to_h3)` → `edge_index` |
| [H3_UNIDIRECTIONAL_EDGE_IS_VALID](/tidb-cloud-lake/sql/h3-unidirectional-edge-is-valid.md) | 检查边索引是否有效 | `H3_UNIDIRECTIONAL_EDGE_IS_VALID(edge_index)` → `TRUE` |
| [H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-origin-index-unidirectional-edge.md) | 从边返回起始单元 | `H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `from_h3` |
| [H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-destination-index-unidirectional-edge.md) | 从边返回目标单元 | `H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `to_h3` |
| [H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE](/tidb-cloud-lake/sql/h3-get-indexes-unidirectional-edge.md) | 返回一条边对应的两个单元 | `H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE(edge_index)` → `[from_h3, to_h3]` |
| [H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON](/tidb-cloud-lake/sql/h3-get-unidirectional-edges-hexagon.md) | 列出从某个单元出发的边 | `H3_GET_UNIDIRECTIONAL_EDGES_FROM_HEXAGON(h3_index)` → `[edge1, edge2, ...]` |
| [H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY](/tidb-cloud-lake/sql/h3-get-unidirectional-edge-boundary.md) | 返回边的边界 | `H3_GET_UNIDIRECTIONAL_EDGE_BOUNDARY(edge_index)` → `[[lon1,lat1], [lon2,lat2]]` |

## H3 度量与角度 {#h3-measurements-angles}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [H3_EDGE_LENGTH_KM](/tidb-cloud-lake/sql/h3-edge-length-km.md) | 返回平均边长（千米） | `H3_EDGE_LENGTH_KM(10)` → `0.065` |
| [H3_EDGE_LENGTH_M](/tidb-cloud-lake/sql/h3-edge-length-m.md) | 返回平均边长（米） | `H3_EDGE_LENGTH_M(10)` → `65.91` |
| [H3_EXACT_EDGE_LENGTH_KM](/tidb-cloud-lake/sql/h3-exact-edge-length-km.md) | 返回精确边长（千米） | `H3_EXACT_EDGE_LENGTH_KM(edge_index)` → `0.066` |
| [H3_EXACT_EDGE_LENGTH_M](/tidb-cloud-lake/sql/h3-exact-edge-length-m.md) | 返回精确边长（米） | `H3_EXACT_EDGE_LENGTH_M(edge_index)` → `66.12` |
| [H3_EXACT_EDGE_LENGTH_RADS](/tidb-cloud-lake/sql/h3-exact-edge-length-rads.md) | 返回精确边长（弧度） | `H3_EXACT_EDGE_LENGTH_RADS(edge_index)` → `0.00001` |
| [H3_EDGE_ANGLE](/tidb-cloud-lake/sql/h3-edge-angle.md) | 返回两条边之间的夹角（弧度） | `H3_EDGE_ANGLE(edge1, edge2)` → `1.047` |