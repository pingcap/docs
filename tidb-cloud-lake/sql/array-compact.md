---
title: ARRAY_COMPACT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Removes all NULL values from an array.

## Syntax

```sql
ARRAY_COMPACT(array)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The array from which to remove NULL values. |

## Return Type

Array without NULL values.

## Notes

This function works with both standard array types and variant array types.

## Examples

### Example 1: Removing NULLs from a Standard Array

```sql
SELECT ARRAY_COMPACT([1, NULL, 2, NULL, 3]);
```

Result:

```
[1, 2, 3]
```

### Example 2: Removing NULLs from a Variant Array

```sql
SELECT ARRAY_COMPACT(PARSE_JSON('["apple", null, "banana", null, "orange"]'));
```

Result:

```
["apple", "banana", "orange"]
```

### Example 3: Array with No NULLs

```sql
SELECT ARRAY_COMPACT([1, 2, 3]);
```

Result:

```
[1, 2, 3]
```
