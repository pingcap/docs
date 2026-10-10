---
title: ST_WITHIN
summary: 最初の GEOMETRY オブジェクトが 2 番目の GEOMETRY オブジェクトの完全に内側にある場合に TRUE を返します。
---

# ST_WITHIN

最初の GEOMETRY オブジェクトが 2 番目の GEOMETRY オブジェクトの完全に内側にある場合に TRUE を返します。

## 構文 {#syntax}

```sql
ST_WITHIN(<geometry1>, <geometry2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|---------------|-------------------------------------------------------|
| `<geometry1>` | 引数は GEOMETRY 型の式である必要があります。 |
| `<geometry2>` | 引数は GEOMETRY 型の式である必要があります。 |

> **Note:**
>
> 2 つの入力 GEOMETRY オブジェクトの SRID が異なる場合、この関数はエラーを返します。

## 戻り値の型 {#return-type}

Boolean。

## 例 {#examples}

```sql
SELECT ST_WITHIN(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))')
) AS within;

╭─────────╮
│  within │
├─────────┤
│ true    │
╰─────────╯
```