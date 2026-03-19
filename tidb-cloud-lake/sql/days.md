---
title: TO_DAYS
summary: Converts a specified number of days into an Interval type.
---

# TO_DAYS

> **Note:**
>
> Introduced or updated in v1.2.677.

Converts a specified number of days into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_DAYS(<days>)
```

## Return Type

Interval (represented in days).

## Examples

```sql
SELECT TO_DAYS(2), TO_DAYS(0), TO_DAYS(-2);

┌────────────────────────────────────────┐
│ to_days(2) │ to_days(0) │ to_days(- 2) │
├────────────┼────────────┼──────────────┤
│ 2 days     │ 00:00:00   │ -2 days      │
└────────────────────────────────────────┘
```
