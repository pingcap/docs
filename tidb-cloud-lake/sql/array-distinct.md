---
title: ARRAY_DISTINCT
title_includes: JSON_ARRAY_DISTINCT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Removes duplicate elements from a JSON array and returns an array with only distinct elements.

## Aliases

- `JSON_ARRAY_DISTINCT`

## Syntax

```sql
ARRAY_DISTINCT(<json_array>)
```

## Return Type

JSON array.

## Examples

```sql
SELECT ARRAY_DISTINCT('["apple", "banana", "apple", "orange", "banana"]'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_distinct('["apple", "banana", "apple", "orange", "banana"]'::VARIANT): ["apple","banana","orange"]
```
