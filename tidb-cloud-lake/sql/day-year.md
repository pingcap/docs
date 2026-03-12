---
title: TO_DAY_OF_YEAR
---

Convert a date or date with time (timestamp/datetime) to a UInt16 number containing the number of the day of the year (1-366).

## Syntax

```sql
TO_DAY_OF_YEAR(<expr>)
```

## Arguments

| Arguments   | Description |
| ----------- | ----------- |
| `<expr>` | date/timestamp |

## Return Type

`SMALLINT`

## Examples

```sql
SELECT
    to_day_of_year('2023-11-12 09:38:18.165575');

┌──────────────────────────────────────────────┐
│ to_day_of_year('2023-11-12 09:38:18.165575') │
├──────────────────────────────────────────────┤
│                                          316 │
└──────────────────────────────────────────────┘
```
