---
title: ARRAY_MEDIAN
---

Returns the median of the numeric values in an array. `NULL` elements are ignored.

## Syntax

```sql
ARRAY_MEDIAN(<array>)
```

## Return Type

Numeric. For even-length inputs the result is the average of the two middle values.

## Examples

```sql
SELECT ARRAY_MEDIAN([1, 3, 2, 4]) AS med_even;

┌────────┐
│ med_even │
├────────┤
│    2.5 │
└────────┘
```

```sql
SELECT ARRAY_MEDIAN([1, 3, 5]) AS med_odd;

┌────────┐
│ med_odd│
├────────┤
│    3.0 │
└────────┘
```

```sql
SELECT ARRAY_MEDIAN([NULL, 10, 20, 30]) AS med_null;

┌────────┐
│ med_null│
├────────┤
│   20.0 │
└────────┘
```
