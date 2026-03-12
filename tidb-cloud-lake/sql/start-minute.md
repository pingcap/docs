---
title: TO_START_OF_MINUTE
---

Rounds down a date with time (timestamp/datetime) to the start of the minute.

## Syntax

```sql
TO_START_OF_MINUTE( <expr> )
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
  to_start_of_minute('2023-11-12 09:38:18.165575');

┌──────────────────────────────────────────────────┐
│ to_start_of_minute('2023-11-12 09:38:18.165575') │
├──────────────────────────────────────────────────┤
│ 2023-11-12 09:38:00                              │
└──────────────────────────────────────────────────┘
```
