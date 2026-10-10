---
title: DEGREES
summary: 引数 x をラジアンから度に変換して返します。x はラジアンで指定します。
---

# DEGREES

引数 `x` をラジアンから度に変換して返します。`x` はラジアンで指定します。

## 構文 {#syntax}

```sql
DEGREES( <x> )
```

## 例 {#examples}

```sql
SELECT DEGREES(PI());

┌───────────────┐
│ degrees(pi()) │
├───────────────┤
│           180 │
└───────────────┘
```