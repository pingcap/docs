---
title: BITMAP_NOT_COUNT
summary: 通过执行逻辑 NOT 操作，统计 bitmap 中值为 0 的位数。
---

# BITMAP_NOT_COUNT

通过执行逻辑 NOT 操作，统计 bitmap 中值为 0 的位数。

## 语法 {#syntax}

```sql
BITMAP_NOT_COUNT( <bitmap> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_NOT_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_not_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```