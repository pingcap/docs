---
title: ST_UNION_AGG
summary: 通过重复应用 `ST_UNION` 聚合多个 GEOMETRY 值，并返回合并后的 GEOMETRY 结果。
---

# ST_UNION_AGG

通过重复应用 `ST_UNION` 聚合多个 GEOMETRY 值，并返回合并后的 GEOMETRY 结果。

此函数仅支持 GEOMETRY。

## 语法 {#syntax}

```sql
ST_UNION_AGG(<geometry>)
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
> - 如果所有输入行均为 NULL，结果为 NULL。
> - 如果输入的 GEOMETRY 值使用了不同的 SRID，该函数会返回错误。

## 示例 {#example}

```sql
WITH data AS (
    SELECT TO_GEOMETRY('POINT(0 0)') AS g
    UNION ALL
    SELECT TO_GEOMETRY('POINT(1 1)')
)
SELECT ST_ASWKT(ST_UNION_AGG(g)) FROM data;

╭───────────────────────────╮
│ st_aswkt(st_union_agg(g)) │
├───────────────────────────┤
│ MULTIPOINT(0 0,1 1)       │
╰───────────────────────────╯
```