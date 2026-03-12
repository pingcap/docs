---
title: ARRAY_REDUCE
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Reduces a JSON array to a single value by applying a specified Lambda expression. For more information about Lambda expression, see [Lambda Expressions](/sql/stored-procedure-scripting/#lambda-expressions).

## Syntax

```sql
ARRAY_REDUCE(<json_array>, <lambda_expression>)
```

## Examples

This example multiplies all the elements in the array (2 _ 3 _ 4):

```sql
SELECT ARRAY_REDUCE(
    [2, 3, 4],
    (acc, d) -> acc::Int * d::Int
);

-[ RECORD 1 ]-----------------------------------
array_reduce([2, 3, 4], (acc, d) -> acc::Int32 * d::Int32): 24
```
