---
title: ST_ASEWKT
summary: GEOMETRY または GEOGRAPHY オブジェクトを EWKT(extended well-known-text) 形式の表現に変換します。
---

# ST_ASEWKT

GEOMETRY または GEOGRAPHY オブジェクトを [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) 形式の表現に変換します。

## 構文 {#syntax}

```sql
ST_ASEWKT(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

文字列。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_ASEWKT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_ewkt;

┌─────────────────────────────────────────────────────┐
│                    pipeline_ewkt                    │
├─────────────────────────────────────────────────────┤
│ SRID=4326;LINESTRING(400000 6000000,401000 6010000) │
└─────────────────────────────────────────────────────┘

SELECT
  ST_ASEWKT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkt;

┌────────────────────────────────┐
│          pipeline_ewkt         │
├────────────────────────────────┤
│ SRID=4326;POINT(-122.35 37.55) │
└────────────────────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_ASEWKT(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkt;

╭────────────────────────────────╮
│          pipeline_ewkt         │
├────────────────────────────────┤
│ SRID=4326;POINT(-122.35 37.55) │
╰────────────────────────────────╯
```