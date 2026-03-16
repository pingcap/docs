---
title: TO_MONTHS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of months into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_MONTHS(<months>)
```

## Return Type

Interval (represented in months).

## Examples

```sql
SELECT TO_MONTHS(2), TO_MONTHS(0), TO_MONTHS((- 2));

┌──────────────────────────────────────────────┐
│ to_months(2) │ to_months(0) │ to_months(- 2) │
├──────────────┼──────────────┼────────────────┤
│ 2 months     │ 00:00:00     │ -2 months      │
└──────────────────────────────────────────────┘
```