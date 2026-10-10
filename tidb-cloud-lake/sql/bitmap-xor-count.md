---
title: BITMAP_XOR_COUNT
summary: 論理 XOR（排他的 OR）演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。
---

# BITMAP_XOR_COUNT

論理 XOR（排他的 OR）演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。

## 構文 {#syntax}

```sql
BITMAP_XOR_COUNT( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_XOR_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_xor_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```