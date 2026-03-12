---
title: TOMORROW
---

Returns tomorrow date, same as `today() + 1`.

## Syntax

```sql
TOMORROW()
```

## Return Type

`DATE`, returns date in “YYYY-MM-DD” format.

## Examples

```sql
SELECT TOMORROW(), TODAY()+1;

┌──────────────────────────┐
│ tomorrow() │ today() + 1 │
├────────────┼─────────────┤
│ 2024-05-23 │ 2024-05-23  │
└──────────────────────────┘
```