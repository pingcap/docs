---
title: ST_INTERSECTS
summary: 2 つの GEOMETRY オブジェクトが空間の一部を共有している場合に TRUE を返します。
---

# ST_INTERSECTS

2 つの GEOMETRY オブジェクトが空間の一部を共有している場合に TRUE を返します。

## 構文 {#syntax}

```sql
ST_INTERSECTS(<geometry1>, <geometry2>)
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
SELECT ST_INTERSECTS(
  TO_GEOMETRY('LINESTRING(0 0, 2 2)'),
  TO_GEOMETRY('LINESTRING(0 2, 2 0)')
) AS intersects;

╭────────────╮
│ intersects │
├────────────┤
│ true       │
╰────────────╯

SELECT ST_INTERSECTS(
  TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'),
  TO_GEOMETRY('POINT(3 3)')
) AS intersects;

╭────────────╮
│ intersects │
├────────────┤
│ false      │
╰────────────╯
```