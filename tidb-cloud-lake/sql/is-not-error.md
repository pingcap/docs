---
title: IS_NOT_ERROR
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.379"/>

Returns a Boolean value indicating whether an expression is an error value.

See also: [IS_ERROR](is-error.md)

## Syntax

```sql
IS_NOT_ERROR( <expr> )
```

## Return Type

Returns `true` if the expression is not an error, otherwise `false`.

## Examples

```sql
-- Indicates division by zero, hence an error
SELECT IS_ERROR(1/0), IS_NOT_ERROR(1/0);

┌───────────────────────────────────────────┐
│ is_error((1 / 0)) │ is_not_error((1 / 0)) │
├───────────────────┼───────────────────────┤
│ true              │ false                 │
└───────────────────────────────────────────┘

-- The conversion to DATE is successful, hence not an error
SELECT IS_ERROR('2024-03-17'::DATE), IS_NOT_ERROR('2024-03-17'::DATE);

┌─────────────────────────────────────────────────────────────────┐
│ is_error('2024-03-17'::date) │ is_not_error('2024-03-17'::date) │
├──────────────────────────────┼──────────────────────────────────┤
│ false                        │ true                             │
└─────────────────────────────────────────────────────────────────┘
```