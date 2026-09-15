---
title: ST_GEOHASH
summary: 返回 GEOMETRY 或 GEOGRAPHY 值的 geohash 字符串，并支持可选的精度参数来控制结果粒度。
---

# ST_GEOHASH

返回 GEOMETRY 或 GEOGRAPHY 对象的 [geohash](https://en.wikipedia.org/wiki/Geohash)。geohash 是一个简短的 base32 字符串，用于标识世界上包含某个位置的测地矩形。可选的 precision 参数用于指定返回的 geohash 的 `precision`。例如，将 5 作为 `precision` 传入时，会返回一个更短的 geohash（长度为 5 个字符），其精度也更低。

## 语法 {#syntax}

```sql
ST_GEOHASH(<geometry_or_geography> [, <precision>])
```

## 参数 {#arguments}

| 参数       | 描述                                                               |
|-----------------|---------------------------------------------------------------------------|
| `<geometry_or_geography>`    | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。                      |
| `[precision]` | 可选。指定返回的 geohash 的精度，默认为 12。 |

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_GEOHASH(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    )
  ) AS pipeline_geohash;

┌──────────────────┐
│ pipeline_geohash │
├──────────────────┤
│ 9q9j8ue2v71y     │
└──────────────────┘

SELECT
  ST_GEOHASH(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    ),
    5
  ) AS pipeline_geohash;

┌──────────────────┐
│ pipeline_geohash │
├──────────────────┤
│ 9q8vx            │
└──────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_GEOHASH(
    ST_GEOGFROMWKT(
      'POINT(-122.306100 37.554162)'
    )
  ) AS pipeline_geohash;

┌──────────────────┐
│ pipeline_geohash │
├──────────────────┤
│ 9q9j8ue2v71y     │
└──────────────────┘
```