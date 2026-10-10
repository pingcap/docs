---
title: ST_COLLECT
summary: 複数の GEOMETRY 値を 1 つの GEOMETRY 結果にまとめます。
---

# ST_COLLECT

複数の GEOMETRY 値を 1 つの GEOMETRY 結果にまとめます。

この関数は GEOMETRY のみをサポートします。

## 構文 {#syntax}

```sql
ST_COLLECT(<geometry>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<geometry>` | GEOMETRY 型の式です。 |

## 戻り値の型 {#return-type}

GEOMETRY。入力に応じて、結果は `MULTIPOINT`、`MULTILINESTRING`、`MULTIPOLYGON`、または `GEOMETRYCOLLECTION` になります。

> **Note:**
>
> - NULL の入力行は無視されます。
> - すべての入力行が NULL の場合、結果は NULL です。
> - 入力 GEOMETRY 値で異なる SRID が使用されている場合、この関数はエラーを返します。

## 例 {#example}

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