---
title: TO_UINT16
summary: 将值转换为 UINT16 数据类型。
---

# TO_UINT16

将值转换为 UINT16 数据类型。

## 语法 {#syntax}

```sql
TO_UINT16( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_UINT16('123');

┌──────────────────┐
│ to_uint16('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```