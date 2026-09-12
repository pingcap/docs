---
title: GEOHASH_DECODE
summary: 将 Geohash 编码的字符串转换为纬度/经度坐标。
---

# GEOHASH_DECODE

将 [Geohash](https://en.wikipedia.org/wiki/Geohash) 编码的字符串转换为纬度/经度坐标。

## 语法 {#syntax}

```sql
GEOHASH_DECODE('<geohashed-string\>')
```

## 示例 {#examples}

```sql
SELECT GEOHASH_DECODE('ezs42');

┌─────────────────────────────────┐
│     geohash_decode('ezs42')     │
├─────────────────────────────────┤
│ (-5.60302734375,42.60498046875) │
└─────────────────────────────────┘
```