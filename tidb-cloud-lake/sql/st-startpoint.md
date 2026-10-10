---
title: ST_STARTPOINT
summary: LineString 内の最初の Point を返します。
---

# ST_STARTPOINT

LineString 内の最初の Point を返します。

## 構文 {#syntax}

```sql
ST_STARTPOINT(<geometry_or_geography>)
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
  ST_STARTPOINT(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_endpoint;

┌───────────────────┐
│ pipeline_endpoint │
├───────────────────┤
│ POINT(1 1)        │
└───────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_STARTPOINT(
    ST_GEOGFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    )
  ) AS pipeline_startpoint;

┌─────────────────────┐
│ pipeline_startpoint │
├─────────────────────┤
│ POINT(1 1)          │
└─────────────────────┘
```