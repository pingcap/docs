---
title: BITMAP_UNION
summary: 通过执行逻辑 UNION 操作，统计 bitmap 中被设置为 1 的位数。
---

# BITMAP_UNION

通过执行逻辑 UNION 操作，统计 bitmap 中被设置为 1 的位数。

## 语法 {#syntax}

```sql
BITMAP_UNION( <bitmap> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_UNION(TO_BITMAP('1, 3, 5'))::String;

┌────────────────────────────────────────────┐
│ bitmap_union(to_bitmap('1, 3, 5'))::string │
├────────────────────────────────────────────┤
│ 1,3,5                                      │
└────────────────────────────────────────────┘
```