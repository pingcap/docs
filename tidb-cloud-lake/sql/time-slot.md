---
title: TIME_SLOT
---

Rounds the time to the half-hour.
## Syntax

```sql
time_slot(<expr>)
```

## Arguments

| Arguments   | Description |
| ----------- | ----------- |
| `<expr>`    | timestamp   |

## Return Type

`TIMESTAMP`, returns in “YYYY-MM-DD hh:mm:ss.ffffff” format.

## Examples

```sql
SELECT
  time_slot('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────┐
│ time_slot('2023-11-12 09:38:18.165575') │
├─────────────────────────────────────────┤
│ 2023-11-12 09:30:00                     │
└─────────────────────────────────────────┘
```
