---
title: TO_DECADES
summary: Converts a specified number of decades into an Interval type.
---

> **Note:**
>
> Introduced or updated in v1.2.677.

Converts a specified number of decades into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_DECADES(<decades>)
```

## Return Type

Interval (represented in years).

## Examples

```sql
SELECT TO_DECADES(2), TO_DECADES(0), TO_DECADES((- 2));

┌─────────────────────────────────────────────────┐
│ to_decades(2) │ to_decades(0) │ to_decades(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 20 years      │ 00:00:00      │ -20 years       │
└─────────────────────────────────────────────────┘
```