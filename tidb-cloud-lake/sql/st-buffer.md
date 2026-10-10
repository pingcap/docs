---
title: ST_BUFFER
summary: 入力ジオメトリからの距離が指定した距離以下であるすべての点を表す GEOMETRY を返します。結果は MultiPolygon または NULL です。
---

# ST_BUFFER

入力ジオメトリからの距離が指定した距離以下であるすべての点を表す GEOMETRY を返します。結果は MultiPolygon または NULL です。

## 構文 {#syntax}

```sql
ST_BUFFER(<geometry>, <distance>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry>` | GEOMETRY 式です。GeometryCollection はサポートされていません。 |
| `<distance>` | バッファ距離です。単位は入力ジオメトリの座標系に一致します。 |

> **Note:**
>
> - Point、MultiPoint、LineString、MultiLineString の場合: distance の絶対値が使用されます（負の値でも正の値と同じように動作します）。
> - Polygon、MultiPolygon の場合: 正の distance は膨張し、負の distance は縮小します。
> - 結果が空の場合は NULL を返します（例: Point に対する距離 0、またはポリゴンを面積 0 を超えて縮小した場合）。
> - distance が 0 の Polygon の場合: MultiPolygon でラップされたポリゴンを返します。
> - 出力では SRID が保持されます。

## 戻り値の型 {#return-type}

Geometry（NULL 可）。

## 例 {#examples}

```sql
-- 点をバッファする（円を近似するポリゴンを生成）
SELECT ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 1) IS NOT NULL;

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

-- ポリゴンに対する距離 0 は、それ自身を MultiPolygon として返す
SELECT ST_ASWKT(
  ST_BUFFER(TO_GEOMETRY('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'), 0)
);

┌─────────────────────────────────────────────────┐
│                     result                      │
├─────────────────────────────────────────────────┤
│ MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0)))          │
└─────────────────────────────────────────────────┘

-- 点に対する距離 0 は NULL を返す
SELECT ST_ASWKT(ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 0));

┌────────┐
│ result │
├────────┤
│ NULL   │
└────────┘

-- SRID は保持される
SELECT ST_SRID(ST_BUFFER(ST_GEOMETRYFROMWKT('POINT(0 0)', 4326), 1));

┌────────┐
│ result │
├────────┤
│ 4326   │
└────────┘
```