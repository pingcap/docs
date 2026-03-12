---
title: TO_HOUR
---

Converts a date with time (timestamp/datetime) to a UInt8 number containing the number of the hour in 24-hour time (0-23).
This function assumes that if clocks are moved ahead, it is by one hour and occurs at 2 a.m., and if clocks are moved back, it is by one hour and occurs at 3 a.m. (which is not always true – even in Moscow the clocks were twice changed at a different time).

## Syntax

```sql
TO_HOUR(<expr>)
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `<expr>`  | timestamp   |

## Return Type

`TINYINT`

## Examples

```sql
SELECT
    to_hour('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────┐
│ to_hour('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────┤
│                                     9 │
└───────────────────────────────────────┘
```
