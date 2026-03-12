---
title: JSON_ARRAY_AGG
title_includes: JSON_AGG
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.595"/>

Converts values into a JSON array while skipping NULLs.

See also: [JSON_OBJECT_AGG](aggregate-json-object-agg.md)

## Syntax

```sql
JSON_ARRAY_AGG(<expr>)
```

## Return Type

JSON array.

## Examples

This example demonstrates how JSON_ARRAY_AGG aggregates values from each column into JSON arrays:

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
    json_array_agg(a) AS aggregated_a, 
    json_array_agg(b) AS aggregated_b, 
    json_array_agg(c) AS aggregated_c, 
    json_array_agg(d) AS aggregated_d, 
    json_array_agg(e) AS aggregated_e
FROM d;

-[ RECORD 1 ]-----------------------------------
aggregated_a: [20.0,10.0,4.23,5.99]
aggregated_b: ["abc","de","xyz"]
aggregated_c: [100,200,300]
aggregated_d: [{"k":"v"},null,"uvw",[1,2,3]]
aggregated_e: [["a","b"],[],["x","y"],["z"]]
```
