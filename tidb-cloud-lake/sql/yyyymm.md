---
title: TO_YYYYMM
---

Converts a date or date with time (timestamp/datetime) to a UInt32 number containing the year and month number.

## Syntax

```sql
TO_YYYYMM(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | date/timestamp |

## Return Type

`INT`, returns in `YYYYMM` format.

## Examples

```sql
SELECT
  to_yyyymm('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────┐
│ to_yyyymm('2023-11-12 09:38:18.165575') │
│                  UInt32                 │
├─────────────────────────────────────────┤
│                                  202311 │
└─────────────────────────────────────────┘
```
