---
title: ST_X
summary: 返回由 GEOMETRY 或 GEOGRAPHY 对象表示的 Point 的经度（X 坐标）。
---

# ST_X

返回由 GEOMETRY 或 GEOGRAPHY 对象表示的 Point 的经度（X 坐标）。

## 语法 {#syntax}

```sql
ST_X(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数    | 描述                                                                   |
|--------------|-------------------------------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式，并且必须包含一个 Point。 |

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_X(
    ST_MAKEGEOMPOINT(
      37.5, 45.5
    )
  ) AS pipeline_x;

┌────────────┐
│ pipeline_x │
├────────────┤
│       37.5 │
└────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_X(
    ST_GEOGFROMWKT(
      'POINT(37.5 45.5)'
    )
  ) AS pipeline_x;

┌────────────┐
│ pipeline_x │
├────────────┤
│       37.5 │
└────────────┘
```