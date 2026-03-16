---
title: OBJECT_KEYS
title_includes: JSON_OBJECT_KEYS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Returns the keys of the outermost JSON object as an array of strings.

## Aliases

- `JSON_OBJECT_KEYS`

## Syntax

```sql
OBJECT_KEYS(<variant>)
```

## Return Type

ARRAY of STRING.

## Examples

```sql
SELECT OBJECT_KEYS('{"a":1, "b":2, "c": {"d":3}}'::VARIANT);

-[ RECORD 1 ]-----------------------------------
object_keys('{"a":1, "b":2, "c": {"d":3}}'::VARIANT): ["a","b","c"]

-- Example with a table
CREATE TABLE t (var VARIANT);
INSERT INTO t VALUES ('{"a":1, "b":2}'), ('{"x":10, "y":20}');

SELECT id, object_keys(var), json_object_keys(var) FROM t;

┌───────────┬──────────────────┬───────────────────────┐
│    id     │  object_keys(var) │ json_object_keys(var) │
├───────────┼──────────────────┼───────────────────────┤
│ 1         │ ["a","b"]        │ ["a","b"]           │
│ 2         │ ["x","y"]        │ ["x","y"]           │
└───────────┴──────────────────┴───────────────────────┘
```
