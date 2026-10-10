---
title: ST_YMIN
summary: 指定した GEOMETRY または GEOGRAPHY オブジェクトに含まれるすべての点の最小緯度（Y 座標）を返します。
---

# ST_YMIN

指定した GEOMETRY または GEOGRAPHY オブジェクトに含まれるすべての点の最小緯度（Y 座標）を返します。

## 構文 {#syntax}

```sql
ST_YMIN(<geometry_or_geography>)
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
  ST_YMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(-180 -10),LINESTRING(-179 0, 179 30),POINT EMPTY)'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│           -10 │
└───────────────┘

SELECT
  ST_YMIN(
    TO_GEOMETRY(
      'GEOMETRYCOLLECTION(POINT(180 0),LINESTRING(-60 -30, 60 30),POLYGON((40 40,20 45,45 30,40 40)))'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│           -30 │
└───────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_YMIN(
    ST_GEOGFROMWKT(
      'LINESTRING(-179 10, 179 22)'
    )
  ) AS pipeline_ymin;

┌───────────────┐
│ pipeline_ymin │
├───────────────┤
│            10 │
└───────────────┘
```