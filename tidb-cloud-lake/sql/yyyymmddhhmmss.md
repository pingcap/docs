---
title: TO_YYYYMMDDHHMMSS
---

Convert a date or date with time (timestamp/datetime) to a UInt64 number containing the year and month number (YYYY * 10000000000 + MM * 100000000 + DD * 1000000 + hh * 10000 + mm * 100 + ss).

## Syntax

```sql
TO_YYYYMMDDHHMMSS(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | date/timestamp |

## Return Type

`BIGINT`, returns in `YYYYMMDDhhmmss` format.

## Examples

```sql
SELECT
  to_yyyymmddhhmmss('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────────────┐
│ to_yyyymmddhhmmss('2023-11-12 09:38:18.165575') │
├─────────────────────────────────────────────────┤
│                                  20231112000000 │
└─────────────────────────────────────────────────┘

SELECT
  to_yyyymmddhhmmss(to_timestamp('2023-11-12 09:38:18.165575'));

┌───────────────────────────────────────────────────────────────┐
│ to_yyyymmddhhmmss(to_timestamp('2023-11-12 09:38:18.165575')) │
├───────────────────────────────────────────────────────────────┤
│                                                20231112093818 │
└───────────────────────────────────────────────────────────────┘
```
