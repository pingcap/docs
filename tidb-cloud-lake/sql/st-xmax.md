---
title: ST_XMAX
summary: 指定した GEOMETRY または GEOGRAPHY オブジェクトに含まれるすべての点の最大経度（X 座標）を返します。
---

# ST_XMAX

指定した GEOMETRY または GEOGRAPHY オブジェクトに含まれるすべての点の最大経度（X 座標）を返します。

## 構文 {#syntax}

```sql
ST_XMAX(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

Double。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_XMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(40 10),LINESTRING(10 10,20 20,10 40),POINT EMPTY)'
    )
  ) AS pipeline_xmax;

┌───────────────┐
│ pipeline_xmax │
├───────────────┤
│            40 │
└───────────────┘

SELECT
  ST_XMAX(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(40 10),LINESTRING(10 10,20 20,10 40),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_xmax;

┌───────────────┐
│ pipeline_xmax │
├───────────────┤
│            45 │
└───────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_XMAX(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 0, 179 0)'
    )
  ) AS pipeline_xmax;

┌───────────────┐
│ pipeline_xmax │
├───────────────┤
│           179 │
└───────────────┘
```