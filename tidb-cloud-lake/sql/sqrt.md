---
title: SQRT
summary: 非負の数 x の平方根を返します。負の入力に対しては Nan を返します。
---

# SQRT

非負の数 `x` の平方根を返します。負の入力に対しては Nan を返します。

## 構文 {#syntax}

```sql
SQRT( <x> )
```

## 例 {#examples}

```sql
SELECT SQRT(4);

┌─────────┐
│ sqrt(4) │
├─────────┤
│       2 │
└─────────┘
```