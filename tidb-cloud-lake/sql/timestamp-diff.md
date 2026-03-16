---
title: TIMESTAMP_DIFF
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.690"/>

Calculates the difference between two timestamps and returns the result as an INTERVAL.

## Syntax

```sql
TIMESTAMP_DIFF(<timestamp1>, <timestamp2>)
```

## Return Type

INTERVAL (formatted as `hours:minutes:seconds`).

## Examples

This example shows that the time difference between February 1, 2025, and January 1, 2025, is 744 hours, corresponding to 31 days:

```sql
SELECT TIMESTAMP_DIFF('2025-02-01'::TIMESTAMP, '2025-01-01'::TIMESTAMP);

┌──────────────────────────────────────────────────────────────────┐
│ timestamp_diff('2025-02-01'::TIMESTAMP, '2025-01-01'::TIMESTAMP) │
├──────────────────────────────────────────────────────────────────┤
│ 744:00:00                                                        │
└──────────────────────────────────────────────────────────────────┘
```