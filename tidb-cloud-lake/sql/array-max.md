---
title: ARRAY_MAX
---

Returns the largest numeric value in an array. `NULL` elements are skipped; non-numeric values cause an error.

## Syntax

```sql
ARRAY_MAX(<array>)
```

## Return Type

Same numeric type as the array elements.

## Examples

```sql
SELECT ARRAY_MAX([5, 2, 9, -1]) AS max_int;

┌─────────┐
│ max_int │
├─────────┤
│       9 │
└─────────┘
```

```sql
SELECT ARRAY_MAX([1.5, -2.25, 3.0]) AS max_decimal;

┌─────────────┐
│ max_decimal │
├─────────────┤
│      3.00   │
└─────────────┘
```

```sql
SELECT ARRAY_MAX([NULL, 10, 4]) AS max_with_null;

┌───────────────┐
│ max_with_null │
├───────────────┤
│           10  │
└───────────────┘
```
