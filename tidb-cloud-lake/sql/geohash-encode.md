---
title: GEOHASH_ENCODE
summary: 緯度と経度の座標の組を Geohash エンコード文字列に変換します。
---

# GEOHASH_ENCODE

緯度と経度の座標の組を [Geohash](https://en.wikipedia.org/wiki/Geohash) エンコード文字列に変換します。

## 構文 {#syntax}

```sql
GEOHASH_ENCODE(lon, lat)
```

## 例 {#examples}

```sql
SELECT GEOHASH_ENCODE(-5.60302734375, 42.593994140625);

┌────────────────────────────────────────────────────┐
│ geohash_encode((- 5.60302734375), 42.593994140625) │
├────────────────────────────────────────────────────┤
│ ezs42d000000                                       │
└────────────────────────────────────────────────────┘
```