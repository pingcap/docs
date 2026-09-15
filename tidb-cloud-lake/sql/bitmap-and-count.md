---
title: BITMAP_AND_COUNT
summary: 通过执行逻辑 AND 运算，统计位图中设置为 1 的位数。
---

# BITMAP_AND_COUNT

通过执行逻辑 AND 运算，统计位图中设置为 1 的位数。

## 语法 {#syntax}

```sql
BITMAP_AND_COUNT( <bitmap> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_AND_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_and_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```