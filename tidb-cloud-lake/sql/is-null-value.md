---
title: IS_NULL_VALUE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

Checks whether the input value is a JSON `null`. Please note that this function examines JSON `null`, not SQL NULL. To check if a value is SQL NULL, use [IS_NULL](../../03-conditional-functions/is-null.md).

```json title='JSON null Example:'
{
  "name": "John",
  "age": null
}   
```

## Syntax

```sql
IS_NULL_VALUE( <expr> )
```

## Return Type

Returns `true` if the input value is a JSON `null`, and `false` otherwise.

## Examples

```sql
SELECT
  IS_NULL_VALUE(PARSE_JSON('{"name":"John", "age":null}') :age), --JSON null
  IS_NULL(NULL); --SQL NULL

┌──────────────────────────────────────────────────────────────────────────────┐
│ is_null_value(parse_json('{"name":"john", "age":null}'):age) │ is_null(null) │
├──────────────────────────────────────────────────────────────┼───────────────┤
│ true                                                         │ true          │
└──────────────────────────────────────────────────────────────────────────────┘
```