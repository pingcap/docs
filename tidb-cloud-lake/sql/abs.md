---
title: ABS
summary: x の絶対値を返します。
---

# ABS

`x` の絶対値を返します。

## 構文 {#syntax}

```sql
ABS( <x> )
```

## 例 {#examples}

```sql
SELECT ABS(-5);

┌────────────┐
│ abs((- 5)) │
├────────────┤
│          5 │
└────────────┘
```