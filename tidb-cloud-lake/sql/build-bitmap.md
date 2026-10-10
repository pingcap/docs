---
title: BUILD_BITMAP
summary: 正の整数の配列を BITMAP 値に変換します。
---

# BUILD_BITMAP

正の整数の配列を BITMAP 値に変換します。

## 構文 {#syntax}

```sql
BUILD_BITMAP( <expr> )
```

## 例 {#examples}

```sql
SELECT BUILD_BITMAP([1,4,5])::String;

┌─────────────────────────────────┐
│ build_bitmap([1, 4, 5])::string │
├─────────────────────────────────┤
│ 1,4,5                           │
└─────────────────────────────────┘
```