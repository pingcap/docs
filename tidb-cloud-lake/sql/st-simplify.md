---
title: ST_SIMPLIFY
summary: 指定した許容値以内で結果の辺までの距離に収まる頂点を削除し、GEOMETRY オブジェクトを単純化したバージョンを返します。Ramer-Douglas-Peucker アルゴリズムを使用します。
---

# ST_SIMPLIFY

指定した許容値以内で結果の辺までの距離に収まる頂点を削除し、GEOMETRY オブジェクトを単純化したバージョンを返します。Ramer-Douglas-Peucker アルゴリズムを使用します。

## 構文 {#syntax}

```sql
ST_SIMPLIFY(<geometry>, <tolerance>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|---------------|-----------------------------------------------------------------------------|
| `<geometry>`  | GEOMETRY 式です。LineString、MultiLineString、Polygon、MultiPolygon で動作します。Point または MultiPoint には影響しません。 |
| `<tolerance>` | 頂点削除の最大距離許容値です。 |

> **Note:**
>
> GeometryCollection はサポートされていません。

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

```sql
SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('LINESTRING(0 0, 1 0, 1 1, 2 1)'), 0.5
  )
) AS simplified;

┌──────────────────────┐
│      simplified      │
├──────────────────────┤
│ LINESTRING(0 0,2 1)  │
└──────────────────────┘

SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('LINESTRING(1100 1100, 2500 2100, 3100 3100, 4900 1100, 3100 1900)'), 500
  )
) AS simplified;

┌──────────────────────────────────────────────────────┐
│                      simplified                      │
├──────────────────────────────────────────────────────┤
│ LINESTRING(1100 1100,3100 3100,4900 1100,3100 1900)  │
└──────────────────────────────────────────────────────┘

SELECT ST_ASWKT(
  ST_SIMPLIFY(
    TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0.5 0.5, 0 1, 0 0))'), 0.6
  )
) AS simplified;

┌──────────────────────────────────┐
│            simplified            │
├──────────────────────────────────┤
│ POLYGON((0 0,1 0,1 1,0 1,0 0))  │
└──────────────────────────────────┘
```