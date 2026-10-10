---
title: GREAT_CIRCLE_ANGLE
summary: 球面上の2点間の中心角を度単位で返します。
---

# GREAT_CIRCLE_ANGLE

球面上の2点間の中心角を度単位で返します。各点は、度単位の経度と緯度で指定します。

## 構文 {#syntax}

```sql
GREAT_CIRCLE_ANGLE(<lon1>, <lat1>, <lon2>, <lat2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<lon1>` | 1つ目の点の経度（度単位）。 |
| `<lat1>` | 1つ目の点の緯度（度単位）。 |
| `<lon2>` | 2つ目の点の経度（度単位）。 |
| `<lat2>` | 2つ目の点の緯度（度単位）。 |

## 戻り値の型 {#return-type}

Float32。

## 例 {#examples}

```sql
SELECT GREAT_CIRCLE_ANGLE(55.755831, 37.617673, -55.755831, -37.617673) AS angle;

╭───────────╮
│   angle   │
├───────────┤
│ 127.05919 │
╰───────────╯
```