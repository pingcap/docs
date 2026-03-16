---
title: TO_MICROSECONDS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of microseconds into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_MICROSECONDS(<microseconds>)
```

## Return Type

Interval (in the format `hh:mm:ss.sssssss`).

## Examples

```sql
SELECT TO_MICROSECONDS(2), TO_MICROSECONDS(0), TO_MICROSECONDS((- 2));

┌────────────────────────────────────────────────────────────────┐
│ to_microseconds(2) │ to_microseconds(0) │ to_microseconds(- 2) │
├────────────────────┼────────────────────┼──────────────────────┤
│ 0:00:00.000002     │ 00:00:00           │ -0:00:00.000002      │
└────────────────────────────────────────────────────────────────┘
```