---
title: IF
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.738"/>

If `<cond1>` is TRUE, it returns `<expr1>`. Otherwise if `<cond2>` is TRUE, it returns `<expr2>`, and so on.

## Syntax

```sql
IF(<cond1>, <expr1>, [<cond2>, <expr2> ...], <expr_else>)
```

## Aliases

- [IFF](iff.md)

## Examples

```sql
SELECT IF(1 > 2, 3, 4 < 5, 6, 7);

┌───────────────────────────────┐
│ if((1 > 2), 3, (4 < 5), 6, 7) │
├───────────────────────────────┤
│                             6 │
└───────────────────────────────┘
```