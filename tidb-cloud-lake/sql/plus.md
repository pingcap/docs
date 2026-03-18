---
title: PLUS
summary: Calculates the sum of two numeric or decimal values.
---
Calculates the sum of two numeric or decimal values.

## Syntax

```sql
PLUS(<number1>, <number2>)
```

## Aliases

- [ADD](/tidb-cloud-lake/sql/add.md)

## Examples

```sql
SELECT ADD(1, 2.3), PLUS(1, 2.3);

┌───────────────────────────────┐
│  add(1, 2.3)  │  plus(1, 2.3) │
├───────────────┼───────────────┤
│ 3.3           │ 3.3           │
└───────────────────────────────┘
```