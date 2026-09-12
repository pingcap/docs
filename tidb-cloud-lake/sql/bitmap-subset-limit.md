---
title: BITMAP_SUBSET_LIMIT
summary: 从源位图中生成一个子位图，从 start 值指定的范围开始，并带有大小限制。
---

# BITMAP_SUBSET_LIMIT

从源位图中生成一个子位图，从 start 值指定的范围开始，并带有大小限制。

## 语法 {#syntax}

```sql
BITMAP_SUBSET_LIMIT( <bitmap>, <start>, <limit> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_SUBSET_LIMIT(BUILD_BITMAP([1,4,5]), 2, 2)::String;

┌────────────────────────────────────────────────────────────┐
│ bitmap_subset_limit(build_bitmap([1, 4, 5]), 2, 2)::string │
├────────────────────────────────────────────────────────────┤
│ 4,5                                                        │
└────────────────────────────────────────────────────────────┘
```