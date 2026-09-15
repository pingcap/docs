---
title: IS_NOT_NULL
summary: 检查一个值是否不是 NULL。
---

# IS_NOT_NULL

检查一个值是否不是 NULL。

## 语法 {#syntax}

```sql
IS_NOT_NULL(<expr>)
```

## 示例 {#examples}

```sql
SELECT IS_NOT_NULL(1);

┌────────────────┐
│ is_not_null(1) │
├────────────────┤
│ true           │
└────────────────┘
```