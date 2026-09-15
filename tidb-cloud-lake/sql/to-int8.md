---
title: TO_INT8
summary: 将值转换为 INT8 数据类型。
---

# TO_INT8

将值转换为 INT8 数据类型。

## 语法 {#syntax}

```sql
TO_INT8( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_INT8('123');

┌────────────────┐
│ to_int8('123') │
│      UInt8     │
├────────────────┤
│            123 │
└────────────────┘
```