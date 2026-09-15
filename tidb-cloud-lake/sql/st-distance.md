---
title: ST_DISTANCE
summary: 返回两个对象之间的最小距离。对于 GEOMETRY 输入，该函数使用欧几里得距离。对于 GEOGRAPHY 输入，该函数使用 haversine 距离。
---

# ST_DISTANCE

返回两个对象之间的最小距离。对于 GEOMETRY 输入，该函数使用[欧几里得距离](https://en.wikipedia.org/wiki/Euclidean_distance)。对于 GEOGRAPHY 输入，该函数使用 [haversine 距离](https://en.wikipedia.org/wiki/Haversine_formula)。

## 语法 {#syntax}

```sql
ST_DISTANCE(<geometry_or_geography1>, <geometry_or_geography2>)
```

## 参数 {#arguments}

| 参数     | 描述                                                                   |
|---------------|-------------------------------------------------------------------------------|
| `<geometry_or_geography1>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式，并且必须包含一个 Point。 |
| `<geometry_or_geography2>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式，并且必须包含一个 Point。 |

> **注意：**
>
> - 如果一个或多个输入点为 NULL，则返回 NULL。
> - 如果两个输入的 GEOMETRY 或 GEOGRAPHY 对象具有不同的 SRID，则该函数会报错。

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_DISTANCE(
    TO_GEOMETRY('POINT(0 0)'),
    TO_GEOMETRY('POINT(1 1)')
  ) AS distance

┌─────────────┐
│   distance  │
├─────────────┤
│ 1.414213562 │
└─────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_DISTANCE(
    ST_GEOGFROMWKT('POINT(0 0)'),
    ST_GEOGFROMWKT('POINT(1 0)')
  ) AS distance

╭──────────────────╮
│     distance     │
├──────────────────┤
│ 111195.080233533 │
╰──────────────────╯
```