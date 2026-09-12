---
title: XXHASH32
summary: 计算字符串的 xxHash32 32 位哈希值。如果参数为 NULL，则返回值为 UInt32 或 NULL。
---

# XXHASH32

计算字符串的 xxHash32 32 位哈希值。如果参数为 NULL，则返回值为 UInt32 或 NULL。

## 语法 {#syntax}

```sql
XXHASH32(expr)
```

## 示例 {#examples}

```sql
SELECT XXHASH32('1234567890');

┌────────────────────────┐
│ xxhash32('1234567890') │
├────────────────────────┤
│             3896585587 │
└────────────────────────┘
```