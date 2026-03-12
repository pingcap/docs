---
title: COALESCE
---

Returns the first non-NULL expression within its arguments; if all arguments are NULL, it returns NULL.

## Syntax

```sql
COALESCE(<expr1>[, <expr2> ...])
```

## Examples

```sql
SELECT COALESCE(1), COALESCE(1, NULL), COALESCE(NULL, 1, 2);

┌────────────────────────────────────────────────────────┐
│ coalesce(1) │ coalesce(1, null) │ coalesce(null, 1, 2) │
├─────────────┼───────────────────┼──────────────────────┤
│           1 │                 1 │                    1 │
└────────────────────────────────────────────────────────┘

SELECT COALESCE('a'), COALESCE('a', NULL), COALESCE(NULL, 'a', 'b');

┌────────────────────────────────────────────────────────────────┐
│ coalesce('a') │ coalesce('a', null) │ coalesce(null, 'a', 'b') │
├───────────────┼─────────────────────┼──────────────────────────┤
│ a             │ a                   │ a                        │
└────────────────────────────────────────────────────────────────┘
```