---
title: GREATEST
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.738"/>

Returns the maximum value from a set of values. If any value in the set is `NULL`, the function returns `NULL`.

See also: [GREATEST_IGNORE_NULLS](greatest-ignore-nulls.md)

## Syntax

```sql
GREATEST(<value1>, <value2> ...)
```

## Examples

```sql
SELECT GREATEST(5, 9, 4), GREATEST(5, 9, null);
```

```sql
┌──────────────────────────────────────────┐
│ greatest(5, 9, 4) │ greatest(5, 9, NULL) │
├───────────────────┼──────────────────────┤
│                 9 │ NULL                 │
└──────────────────────────────────────────┘
```