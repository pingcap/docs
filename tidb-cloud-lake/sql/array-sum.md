---
title: ARRAY_SUM
---

Sums the numeric elements in an array. `NULL` items are skipped, and non-numeric values raise an error.

## Syntax

```sql
ARRAY_SUM(<array>)
```

## Return Type

Numeric (matches the widest numeric type in the array).

## Examples

```sql
SELECT ARRAY_SUM([1, 2, 3, 4]) AS total;

┌───────┐
│ total │
├───────┤
│    10 │
└───────┘
```

```sql
SELECT ARRAY_SUM([1.5, 2.25, 3.0]) AS total;

┌────────┐
│ total  │
├────────┤
│   6.75 │
└────────┘
```

```sql
SELECT ARRAY_SUM([10, NULL, -3]) AS total;

┌───────┐
│ total │
├───────┤
│     7 │
└───────┘
```

## Related

- [ARRAY_AGGREGATE](array-aggregate)
