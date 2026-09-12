---
title: ST_POINTN
summary: 返回 LineString 中指定索引处的 Point。
---

# ST_POINTN

返回 LineString 中指定索引处的 Point。

## 语法 {#syntax}

```sql
ST_POINTN(<geometry_or_geography>, <index>)
```

## 参数 {#arguments}

| 参数    | 描述                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是一个 GEOMETRY 或 GEOGRAPHY 类型的表达式，并且表示一个 LineString。 |
| `<index>`    | 要返回的 Point 的索引。                                                 |

> **注意：**
>
> 索引从 1 开始计数，负索引用作从 LineString 末尾开始的偏移。如果 index 超出范围，函数会返回错误。

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_POINTN(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    ),
    1
  ) AS pipeline_pointn;

┌─────────────────┐
│ pipeline_pointn │
├─────────────────┤
│ POINT(1 1)      │
└─────────────────┘

SELECT
  ST_POINTN(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    ),
    -2
  ) AS pipeline_pointn;

┌─────────────────┐
│ pipeline_pointn │
├─────────────────┤
│ POINT(3 3)      │
└─────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_POINTN(
    ST_GEOGFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    ),
    2
  ) AS pipeline_pointn;

┌─────────────────┐
│ pipeline_pointn │
├─────────────────┤
│ POINT(2 2)      │
└─────────────────┘
```