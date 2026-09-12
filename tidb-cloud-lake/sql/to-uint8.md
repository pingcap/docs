---
title: TO_UINT8
summary: 将一个值转换为 UINT8 数据类型。
---

# TO_UINT8

将一个值转换为 UINT8 数据类型。

## 语法 {#syntax}

```sql
TO_UINT8( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_UINT8('123');

┌─────────────────┐
│ to_uint8('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```