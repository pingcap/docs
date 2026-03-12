---
title: TO_YEAR
---

Converts a date or date with time (timestamp/datetime) to a UInt16 number containing the year number (AD).

## Syntax

```sql
TO_YEAR(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | date/timestamp |

## Aliases

- [YEAR](year.md)

## Return Type

 `SMALLINT`

## Examples

```sql
SELECT NOW(), TO_YEAR(NOW()), YEAR(NOW());

┌───────────────────────────────────────────────────────────┐
│            now()           │ to_year(now()) │ year(now()) │
├────────────────────────────┼────────────────┼─────────────┤
│ 2024-03-14 23:37:03.895166 │           2024 │        2024 │
└───────────────────────────────────────────────────────────┘
```