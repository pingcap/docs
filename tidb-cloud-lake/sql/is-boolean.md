---
title: IS_BOOLEAN
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

Checks if the input JSON value is a boolean.

## Syntax

```sql
IS_BOOLEAN( <expr> )
```

## Return Type

Returns `true` if the input JSON value is a boolean, and `false` otherwise.

## Examples

```sql
SELECT
  IS_BOOLEAN(PARSE_JSON('true')),
  IS_BOOLEAN(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────────┐
│ is_boolean(parse_json('true')) │ is_boolean(parse_json('[1,2,3]')) │
├────────────────────────────────┼───────────────────────────────────┤
│ true                           │ false                             │
└────────────────────────────────────────────────────────────────────┘
```