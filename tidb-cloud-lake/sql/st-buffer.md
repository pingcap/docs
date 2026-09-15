---
title: ST_BUFFER
summary: 返回一个 GEOMETRY，表示与输入几何对象距离小于或等于指定距离的所有点。结果为 MultiPolygon 或 NULL。
---

# ST_BUFFER

返回一个 GEOMETRY，表示与输入几何对象距离小于或等于指定距离的所有点。结果为 MultiPolygon 或 NULL。

## 语法 {#syntax}

```sql
ST_BUFFER(<geometry>, <distance>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry>` | 一个 GEOMETRY 表达式。不支持 GeometryCollection。 |
| `<distance>` | 缓冲距离。单位与输入几何对象的坐标系一致。 |

> **注意：**
>
> - 对于 Point、MultiPoint、LineString 和 MultiLineString：使用 distance 的绝对值（负值与正值行为相同）。
> - 对于 Polygon 和 MultiPolygon：正 distance 表示膨胀，负 distance 表示收缩。
> - 当结果为空时返回 NULL（例如，Point 的 distance 为 0，或 Polygon 收缩后面积降为 0 以下）。
> - 对于 distance 为 0 的 Polygon：返回包装为 MultiPolygon 的该 Polygon。
> - 输出中会保留 SRID。

## 返回类型 {#return-type}

Geometry（可为空）。

## 示例 {#examples}

```sql
-- Buffer a point (produces a polygon approximating a circle)
SELECT ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 1) IS NOT NULL;

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

-- Zero distance on a polygon returns itself as MultiPolygon
SELECT ST_ASWKT(
  ST_BUFFER(TO_GEOMETRY('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'), 0)
);

┌─────────────────────────────────────────────────┐
│                     result                      │
├─────────────────────────────────────────────────┤
│ MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0)))          │
└─────────────────────────────────────────────────┘

-- Zero distance on a point returns NULL
SELECT ST_ASWKT(ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 0));

┌────────┐
│ result │
├────────┤
│ NULL   │
└────────┘

-- SRID is preserved
SELECT ST_SRID(ST_BUFFER(ST_GEOMETRYFROMWKT('POINT(0 0)', 4326), 1));

┌────────┐
│ result │
├────────┤
│ 4326   │
└────────┘
```