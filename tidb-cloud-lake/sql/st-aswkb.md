---
title: ST_ASWKB
summary: 将 GEOMETRY 或 GEOGRAPHY 对象转换为 WKB(well-known-binary) 格式表示。
---

# ST_ASWKB

将 GEOMETRY 或 GEOGRAPHY 对象转换为 [WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) 格式表示。

## 语法 {#syntax}

```sql
ST_ASWKB(<geometry_or_geography>)
```

## 别名 {#aliases}

- [ST_ASBINARY](/tidb-cloud-lake/sql/st-asbinary.md)

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
  ST_ASWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_wkb;

┌────────────────────────────────────────────────────────────────────────────────────┐
│                                    pipeline_wkb                                    │
├────────────────────────────────────────────────────────────────────────────────────┤
│ 01020000000200000000000000006A18410000000060E3564100000000A07918410000000024ED5641 │
└────────────────────────────────────────────────────────────────────────────────────┘

SELECT
  ST_ASBINARY(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkb;

┌────────────────────────────────────────────┐
│                pipeline_wkb                │
├────────────────────────────────────────────┤
│ 01010000006666666666965EC06666666666C64240 │
└────────────────────────────────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_ASWKB(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_wkb;

╭────────────────────────────────────────────╮
│                pipeline_wkb                │
├────────────────────────────────────────────┤
│ 01010000006666666666965EC06666666666C64240 │
╰────────────────────────────────────────────╯
```