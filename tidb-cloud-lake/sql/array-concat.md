---
title: ARRAY_CONCAT
summary: 2 つの配列を連結します。
---

# ARRAY_CONCAT

2 つの配列を連結します。

## 構文 {#syntax}

```sql
ARRAY_CONCAT( <array1>, <array2> )
```

## 例 {#examples}

```sql
SELECT ARRAY_CONCAT([1, 2], [3, 4]);

┌──────────────────────────────┐
│ array_concat([1, 2], [3, 4]) │
├──────────────────────────────┤
│ [1,2,3,4]                    │
└──────────────────────────────┘
```