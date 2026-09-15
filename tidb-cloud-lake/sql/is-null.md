---
title: IS_NULL
summary: 检查一个值是否为 NULL。
---

# IS_NULL

检查一个值是否为 NULL。

## 语法 {#syntax}

```sql
IS_NULL(<expr>)
```

## 示例 {#examples}

```sql
SELECT IS_NULL(1);

┌────────────┐
│ is_null(1) │
├────────────┤
│ false      │
└────────────┘
```