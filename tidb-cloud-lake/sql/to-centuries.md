---
title: TO_CENTURIES
summary: Converts a specified number of centuries into an Interval type.
---

# TO_CENTURIES

> **Note:**
>
> Introduced or updated in v1.2.677.

Converts a specified number of centuries into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_CENTURIES(<centuries>)
```

## Return Type

Interval (represented in years).

## Examples

```sql
SELECT TO_CENTURIES(2), TO_CENTURIES(0), TO_CENTURIES(-2);

┌───────────────────────────────────────────────────────┐
│ to_centuries(2) │ to_centuries(0) │ to_centuries(- 2) │
├─────────────────┼─────────────────┼───────────────────┤
│ 200 years       │ 00:00:00        │ -200 years        │
└───────────────────────────────────────────────────────┘
```
