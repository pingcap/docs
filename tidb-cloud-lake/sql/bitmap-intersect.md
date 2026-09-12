---
title: BITMAP_INTERSECT
summary: 通过执行逻辑 INTERSECT 操作，统计 bitmap 中值为 1 的位数。
---

# BITMAP_INTERSECT

通过执行逻辑 INTERSECT 操作，统计 bitmap 中值为 1 的位数。

## 语法 {#syntax}

```sql
BITMAP_INTERSECT( <bitmap> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_INTERSECT(TO_BITMAP('1, 3, 5'))::String;

┌────────────────────────────────────────────────┐
│ bitmap_intersect(to_bitmap('1, 3, 5'))::string │
├────────────────────────────────────────────────┤
│ 1,3,5                                          │
└────────────────────────────────────────────────┘
```