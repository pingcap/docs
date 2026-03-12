---
title: TO_HOURS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of hours into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_HOURS(<hours>)
```

## Return Type

Interval (in the format `hh:mm:ss`).

## Examples

```sql
SELECT TO_HOURS(2), TO_HOURS(0), TO_HOURS((- 2));

┌───────────────────────────────────────────┐
│ to_hours(2) │ to_hours(0) │ to_hours(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 2:00:00     │ 00:00:00    │ -2:00:00      │
└───────────────────────────────────────────┘
```