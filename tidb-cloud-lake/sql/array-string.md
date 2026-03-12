---
title: ARRAY_TO_STRING
---

Concatenates the string elements of an array into a single string, separated by a delimiter. `NULL` elements are skipped.

## Syntax

```sql
ARRAY_TO_STRING(<array_of_strings>, <delimiter>)
```

## Return Type

`STRING`

## Examples

```sql
SELECT ARRAY_TO_STRING(['a', 'b', 'c'], ',') AS joined;

┌────────┐
│ joined │
├────────┤
│ a,b,c  │
└────────┘
```

```sql
SELECT ARRAY_TO_STRING([NULL, 'x', 'y'], '-') AS joined_no_nulls;

┌──────────────────┐
│ joined_no_nulls  │
├──────────────────┤
│ x-y              │
└──────────────────┘
```
