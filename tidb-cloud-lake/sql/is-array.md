---
title: IS_ARRAY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.368"/>

Checks if the input value is a JSON array. Please note that a JSON array is not the same as the [ARRAY](../../../00-sql-reference/10-data-types/array.md) data type. A JSON array is a data structure commonly used in JSON, representing an ordered collection of values enclosed within square brackets `[ ]`. It is a flexible format for organizing and exchanging various data types, including strings, numbers, booleans, objects, and nulls. 

```json title='JSON Array Example:'
[
  "Apple",
  42,
  true,
  {"name": "John", "age": 30, "isStudent": false},
  [1, 2, 3],
  null
]
```

## Syntax

```sql
IS_ARRAY( <expr> )
```

## Return Type

Returns `true` if the input value is a JSON array, and `false` otherwise.

## Examples

```sql
SELECT
  IS_ARRAY(PARSE_JSON('true')),
  IS_ARRAY(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────┐
│ is_array(parse_json('true')) │ is_array(parse_json('[1,2,3]')) │
├──────────────────────────────┼─────────────────────────────────┤
│ false                        │ true                            │
└────────────────────────────────────────────────────────────────┘
```