---
title: TO_YYYYMMDD
---

Converts a date or date with time (timestamp/datetime) to a UInt32 number containing the year and month number (YYYY * 10000 + MM * 100 + DD).
## Syntax

```sql
TO_YYYYMMDD(<expr>)
```

## Arguments

| Arguments | Description   |
|-----------|---------------|
| `<expr>`  | date/datetime |

## Return Type

`INT`, returns in `YYYYMMDD` format.

## Examples

```sql
SELECT
  to_yyyymmdd('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────┐
│ to_yyyymmdd('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────┤
│                                  20231112 │
└───────────────────────────────────────────┘
```
