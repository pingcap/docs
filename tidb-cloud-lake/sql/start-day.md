---
title: TO_START_OF_DAY
---

Rounds down a date with time (timestamp/datetime) to the start of the day.
## Syntax

```sql
TO_START_OF_DAY( <expr> )
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `<expr>`  | timestamp   |

## Return Type

`TIMESTAMP`, returns date in “YYYY-MM-DD hh:mm:ss.ffffff” format.

## Examples

```sql
SELECT
  to_start_of_day('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────────┐
│ to_start_of_day('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────────┤
│ 2023-11-12 00:00:00                           │
└───────────────────────────────────────────────┘
```
