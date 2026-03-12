---
title: TO_UNIX_TIMESTAMP
---

Converts a timestamp in a date/time format to a Unix timestamp format. A Unix timestamp represents the number of seconds that have elapsed since January 1, 1970, at 00:00:00 UTC.

## Syntax

```sql
TO_UNIX_TIMESTAMP(<expr>)
```

## Arguments

| Arguments   | Description         |
| ----------- | ------------------- |
| `<expr>`    | Timestamp           |

For more information about the timestamp data type, see [Date & Time](../../00-sql-reference/10-data-types/datetime.md).

## Return Type

`BIGINT`

## Examples

```sql
SELECT
  to_unix_timestamp('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────────────┐
│ to_unix_timestamp('2023-11-12 09:38:18.165575') │
├─────────────────────────────────────────────────┤
│                                      1699781898 │
└─────────────────────────────────────────────────┘
```