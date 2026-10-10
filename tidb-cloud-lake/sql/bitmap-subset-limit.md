---
title: BITMAP_SUBSET_LIMIT
summary: サイズ制限付きで、開始値からの範囲を起点として、元のビットマップのサブビットマップを生成します。
---

# BITMAP_SUBSET_LIMIT

サイズ制限付きで、開始値からの範囲を起点として、元のビットマップのサブビットマップを生成します。

## 構文 {#syntax}

```sql
BITMAP_SUBSET_LIMIT( <bitmap>, <start>, <limit> )
```

## 例 {#examples}

```sql
SELECT BITMAP_SUBSET_LIMIT(BUILD_BITMAP([1,4,5]), 2, 2)::String;

┌────────────────────────────────────────────────────────────┐
│ bitmap_subset_limit(build_bitmap([1, 4, 5]), 2, 2)::string │
├────────────────────────────────────────────────────────────┤
│ 4,5                                                        │
└────────────────────────────────────────────────────────────┘
```