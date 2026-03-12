---
title: TO_MINUTES
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of minutes into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_MINUTES(<minutes>)
```

## Return Type

Interval (in the format `hh:mm:ss`).

## Examples

```sql
SELECT TO_MINUTES(2), TO_MINUTES(0), TO_MINUTES((- 2));

┌─────────────────────────────────────────────────┐
│ to_minutes(2) │ to_minutes(0) │ to_minutes(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 0:02:00       │ 00:00:00      │ -0:02:00        │
└─────────────────────────────────────────────────┘
```