---
title: ARRAY_CONTAINS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Returns true if the array contains the specified element.

## Syntax

```sql
ARRAY_CONTAINS(array, element)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The array to search within. |
| element   | The element to search for. |

## Return Type

BOOLEAN

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Checking a Standard Array

```sql
SELECT ARRAY_CONTAINS([1, 2, 3], 2);
```

Result:

```
true
```

### Example 2: Checking a Variant Array

```sql
SELECT ARRAY_CONTAINS(PARSE_JSON('["apple", "banana", "orange"]'), 'banana');
```

Result:

```
true
```

### Example 3: Element Not Found

```sql
SELECT ARRAY_CONTAINS([1, 2, 3], 4);
```

Result:

```
false
```
