---
title: ST_STARTPOINT
summary: 返回 LineString 中的第一个 Point。
---

# ST_STARTPOINT

返回 LineString 中的第一个 Point。

## 语法 {#syntax}

```sql
ST_STARTPOINT(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数    | 描述                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是一个 GEOMETRY 或 GEOGRAPHY 类型的表达式，并且表示一个 LineString。 |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_STARTPOINT(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_endpoint;

┌───────────────────┐
│ pipeline_endpoint │
├───────────────────┤
│ POINT(1 1)        │
└───────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_STARTPOINT(
    ST_GEOGFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_startpoint;

┌─────────────────────┐
│ pipeline_startpoint │
├─────────────────────┤
│ POINT(1 1)          │
└─────────────────────┘
```