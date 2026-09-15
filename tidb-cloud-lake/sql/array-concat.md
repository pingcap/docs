---
title: ARRAY_CONCAT
summary: 拼接两个数组。
---

# ARRAY_CONCAT

拼接两个数组。

## 语法 {#syntax}

```sql
ARRAY_CONCAT( <array1>, <array2> )
```

## 示例 {#examples}

```sql
SELECT ARRAY_CONCAT([1, 2], [3, 4]);

┌──────────────────────────────┐
│ array_concat([1, 2], [3, 4]) │
├──────────────────────────────┤
│ [1,2,3,4]                    │
└──────────────────────────────┘
```