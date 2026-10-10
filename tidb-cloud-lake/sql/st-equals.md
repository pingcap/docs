---
title: ST_EQUALS
summary: 2 つの GEOMETRY オブジェクトが空間的に等しい場合に TRUE を返します。
---

# ST_EQUALS

2 つの GEOMETRY オブジェクトが空間的に等しい場合に TRUE を返します。

## 構文 {#syntax}

```sql
ST_EQUALS(<geometry1>, <geometry2>)
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
SELECT ST_EQUALS(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POINT(1 1)')
) AS equals;

╭────────╮
│ equals │
├────────┤
│ true   │
╰────────╯

SELECT ST_EQUALS(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POINT(1 2)')
) AS equals;

╭────────╮
│ equals │
├────────┤
│ false  │
╰────────╯
```