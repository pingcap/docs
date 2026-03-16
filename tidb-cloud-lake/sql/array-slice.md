---
title: ARRAY_SLICE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Extracts a sub-array using slice between start and end arguments.

## Syntax

```sql
ARRAY_SLICE(array, start, end)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The source array from which to extract a slice. |
| start     | The starting position of the slice (inclusive). |
| end       | The ending position of the slice (exclusive). |

## Return Type

Array (slice of the original array).

## Important Note on Indexing

- For standard array types: Indexing is **1-based** (first element is at position 1).
- For variant array types: Indexing is **0-based** (first element is at position 0), for compatibility with Snowflake.

## Examples

### Example 1: Slicing a Standard Array (1-based indexing)

```sql
SELECT ARRAY_SLICE([10, 20, 30, 40, 50], 2, 4);
```

Result:

```
[20, 30]
```

### Example 2: Slicing a Variant Array (0-based indexing)

```sql
SELECT ARRAY_SLICE(PARSE_JSON('["apple", "banana", "orange", "grape", "kiwi"]'), 1, 3);
```

Result:

```
["banana", "orange"]
```

### Example 3: Out of Bounds Slice

```sql
SELECT ARRAY_SLICE([1, 2, 3], 4, 6);
```

Result:

```
[]
```
