---
title: ST_XMIN
summary: 返回指定 GEOMETRY 或 GEOGRAPHY 对象中包含的所有点的最小经度（X 坐标）。
---

# ST_XMIN

返回指定 GEOMETRY 或 GEOGRAPHY 对象中包含的所有点的最小经度（X 坐标）。

## 语法 {#syntax}

```sql
ST_XMIN(<geometry_or_geography>)
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
  ST_XMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(180 10),LINESTRING(20 10,30 20,40 40),POINT EMPTY)'
    )
  ) AS pipeline_xmin;

┌───────────────┐
│ pipeline_xmin │
├───────────────┤
│            20 │
└───────────────┘

SELECT
  ST_XMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(40 10),LINESTRING(20 10,30 20,10 40),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_xmin;

┌───────────────┐
│ pipeline_xmin │
├───────────────┤
│            10 │
└───────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_XMIN(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 0, 179 0)'
    )
  ) AS pipeline_xmin;

┌───────────────┐
│ pipeline_xmin │
├───────────────┤
│          -179 │
└───────────────┘
```