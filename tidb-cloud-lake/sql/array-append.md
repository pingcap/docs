---
title: ARRAY_APPEND
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Appends an element to the end of an array.

## Syntax

```sql
ARRAY_APPEND(array, element)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The source array to which the element will be appended. |
| element   | The element to append to the array. |

## Return Type

Array with the appended element.

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Appending to a Standard Array

```sql
SELECT ARRAY_APPEND([1, 2, 3], 4);
```

Result:

```
[1, 2, 3, 4]
```

### Example 2: Appending to a Variant Array

```sql
SELECT ARRAY_APPEND(PARSE_JSON('[1, 2, 3]'), 4);
```

Result:

```
[1, 2, 3, 4]
```

### Example 3: Appending Different Data Types

```sql
SELECT ARRAY_APPEND(['a', 'b'], 'c');
```

Result:

```
["a", "b", "c"]
```

## Related Functions

- [ARRAY_PREPEND](array-prepend): Prepends an element to the beginning of an array
- [ARRAY_CONCAT](array-concat): Concatenates two arrays
