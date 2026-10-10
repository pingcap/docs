---
title: ST_DIFFERENCE
summary: 2 番目の GEOMETRY オブジェクトでカバーされていない、1 番目の GEOMETRY オブジェクトの部分を返します。
---

# ST_DIFFERENCE

2 番目の GEOMETRY オブジェクトでカバーされていない、1 番目の GEOMETRY オブジェクトの部分を返します。

この関数は GEOMETRY 値のみをサポートします。

## 構文 {#syntax}

```sql
ST_DIFFERENCE(<geometry1>, <geometry2>)
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
SELECT ST_ASWKT(ST_DIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')));

╭───────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_difference(to_geometry('POINT(0 0)'), to_geometry('POINT(1 1)'))) │
├───────────────────────────────────────────────────────────────────────────────┤
│ POINT(0 0)                                                                    │
╰───────────────────────────────────────────────────────────────────────────────╯
```