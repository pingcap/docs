---
title: GEOHASH_DECODE
summary: Geohash でエンコードされた文字列を緯度/経度座標に変換します。
---

# GEOHASH_DECODE

[Geohash](https://en.wikipedia.org/wiki/Geohash) でエンコードされた文字列を緯度/経度座標に変換します。

## 構文 {#syntax}

```sql
GEOHASH_DECODE('<geohashed-string\>')
```

## 例 {#examples}

```sql
SELECT GEOHASH_DECODE('ezs42');

┌─────────────────────────────────┐
│     geohash_decode('ezs42')     │
├─────────────────────────────────┤
│ (-5.60302734375,42.60498046875) │
└─────────────────────────────────┘
```