---
title: TO_QUARTER
summary: Retrieves the quarter (1, 2, 3, or 4) from a given date or timestamp.
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.153"/>

Retrieves the quarter (1, 2, 3, or 4) from a given date or timestamp.

## Syntax

```sql
TO_QUARTER( <date_or_time_expr> )
```

## Aliases

- [QUARTER](/tidb-cloud-lake/sql/quarter.md)

## Return Type

Integer.

## Examples

```sql
SELECT NOW(), TO_QUARTER(NOW()), QUARTER(NOW());

┌─────────────────────────────────────────────────────────────────┐
│            now()           │ to_quarter(now()) │ quarter(now()) │
├────────────────────────────┼───────────────────┼────────────────┤
│ 2024-03-14 23:32:52.743133 │                 1 │              1 │
└─────────────────────────────────────────────────────────────────┘
```