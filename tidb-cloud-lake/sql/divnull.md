---
title: DIVNULL
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.345"/>

Returns the quotient by dividing the first number by the second one. Returns NULL if the second number is 0 or NULL.

See also:

- [DIV](div.md)
- [DIV0](div0.md)

## Syntax

```sql
DIVNULL(<number1>, <number2>)
```

## Examples

```sql
SELECT
  DIVNULL(20, 6),
  DIVNULL(20, 0),
  DIVNULL(20, NULL);

┌─────────────────────────────────────────────────────────┐
│   divnull(20, 6)   │ divnull(20, 0) │ divnull(20, null) │
├────────────────────┼────────────────┼───────────────────┤
│ 3.3333333333333335 │ NULL           │ NULL              │
└─────────────────────────────────────────────────────────┘
```