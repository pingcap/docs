---
title: ST_DIMENSION
summary: 返回几何对象的维度。GEOMETRY 或 GEOGRAPHY 对象的维度如下。
---

# ST_DIMENSION

返回几何对象的维度。GEOMETRY 或 GEOGRAPHY 对象的维度如下：

| 地理空间对象类型 | 维度 |
|------------------------------|------------|
| 点 / 多点           | 0          |
| 线串 / 多线串 | 1          |
| 多边形 / 多多边形       | 2          |

## 语法 {#syntax}

```sql
ST_DIMENSION(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数    | 描述                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

UInt8。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  0 │
└────────────────────┘

SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(-124.20 42.00, -120.01 41.99)'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  1 │
└────────────────────┘

SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'POLYGON((-124.20 42.00, -120.01 41.99, -121.1 42.01, -124.20 42.00))'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  2 │
└────────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_DIMENSION(
    ST_GEOGFROMWKT(
      'LINESTRING(-124.20 42.00, -120.01 41.99)'
    )
  ) AS pipeline_dimension;

╭────────────────────╮
│ pipeline_dimension │
├────────────────────┤
│                  1 │
╰────────────────────╯
```