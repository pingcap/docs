---
title: ARRAY_SKEWNESS
---

Returns the skewness of numeric values in an array. `NULL` items are ignored; non-numeric items raise an error.

## Syntax

```sql
ARRAY_SKEWNESS(<array>)
```

## Return Type

Floating-point.

## Examples

```sql
SELECT ARRAY_SKEWNESS([1, 2, 3, 4]) AS skew;

┌──────┐
│ skew │
├──────┤
│    0 │
└──────┘
```

```sql
SELECT ARRAY_SKEWNESS([1.5, 2.5, 3.5, 4.5]) AS skew_decimal;

┌────────────┐
│ skew_decimal│
├────────────┤
│          0 │
└────────────┘
```

```sql
SELECT ARRAY_SKEWNESS([NULL, 2, 3, 10]) AS skew_null;

┌────────────────────┐
│ skew_null          │
├────────────────────┤
│ 1.6300591617118865 │
└────────────────────┘
```
