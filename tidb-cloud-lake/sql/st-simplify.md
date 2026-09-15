---
title: ST_SIMPLIFY
summary: 通过移除到结果边的距离在指定容差范围内的顶点，返回 GEOMETRY 对象的简化版本。使用 Ramer-Douglas-Peucker 算法。
---

# ST_SIMPLIFY

通过移除到结果边的距离在指定容差范围内的顶点，返回 GEOMETRY 对象的简化版本。使用 Ramer-Douglas-Peucker 算法。

## 语法 {#syntax}

```sql
ST_SIMPLIFY(<geometry>, <tolerance>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|---------------|-----------------------------------------------------------------------------|
| `<geometry>`  | 一个 GEOMETRY 表达式。适用于 LineString、MultiLineString、Polygon 和 MultiPolygon。对 Point 或 MultiPoint 无影响。 |
| `<tolerance>` | 用于移除顶点的最大距离容差。 |

> **注意：**
>
> 不支持 GeometryCollection。

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('LINESTRING(0 0, 1 0, 1 1, 2 1)'), 0.5
  )
) AS simplified;

┌──────────────────────┐
│      simplified      │
├──────────────────────┤
│ LINESTRING(0 0,2 1)  │
└──────────────────────┘

SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('LINESTRING(1100 1100, 2500 2100, 3100 3100, 4900 1100, 3100 1900)'), 500
  )
) AS simplified;

┌──────────────────────────────────────────────────────┐
│                      simplified                      │
├──────────────────────────────────────────────────────┤
│ LINESTRING(1100 1100,3100 3100,4900 1100,3100 1900)  │
└──────────────────────────────────────────────────────┘

SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0.5 0.5, 0 1, 0 0))'), 0.6
  )
) AS simplified;

┌──────────────────────────────────┐
│            simplified            │
├──────────────────────────────────┤
│ POLYGON((0 0,1 0,1 1,0 1,0 0))  │
└──────────────────────────────────┘
```