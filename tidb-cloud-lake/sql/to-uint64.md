---
title: TO_UINT64
summary: 将一个值转换为 UINT64 数据类型。
---

# TO_UINT64

将一个值转换为 UINT64 数据类型。

## 语法 {#syntax}

```sql
TO_UINT64( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_UINT64('123');

┌──────────────────┐
│ to_uint64('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```