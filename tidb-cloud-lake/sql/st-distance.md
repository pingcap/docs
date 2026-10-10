---
title: ST_DISTANCE
summary: 2 つのオブジェクト間の最小距離を返します。GEOMETRY 入力の場合、この関数はユークリッド距離を使用します。GEOGRAPHY 入力の場合、この関数は haversine 距離を使用します。
---

# ST_DISTANCE

2 つのオブジェクト間の最小距離を返します。GEOMETRY 入力の場合、この関数は [ユークリッド距離](https://en.wikipedia.org/wiki/Euclidean_distance) を使用します。GEOGRAPHY 入力の場合、この関数は [haversine 距離](https://en.wikipedia.org/wiki/Haversine_formula) を使用します。

## 構文 {#syntax}

```sql
ST_DISTANCE(<geometry_or_geography1>, <geometry_or_geography2>)
```

## 引数 {#arguments}

| 引数     | 説明                                                                   |
|---------------|-------------------------------------------------------------------------------|
| `<geometry_or_geography1>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があり、Point を含んでいる必要があります。 |
| `<geometry_or_geography2>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があり、Point を含んでいる必要があります。 |

> **Note:**
>
> - 1 つ以上の入力ポイントが NULL の場合は NULL を返します。
> - 2 つの入力 GEOMETRY または GEOGRAPHY オブジェクトの SRID が異なる場合、この関数はエラーを報告します。

## 戻り値の型 {#return-type}

Double。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_DISTANCE(
    TO_GEOMETRY('POINT(0 0)'),
    TO_GEOMETRY('POINT(1 1)')
  ) AS distance

┌─────────────┐
│   distance  │
├─────────────┤
│ 1.414213562 │
└─────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_DISTANCE(
    ST_GEOGFROMWKT('POINT(0 0)'),
    ST_GEOGFROMWKT('POINT(1 0)')
  ) AS distance

╭──────────────────╮
│     distance     │
├──────────────────┤
│ 111195.080233533 │
╰──────────────────╯
```