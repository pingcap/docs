---
title: UNNEST
summary: 将数组展开并返回元素集合。
---

# UNNEST

将数组展开并返回元素集合。

## 语法 {#syntax}

```sql
UNNEST( <array> )
```

## 示例 {#examples}

```sql
SELECT UNNEST([1, 2]);

┌─────────────────┐
│  unnest([1, 2]) │
├─────────────────┤
│               1 │
│               2 │
└─────────────────┘

-- UNNEST(array) can be used as a table function.
SELECT * FROM UNNEST([1, 2]);

┌─────────────────┐
│      value      │
├─────────────────┤
│               1 │
│               2 │
└─────────────────┘
```