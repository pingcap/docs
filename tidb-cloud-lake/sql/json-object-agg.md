---
title: JSON_OBJECT_AGG
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.611"/>

Converts key-value pairs into a JSON object. For each row in the input, it generates a key-value pair where the key is derived from the `<key_expression>` and the value is derived from the `<value_expression>`. These key-value pairs are then combined into a single JSON object.

See also: [JSON_ARRAY_AGG](aggregate-json-array-agg.md)

## Syntax

```sql
JSON_OBJECT_AGG(<key_expression>, <value_expression>)
```

| Parameter        | Description                                                                                                                                            |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| key_expression   | Specifies the key in the JSON object. **Only supports string** expressions. If the `key_expression` evaluates to NULL, the key-value pair is skipped.  |
| value_expression | Specifies the value in the JSON object. It can be any supported data type. If the `value_expression` evaluates to NULL, the key-value pair is skipped. |

## Return Type

JSON object.

## Examples

This example demonstrates how JSON_OBJECT_AGG can be used to aggregate different types of data—such as decimals, integers, JSON variants, and arrays—into JSON objects, with the column b as the key for each JSON object:

```sql
CREATE TABLE d (
    a DECIMAL(10, 2), 
    b STRING, 
    c INT, 
    d VARIANT, 
    e ARRAY(STRING)
);

INSERT INTO d VALUES
    (20, 'abc', NULL, '{"k":"v"}', ['a','b']),
    (10, 'de', 100, 'null', []),
    (4.23, NULL, 200, '"uvw"', ['x','y']),
    (5.99, 'xyz', 300, '[1,2,3]', ['z']);

SELECT
    json_object_agg(b, a) AS json_a,
    json_object_agg(b, c) AS json_c,
    json_object_agg(b, d) AS json_d,
    json_object_agg(b, e) AS json_e
FROM
    d;

-[ RECORD 1 ]-----------------------------------
json_a: {"abc":20.0,"de":10.0,"xyz":5.99}
json_c: {"de":100,"xyz":300}
json_d: {"abc":{"k":"v"},"de":null,"xyz":[1,2,3]}
json_e: {"abc":["a","b"],"de":[],"xyz":["z"]}
```