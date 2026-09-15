---
title: ST_ENVELOPE_AGG
summary: 聚合多个 GEOMETRY 值，并返回覆盖所有非 NULL 输入的最小外接矩形。
---

# ST_ENVELOPE_AGG

聚合多个 GEOMETRY 值，并返回覆盖所有非 NULL 输入的最小外接矩形。

此函数仅支持 GEOMETRY。

## 语法 {#syntax}

```sql
ST_ENVELOPE_AGG(<geometry>)
```

## 参数 {#arguments}

| 参数 | 描述 |
| --------- | ----------- |
| `<geometry>` | 一个 GEOMETRY 类型的表达式。 |

## 返回类型 {#return-type}

GEOMETRY。

> **注意：**
>
> - NULL 输入行会被忽略。
> - 如果所有输入行均为 NULL，结果为 NULL。
> - 如果输入的 GEOMETRY 值使用了不同的 SRID，该函数会返回错误。

## 示例 {#example}

```sql
WITH data AS (
    SELECT TO_GEOMETRY('POINT(1 1)') AS g
    UNION ALL
    SELECT TO_GEOMETRY('POINT(4 2)')
    UNION ALL
    SELECT TO_GEOMETRY('POINT(2 5)')
)
SELECT ST_ASWKT(ST_ENVELOPE_AGG(g)) FROM data;

╭────────────────────────────────╮
│  st_aswkt(st_envelope_agg(g))  │
├────────────────────────────────┤
│ POLYGON((1 1,4 1,4 5,1 5,1 1)) │
╰────────────────────────────────╯
```