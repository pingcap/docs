---
title: NVL
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.312"/>

If `<expr1>` is NULL, returns `<expr2>`, otherwise returns `<expr1>`.

## Syntax

```sql
NVL(<expr1>, <expr2>)
```

## Aliases

- [IFNULL](ifnull.md)

## Examples

```sql
SELECT NVL(NULL, 'b'), NVL('a', 'b');

┌────────────────────────────────┐
│ nvl(null, 'b') │ nvl('a', 'b') │
├────────────────┼───────────────┤
│ b              │ a             │
└────────────────────────────────┘

SELECT NVL(NULL, 2), NVL(1, 2);

┌──────────────────────────┐
│ nvl(null, 2) │ nvl(1, 2) │
├──────────────┼───────────┤
│            2 │         1 │
└──────────────────────────┘
```