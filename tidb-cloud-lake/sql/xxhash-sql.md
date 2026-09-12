---
title: XXHASH64
summary: 计算字符串的 xxHash64 64 位哈希值。如果参数为 NULL，则返回值为 UInt64 或 NULL。
---

# XXHASH64

计算字符串的 xxHash64 64 位哈希值。如果参数为 NULL，则返回值为 UInt64 或 NULL。

## 语法 {#syntax}

```sql
XXHASH64(expr)
```

## 示例 {#examples}

```sql
SELECT XXHASH64('1234567890');

┌────────────────────────┐
│ xxhash64('1234567890') │
├────────────────────────┤
│   12237639266330420150 │
└────────────────────────┘
```