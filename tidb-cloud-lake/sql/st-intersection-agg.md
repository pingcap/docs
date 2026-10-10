---
title: ST_INTERSECTION_AGG
summary: 複数の GEOMETRY 値に `ST_INTERSECTION` を繰り返し適用して集約し、共通して重なっている部分を返します。
---

# ST_INTERSECTION_AGG

複数の GEOMETRY 値に `ST_INTERSECTION` を繰り返し適用して集約し、共通して重なっている部分を返します。

この関数は GEOMETRY のみをサポートします。

## 構文 {#syntax}

```sql
ST_INTERSECTION_AGG(<geometry>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<geometry>` | GEOMETRY 型の式です。 |

## 戻り値の型 {#return-type}

GEOMETRY。

> **Note:**
>
> - NULL の入力行は無視されます。
> - すべての入力行が NULL の場合、結果は NULL になります。
> - 入力された GEOMETRY 値で異なる SRID が使用されている場合、この関数はエラーを返します。

## 例 {#example}

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