---
title: STRIP_NULL_VALUE
title_includes: JSON_STRIP_NULLS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Removes all properties with null values from a JSON object. 

## Syntax

```sql
STRIP_NULL_VALUE(<json_string>)
```

## Return Type

Returns a value of the same type as the input JSON value.

## Examples

```sql
SELECT STRIP_NULL_VALUE(PARSE_JSON('{"name": "Alice", "age": 30, "city": null}'));

strip_null_value(parse_json('{"name": "alice", "age": 30, "city": null}'))|
--------------------------------------------------------------------------+
{"age":30,"name":"Alice"}                                                 |
```
