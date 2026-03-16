---
title: TO_MILLENNIA
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of millennia into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_MILLENNIA(<millennia>)
```

## Return Type

Interval (represented in years).

## Examples

```sql
SELECT TO_MILLENNIA(2), TO_MILLENNIA(0), TO_MILLENNIA((- 2));

┌───────────────────────────────────────────────────────┐
│ to_millennia(2) │ to_millennia(0) │ to_millennia(- 2) │
├─────────────────┼─────────────────┼───────────────────┤
│ 2000 years      │ 00:00:00        │ -2000 years       │
└───────────────────────────────────────────────────────┘
```