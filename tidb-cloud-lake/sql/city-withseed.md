---
title: CITY64WITHSEED
summary: 计算字符串的 City64WithSeed 64 位哈希值。
---

# CITY64WITHSEED

计算字符串的 City64WithSeed 64 位哈希值。

## 语法 {#syntax}

```sql
CITY64WITHSEED(<expr1>, <expr2>)
```

## 示例 {#examples}

```sql
SELECT CITY64WITHSEED('1234567890', 12);

┌──────────────────────────────────┐
│ city64withseed('1234567890', 12) │
├──────────────────────────────────┤
│             10660895976650300430 │
└──────────────────────────────────┘
```