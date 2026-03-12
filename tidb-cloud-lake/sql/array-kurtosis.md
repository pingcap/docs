---
title: ARRAY_KURTOSIS
---

Returns the excess kurtosis of the numeric values in an array. `NULL` elements are ignored; non-numeric elements raise an error.

## Syntax

```sql
ARRAY_KURTOSIS(<array>)
```

## Return Type

Floating-point.

## Examples

```sql
SELECT ARRAY_KURTOSIS([1, 2, 3, 4]) AS kurt;

┌────────────────────────┐
│ kurt                   │
├────────────────────────┤
│ -1.200000000000001     │
└────────────────────────┘
```

```sql
SELECT ARRAY_KURTOSIS([1.5, 2.5, 3.5, 4.5]) AS kurt_decimal;

┌────────────────────────┐
│ kurt_decimal           │
├────────────────────────┤
│ -1.200000000000001     │
└────────────────────────┘
```

```sql
SELECT ARRAY_KURTOSIS([NULL, 2, 3, 4]) AS kurt_null;

┌────────────────┐
│ kurt_null      │
├────────────────┤
│ 0              │
└────────────────┘
```
