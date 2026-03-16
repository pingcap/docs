---
title: IS_FLOAT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

Checks if the input JSON value is a float.

## Syntax

```sql
IS_FLOAT( <expr> )
```

## Return Type

Returns `true` if the input JSON value is a float, and `false` otherwise.

## Examples

```sql
SELECT
  IS_FLOAT(PARSE_JSON('1.23')),
  IS_FLOAT(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────┐
│ is_float(parse_json('1.23')) │ is_float(parse_json('[1,2,3]')) │
├──────────────────────────────┼─────────────────────────────────┤
│ true                         │ false                           │
└────────────────────────────────────────────────────────────────┘
```