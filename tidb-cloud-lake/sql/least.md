---
title: LEAST
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.738"/>

Returns the minimum value from a set of values. If any value in the set is `NULL`, the function returns `NULL`.

See also: [LEAST_IGNORE_NULLS](least-ignore-nulls.md)

## Syntax

```sql
LEAST(<value1>, <value2> ...)
```

## Examples

```sql
SELECT LEAST(5, 9, 4), LEAST(5, 9, null);
```

```
┌────────────────────────────────────┐
│ least(5, 9, 4) │ least(5, 9, NULL) │
├────────────────┼───────────────────┤
│              4 │ NULL              │
└────────────────────────────────────┘
```