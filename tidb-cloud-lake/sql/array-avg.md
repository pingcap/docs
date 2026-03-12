---
title: ARRAY_AVG
---

Returns the average of the numeric items in an array. `NULL` elements are ignored; non-numeric values raise an error.

## Syntax

```sql
ARRAY_AVG(<array>)
```

## Return Type

Numeric (uses the smallest numeric type that can represent the result).

## Examples

```sql
SELECT ARRAY_AVG([1, 2, 3, 4]) AS avg_int;

┌─────────┐
│ avg_int │
├─────────┤
│     2.5 │
└─────────┘
```

```sql
SELECT ARRAY_AVG([1.5, 2.5, 3.5]) AS avg_decimal;

┌──────────────┐
│ avg_decimal  │
├──────────────┤
│       2.5000 │
└──────────────┘
```

```sql
SELECT ARRAY_AVG([10, NULL, 4]) AS avg_with_null;

┌──────────────┐
│ avg_with_null│
├──────────────┤
│          7.0 │
└──────────────┘
```
