---
title: ARRAY_FILTER
summary: Filters elements from a JSON array based on a specified Lambda expression, returning only the elements that satisfy the condition. For more information about Lambda expression, see Lambda Expressions.
---

# ARRAY_FILTER

> **Note:**
>
> Introduced or updated in v1.2.762.

Filters elements from a JSON array based on a specified Lambda expression, returning only the elements that satisfy the condition. For more information about Lambda expression, see [Lambda Expressions](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions).

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
