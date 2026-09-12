---
title: ST_LENGTH
summary: 返回 GEOMETRY 或 GEOGRAPHY 对象中 LineString 的欧几里得长度。
---

# ST_LENGTH

返回 GEOMETRY 或 GEOGRAPHY 对象中 LineString 的欧几里得长度。

## 语法 {#syntax}

```sql
ST_LENGTH(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数    | 描述                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是一个 GEOMETRY 或 GEOGRAPHY 类型的表达式，且其中包含 linestring。 |

> **注意：**
>
> - 如果 `<geometry_or_geography>` 不是 `LineString`、`MultiLineString` 或包含 linestring 的 `GeometryCollection`，则返回 0。
> - 如果 `<geometry_or_geography>` 是 `GeometryCollection`，则返回该集合中所有 linestring 长度之和。

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_LENGTH(TO_GEOMETRY('POINT(1 1)')) AS length

┌─────────┐
│  length │
├─────────┤
│       0 │
└─────────┘

SELECT
  ST_LENGTH(TO_GEOMETRY('LINESTRING(0 0, 1 1)')) AS length

┌─────────────┐
│    length   │
├─────────────┤
│ 1.414213562 │
└─────────────┘

SELECT
  ST_LENGTH(
    TO_GEOMETRY('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))')
  ) AS length

┌─────────┐
│  length │
├─────────┤
│       0 │
└─────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_LENGTH(
    ST_GEOGFROMWKT(
      'LINESTRING(0 0, 1 0)'
    )
  ) AS length

╭──────────────────╮
│      length      │
├──────────────────┤
│ 111319.490793274 │
╰──────────────────╯
```