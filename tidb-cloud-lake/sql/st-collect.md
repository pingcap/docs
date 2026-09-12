---
title: ST_COLLECT
summary: 将多个 GEOMETRY 值收集为单个 GEOMETRY 结果。
---

# ST_COLLECT

将多个 GEOMETRY 值收集为单个 GEOMETRY 结果。

此函数仅支持 GEOMETRY。

## 语法 {#syntax}

```sql
ST_COLLECT(<geometry>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<geometry>` | 一个 GEOMETRY 类型的表达式。 |

## 返回类型 {#return-type}

GEOMETRY。根据输入不同，结果可以是 `MULTIPOINT`、`MULTILINESTRING`、`MULTIPOLYGON` 或 `GEOMETRYCOLLECTION`。

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
    SELECT TO_GEOMETRY('LINESTRING(1 1,2 2)')
)
SELECT ST_ASWKT(ST_COLLECT(g)) FROM data;

╭────────────────────────────────────────────────────╮
│               st_aswkt(st_collect(g))              │
├────────────────────────────────────────────────────┤
│ GEOMETRYCOLLECTION(POINT(0 0),LINESTRING(1 1,2 2)) │
╰────────────────────────────────────────────────────╯
```