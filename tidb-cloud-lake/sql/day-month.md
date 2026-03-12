---
title: TO_DAY_OF_MONTH
---

Convert a date or date with time (timestamp/datetime) to a UInt8 number containing the number of the day of the month (1-31).

## Syntax

```sql
TO_DAY_OF_MONTH(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | date/timestamp |

## Aliases

- [DAY](day.md)

## Return Type

`TINYINT`

## Examples

```sql
SELECT NOW(), TO_DAY_OF_MONTH(NOW()), DAY(NOW());

┌──────────────────────────────────────────────────────────────────┐
│            now()           │ to_day_of_month(now()) │ day(now()) │
├────────────────────────────┼────────────────────────┼────────────┤
│ 2024-03-14 23:35:41.947962 │                     14 │         14 │
└──────────────────────────────────────────────────────────────────┘
```