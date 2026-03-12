---
title: Structured & Semi-Structured Functions
---

Structured and semi-structured functions in Databend enable efficient processing of arrays, objects, maps, JSON, and other structured data formats. These functions provide comprehensive capabilities for creating, parsing, querying, transforming, and manipulating structured and semi-structured data.

## JSON Functions

### Parsing & Validation
| Function | Description | Example |
|----------|-------------|--------|
| [PARSE_JSON](semi-structured-functions/json/parse-json) | Parses a JSON string into a variant value | `PARSE_JSON('[1,2,3]')` |
| [CHECK_JSON](semi-structured-functions/json/check-json) | Validates if a string is valid JSON | `CHECK_JSON('{"a":1}')` |
| [JSON_TYPEOF](semi-structured-functions/json/json-typeof) | Returns the type of a JSON value | `JSON_TYPEOF(PARSE_JSON('[1,2,3]'))` |

### Path-based Querying
| Function | Description | Example |
|----------|-------------|--------|
| [JSON_PATH_EXISTS](semi-structured-functions/json/json-path-exists) | Checks if a JSON path exists | `JSON_PATH_EXISTS(json_obj, '$.name')` |
| [JSON_PATH_QUERY](semi-structured-functions/json/json-path-query) | Queries JSON data using JSONPath | `JSON_PATH_QUERY(json_obj, '$.items[*]')` |
| [JSON_PATH_QUERY_ARRAY](semi-structured-functions/json/json-path-query-array) | Queries JSON data and returns results as an array | `JSON_PATH_QUERY_ARRAY(json_obj, '$.items')` |
| [JSON_PATH_QUERY_FIRST](semi-structured-functions/json/json-path-query-first) | Returns the first result from a JSON path query | `JSON_PATH_QUERY_FIRST(json_obj, '$.items[*]')` |
| [JSON_PATH_MATCH](semi-structured-functions/json/json-path-match) | Matches JSON values against a path pattern | `JSON_PATH_MATCH(json_obj, '$.age')` |
| [JQ](semi-structured-functions/json/jq) | Advanced JSON processing using jq syntax | `JQ('.name', json_obj)` |

### Value Extraction
| Function | Description | Example |
|----------|-------------|--------|
| [GET](semi-structured-functions/json/get) | Gets a value from a JSON object by key or array by index | `GET(PARSE_JSON('[1,2,3]'), 0)` |
| [GET_PATH](semi-structured-functions/json/get-path) | Gets a value from a JSON object using a path expression | `GET_PATH(json_obj, 'user.name')` |
| [GET_IGNORE_CASE](semi-structured-functions/json/get-ignore-case) | Gets a value with case-insensitive key matching | `GET_IGNORE_CASE(json_obj, 'NAME')` |
| [JSON_EXTRACT_PATH_TEXT](semi-structured-functions/json/json-extract-path-text) | Extracts text value from JSON using path | `JSON_EXTRACT_PATH_TEXT(json_obj, 'name')` |

### Transformation & Output
| Function | Description | Example |
|----------|-------------|--------|
| [JSON_TO_STRING](semi-structured-functions/json/json-to-string) | Converts a JSON value to a string | `JSON_TO_STRING(PARSE_JSON('{"a":1}'))` |
| [JSON_PRETTY](semi-structured-functions/json/json-pretty) | Formats JSON with proper indentation | `JSON_PRETTY(PARSE_JSON('{"a":1}'))` |
| [STRIP_NULL_VALUE](semi-structured-functions/json/strip-null-value) | Removes null values from JSON | `STRIP_NULL_VALUE(PARSE_JSON('{"a":1,"b":null}'))` |

### Array/Object Expansion
| Function | Description | Example |
|----------|-------------|--------|
| [JSON_EACH](semi-structured-functions/json/json-each) | Expands JSON object into key-value pairs | `JSON_EACH(PARSE_JSON('{"a":1,"b":2}'))` |
| [JSON_ARRAY_ELEMENTS](semi-structured-functions/json/json-array-elements) | Expands JSON array into individual elements | `JSON_ARRAY_ELEMENTS(PARSE_JSON('[1,2,3]'))` |

## Array Functions

| Function | Description | Example |
|----------|-------------|--------|
| [ARRAY](semi-structured-functions/array/array) | Builds an array from expressions | `ARRAY(1, 2, 3)` |
| [ARRAY_CONSTRUCT](semi-structured-functions/array/array-construct) | Creates an array from individual values | `ARRAY_CONSTRUCT(1, 2, 3)` |
| [RANGE](semi-structured-functions/array/range) | Generates an array of sequential numbers | `RANGE(1, 5)` |
| [ARRAY_GENERATE_RANGE](semi-structured-functions/array/array-generate-range) | Generates a sequence with optional step | `ARRAY_GENERATE_RANGE(0, 6, 2)` |
| [GET](semi-structured-functions/array/get) | Gets an element from an array by index | `GET([1,2,3], 0)` |
| [ARRAY_GET](semi-structured-functions/array/array-get) | Alias for GET function | `ARRAY_GET([1,2,3], 1)` |
| [CONTAINS](semi-structured-functions/array/contains) | Checks if an array contains a specific value | `CONTAINS([1,2,3], 2)` |
| [ARRAY_CONTAINS](semi-structured-functions/array/array-contains) | Checks if an array contains a specific value | `ARRAY_CONTAINS([1,2,3], 2)` |
| [ARRAY_SIZE](semi-structured-functions/array/array-size) | Returns array length (alias: `ARRAY_LENGTH`) | `ARRAY_SIZE([1,2,3])` |
| [ARRAY_COUNT](semi-structured-functions/array/array-count) | Counts the non-`NULL` elements | `ARRAY_COUNT([1,NULL,2])` |
| [ARRAY_ANY](semi-structured-functions/array/array-any) | Returns the first non-`NULL` entry | `ARRAY_ANY([NULL,'a','b'])` |
| [ARRAY_APPEND](semi-structured-functions/array/array-append) | Appends an element to the end of an array | `ARRAY_APPEND([1,2], 3)` |
| [ARRAY_PREPEND](semi-structured-functions/array/array-prepend) | Prepends an element to the beginning of an array | `ARRAY_PREPEND([2,3], 1)` |
| [ARRAY_INSERT](semi-structured-functions/array/array-insert) | Inserts an element at a specific position | `ARRAY_INSERT([1,3], 1, 2)` |
| [ARRAY_REMOVE](semi-structured-functions/array/array-remove) | Removes all occurrences of a specified element | `ARRAY_REMOVE([1,2,2,3], 2)` |
| [ARRAY_REMOVE_FIRST](semi-structured-functions/array/array-remove-first) | Removes the first element from an array | `ARRAY_REMOVE_FIRST([1,2,3])` |
| [ARRAY_REMOVE_LAST](semi-structured-functions/array/array-remove-last) | Removes the last element from an array | `ARRAY_REMOVE_LAST([1,2,3])` |
| [ARRAY_CONCAT](semi-structured-functions/array/array-concat) | Concatenates multiple arrays | `ARRAY_CONCAT([1,2], [3,4])` |
| [ARRAY_SLICE](semi-structured-functions/array/array-slice) | Extracts a portion of an array | `ARRAY_SLICE([1,2,3,4], 1, 2)` |
| [SLICE](semi-structured-functions/array/slice) | Alias for ARRAY_SLICE function | `SLICE([1,2,3,4], 1, 2)` |
| [ARRAYS_ZIP](semi-structured-functions/array/arrays-zip) | Combines multiple arrays element-wise | `ARRAYS_ZIP([1,2], ['a','b'])` |
| [ARRAY_DISTINCT](semi-structured-functions/array/array-distinct) | Returns unique elements from an array | `ARRAY_DISTINCT([1,2,2,3])` |
| [ARRAY_UNIQUE](semi-structured-functions/array/array-unique) | Alias for ARRAY_DISTINCT function | `ARRAY_UNIQUE([1,2,2,3])` |
| [ARRAY_INTERSECTION](semi-structured-functions/array/array-intersection) | Returns common elements between arrays | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` |
| [ARRAY_EXCEPT](semi-structured-functions/array/array-except) | Returns elements in first array but not in second | `ARRAY_EXCEPT([1,2,3], [2,3])` |
| [ARRAY_OVERLAP](semi-structured-functions/array/array-overlap) | Checks if arrays have common elements | `ARRAY_OVERLAP([1,2], [2,3])` |
| [ARRAY_TRANSFORM](semi-structured-functions/array/array-transform) | Applies a function to each array element | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` |
| [ARRAY_FILTER](semi-structured-functions/array/array-filter) | Filters array elements based on a condition | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` |
| [ARRAY_REDUCE](semi-structured-functions/array/array-reduce) | Reduces array to a single value using aggregation | `ARRAY_REDUCE([1,2,3], 0, (acc, x) -> acc + x)` |
| [ARRAY_AGGREGATE](semi-structured-functions/array/array-aggregate) | Aggregates array elements using a function | `ARRAY_AGGREGATE([1,2,3], 'sum')` |
| [ARRAY_SUM](semi-structured-functions/array/array-sum) | Sum of numeric values | `ARRAY_SUM([1,2,3])` |
| [ARRAY_AVG](semi-structured-functions/array/array-avg) | Average of numeric values | `ARRAY_AVG([1,2,3])` |
| [ARRAY_MEDIAN](semi-structured-functions/array/array-median) | Median of numeric values | `ARRAY_MEDIAN([1,3,2])` |
| [ARRAY_MIN](semi-structured-functions/array/array-min) | Minimum value | `ARRAY_MIN([1,2,3])` |
| [ARRAY_MAX](semi-structured-functions/array/array-max) | Maximum value | `ARRAY_MAX([1,2,3])` |
| [ARRAY_STDDEV_POP](semi-structured-functions/array/array-stddev-pop) | Population standard deviation | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](semi-structured-functions/array/array-stddev-samp) | Sample standard deviation | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](semi-structured-functions/array/array-kurtosis) | Excess kurtosis | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](semi-structured-functions/array/array-skewness) | Skewness | `ARRAY_SKEWNESS([1,2,3,10])` |
| [ARRAY_APPROX_COUNT_DISTINCT](semi-structured-functions/array/array-approx-count-distinct) | Approximate distinct count | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` |
| [ARRAY_SORT](semi-structured-functions/array/array-sort) | Sorts values; variants control order/nulls | `ARRAY_SORT([3,1,2])` |
| [ARRAY_TO_STRING](semi-structured-functions/array/array-to-string) | Joins array elements | `ARRAY_TO_STRING(['a','b'], ',')` |
| [ARRAY_COMPACT](semi-structured-functions/array/array-compact) | Removes null values from an array | `ARRAY_COMPACT([1, NULL, 2, NULL, 3])` |
| [ARRAY_FLATTEN](semi-structured-functions/array/array-flatten) | Flattens nested arrays into a single array | `ARRAY_FLATTEN([[1,2], [3,4]])` |
| [ARRAY_REVERSE](semi-structured-functions/array/array-reverse) | Reverses the order of array elements | `ARRAY_REVERSE([1,2,3])` |
| [ARRAY_INDEXOF](semi-structured-functions/array/array-indexof) | Returns the index of first occurrence of an element | `ARRAY_INDEXOF([1,2,3,2], 2)` |
| [UNNEST](semi-structured-functions/array/unnest) | Expands an array into individual rows | `UNNEST([1,2,3])` |

## Object Functions

| Function | Description | Example |
|----------|-------------|--------|
| [OBJECT_CONSTRUCT](semi-structured-functions/object/object-construct) | Creates a JSON object from key-value pairs | `OBJECT_CONSTRUCT('name', 'John', 'age', 30)` |
| [OBJECT_CONSTRUCT_KEEP_NULL](semi-structured-functions/object/object-construct-keep-null) | Creates a JSON object keeping null values | `OBJECT_CONSTRUCT_KEEP_NULL('a', 1, 'b', NULL)` |
| [OBJECT_KEYS](semi-structured-functions/object/object-keys) | Returns all keys from a JSON object as an array | `OBJECT_KEYS(PARSE_JSON('{"a":1,"b":2}'))` |
| [OBJECT_INSERT](semi-structured-functions/object/object-insert) | Inserts or updates a key-value pair in a JSON object | `OBJECT_INSERT(json_obj, 'new_key', 'value')` |
| [OBJECT_DELETE](semi-structured-functions/object/object-delete) | Removes a key-value pair from a JSON object | `OBJECT_DELETE(json_obj, 'key_to_remove')` |
| [OBJECT_PICK](semi-structured-functions/object/object-pick) | Creates a new object with only specified keys | `OBJECT_PICK(json_obj, 'name', 'age')` |

## Map Functions

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_CAT](semi-structured-functions/map/map-cat) | Combines multiple maps into a single map | `MAP_CAT({'a':1}, {'b':2})` |
| [MAP_KEYS](semi-structured-functions/map/map-keys) | Returns all keys from a map as an array | `MAP_KEYS({'a':1, 'b':2})` |
| [MAP_VALUES](semi-structured-functions/map/map-values) | Returns all values from a map as an array | `MAP_VALUES({'a':1, 'b':2})` |
| [MAP_SIZE](semi-structured-functions/map/map-size) | Returns the number of key-value pairs in a map | `MAP_SIZE({'a':1, 'b':2})` |
| [MAP_CONTAINS_KEY](semi-structured-functions/map/map-contains-key) | Checks if a map contains a specific key | `MAP_CONTAINS_KEY({'a':1}, 'a')` |
| [MAP_INSERT](semi-structured-functions/map/map-insert) | Inserts a key-value pair into a map | `MAP_INSERT({'a':1}, 'b', 2)` |
| [MAP_DELETE](semi-structured-functions/map/map-delete) | Removes a key-value pair from a map | `MAP_DELETE({'a':1, 'b':2}, 'b')` |
| [MAP_TRANSFORM_KEYS](semi-structured-functions/map/map-transform-keys) | Applies a function to each key in a map | `MAP_TRANSFORM_KEYS(map, k -> UPPER(k))` |
| [MAP_TRANSFORM_VALUES](semi-structured-functions/map/map-transform-values) | Applies a function to each value in a map | `MAP_TRANSFORM_VALUES(map, v -> v * 2)` |
| [MAP_FILTER](semi-structured-functions/map/map-filter) | Filters key-value pairs based on a predicate | `MAP_FILTER(map, (k, v) -> v > 10)` |
| [MAP_PICK](semi-structured-functions/map/map-pick) | Creates a new map with only specified keys | `MAP_PICK({'a':1, 'b':2, 'c':3}, 'a', 'c')` |

## Type Conversion Functions

| Function | Description | Example |
|----------|-------------|---------|
| [AS_BOOLEAN](semi-structured-functions/conversion/as-boolean) | Converts a VARIANT value to BOOLEAN | `AS_BOOLEAN(PARSE_JSON('true'))` |
| [AS_INTEGER](semi-structured-functions/conversion/as-integer) | Converts a VARIANT value to BIGINT | `AS_INTEGER(PARSE_JSON('42'))` |
| [AS_FLOAT](semi-structured-functions/conversion/as-float) | Converts a VARIANT value to DOUBLE | `AS_FLOAT(PARSE_JSON('3.14'))` |
| [AS_DECIMAL](semi-structured-functions/conversion/as-decimal) | Converts a VARIANT value to DECIMAL | `AS_DECIMAL(PARSE_JSON('12.34'))` |
| [AS_STRING](semi-structured-functions/conversion/as-string) | Converts a VARIANT value to STRING | `AS_STRING(PARSE_JSON('"hello"'))` |
| [AS_BINARY](semi-structured-functions/conversion/as-binary) | Converts a VARIANT value to BINARY | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` |
| [AS_DATE](semi-structured-functions/conversion/as-date) | Converts a VARIANT value to DATE | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` |
| [AS_ARRAY](semi-structured-functions/conversion/as-array) | Converts a VARIANT value to ARRAY | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [AS_OBJECT](semi-structured-functions/conversion/as-object) | Converts a VARIANT value to OBJECT | `AS_OBJECT(PARSE_JSON('{"a":1}'))` |

## Type Predicate Functions

| Function | Description | Example |
|----------|-------------|--------|
| [IS_ARRAY](semi-structured-functions/type-predicate/is-array) | Checks if a JSON value is an array | `IS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [IS_OBJECT](semi-structured-functions/type-predicate/is-object) | Checks if a JSON value is an object | `IS_OBJECT(PARSE_JSON('{"a":1}'))` |
| [IS_STRING](semi-structured-functions/type-predicate/is-string) | Checks if a JSON value is a string | `IS_STRING(PARSE_JSON('"hello"'))` |
| [IS_INTEGER](semi-structured-functions/type-predicate/is-integer) | Checks if a JSON value is an integer | `IS_INTEGER(PARSE_JSON('42'))` |
| [IS_FLOAT](semi-structured-functions/type-predicate/is-float) | Checks if a JSON value is a floating-point number | `IS_FLOAT(PARSE_JSON('3.14'))` |
| [IS_BOOLEAN](semi-structured-functions/type-predicate/is-boolean) | Checks if a JSON value is a boolean | `IS_BOOLEAN(PARSE_JSON('true'))` |
| [IS_NULL_VALUE](semi-structured-functions/type-predicate/is-null-value) | Checks if a JSON value is null | `IS_NULL_VALUE(PARSE_JSON('null'))` |
