---
title: ARRAY_PREPEND
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Prepends an element to the beginning of an array.

## Syntax

```sql
ARRAY_PREPEND(element, array)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| element   | The element to prepend to the array. |
| array     | The source array to which the element will be prepended. |

## Return Type

Array with the prepended element.

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Prepending to a Standard Array

```sql
SELECT ARRAY_PREPEND(0, [1, 2, 3]);
```

Result:

```
[0, 1, 2, 3]
```

### Example 2: Prepending to a Variant Array

```sql
SELECT ARRAY_PREPEND('apple', PARSE_JSON('["banana", "orange"]'));
```

Result:

```
["apple", "banana", "orange"]
```

### Example 3: Prepending a Complex Element

```sql
SELECT ARRAY_PREPEND(PARSE_JSON('{"value": 0}'), [1, 2, 3]);
```

Result:

```
[{"value": 0}, 1, 2, 3]
```
