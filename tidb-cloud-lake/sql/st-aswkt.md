---
title: ST_ASWKT
summary: GEOMETRY または GEOGRAPHY オブジェクトを WKT(well-known-text) 形式の表現に変換します。
---

# ST_ASWKT

GEOMETRY または GEOGRAPHY オブジェクトを [WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) 形式の表現に変換します。

## 構文 {#syntax}

```sql
ST_ASWKT(<geometry_or_geography>)
```

## エイリアス {#aliases}

- [ST_ASTEXT](/tidb-cloud-lake/sql/st-astext.md)

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
  ST_ASWKT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_wkt;

┌───────────────────────────────────────────┐
│                pipeline_wkt               │
├───────────────────────────────────────────┤
│ LINESTRING(400000 6000000,401000 6010000) │
└───────────────────────────────────────────┘

SELECT
  ST_ASTEXT(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkt;

┌──────────────────────┐
│     pipeline_wkt     │
├──────────────────────┤
│ POINT(-122.35 37.55) │
└──────────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_ASWKT(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkt;

╭──────────────────────╮
│     pipeline_wkt     │
├──────────────────────┤
│ POINT(-122.35 37.55) │
╰──────────────────────╯
```