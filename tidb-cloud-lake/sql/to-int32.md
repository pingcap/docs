---
title: TO_INT32
summary: 将值转换为 INT32 数据类型。
---

# TO_INT32

将值转换为 INT32 数据类型。

## 语法 {#syntax}

```sql
TO_INT32( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_INT32('123');

┌─────────────────┐
│ to_int32('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```