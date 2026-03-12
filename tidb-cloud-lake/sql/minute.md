---
title: TO_MINUTE
---

Converts a date with time (timestamp/datetime) to a UInt8 number containing the number of the minute of the hour (0-59).

## Syntax

```sql
TO_MINUTE(<expr>)
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
    to_minute('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────┐
│ to_minute('2023-11-12 09:38:18.165575') │
├─────────────────────────────────────────┤
│                                      38 │
└─────────────────────────────────────────┘
```
