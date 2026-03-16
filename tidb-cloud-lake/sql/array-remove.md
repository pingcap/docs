---
title: ARRAY_REMOVE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Removes all occurrences of an element from an array.

## Syntax

```sql
ARRAY_REMOVE(array, element)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The source array from which to remove elements. |
| element   | The element to remove from the array. |

## Return Type

Array with all occurrences of the specified element removed.

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Removing from a Standard Array

```sql
SELECT ARRAY_REMOVE([1, 2, 2, 3, 2], 2);
```

Result:

```
[1, 3]
```

### Example 2: Removing from a Variant Array

```sql
SELECT ARRAY_REMOVE(PARSE_JSON('["apple", "banana", "apple", "orange"]'), 'apple');
```

Result:

```
["banana", "orange"]
```

### Example 3: Element Not Found

```sql
SELECT ARRAY_REMOVE([1, 2, 3], 4);
```

Result:

```
[1, 2, 3]
```
