---
title: ST_YMIN
summary: 返回指定 GEOMETRY 或 GEOGRAPHY 对象中所有点的最小纬度（Y 坐标）。
---

# ST_YMIN

返回指定 GEOMETRY 或 GEOGRAPHY 对象中所有点的最小纬度（Y 坐标）。

## 语法 {#syntax}

```sql
ST_YMIN(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数    | 描述                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_YMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(-180 -10),LINESTRING(-179 0, 179 30),POINT EMPTY)'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│           -10 │
└───────────────┘

SELECT
  ST_YMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(180 0),LINESTRING(-60 -30, 60 30),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│           -30 │
└───────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_YMIN(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 10, 179 22)'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│            10 │
└───────────────┘
```