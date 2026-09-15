---
title: TO_INT64
summary: 将值转换为 INT64 数据类型。
---

# TO_INT64

将值转换为 INT64 数据类型。

## 语法 {#syntax}

```sql
TO_INT64( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_INT64('123');

┌─────────────────┐
│ to_int64('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```