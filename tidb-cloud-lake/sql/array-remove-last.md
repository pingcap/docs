---
title: ARRAY_REMOVE_LAST
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Removes the last occurrence of an element from an array.

## Syntax

```sql
ARRAY_REMOVE_LAST(array, element)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The source array from which to remove the element. |
| element   | The element to remove from the array. |

## Return Type

Array with the last occurrence of the specified element removed.

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Removing from a Standard Array

```sql
SELECT ARRAY_REMOVE_LAST([1, 2, 2, 3], 2);
```

Result:

```
[1, 2, 3]
```

### Example 2: Removing from a Variant Array

```sql
SELECT ARRAY_REMOVE_LAST(PARSE_JSON('["apple", "banana", "apple", "orange"]'), 'apple');
```

Result:

```
["apple", "banana", "orange"]
```

### Example 3: Element Not Found

```sql
SELECT ARRAY_REMOVE_LAST([1, 2, 3], 4);
```

Result:

```
[1, 2, 3]
```
