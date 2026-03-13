---
title: NVL2
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.312"/>

Returns `<expr2>` if `<expr1>` is not NULL; otherwise, it returns `<expr3>`.

## Syntax

```sql
NVL2(<expr1> , <expr2> , <expr3>)
```

## Examples

```sql
SELECT NVL2('a', 'b', 'c'), NVL2(NULL, 'b', 'c');

┌────────────────────────────────────────────┐
│ nvl2('a', 'b', 'c') │ nvl2(null, 'b', 'c') │
├─────────────────────┼──────────────────────┤
│ b                   │ c                    │
└────────────────────────────────────────────┘

SELECT NVL2(1, 2, 3), NVL2(NULL, 2, 3);

┌──────────────────────────────────┐
│ nvl2(1, 2, 3) │ nvl2(null, 2, 3) │
├───────────────┼──────────────────┤
│             2 │                3 │
└──────────────────────────────────┘
```