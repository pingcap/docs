---
title: GREAT_CIRCLE_DISTANCE
summary: 球面上の 2 点間の大円距離をメートル単位で返します。
---

# GREAT_CIRCLE_DISTANCE

球面上の 2 点間の大円距離をメートル単位で返します。各点は、経度と緯度を度単位で指定します。

## 構文 {#syntax}

```sql
GREAT_CIRCLE_DISTANCE(<lon1>, <lat1>, <lon2>, <lat2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<lon1>` | 1 つ目の点の経度（度単位）。 |
| `<lat1>` | 1 つ目の点の緯度（度単位）。 |
| `<lon2>` | 2 つ目の点の経度（度単位）。 |
| `<lat2>` | 2 つ目の点の緯度（度単位）。 |

## 戻り値の型 {#return-type}

Float32。

## 例 {#examples}

```sql
SELECT GREAT_CIRCLE_DISTANCE(55.755831, 37.617673, -55.755831, -37.617673) AS distance;

╭────────────╮
│  distance  │
├────────────┤
│ 14128353.0 │
╰────────────╯
```