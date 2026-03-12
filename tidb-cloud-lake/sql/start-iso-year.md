---
title: TO_START_OF_ISO_YEAR
---

Returns the first day of the ISO year for a date or a date with time (timestamp/datetime).

## Syntax

```sql
TO_START_OF_ISO_YEAR(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | date/timestamp |

## Return Type

`DATE`, returns date in “YYYY-MM-DD” format.

## Examples

```sql
SELECT
  to_start_of_iso_year('2023-11-12 09:38:18.165575');

┌────────────────────────────────────────────────────┐
│ to_start_of_iso_year('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────────┤
│ 2023-01-02                                         │
└────────────────────────────────────────────────────┘
```
