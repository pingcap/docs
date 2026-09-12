---
title: ST_ASWKT
summary: 将 GEOMETRY 或 GEOGRAPHY 对象转换为 WKT(well-known-text) 格式表示。
---

# ST_ASWKT

将 GEOMETRY 或 GEOGRAPHY 对象转换为 [WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) 格式表示。

## 语法 {#syntax}

```sql
ST_ASWKT(<geometry_or_geography>)
```

## 别名 {#aliases}

- [ST_ASTEXT](/tidb-cloud-lake/sql/st-astext.md)

## 参数 {#arguments}

| 参数    | 描述                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

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

### GEOGRAPHY 示例 {#geography-examples}

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