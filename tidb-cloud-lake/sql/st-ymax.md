---
title: ST_YMAX
summary: 返回指定 GEOMETRY 或 GEOGRAPHY 对象中包含的所有点的最大纬度（Y 坐标）。
---

# ST_YMAX

返回指定 GEOMETRY 或 GEOGRAPHY 对象中包含的所有点的最大纬度（Y 坐标）。

## 语法 {#syntax}

```sql
ST_YMAX(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_YMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(180 50),LINESTRING(10 10,20 20,10 40),POINT EMPTY)'
    )
  ) AS pipeline_ymax;

┌───────────────┐
│ pipeline_ymax │
├───────────────┤
│            50 │
└───────────────┘

SELECT
  ST_YMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(40 10),LINESTRING(10 10,20 20,10 40),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_ymax;

┌───────────────┐
│ pipeline_ymax │
├───────────────┤
│            45 │
└───────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_YMAX(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 10, 179 22)'
    )
  ) AS pipeline_ymax;

┌───────────────┐
│ pipeline_ymax │
├───────────────┤
│            22 │
└───────────────┘
```