---
title: TO_START_OF_HOUR
---

Rounds down a date with time (timestamp/datetime) to the start of the hour.
## Syntax

```sql
TO_START_OF_HOUR(<expr>)
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
  to_start_of_hour('2023-11-12 09:38:18.165575');

┌────────────────────────────────────────────────┐
│ to_start_of_hour('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────┤
│ 2023-11-12 09:00:00                            │
└────────────────────────────────────────────────┘
```
