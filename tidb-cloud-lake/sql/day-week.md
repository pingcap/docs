---
title: TO_DAY_OF_WEEK
---

Converts a date or date with time (timestamp/datetime) to a UInt8 number containing the number of the day of the week (Monday is 1, and Sunday is 7).

## Syntax

```sql
TO_DAY_OF_WEEK(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | date/timestamp |

## Return Type

`TINYINT`

## Examples

```sql

SELECT
    to_day_of_week('2023-11-12 09:38:18.165575');

┌──────────────────────────────────────────────┐
│ to_day_of_week('2023-11-12 09:38:18.165575') │
├──────────────────────────────────────────────┤
│                                            7 │
└──────────────────────────────────────────────┘
```
