---
title: ST_ENVELOPE_AGG
summary: 複数の GEOMETRY 値を集約し、NULL でないすべての入力を包含する最小外接矩形を返します。
---

# ST_ENVELOPE_AGG

複数の GEOMETRY 値を集約し、NULL でないすべての入力を包含する最小外接矩形を返します。

この関数は GEOMETRY のみをサポートします。

## 構文 {#syntax}

```sql
ST_ENVELOPE_AGG(<geometry>)
```

## 引数 {#arguments}

| 引数 | 説明 |
| --------- | ----------- |
| `<geometry>` | GEOMETRY 型の式。 |

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