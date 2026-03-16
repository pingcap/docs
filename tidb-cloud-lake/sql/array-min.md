---
title: ARRAY_MIN
---

Returns the smallest numeric value in an array. `NULL` elements are skipped; non-numeric values cause an error.

## Syntax

```sql
ARRAY_MIN(<array>)
```

## Return Type

Same numeric type as the array elements.

## Examples

```sql
SELECT ARRAY_MIN([5, 2, 9, -1]) AS min_int;

┌─────────┐
│ min_int │
├─────────┤
│      -1 │
└─────────┘
```

```sql
SELECT ARRAY_MIN([1.5, -2.25, 3.0]) AS min_decimal;

┌──────────────┐
│ min_decimal  │
├──────────────┤
│       -2.25  │
└──────────────┘
```

```sql
SELECT ARRAY_MIN([NULL, 10, 4]) AS min_with_null;

┌──────────────┐
│ min_with_null│
├──────────────┤
│            4 │
└──────────────┘
```
