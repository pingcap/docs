---
title: ARRAY_EXCEPT
title_includes: JSON_ARRAY_EXCEPT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Returns a new JSON array containing the elements from the first JSON array that are not present in the second JSON array.

## Aliases

- `JSON_ARRAY_EXCEPT`

## Syntax

```sql
ARRAY_EXCEPT(<source_array>, <array_of_elements_to_exclude>)
```

## Return Type

JSON array.

## Examples

```sql
SELECT ARRAY_EXCEPT(
    '["apple", "banana", "orange"]'::VARIANT,  
    '["banana", "grapes"]'::VARIANT         
);

-[ RECORD 1 ]-----------------------------------
array_except('["apple", "banana", "orange"]'::VARIANT, '["banana", "grapes"]'::VARIANT): ["apple","orange"]

-- Return an empty array because all elements in the first array are present in the second array.
SELECT ARRAY_EXCEPT('["apple", "banana", "orange"]'::VARIANT, '["apple", "banana", "orange"]'::VARIANT)

-[ RECORD 1 ]-----------------------------------
array_except('["apple", "banana", "orange"]'::VARIANT, '["apple", "banana", "orange"]'::VARIANT): []
```
