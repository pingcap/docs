---
title: ARRAY_FILTER
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Filters elements from a JSON array based on a specified Lambda expression, returning only the elements that satisfy the condition. For more information about Lambda expression, see [Lambda Expressions](/sql/stored-procedure-scripting/#lambda-expressions).

## Syntax

```sql
ARRAY_FILTER(<json_array>, <lambda_expression>)
```

## Return Type

JSON array.

## Examples

This example filters the array to return only the strings that start with the letter `a`, resulting in `["apple", "avocado"]`:

```sql
SELECT ARRAY_FILTER(
    ['apple', 'banana', 'avocado', 'grape'],
    d -> d::String LIKE 'a%'
);

-[ RECORD 1 ]-----------------------------------
array_filter(['apple', 'banana', 'avocado', 'grape'], d -> d::STRING LIKE 'a%'): ["apple","avocado"]
```
