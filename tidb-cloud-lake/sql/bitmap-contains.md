---
title: BITMAP_CONTAINS
summary: ビットマップに特定の値が含まれているかを確認します。
---

# BITMAP_CONTAINS

ビットマップに特定の値が含まれているかを確認します。

## 構文 {#syntax}

```sql
BITMAP_CONTAINS( <bitmap>, <value> )
```

## 例 {#examples}

```sql
SELECT BITMAP_CONTAINS(BUILD_BITMAP([1,4,5]), 1);

┌─────────────────────────────────────────────┐
│ bitmap_contains(build_bitmap([1, 4, 5]), 1) │
├─────────────────────────────────────────────┤
│ true                                        │
└─────────────────────────────────────────────┘
```