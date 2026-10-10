---
title: BITMAP_MAX
summary: ビットマップ内の最大値を取得します。
---

# BITMAP_MAX

ビットマップ内の最大値を取得します。

## 構文 {#syntax}

```sql
BITMAP_MAX( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_MAX(BUILD_BITMAP([1,4,5]));

┌─────────────────────────────────────┐
│ bitmap_max(build_bitmap([1, 4, 5])) │
├─────────────────────────────────────┤
│                                   5 │
└─────────────────────────────────────┘
```