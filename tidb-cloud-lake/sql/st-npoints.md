---
title: ST_NPOINTS
summary: GEOMETRY または GEOGRAPHY オブジェクト内の点の数を返します。
---

# ST_NPOINTS

GEOMETRY または GEOGRAPHY オブジェクト内の点の数を返します。

## 構文 {#syntax}

```sql
ST_NPOINTS(<geometry_or_geography>)
```

## エイリアス {#aliases}

- [ST_NUMPOINTS](/tidb-cloud-lake/sql/st-numpoints.md)

## 引数 {#arguments}

| 引数    | 説明                                                 |
|--------------|-------------------------------------------------------------|
| `<geometry_or_geography>` | 引数は、GEOMETRY または GEOGRAPHY オブジェクト型の式である必要があります。 |

## 戻り値の型 {#return-type}

UInt8。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT ST_NPOINTS(TO_GEOMETRY('POINT(66 12)')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       1 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('MULTIPOINT((45 21),(12 54))')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       2 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('LINESTRING(40 60,50 50,60 40)')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       3 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('MULTILINESTRING((1 1,32 17),(33 12,73 49,87.1 6.1))')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       5 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('GEOMETRYCOLLECTION(POLYGON((-10 0,0 10,10 0,-10 0)),LINESTRING(40 60,50 50,60 40),POINT(99 11))')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       8 │
└─────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT ST_NPOINTS(ST_GEOGFROMWKT('LINESTRING(40 60,50 50,60 40)')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       3 │
└─────────┘
```