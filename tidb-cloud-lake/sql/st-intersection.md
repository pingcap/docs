---
title: ST_INTERSECTION
summary: 2 つの GEOMETRY オブジェクトの共有部分を返します。
---

# ST_INTERSECTION

2 つの GEOMETRY オブジェクトの共有部分を返します。

この関数は GEOMETRY 値のみをサポートします。

## 構文 {#syntax}

```sql
ST_INTERSECTION(<geometry1>, <geometry2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|---------------|--------------------------------------------------------|
| `<geometry1>` | 引数は GEOMETRY 型の式である必要があります。 |
| `<geometry2>` | 引数は GEOMETRY 型の式である必要があります。 |

> **Note:**
>
> 2 つの入力 GEOMETRY オブジェクトの SRID が異なる場合、この関数はエラーを報告します。

## 戻り値の型 {#return-type}

GEOMETRY。

## 例 {#examples}

```sql
SELECT ST_ASWKT(ST_INTERSECTION(TO_GEOMETRY('LINESTRING(0 0, 1 1)'), TO_GEOMETRY('LINESTRING(0 0, 1 1)')));

╭─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_intersection(to_geometry('LINESTRING(0 0, 1 1)'), to_geometry('LINESTRING(0 0, 1 1)'))) │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LINESTRING(0 0,1 1)                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
```