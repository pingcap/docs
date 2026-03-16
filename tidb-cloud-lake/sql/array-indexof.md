---
title: ARRAY_INDEXOF
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Returns the index of the first occurrence of an element in an array.

## Syntax

```sql
ARRAY_INDEXOF(array, element)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| array     | The array to search within. |
| element   | The element to search for. |

## Return Type

INTEGER

## Important Note on Indexing

- For standard array types: Indexing is **1-based** (first element is at position 1).
- For variant array types: Indexing is **0-based** (first element is at position 0), for compatibility with Snowflake.

## Examples

### Example 1: Finding an Element in a Standard Array (1-based indexing)

```sql
SELECT ARRAY_INDEXOF([10, 20, 30, 20], 20);
```

Result:

```
2
```

### Example 2: Finding an Element in a Variant Array (0-based indexing)

```sql
SELECT ARRAY_INDEXOF(PARSE_JSON('["apple", "banana", "orange"]'), 'banana');
```

Result:

```
1
```

### Example 3: Element Not Found

```sql
SELECT ARRAY_INDEXOF([1, 2, 3], 4);
```

Result:

```
0
```
