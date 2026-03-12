---
title: ARRAY_REVERSE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Reverses the order of elements in an array.

## Syntax

```sql
ARRAY_REVERSE(array)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The array to reverse. |

## Return Type

Array with elements in reversed order.

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Reversing a Standard Array

```sql
SELECT ARRAY_REVERSE([1, 2, 3, 4, 5]);
```

Result:

```
[5, 4, 3, 2, 1]
```

### Example 2: Reversing a Variant Array

```sql
SELECT ARRAY_REVERSE(PARSE_JSON('["apple", "banana", "orange"]'));
```

Result:

```
["orange", "banana", "apple"]
```

### Example 3: Reversing an Empty Array

```sql
SELECT ARRAY_REVERSE([]);
```

Result:

```
[]
```
