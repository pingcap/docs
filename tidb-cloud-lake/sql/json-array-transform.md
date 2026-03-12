---
title: JSON_ARRAY_TRANSFORM
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Transforms each element of a JSON array using a specified transformation Lambda expression. For more information about Lambda expression, see [Lambda Expressions](../../../30-stored-procedure-scripting/index.md#lambda-expressions).

## Syntax

```sql
ARRAY_TRANSFORM(<json_array>, <lambda_expression>)
```

## Return Type

JSON array.

## Examples

In this example, each numeric element in the array is multiplied by 10, transforming the original array into `[10, 20, 30, 40]`:

```sql
SELECT ARRAY_TRANSFORM(
    [1, 2, 3, 4],
    data -> (data::Int * 10)
);

-[ RECORD 1 ]-----------------------------------
array_transform([1, 2, 3, 4], data -> data::Int32 * 10): [10,20,30,40]
```
