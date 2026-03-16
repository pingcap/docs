---
title: IS_STRING
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

Checks if the input JSON value is a string.

## Syntax

```sql
IS_STRING( <expr> )
```

## Return Type

Returns `true` if the input JSON value is a string, and `false` otherwise.

## Examples

```sql
SELECT
  IS_STRING(PARSE_JSON('"abc"')),
  IS_STRING(PARSE_JSON('123'));

┌───────────────────────────────────────────────────────────────┐
│ is_string(parse_json('"abc"')) │ is_string(parse_json('123')) │
├────────────────────────────────┼──────────────────────────────┤
│ true                           │ false                        │
└───────────────────────────────────────────────────────────────┘
```