---
title: CITY64WITHSEED
summary: 文字列に対して City64WithSeed の 64 ビットハッシュを計算します。
---

# CITY64WITHSEED

文字列に対して City64WithSeed の 64 ビットハッシュを計算します。

## 構文 {#syntax}

```sql
CITY64WITHSEED(<expr1>, <expr2>)
```

## 例 {#examples}

```sql
SELECT CITY64WITHSEED('1234567890', 12);

┌──────────────────────────────────┐
│ city64withseed('1234567890', 12) │
├──────────────────────────────────┤
│             10660895976650300430 │
└──────────────────────────────────┘
```