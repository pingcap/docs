---
title: ST_ASEWKT
summary: 将 GEOMETRY 或 GEOGRAPHY 对象转换为 EWKT(extended well-known-text) 格式表示。
---

# ST_ASEWKT

将 GEOMETRY 或 GEOGRAPHY 对象转换为 [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) 格式表示。

## 语法 {#syntax}

```sql
ST_ASEWKT(<geometry_or_geography>)
```

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

### GEOGRAPHY 示例 {#geography-examples}

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