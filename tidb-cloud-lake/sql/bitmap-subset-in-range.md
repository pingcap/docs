---
title: BITMAP_SUBSET_IN_RANGE
summary: 指定した範囲内で、ソース bitmap のサブ bitmap を生成します。
---

# BITMAP_SUBSET_IN_RANGE

指定した範囲内で、ソース bitmap のサブ bitmap を生成します。

## 構文 {#syntax}

```sql
BITMAP_SUBSET_IN_RANGE( <bitmap>, <start>, <end> )
```

## 例 {#examples}

```sql
SELECT BITMAP_SUBSET_IN_RANGE(BUILD_BITMAP([5,7,9]), 6, 9)::String;

┌───────────────────────────────────────────────────────────────┐
│ bitmap_subset_in_range(build_bitmap([5, 7, 9]), 6, 9)::string │
├───────────────────────────────────────────────────────────────┤
│ 7                                                             │
└───────────────────────────────────────────────────────────────┘
```