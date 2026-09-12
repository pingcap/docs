---
title: GEOHASH_ENCODE
summary: 将一对纬度和经度坐标转换为 Geohash 编码的字符串。
---

# GEOHASH_ENCODE

将一对纬度和经度坐标转换为 [Geohash](https://en.wikipedia.org/wiki/Geohash) 编码的字符串。

## 语法 {#syntax}

```sql
GEOHASH_ENCODE(lon, lat)
```

## 示例 {#examples}

```sql
SELECT GEOHASH_ENCODE(-5.60302734375, 42.593994140625);

┌────────────────────────────────────────────────────┐
│ geohash_encode((- 5.60302734375), 42.593994140625) │
├────────────────────────────────────────────────────┤
│ ezs42d000000                                       │
└────────────────────────────────────────────────────┘
```