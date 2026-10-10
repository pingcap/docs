---
title: BITMAP_MIN
summary: ビットマップ内の最小値を取得します。
---

# BITMAP_MIN

ビットマップ内の最小値を取得します。

## 構文 {#syntax}

```sql
BITMAP_MIN( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_MIN(BUILD_BITMAP([1,4,5]));

┌─────────────────────────────────────┐
│ bitmap_min(build_bitmap([1, 4, 5])) │
├─────────────────────────────────────┤
│                                   1 │
└─────────────────────────────────────┘
```