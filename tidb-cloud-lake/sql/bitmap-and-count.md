---
title: BITMAP_AND_COUNT
summary: 論理 AND 演算を実行して、ビットマップ内で 1 に設定されているビット数をカウントします。
---

# BITMAP_AND_COUNT

論理 AND 演算を実行して、ビットマップ内で 1 に設定されているビット数をカウントします。

## 構文 {#syntax}

```sql
BITMAP_AND_COUNT( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_AND_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_and_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```