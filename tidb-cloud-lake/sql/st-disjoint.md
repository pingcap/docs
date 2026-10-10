---
title: ST_DISJOINT
summary: 2 つの GEOMETRY オブジェクトが交差しない場合に TRUE を返します。
---

# ST_DISJOINT

2 つの GEOMETRY オブジェクトが交差しない場合に TRUE を返します。

## 構文 {#syntax}

```sql
ST_DISJOINT(<geometry1>, <geometry2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|---------------|-------------------------------------------------------|
| `<geometry1>` | 引数は GEOMETRY 型の式である必要があります。 |
| `<geometry2>` | 引数は GEOMETRY 型の式である必要があります。 |

> **Note:**
>
> 2 つの入力 GEOMETRY オブジェクトの SRID が異なる場合、この関数はエラーを報告します。

## 戻り値の型 {#return-type}

Boolean。

## 例 {#examples}

```sql
SELECT ST_DISJOINT(
  TO_GEOMETRY('POINT(3 3)'),
  TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))')
) AS disjoint;

╭──────────╮
│ disjoint │
├──────────┤
│ true     │
╰──────────╯

SELECT ST_DISJOINT(
  TO_GEOMETRY('LINESTRING(0 0, 2 2)'),
  TO_GEOMETRY('LINESTRING(0 2, 2 0)')
) AS disjoint;

╭──────────╮
│ disjoint │
├──────────┤
│ false    │
╰──────────╯
```