---
title: BITMAP_NOT_COUNT
summary: 論理 NOT 演算を実行して、bitmap 内で 0 に設定されているビット数をカウントします。
---

# BITMAP_NOT_COUNT

論理 NOT 演算を実行して、bitmap 内で 0 に設定されているビット数をカウントします。

## 構文 {#syntax}

```sql
BITMAP_NOT_COUNT( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_NOT_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_not_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```