---
title: TO_INT16
summary: 将一个值转换为 INT16 数据类型。
---

# TO_INT16

将一个值转换为 INT16 数据类型。

## 语法 {#syntax}

```sql
TO_INT16( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_INT16('123');

┌─────────────────┐
│ to_int16('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```