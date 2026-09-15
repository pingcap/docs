---
title: ABS
summary: 返回 x 的绝对值。
---

# ABS

返回 `x` 的绝对值。

## 语法 {#syntax}

```sql
ABS( <x> )
```

## 示例 {#examples}

```sql
SELECT ABS(-5);

┌────────────┐
│ abs((- 5)) │
├────────────┤
│          5 │
└────────────┘
```