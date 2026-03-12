---
title: TO_START_OF_WEEK
---

Returns the first day of the week for a date or a date with time (timestamp/datetime).
The first day of a week can be Sunday or Monday, which is specified by the argument `mode`.

## Syntax

```sql
TO_START_OF_WEEK(<expr> [, mode])
```

## Arguments

| Arguments | Description                                                                                         |
|-----------|-----------------------------------------------------------------------------------------------------|
| `<expr>`  | date/timestamp                                                                                      |
| `[mode]`  | Optional. If it is 0, the result is Sunday, otherwise, the result is Monday. The default value is 0 |

## Return Type

`DATE`, returns date in “YYYY-MM-DD” format.

## Examples

```sql
SELECT
  to_start_of_week('2023-11-12 09:38:18.165575');

┌────────────────────────────────────────────────┐
│ to_start_of_week('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────┤
│ 2023-11-12                                     │
└────────────────────────────────────────────────┘
```
