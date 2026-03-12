---
title: JSON_PATH_MATCH
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.241"/>

Checks whether a specified JSON path expression matches certain conditions within a JSON data. Please note that the `@@` operator is synonymous with this function. For more information, see [JSON Operators](../../../10-sql-commands/30-query-operators/index.md).

## Syntax

```sql
JSON_PATH_MATCH(<json_data>, <json_path_expression>)
```

- `json_data`: Specifies the JSON data you want to examine. It can be a JSON object or an array.
- `json_path_expression`: Specifies the conditions to be checked within the JSON data. This expression describes the specific path or criteria to be matched, such as verifying whether specific field values in the JSON structure meet certain conditions. The `$` symbol represents the root of the JSON data. It is used to start the path expression and indicates the top-level object in the JSON structure.

## Return Type

The function returns:

- `true` if the specified JSON path expression matches the conditions within the JSON data.
- `false` if the specified JSON path expression does not match the conditions within the JSON data.
- NULL if either `json_data` or `json_path_expression` is NULL or invalid.

## Examples

```sql
-- Check if the value at JSON path $.a is equal to 1
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.a == 1');

┌────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.a == 1') │
├────────────────────────────────────────────────────────────────┤
│ true                                                           │
└────────────────────────────────────────────────────────────────┘

-- Check if the first element in the array at JSON path $.b is greater than 1
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[0] > 1');

┌──────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[0] > 1') │
├──────────────────────────────────────────────────────────────────┤
│ false                                                            │
└──────────────────────────────────────────────────────────────────┘

-- Check if any element in the array at JSON path $.b
-- from the second one to the last are greater than or equal to 2
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[1 to last] >= 2');

┌───────────────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[1 to last] >= 2') │
├───────────────────────────────────────────────────────────────────────────┤
│ true                                                                      │
└───────────────────────────────────────────────────────────────────────────┘

-- NULL is returned if either the json_data or json_path_expression is NULL or invalid.
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), NULL);

┌──────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), null) │
├──────────────────────────────────────────────────────────┤
│ NULL                                                     │
└──────────────────────────────────────────────────────────┘

SELECT JSON_PATH_MATCH(NULL, '$.a == 1');

┌───────────────────────────────────┐
│ json_path_match(null, '$.a == 1') │
├───────────────────────────────────┤
│ NULL                              │
└───────────────────────────────────┘
```