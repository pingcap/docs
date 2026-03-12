---
title: TO_START_OF_TEN_MINUTES
---

Rounds down a date with time (timestamp/datetime) to the start of the ten-minute interval.

## Syntax

```sql
TO_START_OF_TEN_MINUTES(<expr>)
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
  to_start_of_ten_minutes('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────────────────┐
│ to_start_of_ten_minutes('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────────────────┤
│ 2023-11-12 09:30:00                                   │
└───────────────────────────────────────────────────────┘
```
