---
title: ARRAY_GENERATE_RANGE
---

Builds an array of evenly spaced integers between a start and end value. The `end` bound is exclusive.

## Syntax

```sql
ARRAY_GENERATE_RANGE(<start>, <end>[, <step>])
```

- `<start>`: First value to include.
- `<end>`: Exclusive upper (or lower) bound.
- `<step>`: Optional increment (default `1`). Negative steps produce descending sequences.

## Return Type

`ARRAY`

## Examples

```sql
SELECT ARRAY_GENERATE_RANGE(1, 5) AS seq;

┌──────────┐
│ seq      │
├──────────┤
│ [1,2,3,4]│
└──────────┘
```

```sql
SELECT ARRAY_GENERATE_RANGE(0, 6, 2) AS seq_step;

┌────────────┐
│ seq_step   │
├────────────┤
│ [0,2,4]    │
└────────────┘
```

```sql
SELECT ARRAY_GENERATE_RANGE(5, 0, -2) AS seq_down;

┌────────────┐
│ seq_down   │
├────────────┤
│ [5,3,1]    │
└────────────┘
```
