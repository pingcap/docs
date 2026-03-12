---
title: TO_YEARS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of years into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_YEARS(<years>)
```

## Return Type

Interval (represented in years).

## Examples

```sql
SELECT TO_YEARS(2), TO_YEARS(0), TO_YEARS((- 2));

┌───────────────────────────────────────────┐
│ to_years(2) │ to_years(0) │ to_years(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 2 years     │ 00:00:00    │ -2 years      │
└───────────────────────────────────────────┘
```