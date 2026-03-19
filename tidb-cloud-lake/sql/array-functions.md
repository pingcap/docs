---
title: Array Functions
summary: This section provides reference information for array functions in Databend. Array functions enable creation, manipulation, searching, and transformation of array data structures.
---

# Array Functions

This section provides reference information for array functions in Databend. Array functions enable creation, manipulation, searching, and transformation of array data structures.

## Array Creation & Construction

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY](/tidb-cloud-lake/sql/array.md) | Builds an array from expressions | `ARRAY(1, 2, 3)` → `[1,2,3]` |
| [ARRAY_CONSTRUCT](/tidb-cloud-lake/sql/array-construct.md) | Creates an array from individual values | `ARRAY_CONSTRUCT(1, 2, 3)` → `[1,2,3]` |
| [RANGE](/tidb-cloud-lake/sql/range.md) | Generates an array of sequential numbers | `RANGE(1, 5)` → `[1,2,3,4]` |
| [ARRAY_GENERATE_RANGE](/tidb-cloud-lake/sql/array-generate-range.md) | Generates a sequence with optional step | `ARRAY_GENERATE_RANGE(0, 6, 2)` → `[0,2,4]` |

## Array Access & Information

| Function | Description | Example |
|----------|-------------|---------|
| [GET](/tidb-cloud-lake/sql/get.md) | Gets an element from an array by index | `GET([1,2,3], 1)` → `1` |
| [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md) | Alias for GET function | `ARRAY_GET([1,2,3], 1)` → `1` |
| [CONTAINS](/tidb-cloud-lake/sql/contains.md) | Checks if an array contains a specific value | `CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md) | Checks if an array contains a specific value | `ARRAY_CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_SIZE](/tidb-cloud-lake/sql/array-size.md) | Returns array length (alias: `ARRAY_LENGTH`) | `ARRAY_SIZE([1,2,3])` → `3` |
| [ARRAY_COUNT](/tidb-cloud-lake/sql/array-count.md) | Counts non-`NULL` entries | `ARRAY_COUNT([1,NULL,2])` → `2` |
| [ARRAY_ANY](/tidb-cloud-lake/sql/array-any.md) | Returns the first non-`NULL` value | `ARRAY_ANY([NULL,'a','b'])` → `'a'` |

## Array Modification

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_APPEND](/tidb-cloud-lake/sql/array-append.md) | Appends an element to the end of an array | `ARRAY_APPEND([1,2], 3)` → `[1,2,3]` |
| [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md) | Prepends an element to the beginning of an array | `ARRAY_PREPEND(0, [1,2])` → `[0,1,2]` |
| [ARRAY_INSERT](/tidb-cloud-lake/sql/array-insert.md) | Inserts an element at a specific position | `ARRAY_INSERT([1,3], 1, 2)` → `[1,2,3]` |
| [ARRAY_REMOVE](/tidb-cloud-lake/sql/array-remove.md) | Removes all occurrences of a specified element | `ARRAY_REMOVE([1,2,2,3], 2)` → `[1,3]` |
| [ARRAY_REMOVE_FIRST](/tidb-cloud-lake/sql/array-remove-first.md) | Removes the first element from an array | `ARRAY_REMOVE_FIRST([1,2,3])` → `[2,3]` |
| [ARRAY_REMOVE_LAST](/tidb-cloud-lake/sql/array-remove-last.md) | Removes the last element from an array | `ARRAY_REMOVE_LAST([1,2,3])` → `[1,2]` |

## Array Combination & Manipulation

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md) | Concatenates multiple arrays | `ARRAY_CONCAT([1,2], [3,4])` → `[1,2,3,4]` |
| [ARRAY_SLICE](/tidb-cloud-lake/sql/array-slice.md) | Extracts a portion of an array | `ARRAY_SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [SLICE](/tidb-cloud-lake/sql/slice.md) | Alias for ARRAY_SLICE function | `SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [ARRAYS_ZIP](/tidb-cloud-lake/sql/arrays-zip.md) | Combines multiple arrays element-wise | `ARRAYS_ZIP([1,2], ['a','b'])` → `[(1,'a'),(2,'b')]` |
| [ARRAY_SORT](/tidb-cloud-lake/sql/array-sort.md) | Sorts values; variants control order/nulls | `ARRAY_SORT([3,1,2])` → `[1,2,3]` |

## Array Set Operations

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_DISTINCT](/tidb-cloud-lake/sql/array-distinct.md) | Returns unique elements from an array | `ARRAY_DISTINCT([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_UNIQUE](/tidb-cloud-lake/sql/array-unique.md) | Alias for ARRAY_DISTINCT function | `ARRAY_UNIQUE([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_INTERSECTION](/tidb-cloud-lake/sql/array-intersection.md) | Returns common elements between arrays | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` → `[2,3]` |
| [ARRAY_EXCEPT](/tidb-cloud-lake/sql/array-except.md) | Returns elements in first array but not in second | `ARRAY_EXCEPT([1,2,3], [2,4])` → `[1,3]` |
| [ARRAY_OVERLAP](/tidb-cloud-lake/sql/array-overlap.md) | Checks if arrays have common elements | `ARRAY_OVERLAP([1,2,3], [3,4,5])` → `true` |

## Array Processing & Transformation

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_TRANSFORM](/tidb-cloud-lake/sql/json-array-transform.md) | Applies a function to each array element | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` → `[2,4,6]` |
| [ARRAY_FILTER](/tidb-cloud-lake/sql/array-filter.md) | Filters array elements based on a condition | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` → `[3,4]` |
| [ARRAY_REDUCE](/tidb-cloud-lake/sql/array-reduce.md) | Reduces array to a single value using aggregation | `ARRAY_REDUCE([1,2,3], 0, (acc,x) -> acc + x)` → `6` |
| [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md) | Aggregates array elements using a function | `ARRAY_AGGREGATE([1,2,3], 'sum')` → `6` |

## Array Aggregations & Statistics

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_SUM](/tidb-cloud-lake/sql/array-sum.md) | Sum of numeric values | `ARRAY_SUM([1,2,3])` → `6` |
| [ARRAY_AVG](/tidb-cloud-lake/sql/array-avg.md) | Average of numeric values | `ARRAY_AVG([1,2,3])` → `2` |
| [ARRAY_MEDIAN](/tidb-cloud-lake/sql/array-median.md) | Median of numeric values | `ARRAY_MEDIAN([1,3,2])` → `2` |
| [ARRAY_MIN](/tidb-cloud-lake/sql/array-min.md) | Minimum value | `ARRAY_MIN([3,1,2])` → `1` |
| [ARRAY_MAX](/tidb-cloud-lake/sql/array-max.md) | Maximum value | `ARRAY_MAX([3,1,2])` → `3` |
| [ARRAY_STDDEV_POP](/tidb-cloud-lake/sql/array-stddev-pop.md) | Population standard deviation (alias: `ARRAY_STD`) | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](/tidb-cloud-lake/sql/array-stddev-samp.md) | Sample standard deviation (alias: `ARRAY_STDDEV`) | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](/tidb-cloud-lake/sql/array-kurtosis.md) | Excess kurtosis of values | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](/tidb-cloud-lake/sql/array-skewness.md) | Skewness of values | `ARRAY_SKEWNESS([1,2,3,4])` |
| [ARRAY_APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/array-approx-count-distinct.md) | Approximate distinct count | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` → `2` |

## Array Formatting

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_TO_STRING](/tidb-cloud-lake/sql/array-to-string.md) | Joins array elements into a string | `ARRAY_TO_STRING(['a','b'], ',')` → `'a,b'` |

## Array Utility Functions

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_COMPACT](/tidb-cloud-lake/sql/array-compact.md) | Removes null values from an array | `ARRAY_COMPACT([1,null,2,null,3])` → `[1,2,3]` |
| [ARRAY_FLATTEN](/tidb-cloud-lake/sql/array-flatten.md) | Flattens nested arrays into a single array | `ARRAY_FLATTEN([[1,2],[3,4]])` → `[1,2,3,4]` |
| [ARRAY_REVERSE](/tidb-cloud-lake/sql/array-reverse.md) | Reverses the order of array elements | `ARRAY_REVERSE([1,2,3])` → `[3,2,1]` |
| [ARRAY_INDEXOF](/tidb-cloud-lake/sql/array-indexof.md) | Returns the index of first occurrence of an element | `ARRAY_INDEXOF([1,2,3,2], 2)` → `1` |
| [UNNEST](/tidb-cloud-lake/sql/unnest.md) | Expands an array into individual rows | `UNNEST([1,2,3])` → `1, 2, 3` (as separate rows) |
