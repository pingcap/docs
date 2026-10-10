---
title: FACTORIAL
summary: x の階乗を返します。x が 0 以下の場合、この関数は 0 を返します。
---

# FACTORIAL

`x` の階乗を返します。`x` が 0 以下の場合、この関数は 0 を返します。

## 構文 {#syntax}

```sql
FACTORIAL( <x> )
```

## 例 {#examples}

```sql
SELECT FACTORIAL(5);

┌──────────────┐
│ factorial(5) │
├──────────────┤
│          120 │
└──────────────┘
```