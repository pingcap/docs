---
title: TO_FLOAT64
summary: 将一个值转换为 FLOAT64 数据类型。
---

# TO_FLOAT64

将一个值转换为 FLOAT64 数据类型。

## 语法 {#syntax}

```sql
TO_FLOAT64( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_FLOAT64('1.2');

┌───────────────────┐
│ to_float64('1.2') │
├───────────────────┤
│               1.2 │
└───────────────────┘
```