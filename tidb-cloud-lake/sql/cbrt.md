---
title: CBRT
summary: 非負の数 x の立方根を返します。
---

# CBRT

非負の数 `x` の立方根を返します。

## 構文 {#syntax}

```sql
CBRT( <x> )
```

## 例 {#examples}

```sql
SELECT CBRT(27);

┌──────────┐
│ cbrt(27) │
├──────────┤
│        3 │
└──────────┘
```