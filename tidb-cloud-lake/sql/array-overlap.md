---
title: ARRAY_OVERLAP
title_includes: JSON_ARRAY_OVERLAP
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Checks if there is any overlap between two JSON arrays and returns `true` if there are common elements; otherwise, it returns `false`.

## Aliases

- `JSON_ARRAY_OVERLAP`

## Syntax

```sql
ARRAY_OVERLAP(<json_array1>, <json_array2>)
```

## Return Type

The function returns a boolean value:

- `true` if there is at least one common element between the two JSON arrays,
- `false` if there are no common elements.

## Examples

```sql
SELECT ARRAY_OVERLAP(
    '["apple", "banana", "cherry"]'::JSON,  
    '["banana", "kiwi", "mango"]'::JSON
);

-[ RECORD 1 ]-----------------------------------
array_overlap('["apple", "banana", "cherry"]'::VARIANT, '["banana", "kiwi", "mango"]'::VARIANT): true


SELECT ARRAY_OVERLAP(
    '["grape", "orange"]'::JSON,  
    '["apple", "kiwi"]'::JSON     
);

-[ RECORD 1 ]-----------------------------------
array_overlap('["grape", "orange"]'::VARIANT, '["apple", "kiwi"]'::VARIANT): false
```
