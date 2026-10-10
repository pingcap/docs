---
title: ST_GEOHASH
summary: GEOMETRY または GEOGRAPHY 値の geohash 文字列を返し、結果の粒度を制御するためのオプションの精度をサポートします。
---

# ST_GEOHASH

GEOMETRY または GEOGRAPHY オブジェクトの [geohash](https://en.wikipedia.org/wiki/Geohash) を返します。geohash は、世界上のある位置を含む測地矩形を識別する短い base32 文字列です。オプションの precision 引数は、返される geohash の `precision` を指定します。たとえば、`precision` に 5 を渡すと、より短い geohash（5 文字長）が返され、精度は低くなります。

## 構文 {#syntax}

```sql
ST_GEOHASH(<geometry_or_geography> [, <precision>])
```

## 引数 {#arguments}

| 引数       | 説明                                                               |
|-----------------|---------------------------------------------------------------------------|
| `<geometry_or_geography>`    | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。                      |
| `[precision]` | オプション。返される geohash の精度を指定します。デフォルトは 12 です。 |

## 戻り値の型 {#return-type}

文字列。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

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

### GEOGRAPHY の例 {#geography-examples}

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