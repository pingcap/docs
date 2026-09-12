---
title: ST_INTERSECTION_AGG
summary: 通过重复应用 ST_INTERSECTION 对多个 GEOMETRY 值进行聚合，并返回共同重叠的部分。
---

# ST_INTERSECTION_AGG

通过重复应用 `ST_INTERSECTION` 对多个 GEOMETRY 值进行聚合，并返回共同重叠的部分。

此函数仅支持 GEOMETRY。

## 语法 {#syntax}

```sql
ST_INTERSECTION_AGG(<geometry>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<geometry>` | 一个 GEOMETRY 类型的表达式。 |

## 返回类型 {#return-type}

GEOMETRY。

> **注意：**
>
> - 会忽略输入中的 NULL 行。
> - 如果所有输入行均为 NULL，则结果为 NULL。
> - 如果输入的 GEOMETRY 值使用了不同的 SRID，则该函数会返回错误。

## 示例 {#example}

```sql
WITH data AS (
    SELECT TO_GEOMETRY('POLYGON((0 0,4 0,4 4,0 4,0 0))') AS g
    UNION ALL
    SELECT TO_GEOMETRY('POLYGON((1 1,3 1,3 3,1 3,1 1))')
)
SELECT ST_ASWKT(ST_INTERSECTION_AGG(g)) FROM data;

╭──────────────────────────────────╮
│ st_aswkt(st_intersection_agg(g)) │
├──────────────────────────────────┤
│ POLYGON((1 3,1 1,3 1,3 3,1 3))   │
╰──────────────────────────────────╯
```