---
title: TO_FLOAT32
summary: 将值转换为 FLOAT32 数据类型。
---

# TO_FLOAT32

将值转换为 FLOAT32 数据类型。

## 语法 {#syntax}

```sql
TO_FLOAT32( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_FLOAT32('1.2');

┌───────────────────┐
│ to_float32('1.2') │
├───────────────────┤
│               1.2 │
└───────────────────┘
```