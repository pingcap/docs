---
title: IS_OBJECT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

Checks if the input value is a JSON object.

## Syntax

```sql
IS_OBJECT( <expr> )
```

## Return Type

Returns `true` if the input JSON value is a JSON object, and `false` otherwise.

## Examples

```sql
SELECT
  IS_OBJECT(PARSE_JSON('{"a":"b"}')), -- JSON Object
  IS_OBJECT(PARSE_JSON('["a","b","c"]')); --JSON Array

┌─────────────────────────────────────────────────────────────────────────────┐
│ is_object(parse_json('{"a":"b"}')) │ is_object(parse_json('["a","b","c"]')) │
├────────────────────────────────────┼────────────────────────────────────────┤
│ true                               │ false                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```