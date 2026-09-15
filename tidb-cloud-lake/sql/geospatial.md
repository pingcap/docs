---
title: Geospatial
summary: "{{{ .lake }}} 通过两种数据类型存储空间数据。"
---

# Geospatial

{{{ .lake }}} 通过两种数据类型存储空间数据：

- `GEOMETRY` 是平面类型（默认 SRID 为 0，或使用你指定的任意 SRID），适用于本地/投影类工作负载。
- `GEOGRAPHY` 是球面类型（WGS 84，SRID 4326），并对全局工作负载中的经纬度进行校验。

这两种类型都以 EWKB 格式将坐标持久化为 IEEE 754 `Float64` 值，覆盖所有常见几何对象（从 Point 到 GeometryCollection），可输出 WKT/WKB/GeoJSON，并且可以通过 `ST_TRANSFORM` 等函数进行重投影。

## 数据类型 {#data-types}

### GEOMETRY {#geometry}

- 使用笛卡尔坐标，适合校园、城市或省级范围的数据，在这些场景中平面计算已足够。
- 默认 SRID 为 0；你可以在创建列或写入数据时设置其他 SRID。
- 适用于大多数空间操作符，并且可以通过 `ST_TRANSFORM` 进行重投影，以供下游使用方消费。

### GEOGRAPHY {#geography}

- 在 WGS 84（SRID 4326）上存储经度/纬度对；超出 [-180°, 180°] / [-90°, 90°] 范围的值会被拒绝。
- 推荐用于需要椭球公式的洲际或全球距离/面积计算。
- 当需要平面算法时，可以转换为 GEOMETRY。

| 特性 | GEOMETRY | GEOGRAPHY |
| :--- | :--- | :--- |
| **坐标系** | 笛卡尔（平面） | 椭球（球面） |
| **SRID** | 0（默认）或自定义 | 仅 4326（WGS 84） |
| **X / Y 含义** | 平面上的 X、Y | 球面上的经度、纬度 |
| **边的解释** | 平面上的直线 | 大圆弧（球面上的最短路径） |
| **主要使用场景** | 本地 / 投影数据（例如城市、建筑） | 全局数据（例如 GPS 轨迹、航运路线） |

## 精度与坐标控制 {#precision-and-coordinate-control}

- **全程双精度**：`ST_MAKEPOINT` 和 `ST_GEOMETRYFROMEWKT` 等函数接收 `Float64` 值并以 EWKB 持久化，因此坐标会保留其原始有效数字。
- **SRID 行为**：GEOMETRY 保留你指定的任意 SRID（默认 0），而 GEOGRAPHY 固定为 SRID 4326，并拒绝其他 SRID。
- **坐标安全性**：GEOGRAPHY 输入会经过 `check_point`，确保经度/纬度保持在 [-180°, 180°] / [-90°, 90°] 范围内。
- **投影**：`ST_TRANSFORM` 可切换 GEOMETRY 的 SRID（例如 4326 → 3857），或将 GEOGRAPHY 数据转换为平面坐标系以供下游处理。

## 支持的对象类型 {#supported-object-types}

| 对象类型 | 描述与示例 | 精度说明 |
| --- | --- | --- |
| Point | 单个坐标，例如 `POINT(113.98765432109876 23.456789012345678)` | 每个坐标都以 `Float64` 存储，并保留约 15–16 位精度。 |
| LineString | 连续路径，例如 `LINESTRING(10 20, 30 40, 50 60)` | 每个顶点都使用相同的双精度，因此派生长度依赖原始值。 |
| Polygon | 封闭区域，例如 `POLYGON((10 20, 30 40, 50 60, 10 20))` | 所有环共享 `Float64` 顶点，从而在面积/包含关系测试中保留多边形边界。 |
| MultiPoint | 多个点，例如 `MULTIPOINT((10 20), (30 40))` | 每个成员点都继承与独立点相同的双精度存储方式。 |
| MultiLineString | 多条路径，例如 `MULTILINESTRING((10 20, 30 40), (50 60, 70 80))` | 每个顶点的精度都会保留，从而确保长度或相交计算的准确性。 |
| MultiPolygon | 多个区域，例如 `MULTIPOLYGON(((10 20, 30 40, 50 60, 10 20)), ((15 25, 25 35, 35 45, 15 25)))` | 每个多边形的坐标都保持为 `Float64`，因此组合面积/重叠计算可保留完整精度。 |
| GeometryCollection | 混合对象，例如 `GEOMETRYCOLLECTION(POINT(10 20), LINESTRING(10 20, 30 40))` | 无论几何类型如何，各成员都保留其原生双精度坐标。 |

## 输出格式 {#output-formats}

{{{ .lake }}} 以 EWKB 持久化空间值，但提供多种输出格式。你可以设置 `geometry_output_format` 会话参数（默认值：`WKT`），或调用显式转换函数：

- **WKT / EWKT** – 文本表示；EWKT 会带上 SRID 前缀（例如 `SRID=4326;POINT(-44.3 60.1)`）。
- **WKB / EWKB** – 紧凑的二进制格式，便于与其他 GIS 运行时互操作。
- **GeoJSON** – 用于 Web 地图和 API 的 JSON 表示。

```sql
SET geometry_output_format = 'GeoJSON';
SELECT ST_ASWKB(geo), ST_ASEWKT(geo), ST_ASGEOJSON(geo) FROM ...;
```

## 函数 {#functions}

可在此查看已编目的空间函数列表：

- [Geospatial Functions](/tidb-cloud-lake/sql/geospatial-functions.md)

## 示例 {#examples}

下面的每个示例都突出展示一种对象类型、它解决的场景、生成它的 SQL，以及一个示例结果表。`CAST('…' AS GEOMETRY)` 会解析内联 WKT 字面量，因此你无需创建表即可进行实验。

### Point — 精确定位单个传感器 {#point-pinpoint-a-single-sensor}

*场景*：存储 IoT 设备产生的精确经纬度，并同时输出 GeoJSON 和数值坐标。

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

### LineString — 描述一条路线 {#linestring-describe-a-route}

*场景*：记录一条简单的驾驶路线，并以坐标单位测量其长度。

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

### Polygon — 表示区域或地理围栏 {#polygon-capture-an-area-or-geofence}

*场景*：为某设施定义一个矩形地理围栏，带 SRID 信息读回，并计算其面积。

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

### MultiPoint — 将多个站点归为一组 {#multipoint-tag-multiple-sites-together}

*场景*：将三个服务点的坐标一起保存，并输出 GeoJSON 载荷和总数量。

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

### MultiLineString — 表示平行线段 {#multilinestring-represent-parallel-lines}

*场景*：将两条平行道路分段归为一组，以 WKT 读回，并使用 `ST_NUMPOINTS` 统计总顶点数。

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

### MultiPolygon — 覆盖不相连的区域 {#multipolygon-cover-disjoint-districts}

*场景*：表示两个彼此分离的服务区域，并计算其总面积。

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

### GeometryCollection — 混合异构形状 {#geometrycollection-mix-heterogenous-shapes}

*场景*：将地标标记及其连接路径一起保存，并展示混合的 GeoJSON 以及最大维度。

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