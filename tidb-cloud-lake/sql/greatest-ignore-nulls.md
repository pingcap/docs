---
title: GREATEST_IGNORE_NULLS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.738"/>

Returns the maximum value from a set of values, ignoring any NULL values.

See also: [GREATEST](greatest.md)

## Syntax

```sql
GREATEST_IGNORE_NULLS(<value1>, <value2> ...)
```

## Examples

```sql
SELECT GREATEST_IGNORE_NULLS(5, 9, 4), GREATEST_IGNORE_NULLS(5, 9, null);
```

```sql
┌────────────────────────────────────────────────────────────────────┐
│ greatest_ignore_nulls(5, 9, 4) │ greatest_ignore_nulls(5, 9, NULL) │
├────────────────────────────────┼───────────────────────────────────┤
│                              9 │                                 9 │
└────────────────────────────────────────────────────────────────────┘
```