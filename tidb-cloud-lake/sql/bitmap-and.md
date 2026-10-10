---
title: BITMAP_AND
summary: 2 つのビットマップに対してビット単位の AND 演算を実行します。
---

# BITMAP_AND

2 つのビットマップに対してビット単位の AND 演算を実行します。

## 構文 {#syntax}

```sql
BITMAP_AND( <bitmap1>, <bitmap2> )
```

## 例 {#examples}

```sql
SELECT BITMAP_AND(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([4,5]))::String;

┌───────────────────────────────────────────────────────────────────┐
│ bitmap_and(build_bitmap([1, 4, 5]), build_bitmap([4, 5]))::string │
├───────────────────────────────────────────────────────────────────┤
│ 4,5                                                               │
└───────────────────────────────────────────────────────────────────┘
```