---
title: BITMAP_INTERSECT
summary: 論理 INTERSECT 演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。
---

# BITMAP_INTERSECT

論理 INTERSECT 演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。

## 構文 {#syntax}

```sql
BITMAP_INTERSECT( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_INTERSECT(TO_BITMAP('1, 3, 5'))::String;

┌────────────────────────────────────────────────┐
│ bitmap_intersect(to_bitmap('1, 3, 5'))::string │
├────────────────────────────────────────────────┤
│ 1,3,5                                          │
└────────────────────────────────────────────────┘
```