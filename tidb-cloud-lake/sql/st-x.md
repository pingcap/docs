---
title: ST_X
summary: GEOMETRY または GEOGRAPHY オブジェクトで表される Point の経度（X 座標）を返します。
---

# ST_X

GEOMETRY または GEOGRAPHY オブジェクトで表される Point の経度（X 座標）を返します。

## 構文 {#syntax}

```sql
ST_X(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                                                   |
|--------------|-------------------------------------------------------------------------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があり、Point を含んでいる必要があります。 |

## 戻り値の型 {#return-type}

Double。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_X(
    ST_MAKEGEOMPOINT(
      37.5, 45.5
    )
  ) AS pipeline_x;

┌────────────┐
│ pipeline_x │
├────────────┤
│       37.5 │
└────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_X(
    ST_GEOGFROMWKT(
      'POINT(37.5 45.5)'
    )
  ) AS pipeline_x;

┌────────────┐
│ pipeline_x │
├────────────┤
│       37.5 │
└────────────┘
```