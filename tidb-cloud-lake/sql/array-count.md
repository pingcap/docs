---
title: ARRAY_COUNT
summary: Counts the non-NULL elements in an array.
---

# ARRAY_COUNT

Counts the non-`NULL` elements in an array.

## Syntax

```sql
ARRAY_COUNT(<array>)
```

## Return Type

`BIGINT`

## Examples

```sql
SELECT ARRAY_COUNT([1, 2, 3]) AS cnt;

┌─────┐
│ cnt │
├─────┤
│   3 │
└─────┘
```

```sql
SELECT ARRAY_COUNT([1, NULL, 3]) AS cnt_with_null;

┌──────────────┐
│ cnt_with_null│
├──────────────┤
│            2 │
└──────────────┘
```

```sql
SELECT ARRAY_COUNT(['a', 'b', NULL]) AS cnt_text;

┌─────────┐
│ cnt_text│
├─────────┤
│       2 │
└─────────┘
```
