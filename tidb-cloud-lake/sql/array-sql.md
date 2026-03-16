---
title: ARRAY
---

Builds an array literal from the supplied expressions. Each argument is evaluated and stored in order. All elements must be castable to a common type.

## Syntax

```sql
ARRAY(<expr1>, <expr2>, ... )
```

## Return Type

`ARRAY`

## Examples

```sql
SELECT ARRAY(1, 2, 3) AS arr_int;

┌─────────┐
│ arr_int │
├─────────┤
│ [1,2,3] │
└─────────┘
```

```sql
SELECT ARRAY('alpha', UPPER('beta')) AS arr_text;

┌───────────┐
│ arr_text  │
├───────────┤
│ ["alpha","BETA"] │
└───────────┘
```

```sql
SELECT ARRAY(1, NULL, 3) AS arr_with_null;

┌────────────────┐
│ arr_with_null  │
├────────────────┤
│ [1,NULL,3]     │
└────────────────┘
```
