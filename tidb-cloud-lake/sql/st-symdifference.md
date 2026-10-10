---
title: ST_SYMDIFFERENCE
summary: 2 つの GEOMETRY オブジェクトの重なっていない部分を返します。
---

# ST_SYMDIFFERENCE

2 つの GEOMETRY オブジェクトのうち、重なっていない部分を返します。

この関数は GEOMETRY 値のみをサポートします。

## 構文 {#syntax}

```sql
ST_SYMDIFFERENCE(<geometry1>, <geometry2>)
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
SELECT ST_ASWKT(ST_SYMDIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')));

╭──────────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_symdifference(to_geometry('POINT(0 0)'), to_geometry('POINT(1 1)'))) │
├──────────────────────────────────────────────────────────────────────────────────┤
│ MULTIPOINT(0 0,1 1)                                                              │
╰──────────────────────────────────────────────────────────────────────────────────╯
```