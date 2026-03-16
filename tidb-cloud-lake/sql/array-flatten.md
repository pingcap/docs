---
title: ARRAY_FLATTEN
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Flattens a nested array into a single-dimensional array.

## Syntax

```sql
ARRAY_FLATTEN(array)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The nested array to flatten. |

## Return Type

Array (flattened).

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Flattening a Nested Array

```sql
SELECT ARRAY_FLATTEN([[1, 2], [3, 4]]);
```

Result:

```
[1, 2, 3, 4]
```

### Example 2: Flattening a Variant Array

```sql
SELECT ARRAY_FLATTEN(PARSE_JSON('[["a", "b"], ["c", "d"]]'));
```

Result:

```
["a", "b", "c", "d"]
```
