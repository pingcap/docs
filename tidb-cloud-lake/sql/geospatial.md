---
title: Geospatial
summary: "{{{ .lake }}} は 2 つのデータ型を通じて空間データを格納します。"
---

# Geospatial

{{{ .lake }}} は、2 つのデータ型を通じて空間データを格納します。

- `GEOMETRY` は平面型（デフォルト SRID は 0、または任意に割り当てた SRID）で、ローカルまたは投影座標系のワークロードに適しています。
- `GEOGRAPHY` は球面型（WGS 84、SRID 4326）で、グローバルなワークロード向けに緯度/経度の検証を行います。

どちらの型も、座標を EWKB 内で IEEE 754 `Float64` 値として永続化し、一般的なすべてのジオメトリ（Point から GeometryCollection まで）をサポートし、WKT/WKB/GeoJSON を出力でき、`ST_TRANSFORM` などの関数で再投影できます。

## データ型 {#data-types}

### GEOMETRY {#geometry}

- デカルト座標を使用し、平面計算で十分なキャンパス、市区町村、都道府県規模のデータに最適です。
- デフォルトの SRID は 0 です。カラム作成時またはデータ書き込み時に別の SRID を設定できます。
- ほとんどの空間演算子で利用でき、下流の利用者向けに `ST_TRANSFORM` で再投影できます。

### GEOGRAPHY {#geography}

- WGS 84（SRID 4326）上の経度/緯度ペアを格納します。[-180°, 180°] / [-90°, 90°] の範囲外の値は拒否されます。
- 楕円体の数式が必要な大陸規模または全球規模の距離/面積計算に推奨されます。
- 平面アルゴリズムが必要な場合は GEOMETRY に変換できます。

| 機能 | GEOMETRY | GEOGRAPHY |
| :--- | :--- | :--- |
| **座標系** | Cartesian（平面） | Ellipsoidal（球面） |
| **SRID** | 0（デフォルト）または Custom | 4326（WGS 84）のみ |
| **X / Y の解釈** | 平面上の X, Y | 球面上の Longitude, Latitude |
| **辺の解釈** | 平面上の直線 | 大円弧（球面上の最短経路） |
| **主なユースケース** | ローカル / 投影データ（例: 都市、建物） | グローバルデータ（例: GPS 軌跡、航路） |

## 精度と座標制御 {#precision-and-coordinate-control}

- **全体で倍精度**: `ST_MAKEPOINT` や `ST_GEOMETRYFROMEWKT` などの関数は `Float64` 値を取り込み、EWKB に永続化するため、座標は元の桁数を保持します。
- **SRID の動作**: GEOMETRY は割り当てた SRID（デフォルトは 0）を保持します。一方、GEOGRAPHY は SRID 4326 に固定されており、他の SRID は拒否されます。
- **座標の安全性**: GEOGRAPHY への入力は `check_point` を通過し、経度/緯度が [-180°, 180°] / [-90°, 90°] の範囲内に収まることを保証します。
- **投影**: `ST_TRANSFORM` は GEOMETRY の SRID を切り替え（例: 4326 → 3857）、または GEOGRAPHY データを下流処理向けの平面座標系に変換します。

## サポートされるオブジェクト型 {#supported-object-types}

| オブジェクト型 | 説明と例 | 精度に関する注意 |
| --- | --- | --- |
| Point | 単一の座標。例: `POINT(113.98765432109876 23.456789012345678)` | 各座標は `Float64` として格納され、約 15～16 桁の精度を保持します。 |
| LineString | 接続された経路。例: `LINESTRING(10 20, 30 40, 50 60)` | すべての頂点で同じ倍精度が使われるため、導出される長さは元の値に基づきます。 |
| Polygon | 閉じた領域。例: `POLYGON((10 20, 30 40, 50 60, 10 20))` | すべてのリングで `Float64` 頂点を共有するため、面積計算や包含判定において Polygon の辺が保持されます。 |
| MultiPoint | 複数の点。例: `MULTIPOINT((10 20), (30 40))` | 各構成 Point は、単独の Point と同じ倍精度ストレージを継承します。 |
| MultiLineString | 複数の経路。例: `MULTILINESTRING((10 20, 30 40), (50 60, 70 80))` | 頂点ごとに精度が維持されるため、長さや交差の計算を正確に行えます。 |
| MultiPolygon | 複数の領域。例: `MULTIPOLYGON(((10 20, 30 40, 50 60, 10 20)), ((15 25, 25 35, 35 45, 15 25)))` | 各 Polygon の座標は `Float64` のままなので、合計面積や重なりの計算でも完全な精度が保たれます。 |
| GeometryCollection | 混在したオブジェクト。例: `GEOMETRYCOLLECTION(POINT(10 20), LINESTRING(10 20, 30 40))` | 各メンバーは、ジオメトリ型に関係なく本来の倍精度座標を保持します。 |

## 出力形式 {#output-formats}

{{{ .lake }}} は空間値を EWKB として永続化しますが、複数の出力形式を提供します。`geometry_output_format` セッション設定（デフォルト: `WKT`）を設定するか、明示的な変換関数を呼び出してください。

- **WKT / EWKT** – テキスト表現。EWKT は SRID を先頭に付加します（例: `SRID=4326;POINT(-44.3 60.1)`）。
- **WKB / EWKB** – コンパクトなバイナリ形式で、他の GIS ランタイムとの相互運用に便利です。
- **GeoJSON** – Web マップや API 向けの JSON 表現です。

```sql
SET geometry_output_format = 'GeoJSON';
SELECT ST_ASWKB(geo), ST_ASEWKT(geo), ST_ASGEOJSON(geo) FROM ...;
```

## 関数 {#functions}

空間関数の一覧は次を参照してください。

- [Geospatial Functions](/tidb-cloud-lake/sql/geospatial-functions.md)

## 例 {#examples}

以下の各例では、1 つのオブジェクト型、その解決するシナリオ、それを生成する SQL、およびサンプル結果テーブルを示します。`CAST('…' AS GEOMETRY)` はインラインの WKT リテラルを解析するため、テーブルを作成しなくても試すことができます。

### Point — 単一のセンサー位置を特定する {#point-pinpoint-a-single-sensor}

*シナリオ*: IoT デバイスが生成した正確な緯度/経度を格納し、GeoJSON と数値座標の両方を公開します。

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

### LineString — ルートを表現する {#linestring-describe-a-route}

*シナリオ*: 単純な走行ルートを記録し、その長さを座標単位で測定します。

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

### Polygon — 領域またはジオフェンスを表す {#polygon-capture-an-area-or-geofence}

*シナリオ*: 施設の矩形ジオフェンスを定義し、SRID 情報付きで読み戻して、その面積を計算します。

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

### MultiPoint — 複数の地点をまとめて扱う {#multipoint-tag-multiple-sites-together}

*シナリオ*: 3 つのキオスクの座標をまとめて保持し、GeoJSON ペイロードと合計数の両方を報告します。

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

### MultiLineString — 平行な線を表現する {#multilinestring-represent-parallel-lines}

*シナリオ*: 2 本の平行な道路区間をグループ化し、WKT として読み戻し、`ST_NUMPOINTS` で頂点の総数を数えます。

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

### MultiPolygon — 離れた区域をカバーする {#multipolygon-cover-disjoint-districts}

*シナリオ*: 分離した 2 つのサービス区域を表現し、合計面積を計算します。

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

### GeometryCollection — 異種の図形を混在させる {#geometrycollection-mix-heterogenous-shapes}

*シナリオ*: ランドマークのマーカーとそれに接続する経路をまとめて保持し、混在した GeoJSON と最大次元を公開します。

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