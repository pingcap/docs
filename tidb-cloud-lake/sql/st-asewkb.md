---
title: ST_ASEWKB
summary: 将 GEOMETRY 或 GEOGRAPHY 对象转换为 EWKB(extended well-known-binary) 格式表示。
---

# ST_ASEWKB

将 GEOMETRY 或 GEOGRAPHY 对象转换为 [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) 格式表示。

## 语法 {#syntax}

```sql
ST_ASEWKB(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数    | 描述                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

Binary。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_ASEWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_ewkb;

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        pipeline_ewkb                                       │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ 0102000020E61000000200000000000000006A18410000000060E3564100000000A07918410000000024ED5641 │
└────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT
  ST_ASEWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkb;

┌────────────────────────────────────────────────────┐
│                    pipeline_ewkb                   │
├────────────────────────────────────────────────────┤
│ 0101000020E61000006666666666965EC06666666666C64240 │
└────────────────────────────────────────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_ASEWKB(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkb;

╭────────────────────────────────────────────────────╮
│                    pipeline_ewkb                   │
├────────────────────────────────────────────────────┤
│ 0101000020E61000006666666666965EC06666666666C64240 │
╰────────────────────────────────────────────────────╯
```