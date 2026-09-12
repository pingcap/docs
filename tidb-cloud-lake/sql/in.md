---
title: NOT ] IN
summary: 检查某个值是否（或是否不）在显式列表中。
---

# NOT ] IN

检查某个值是否（或是否不）在显式列表中。

## 语法 {#syntax}

```sql
<value> [ NOT ] IN (<value1>, <value2> ...)
```

## 示例 {#examples}

```sql
SELECT 1 NOT IN (2, 3);

┌────────────────┐
│ 1 not in(2, 3) │
├────────────────┤
│ true           │
└────────────────┘
```