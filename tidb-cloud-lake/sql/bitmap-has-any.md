---
title: BITMAP_HAS_ANY
summary: 1 つ目の bitmap に、2 つ目の bitmap のビットと一致するビットがあるかどうかを確認します。
---

# BITMAP_HAS_ANY

1 つ目の bitmap に、2 つ目の bitmap のビットと一致するビットがあるかどうかを確認します。

## 構文 {#syntax}

```sql
BITMAP_HAS_ANY( <bitmap1>, <bitmap2> )
```

## 例 {#examples}

```sql
SELECT BITMAP_HAS_ANY(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([1,2]));

┌───────────────────────────────────────────────────────────────┐
│ bitmap_has_any(build_bitmap([1, 4, 5]), build_bitmap([1, 2])) │
├───────────────────────────────────────────────────────────────┤
│ true                                                          │
└───────────────────────────────────────────────────────────────┘
```