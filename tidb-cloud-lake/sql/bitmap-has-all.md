---
title: BITMAP_HAS_ALL
summary: 1 番目の bitmap に 2 番目の bitmap のすべてのビットが含まれているかを確認します。
---

# BITMAP_HAS_ALL

1 番目の bitmap に 2 番目の bitmap のすべてのビットが含まれているかを確認します。

## 構文 {#syntax}

```sql
BITMAP_HAS_ALL( <bitmap1>, <bitmap2> )
```

## 例 {#examples}

```sql
SELECT BITMAP_HAS_ALL(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([1,2]));

┌───────────────────────────────────────────────────────────────┐
│ bitmap_has_all(build_bitmap([1, 4, 5]), build_bitmap([1, 2])) │
├───────────────────────────────────────────────────────────────┤
│ false                                                         │
└───────────────────────────────────────────────────────────────┘
```