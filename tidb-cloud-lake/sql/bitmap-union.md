---
title: BITMAP_UNION
summary: 論理 UNION 演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。
---

# BITMAP_UNION

論理 UNION 演算を実行して、bitmap 内で 1 に設定されているビット数をカウントします。

## 構文 {#syntax}

```sql
BITMAP_UNION( <bitmap> )
```

## 例 {#examples}

```sql
SELECT BITMAP_UNION(TO_BITMAP('1, 3, 5'))::String;

┌────────────────────────────────────────────┐
│ bitmap_union(to_bitmap('1, 3, 5'))::string │
├────────────────────────────────────────────┤
│ 1,3,5                                      │
└────────────────────────────────────────────┘
```