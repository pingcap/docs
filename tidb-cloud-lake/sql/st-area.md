---
title: ST_AREA
summary: GEOMETRY または GEOGRAPHY オブジェクトの面積を返します。GEOMETRY 入力の場合、この関数は [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula) に基づく平面面積を使用します。GEOGRAPHY 入力の場合、この関数は [Karney (2013)](https://arxiv.org/pdf/1109.4448.pdf) で説明されている手法を使用して、地球の楕円体モデル上の測地面積を計測します。
---

# ST_AREA

GEOMETRY または GEOGRAPHY オブジェクトの面積を返します。GEOMETRY 入力の場合、この関数は [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula) に基づく平面面積を使用します。GEOGRAPHY 入力の場合、この関数は [Karney (2013)](https://arxiv.org/pdf/1109.4448.pdf) で説明されている手法を使用して、地球の楕円体モデル上の測地面積を計測します。

## 構文 {#syntax}

```sql
ST_AREA(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数                        | 説明                                                               |
|---------------------------|-----------------------------------------------------------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

Double。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_AREA(
    TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')
  ) AS area

┌──────┐
│ area │
├──────┤
│ 1.0  │
└──────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_AREA(
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')
  ) AS area

╭────────────────────╮
│        area        │
├────────────────────┤
│ 12308778361.469452 │
╰────────────────────╯
```