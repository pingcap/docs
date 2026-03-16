---
title: TO_MILLISECONDS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

Converts a specified number of milliseconds into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_MILLISECONDS(<milliseconds>)
```

## Return Type

Interval (in the format `hh:mm:ss.sss`).

## Examples

```sql
SELECT TO_MILLISECONDS(2), TO_MILLISECONDS(0), TO_MILLISECONDS((- 2));

┌────────────────────────────────────────────────────────────────┐
│ to_milliseconds(2) │ to_milliseconds(0) │ to_milliseconds(- 2) │
├────────────────────┼────────────────────┼──────────────────────┤
│ 0:00:00.002        │ 00:00:00           │ -0:00:00.002         │
└────────────────────────────────────────────────────────────────┘
```