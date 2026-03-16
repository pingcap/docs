---
title: YESTERDAY
---

Returns yesterday date, same as `today() - 1`.

## Syntax

```sql
YESTERDAY()
```

## Return Type

`DATE`, returns date in “YYYY-MM-DD” format.

## Examples

```sql
SELECT YESTERDAY(), TODAY()-1;

┌───────────────────────────┐
│ yesterday() │ today() - 1 │
├─────────────┼─────────────┤
│ 2024-05-21  │ 2024-05-21  │
└───────────────────────────┘
```
