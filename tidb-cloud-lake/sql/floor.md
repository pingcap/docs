---
title: FLOOR
summary: 数値を切り捨てます。
---

# FLOOR

数値を切り捨てます。

## 構文 {#syntax}

```sql
FLOOR( <x> )
```

## 例 {#examples}

```sql
SELECT FLOOR(1.23);

┌─────────────┐
│ floor(1.23) │
├─────────────┤
│           1 │
└─────────────┘
```