---
title: ARRAY_REMOVE_FIRST
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Removes the first occurrence of an element from an array.

## Syntax

```sql
ARRAY_REMOVE_FIRST(array, element)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The source array from which to remove the element. |
| element   | The element to remove from the array. |

## Return Type

Array with the first occurrence of the specified element removed.

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Removing from a Standard Array

```sql
SELECT ARRAY_REMOVE_FIRST([1, 2, 2, 3], 2);
```

Result:

```
[1, 2, 3]
```

### Example 2: Removing from a Variant Array

```sql
SELECT ARRAY_REMOVE_FIRST(PARSE_JSON('["apple", "banana", "apple", "orange"]'), 'apple');
```

Result:

```
["banana", "apple", "orange"]
```

### Example 3: Element Not Found

```sql
SELECT ARRAY_REMOVE_FIRST([1, 2, 3], 4);
```

Result:

```
[1, 2, 3]
```
