---
title: MAP_TRANSFORM_VALUES
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Applies a transformation to each value in a JSON object using a [lambda expression](/sql/stored-procedure-scripting/#lambda-expressions).

## Syntax

```sql
MAP_TRANSFORM_VALUES(<json_object>, (<key>, <value>) -> <value_transformation>)
```

## Return Type

Returns a JSON object with the same keys as the input JSON object, but with values modified according to the specified lambda transformation.

## Examples

This example multiplies each numeric value by 10, transforming the original object into `{"a":10,"b":20}`:

```sql
SELECT MAP_TRANSFORM_VALUES('{"a":1,"b":2}'::VARIANT, (k, v) -> v * 10) AS transformed_values;

┌────────────────────┐
│ transformed_values │
├────────────────────┤
│ {"a":10,"b":20}    │
└────────────────────┘
```
