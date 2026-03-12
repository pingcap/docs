---
title: OBJECT_CONSTRUCT_KEEP_NULL
title_includes: TRY_OBJECT_CONSTRUCT_KEEP_NULL, JSON_OBJECT_KEEP_NULL, TRY_JSON_OBJECT_KEEP_NULL
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Creates a JSON object with keys and values.

- The arguments are zero or more key-value pairs(where keys are strings, and values are of any type).
- If a key is NULL, the key-value pair is omitted from the resulting object. However, if a value is NULL, the key-value pair will be kept.
- The keys must be distinct from each other, and their order in the resulting JSON might be different from the order you specify.
- `TRY_OBJECT_CONSTRUCT_KEEP_NULL` returns a NULL value if an error occurs when building the object.

## Aliases

- `JSON_OBJECT_KEEP_NULL`
- `TRY_JSON_OBJECT_KEEP_NULL`

See also: [OBJECT_CONSTRUCT](object-construct.md)

## Syntax

```sql
OBJECT_CONSTRUCT_KEEP_NULL(key1, value1[, key2, value2[, ...]])

TRY_OBJECT_CONSTRUCT_KEEP_NULL(key1, value1[, key2, value2[, ...]])
```

## Return Type

JSON object.

## Examples

```sql
SELECT OBJECT_CONSTRUCT_KEEP_NULL();
┌──────────────────────────────┐
│ object_construct_keep_null() │
├──────────────────────────────┤
│ {}                      │
└──────────────────────────────┘

SELECT OBJECT_CONSTRUCT_KEEP_NULL('a', 3.14, 'b', 'xx', 'c', NULL);
┌───────────────────────────────────────────────────────────┐
│ object_construct_keep_null('a', 3.14, 'b', 'xx', 'c', null) │
├───────────────────────────────────────────────────────────┤
│ {"a":3.14,"b":"xx","c":null}                           │
└───────────────────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT_KEEP_NULL('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']);
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ object_construct_keep_null('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']) │
├───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {"fruits":["apple","banana","orange"],"vegetables":["carrot","celery"]}                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT_KEEP_NULL('key');
  |
1 | SELECT OBJECT_CONSTRUCT_KEEP_NULL('key')
  |        ^^^^^^^^^^^^^^^^^^ The number of keys and values must be equal while evaluating function `object_construct_keep_null('key')`


SELECT TRY_OBJECT_CONSTRUCT_KEEP_NULL('key');
┌─────────────────────────────────────┐
│ try_object_construct_keep_null('key') │
├─────────────────────────────────────┤
│ NULL                             │
└─────────────────────────────────────┘
```
