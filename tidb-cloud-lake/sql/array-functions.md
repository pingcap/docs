---
title: Array Functions
---

This section provides reference information for array functions in Databend. Array functions enable creation, manipulation, searching, and transformation of array data structures.

## Array Creation & Construction

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY](array/array) | Builds an array from expressions | `ARRAY(1, 2, 3)` → `[1,2,3]` |
| [ARRAY_CONSTRUCT](array/array-construct) | Creates an array from individual values | `ARRAY_CONSTRUCT(1, 2, 3)` → `[1,2,3]` |
| [RANGE](array/range) | Generates an array of sequential numbers | `RANGE(1, 5)` → `[1,2,3,4]` |
| [ARRAY_GENERATE_RANGE](array/array-generate-range) | Generates a sequence with optional step | `ARRAY_GENERATE_RANGE(0, 6, 2)` → `[0,2,4]` |

## Array Access & Information

| Function | Description | Example |
|----------|-------------|---------|
| [GET](array/get) | Gets an element from an array by index | `GET([1,2,3], 1)` → `1` |
| [ARRAY_GET](array/array-get) | Alias for GET function | `ARRAY_GET([1,2,3], 1)` → `1` |
| [CONTAINS](array/contains) | Checks if an array contains a specific value | `CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_CONTAINS](array/array-contains) | Checks if an array contains a specific value | `ARRAY_CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_SIZE](array/array-size) | Returns array length (alias: `ARRAY_LENGTH`) | `ARRAY_SIZE([1,2,3])` → `3` |
| [ARRAY_COUNT](array/array-count) | Counts non-`NULL` entries | `ARRAY_COUNT([1,NULL,2])` → `2` |
| [ARRAY_ANY](array/array-any) | Returns the first non-`NULL` value | `ARRAY_ANY([NULL,'a','b'])` → `'a'` |

## Array Modification

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_APPEND](array/array-append) | Appends an element to the end of an array | `ARRAY_APPEND([1,2], 3)` → `[1,2,3]` |
| [ARRAY_PREPEND](array/array-prepend) | Prepends an element to the beginning of an array | `ARRAY_PREPEND(0, [1,2])` → `[0,1,2]` |
| [ARRAY_INSERT](array/array-insert) | Inserts an element at a specific position | `ARRAY_INSERT([1,3], 1, 2)` → `[1,2,3]` |
| [ARRAY_REMOVE](array/array-remove) | Removes all occurrences of a specified element | `ARRAY_REMOVE([1,2,2,3], 2)` → `[1,3]` |
| [ARRAY_REMOVE_FIRST](array/array-remove-first) | Removes the first element from an array | `ARRAY_REMOVE_FIRST([1,2,3])` → `[2,3]` |
| [ARRAY_REMOVE_LAST](array/array-remove-last) | Removes the last element from an array | `ARRAY_REMOVE_LAST([1,2,3])` → `[1,2]` |

## Array Combination & Manipulation

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_CONCAT](array/array-concat) | Concatenates multiple arrays | `ARRAY_CONCAT([1,2], [3,4])` → `[1,2,3,4]` |
| [ARRAY_SLICE](array/array-slice) | Extracts a portion of an array | `ARRAY_SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [SLICE](array/slice) | Alias for ARRAY_SLICE function | `SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [ARRAYS_ZIP](array/arrays-zip) | Combines multiple arrays element-wise | `ARRAYS_ZIP([1,2], ['a','b'])` → `[(1,'a'),(2,'b')]` |
| [ARRAY_SORT](array/array-sort) | Sorts values; variants control order/nulls | `ARRAY_SORT([3,1,2])` → `[1,2,3]` |

## Array Set Operations

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_DISTINCT](array/array-distinct) | Returns unique elements from an array | `ARRAY_DISTINCT([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_UNIQUE](array/array-unique) | Alias for ARRAY_DISTINCT function | `ARRAY_UNIQUE([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_INTERSECTION](array/array-intersection) | Returns common elements between arrays | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` → `[2,3]` |
| [ARRAY_EXCEPT](array/array-except) | Returns elements in first array but not in second | `ARRAY_EXCEPT([1,2,3], [2,4])` → `[1,3]` |
| [ARRAY_OVERLAP](array/array-overlap) | Checks if arrays have common elements | `ARRAY_OVERLAP([1,2,3], [3,4,5])` → `true` |

## Array Processing & Transformation

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_TRANSFORM](array/array-transform) | Applies a function to each array element | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` → `[2,4,6]` |
| [ARRAY_FILTER](array/array-filter) | Filters array elements based on a condition | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` → `[3,4]` |
| [ARRAY_REDUCE](array/array-reduce) | Reduces array to a single value using aggregation | `ARRAY_REDUCE([1,2,3], 0, (acc,x) -> acc + x)` → `6` |
| [ARRAY_AGGREGATE](array/array-aggregate) | Aggregates array elements using a function | `ARRAY_AGGREGATE([1,2,3], 'sum')` → `6` |

## Array Aggregations & Statistics

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_SUM](array/array-sum) | Sum of numeric values | `ARRAY_SUM([1,2,3])` → `6` |
| [ARRAY_AVG](array/array-avg) | Average of numeric values | `ARRAY_AVG([1,2,3])` → `2` |
| [ARRAY_MEDIAN](array/array-median) | Median of numeric values | `ARRAY_MEDIAN([1,3,2])` → `2` |
| [ARRAY_MIN](array/array-min) | Minimum value | `ARRAY_MIN([3,1,2])` → `1` |
| [ARRAY_MAX](array/array-max) | Maximum value | `ARRAY_MAX([3,1,2])` → `3` |
| [ARRAY_STDDEV_POP](array/array-stddev-pop) | Population standard deviation (alias: `ARRAY_STD`) | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](array/array-stddev-samp) | Sample standard deviation (alias: `ARRAY_STDDEV`) | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](array/array-kurtosis) | Excess kurtosis of values | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](array/array-skewness) | Skewness of values | `ARRAY_SKEWNESS([1,2,3,4])` |
| [ARRAY_APPROX_COUNT_DISTINCT](array/array-approx-count-distinct) | Approximate distinct count | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` → `2` |

## Array Formatting

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_TO_STRING](array/array-to-string) | Joins array elements into a string | `ARRAY_TO_STRING(['a','b'], ',')` → `'a,b'` |

## Array Utility Functions

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_COMPACT](array/array-compact) | Removes null values from an array | `ARRAY_COMPACT([1,null,2,null,3])` → `[1,2,3]` |
| [ARRAY_FLATTEN](array/array-flatten) | Flattens nested arrays into a single array | `ARRAY_FLATTEN([[1,2],[3,4]])` → `[1,2,3,4]` |
| [ARRAY_REVERSE](array/array-reverse) | Reverses the order of array elements | `ARRAY_REVERSE([1,2,3])` → `[3,2,1]` |
| [ARRAY_INDEXOF](array/array-indexof) | Returns the index of first occurrence of an element | `ARRAY_INDEXOF([1,2,3,2], 2)` → `1` |
| [UNNEST](array/unnest) | Expands an array into individual rows | `UNNEST([1,2,3])` → `1, 2, 3` (as separate rows) |
