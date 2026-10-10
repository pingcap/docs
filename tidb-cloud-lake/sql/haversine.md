---
title: HAVERSINE
summary: Haversine formula を使用して、地球表面上の 2 点間の大円距離をキロメートル単位で計算します。2 点は緯度と経度を度単位で指定します。
---

# HAVERSINE

[Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) を使用して、地球表面上の 2 点間の大円距離をキロメートル単位で計算します。2 点は緯度と経度を度単位で指定します。

## 構文 {#syntax}

```sql
HAVERSINE(<lat1>, <lon1>, <lat2>, <lon2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|------------------------------------|
| `<lat1>`  | 1 つ目の点の緯度です。   |
| `<lon1>`  | 1 つ目の点の経度です。  |
| `<lat2>`  | 2 つ目の点の緯度です。  |
| `<lon2>`  | 2 つ目の点の経度です。 |

## 戻り値の型 {#return-type}

Double。

## 例 {#examples}

```sql
SELECT
  HAVERSINE(40.7127, -74.0059, 34.0500, -118.2500) AS distance

┌────────────────┐
│    distance    │
├────────────────┤
│ 3936.390533556 │
└────────────────┘
```