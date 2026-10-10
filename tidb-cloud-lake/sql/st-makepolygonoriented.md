---
title: ST_MAKEPOLYGONORIENTED
summary: 与えられた頂点順序を保持したまま、LineString 入力から Polygon を作成します。ST_MAKEPOLYGON とは異なり、この関数は特定の回転方向を強制するために頂点を並べ替えません。
---

# ST_MAKEPOLYGONORIENTED

与えられた頂点順序を保持したまま、LineString 入力から Polygon を作成します。[ST_MAKEPOLYGON](/tidb-cloud-lake/sql/st-makepolygon.md) とは異なり、この関数は特定の回転方向を強制するために頂点を並べ替えません。

## 構文 {#syntax}

```sql
ST_MAKEPOLYGONORIENTED(<geometry>)
```

## 引数 {#arguments}

| 引数    | 説明                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry>` | LineString 型の GEOMETRY 式です。少なくとも 4 つの点を持ち、最初と最後の点が同一である必要があります。 |

> **Note:**
>
> - 受け付ける入力は LineString のみです。その他の型はエラーになります。
> - LineString は有効なポリゴンを形成している必要があります（自己交差不可）。

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

```sql
SELECT ST_ASWKT(
  ST_MAKEPOLYGONORIENTED(TO_GEOMETRY('LINESTRING(0 0, 1 0, 1 2, 0 2, 0 0)'))
);

┌──────────────────────────────────┐
│             result               │
├──────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0))  │
└──────────────────────────────────┘

-- Reversed winding order is preserved
SELECT ST_ASWKT(
  ST_MAKEPOLYGONORIENTED(TO_GEOMETRY('LINESTRING(0 0, 0 2, 1 2, 1 0, 0 0)'))
);

┌──────────────────────────────────┐
│             result               │
├──────────────────────────────────┤
│ POLYGON((0 0,0 2,1 2,1 0,0 0))  │
└──────────────────────────────────┘
```