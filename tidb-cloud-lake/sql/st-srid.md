---
title: ST_SRID
summary: 返回 GEOMETRY 或 GEOGRAPHY 对象的 SRID（空间参考系统标识符）。
---

# ST_SRID

返回 GEOMETRY 或 GEOGRAPHY 对象的 SRID（空间参考系统标识符）。

## 语法 {#syntax}

```sql
ST_SRID(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数    | 描述                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

INT32。

> **注意：**
>
> - 如果 Geometry 没有 SRID，则返回默认值 `0`。
> - 对于 Geography，SRID 始终为 `4326`。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_SRID(
    TO_GEOMETRY(
      'POINT(-122.306100 37.554162)',
      1234
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│          1234 │
└───────────────┘

SELECT
  ST_SRID(
    ST_MAKEGEOMPOINT(
      37.5, 45.5
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│             0 │
└───────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_SRID(
    ST_GEOGFROMWKT(
      'POINT(1 2)'
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│          4326 │
└───────────────┘
```