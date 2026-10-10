---
title: ST_ASGEOJSON
summary: GEOMETRY または GEOGRAPHY オブジェクトを GeoJSON 表現に変換します。
---

# ST_ASGEOJSON

GEOMETRY または GEOGRAPHY オブジェクトを [GeoJSON](https://geojson.org/) 表現に変換します。

## 構文 {#syntax}

```sql
ST_ASGEOJSON(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

Variant。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

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

### GEOGRAPHY の例 {#geography-examples}

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
╰────────────────────────────────────────────────╯
```