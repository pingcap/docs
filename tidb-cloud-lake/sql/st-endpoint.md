---
title: ST_ENDPOINT
summary: LineString 内の最後の Point を返します。
---

# ST_ENDPOINT

LineString 内の最後の Point を返します。

## 構文 {#syntax}

```sql
ST_ENDPOINT(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| `<geometry_or_geography>` | 引数は、LineString を表す GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_ENDPOINT(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_endpoint;

┌───────────────────┐
│ pipeline_endpoint │
├───────────────────┤
│ POINT(4 4)        │
└───────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_ENDPOINT(
    ST_GEOGFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_endpoint;

┌───────────────────┐
│ pipeline_endpoint │
├───────────────────┤
│ POINT(4 4)        │
└───────────────────┘
```