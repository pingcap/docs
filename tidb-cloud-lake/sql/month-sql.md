---
title: TO_MONTH
---

Convert a date or date with time (timestamp/datetime) to a UInt8 number containing the month number (1-12).

## Syntax

```sql
TO_MONTH(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | date/timestamp |

## Aliases

- [MONTH](month.md)

## Return Type

 `TINYINT`

## Examples

```sql
SELECT NOW(), TO_MONTH(NOW()), MONTH(NOW());

┌─────────────────────────────────────────────────────────────┐
│            now()           │ to_month(now()) │ month(now()) │
├────────────────────────────┼─────────────────┼──────────────┤
│ 2024-03-14 23:34:02.161291 │               3 │            3 │
└─────────────────────────────────────────────────────────────┘
```