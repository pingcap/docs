---
title: ST_UNION_AGG
summary: "`ST_UNION` を繰り返し適用して複数の GEOMETRY 値を集約し、マージされた GEOMETRY 結果を返します。"
---

# ST_UNION_AGG

`ST_UNION` を繰り返し適用して複数の GEOMETRY 値を集約し、マージされた GEOMETRY 結果を返します。

この関数は GEOMETRY のみをサポートします。

## 構文 {#syntax}

```sql
ST_UNION_AGG(<geometry>)
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
> - すべての入力行が NULL の場合、結果は NULL です。
> - 入力された GEOMETRY 値で異なる SRID が使用されている場合、この関数はエラーを返します。

## 例 {#example}

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