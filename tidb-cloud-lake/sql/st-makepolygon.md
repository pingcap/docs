---
title: ST_MAKEPOLYGON
summary: 构造一个表示无孔 Polygon 的 GEOMETRY 或 GEOGRAPHY 对象。该函数使用指定的 LineString 作为外环。
---

# ST_MAKEPOLYGON

构造一个表示无孔 Polygon 的 GEOMETRY 或 GEOGRAPHY 对象。该函数使用指定的 LineString 作为外环。

## 语法 {#syntax}

```sql
ST_MAKEPOLYGON(<geometry_or_geography>)
```

## 别名 {#aliases}

- [ST_POLYGON](/tidb-cloud-lake/sql/st-polygon.md)

## 参数 {#arguments}

| 参数    | 描述                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_MAKEPOLYGON(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)'
    )
  ) AS pipeline_polygon;

┌────────────────────────────────┐
│        pipeline_polygon        │
├────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0)) │
└────────────────────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_MAKEPOLYGON(
    ST_GEOGFROMWKT(
      'LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)'
    )
  ) AS pipeline_polygon;

╭────────────────────────────────╮
│        pipeline_polygon        │
├────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0)) │
╰────────────────────────────────╯
```