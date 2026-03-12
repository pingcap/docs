---
title: ARRAY_CONCAT
---

Concats two arrays.

## Syntax

```sql
ARRAY_CONCAT( <array1>, <array2> )
```

## Examples

```sql
SELECT ARRAY_CONCAT([1, 2], [3, 4]);

┌──────────────────────────────┐
│ array_concat([1, 2], [3, 4]) │
├──────────────────────────────┤
│ [1,2,3,4]                    │
└──────────────────────────────┘
```
