---
title: ST_MAKELINE
summary: 入力された 2 つの GEOMETRY または GEOGRAPHY オブジェクト内の点を結ぶ線を表す GEOMETRY または GEOGRAPHY オブジェクトを構築します。
---

# ST_MAKELINE

入力された 2 つの GEOMETRY または GEOGRAPHY オブジェクト内の点を結ぶ線を表す GEOMETRY または GEOGRAPHY オブジェクトを構築します。

## 構文 {#syntax}

```sql
ST_MAKELINE(<geometry_or_geography1>, <geometry_or_geography2>)
```

## エイリアス {#aliases}

- [ST_MAKE_LINE](/tidb-cloud-lake/sql/st-make-line.md)

## 引数 {#arguments}

| 引数     | 説明                                                                                                 |
|---------------|-------------------------------------------------------------------------------------------------------------|
| `<geometry_or_geography1>` | 接続する点を含む GEOMETRY または GEOGRAPHY オブジェクトです。このオブジェクトは Point、MultiPoint、または LineString である必要があります。 |
| `<geometry_or_geography2>` | 接続する点を含む GEOMETRY または GEOGRAPHY オブジェクトです。このオブジェクトは Point、MultiPoint、または LineString である必要があります。 |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_MAKELINE(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    ),
    ST_GEOMETRYFROMWKT(
      'POINT(-104.874173 56.714538)'
    )
  ) AS pipeline_line;

┌───────────────────────────────────────────────────────┐
│                     pipeline_line                     │
├───────────────────────────────────────────────────────┤
│ LINESTRING(-122.3061 37.554162,-104.874173 56.714538) │
└───────────────────────────────────────────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_MAKELINE(
    ST_GEOGFROMWKT(
      'POINT(-122.306100 37.554162)'
    ),
    ST_GEOGFROMWKT(
      'POINT(-104.874173 56.714538)'
    )
  ) AS pipeline_line;

╭───────────────────────────────────────────────────────╮
│                     pipeline_line                     │
├───────────────────────────────────────────────────────┤
│ LINESTRING(-122.3061 37.554162,-104.874173 56.714538) │
╰───────────────────────────────────────────────────────╯
```