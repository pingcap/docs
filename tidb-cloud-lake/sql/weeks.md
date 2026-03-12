---
title: TO_WEEKS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of weeks into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_WEEKS(<weeks>)
```

## Return Type

Interval (represented in days).

## Examples

```sql
SELECT TO_WEEKS(2), TO_WEEKS(0), TO_WEEKS((- 2));

┌───────────────────────────────────────────┐
│ to_weeks(2) │ to_weeks(0) │ to_weeks(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 14 days     │ 00:00:00    │ -14 days      │
└───────────────────────────────────────────┘
```