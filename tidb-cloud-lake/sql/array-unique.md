---
title: ARRAY_UNIQUE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Returns the number of unique elements in the array.

## Syntax

```sql
ARRAY_UNIQUE(array)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The array to analyze for unique elements. |

## Return Type

INTEGER

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Counting Unique Elements in a Standard Array

```sql
SELECT ARRAY_UNIQUE([1, 2, 2, 3, 3, 3]);
```

Result:

```
3
```

### Example 2: Counting Unique Elements in a Variant Array

```sql
SELECT ARRAY_UNIQUE(PARSE_JSON('["apple", "banana", "apple", "orange", "banana"]'));
```

Result:

```
3
```

### Example 3: Empty Array

```sql
SELECT ARRAY_UNIQUE([]);
```

Result:

```
0
```
