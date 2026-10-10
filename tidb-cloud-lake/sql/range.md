---
title: RANGE
summary: [start, end) で収集された配列を返します。
---

# RANGE

[start, end) で収集された配列を返します。

## 構文 {#syntax}

```sql
RANGE( <start>, <end> )
```

## 例 {#examples}

```sql
SELECT RANGE(1, 5);

┌───────────────┐
│  range(1, 5)  │
├───────────────┤
│ [1,2,3,4]     │
└───────────────┘
```