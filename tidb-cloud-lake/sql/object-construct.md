---
title: OBJECT_CONSTRUCT
title_includes: TRY_OBJECT_CONSTRUCT, JSON_OBJECT, TRY_JSON_OBJECT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Creates a JSON object with keys and values.

- The arguments are zero or more key-value pairs(where keys are strings, and values are of any type).
- If a key or value is NULL, the key-value pair is ommitted from the resulting object.
- The keys must be distinct from each other, and their order in the resulting JSON might be different from the order you specify.
- `TRY_OBJECT_CONSTRUCT` returns a NULL value if an error occurs when building the object.

## Aliases

- `JSON_OBJECT`
- `TRY_JSON_OBJECT`

See also: [OBJECT_CONSTRUCT_KEEP_NULL](object-construct-keep-null.md)

## Syntax

```sql
OBJECT_CONSTRUCT(key1, value1[, key2, value2[, ...]])

TRY_OBJECT_CONSTRUCT(key1, value1[, key2, value2[, ...]])
```

## Return Type

JSON object.

## Examples

```sql
SELECT OBJECT_CONSTRUCT();
┌────────────────┐
│ object_construct() │
├────────────────┤
│ {}            │
└────────────────┘

SELECT OBJECT_CONSTRUCT('a', 3.14, 'b', 'xx', 'c', NULL);
┌──────────────────────────────────────────────┐
│ object_construct('a', 3.14, 'b', 'xx', 'c', null) │
├──────────────────────────────────────────────┤
│ {"a":3.14,"b":"xx"}                          │
└──────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']);
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ object_construct('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']) │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ {"fruits":["apple","banana","orange"],"vegetables":["carrot","celery"]}                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT('key');
  |
1 | SELECT OBJECT_CONSTRUCT('key')
  |        ^^^^^^^^^^^^^^^^^^ The number of keys and values must be equal while evaluating function `object_construct('key')`


SELECT TRY_OBJECT_CONSTRUCT('key');
┌───────────────────────────┐
│ try_object_construct('key') │
├───────────────────────────┤
│ NULL                   │
└───────────────────────────┘
```
