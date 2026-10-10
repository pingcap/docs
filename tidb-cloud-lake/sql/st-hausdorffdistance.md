---
title: ST_HAUSDORFFDISTANCE
summary: 2 つの GEOMETRY オブジェクト間の離散 Hausdorff 距離を返します。これは、一方のオブジェクト内の任意の頂点から他方のオブジェクト内の最も近い頂点までの距離のうち最大のものを求めることで、2 つのジオメトリがどれだけ離れているかを測定します。
---

# ST_HAUSDORFFDISTANCE

2 つの GEOMETRY オブジェクト間の離散 Hausdorff 距離を返します。これは、一方のオブジェクト内の任意の頂点から他方のオブジェクト内の最も近い頂点までの距離のうち最大のものを求めることで、2 つのジオメトリがどれだけ離れているかを測定します。

## 構文 {#syntax}

```sql
ST_HAUSDORFFDISTANCE(<geometry1>, <geometry2>)
```

## 引数 {#arguments}

| 引数          | 説明                         |
|---------------|------------------------------|
| `<geometry1>` | GEOMETRY 式です。            |
| `<geometry2>` | GEOMETRY 式です。            |

## 戻り値の型 {#return-type}

Double。

## 例 {#examples}

```sql
SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('POINT(0 0)'),
  TO_GEOMETRY('POINT(0 1)')
);

┌────────┐
│ result │
├────────┤
│ 1.0    │
└────────┘

SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('LINESTRING(0 0, 1 0)'),
  TO_GEOMETRY('LINESTRING(0 1, 1 1)')
);

┌────────┐
│ result │
├────────┤
│ 1.0    │
└────────┘

SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
  TO_GEOMETRY('POLYGON((2 0, 3 0, 3 1, 2 1, 2 0))')
);

┌────────┐
│ result │
├────────┤
│ 2.0    │
└────────┘
```