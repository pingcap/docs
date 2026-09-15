---
title: TO_UINT32
summary: 将值转换为 UINT32 数据类型。
---

# TO_UINT32

将值转换为 UINT32 数据类型。

## 语法 {#syntax}

```sql
TO_UINT32( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_UINT32('123');

┌──────────────────┐
│ to_uint32('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```