---
title: BITMAP_OR_COUNT
summary: 論理 OR 演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。
---

# BITMAP_OR_COUNT

論理 OR 演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。

## 構文 {#syntax}

```sql
BITMAP_OR_COUNT( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_OR_COUNT(TO_BITMAP('1, 3, 5'));

┌───────────────────────────────────────┐
│ bitmap_or_count(to_bitmap('1, 3, 5')) │
├───────────────────────────────────────┤
│                                     3 │
└───────────────────────────────────────┘
```