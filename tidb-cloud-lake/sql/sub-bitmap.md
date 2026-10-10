---
title: SUB_BITMAP
summary: 開始インデックスから指定したサイズで、ソース bitmap のサブ bitmap を生成します。
---

# SUB_BITMAP

開始インデックスから指定したサイズで、ソース bitmap のサブ bitmap を生成します。

## 構文 {#syntax}

```sql
SUB_BITMAP( <bitmap>, <start>, <size> )
```

## 例 {#examples}

```sql
SELECT SUB_BITMAP(BUILD_BITMAP([1, 2, 3, 4, 5]), 1, 3)::String;

┌─────────────────────────────────────────────────────────┐
│ sub_bitmap(build_bitmap([1, 2, 3, 4, 5]), 1, 3)::string │
├─────────────────────────────────────────────────────────┤
│ 2,3,4                                                   │
└─────────────────────────────────────────────────────────┘
```