---
title: ARRAY_ANY
---

Returns the first non-`NULL` element from an array. Equivalent to `ARRAY_AGGREGATE(<array>, 'ANY')`.

## Syntax

```sql
ARRAY_ANY(<array>)
```

## Return Type

Same as the array element type.

## Examples

```sql
SELECT ARRAY_ANY(['a', 'b', 'c']) AS first_item;

┌────────────┐
│ first_item │
├────────────┤
│ a          │
└────────────┘
```

```sql
SELECT ARRAY_ANY([NULL, 'x', 'y']) AS first_non_null;

┌────────────────┐
│ first_non_null │
├────────────────┤
│ x              │
└────────────────┘
```

```sql
SELECT ARRAY_ANY([NULL, 10, 20]) AS first_number;

┌──────────────┐
│ first_number │
├──────────────┤
│           10 │
└──────────────┘
```
