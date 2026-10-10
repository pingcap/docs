---
title: ST_CONTAINS
summary: 2 番目の GEOMETRY オブジェクトが 1 番目の GEOMETRY オブジェクトの完全に内側にある場合に TRUE を返します。
---

# ST_CONTAINS

2 番目の GEOMETRY オブジェクトが 1 番目の GEOMETRY オブジェクトの完全に内側にある場合に TRUE を返します。

## 構文 {#syntax}

```sql
ST_CONTAINS(<geometry1>, <geometry2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|---------------|----------------------------------------------------------------------------------------------|
| `<geometry1>` | 引数は、GeometryCollection ではない GEOMETRY オブジェクト型の式である必要があります。 |
| `<geometry2>` | 引数は、GeometryCollection ではない GEOMETRY オブジェクト型の式である必要があります。 |

> **Note:**
>
> - 2 つの入力 GEOMETRY オブジェクトの SRID が異なる場合、この関数はエラーを報告します。

## 戻り値の型 {#return-type}

Boolean。

## 例 {#examples}

```sql
SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ true     │
└──────────┘

SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ false    │
└──────────┘

SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('LINESTRING(-2 0, 0 0, 0 1)')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ true     │
└──────────┘

```