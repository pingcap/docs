---
title: DIV0
summary: Returns the quotient by dividing the first number by the second one. Returns 0 if the second number is 0.
---

# DIV0

> **Note:**
>
> Introduced or updated in v1.2.345.

Returns the quotient by dividing the first number by the second one. Returns 0 if the second number is 0.

See also:

- [DIV](/tidb-cloud-lake/sql/div.md)
- [DIVNULL](/tidb-cloud-lake/sql/divnull.md)

## Syntax

```sql
DIV0(<number1>, <number2>)
```

## Examples

```sql
SELECT
  DIV0(20, 6),
  DIV0(20, 0),
  DIV0(20, NULL);

┌───────────────────────────────────────────────────┐
│     div0(20, 6)    │ div0(20, 0) │ div0(20, null) │
├────────────────────┼─────────────┼────────────────┤
│ 3.3333333333333335 │           0 │ NULL           │
└───────────────────────────────────────────────────┘
```
