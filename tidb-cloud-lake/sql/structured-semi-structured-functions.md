---
title: Structured & Semi-Structured Functions
summary: Structured and semi-structured functions in Databend enable efficient processing of arrays, objects, maps, JSON, and other structured data formats. These functions provide comprehensive capabilities for creating, parsing, querying, transforming, and manipulating structured and semi-structured data.
---
Structured and semi-structured functions in Databend enable efficient processing of arrays, objects, maps, JSON, and other structured data formats. These functions provide comprehensive capabilities for creating, parsing, querying, transforming, and manipulating structured and semi-structured data.

## JSON Functions

### Parsing & Validation

| Function | Description | Example |
|----------|-------------|--------|
| [PARSE_JSON](/tidb-cloud-lake/sql/parse-json.md) | Parses a JSON string into a variant value | `PARSE_JSON('[1,2,3]')` |
| [CHECK_JSON](/tidb-cloud-lake/sql/check-json.md) | Validates if a string is valid JSON | `CHECK_JSON('{"a":1}')` |
| [JSON_TYPEOF](/tidb-cloud-lake/sql/json-typeof.md) | Returns the type of a JSON value | `JSON_TYPEOF(PARSE_JSON('[1,2,3]'))` |

### Path-based Querying

| Function | Description | Example |
|----------|-------------|--------|
| [JSON_PATH_EXISTS](/tidb-cloud-lake/sql/json-path-exists.md) | Checks if a JSON path exists | `JSON_PATH_EXISTS(json_obj, '$.name')` |
| [JSON_PATH_QUERY](/tidb-cloud-lake/sql/json-path-query.md) | Queries JSON data using JSONPath | `JSON_PATH_QUERY(json_obj, '$.items[*]')` |
| [JSON_PATH_QUERY_ARRAY](/tidb-cloud-lake/sql/json-path-query-array.md) | Queries JSON data and returns results as an array | `JSON_PATH_QUERY_ARRAY(json_obj, '$.items')` |
| [JSON_PATH_QUERY_FIRST](/tidb-cloud-lake/sql/json-path-query-first.md) | Returns the first result from a JSON path query | `JSON_PATH_QUERY_FIRST(json_obj, '$.items[*]')` |
| [JSON_PATH_MATCH](/tidb-cloud-lake/sql/json-path-match.md) | Matches JSON values against a path pattern | `JSON_PATH_MATCH(json_obj, '$.age')` |
| [JQ](/tidb-cloud-lake/sql/jq.md) | Advanced JSON processing using jq syntax | `JQ('.name', json_obj)` |

### Value Extraction

| Function | Description | Example |
|----------|-------------|--------|
| [GET](/tidb-cloud-lake/sql/get.md) | Gets a value from a JSON object by key or array by index | `GET(PARSE_JSON('[1,2,3]'), 0)` |
| [GET_PATH](/tidb-cloud-lake/sql/get-path.md) | Gets a value from a JSON object using a path expression | `GET_PATH(json_obj, 'user.name')` |
| [GET_IGNORE_CASE](/tidb-cloud-lake/sql/get-ignore-case.md) | Gets a value with case-insensitive key matching | `GET_IGNORE_CASE(json_obj, 'NAME')` |
| [JSON_EXTRACT_PATH_TEXT](/tidb-cloud-lake/sql/json-extract-path-text.md) | Extracts text value from JSON using path | `JSON_EXTRACT_PATH_TEXT(json_obj, 'name')` |

### Transformation & Output

| Function | Description | Example |
|----------|-------------|--------|
| [JSON_TO_STRING](/tidb-cloud-lake/sql/json-to-string.md) | Converts a JSON value to a string | `JSON_TO_STRING(PARSE_JSON('{"a":1}'))` |
| [JSON_PRETTY](/tidb-cloud-lake/sql/json-pretty.md) | Formats JSON with proper indentation | `JSON_PRETTY(PARSE_JSON('{"a":1}'))` |
| [STRIP_NULL_VALUE](/tidb-cloud-lake/sql/strip-null-value.md) | Removes null values from JSON | `STRIP_NULL_VALUE(PARSE_JSON('{"a":1,"b":null}'))` |

### Array/Object Expansion

| Function | Description | Example |
|----------|-------------|--------|
| [JSON_EACH](/tidb-cloud-lake/sql/json-each.md) | Expands JSON object into key-value pairs | `JSON_EACH(PARSE_JSON('{"a":1,"b":2}'))` |
| [JSON_ARRAY_ELEMENTS](/tidb-cloud-lake/sql/json-array-elements.md) | Expands JSON array into individual elements | `JSON_ARRAY_ELEMENTS(PARSE_JSON('[1,2,3]'))` |

## Array Functions

| Function | Description | Example |
|----------|-------------|--------|
| [ARRAY](/tidb-cloud-lake/sql/array.md) | Builds an array from expressions | `ARRAY(1, 2, 3)` |
| [ARRAY_CONSTRUCT](/tidb-cloud-lake/sql/array-construct.md) | Creates an array from individual values | `ARRAY_CONSTRUCT(1, 2, 3)` |
| [RANGE](/tidb-cloud-lake/sql/range.md) | Generates an array of sequential numbers | `RANGE(1, 5)` |
| [ARRAY_GENERATE_RANGE](/tidb-cloud-lake/sql/array-generate-range.md) | Generates a sequence with optional step | `ARRAY_GENERATE_RANGE(0, 6, 2)` |
| [GET](/tidb-cloud-lake/sql/get.md) | Gets an element from an array by index | `GET([1,2,3], 0)` |
| [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md) | Alias for GET function | `ARRAY_GET([1,2,3], 1)` |
| [CONTAINS](/tidb-cloud-lake/sql/contains.md) | Checks if an array contains a specific value | `CONTAINS([1,2,3], 2)` |
| [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md) | Checks if an array contains a specific value | `ARRAY_CONTAINS([1,2,3], 2)` |
| [ARRAY_SIZE](/tidb-cloud-lake/sql/array-size.md) | Returns array length (alias: `ARRAY_LENGTH`) | `ARRAY_SIZE([1,2,3])` |
| [ARRAY_COUNT](/tidb-cloud-lake/sql/array-count.md) | Counts the non-`NULL` elements | `ARRAY_COUNT([1,NULL,2])` |
| [ARRAY_ANY](/tidb-cloud-lake/sql/array-any.md) | Returns the first non-`NULL` entry | `ARRAY_ANY([NULL,'a','b'])` |
| [ARRAY_APPEND](/tidb-cloud-lake/sql/array-append.md) | Appends an element to the end of an array | `ARRAY_APPEND([1,2], 3)` |
| [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md) | Prepends an element to the beginning of an array | `ARRAY_PREPEND([2,3], 1)` |
| [ARRAY_INSERT](/tidb-cloud-lake/sql/array-insert.md) | Inserts an element at a specific position | `ARRAY_INSERT([1,3], 1, 2)` |
| [ARRAY_REMOVE](/tidb-cloud-lake/sql/array-remove.md) | Removes all occurrences of a specified element | `ARRAY_REMOVE([1,2,2,3], 2)` |
| [ARRAY_REMOVE_FIRST](/tidb-cloud-lake/sql/array-remove-first.md) | Removes the first element from an array | `ARRAY_REMOVE_FIRST([1,2,3])` |
| [ARRAY_REMOVE_LAST](/tidb-cloud-lake/sql/array-remove-last.md) | Removes the last element from an array | `ARRAY_REMOVE_LAST([1,2,3])` |
| [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md) | Concatenates multiple arrays | `ARRAY_CONCAT([1,2], [3,4])` |
| [ARRAY_SLICE](/tidb-cloud-lake/sql/array-slice.md) | Extracts a portion of an array | `ARRAY_SLICE([1,2,3,4], 1, 2)` |
| [SLICE](/tidb-cloud-lake/sql/slice.md) | Alias for ARRAY_SLICE function | `SLICE([1,2,3,4], 1, 2)` |
| [ARRAYS_ZIP](/tidb-cloud-lake/sql/arrays-zip.md) | Combines multiple arrays element-wise | `ARRAYS_ZIP([1,2], ['a','b'])` |
| [ARRAY_DISTINCT](/tidb-cloud-lake/sql/array-distinct.md) | Returns unique elements from an array | `ARRAY_DISTINCT([1,2,2,3])` |
| [ARRAY_UNIQUE](/tidb-cloud-lake/sql/array-unique.md) | Alias for ARRAY_DISTINCT function | `ARRAY_UNIQUE([1,2,2,3])` |
| [ARRAY_INTERSECTION](/tidb-cloud-lake/sql/array-intersection.md) | Returns common elements between arrays | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` |
| [ARRAY_EXCEPT](/tidb-cloud-lake/sql/array-except.md) | Returns elements in first array but not in second | `ARRAY_EXCEPT([1,2,3], [2,3])` |
| [ARRAY_OVERLAP](/tidb-cloud-lake/sql/array-overlap.md) | Checks if arrays have common elements | `ARRAY_OVERLAP([1,2], [2,3])` |
| [ARRAY_TRANSFORM](/tidb-cloud-lake/sql/json-array-transform.md) | Applies a function to each array element | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` |
| [ARRAY_FILTER](/tidb-cloud-lake/sql/array-filter.md) | Filters array elements based on a condition | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` |
| [ARRAY_REDUCE](/tidb-cloud-lake/sql/array-reduce.md) | Reduces array to a single value using aggregation | `ARRAY_REDUCE([1,2,3], 0, (acc, x) -> acc + x)` |
| [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md) | Aggregates array elements using a function | `ARRAY_AGGREGATE([1,2,3], 'sum')` |
| [ARRAY_SUM](/tidb-cloud-lake/sql/array-sum.md) | Sum of numeric values | `ARRAY_SUM([1,2,3])` |
| [ARRAY_AVG](/tidb-cloud-lake/sql/array-avg.md) | Average of numeric values | `ARRAY_AVG([1,2,3])` |
| [ARRAY_MEDIAN](/tidb-cloud-lake/sql/array-median.md) | Median of numeric values | `ARRAY_MEDIAN([1,3,2])` |
| [ARRAY_MIN](/tidb-cloud-lake/sql/array-min.md) | Minimum value | `ARRAY_MIN([1,2,3])` |
| [ARRAY_MAX](/tidb-cloud-lake/sql/array-max.md) | Maximum value | `ARRAY_MAX([1,2,3])` |
| [ARRAY_STDDEV_POP](/tidb-cloud-lake/sql/array-stddev-pop.md) | Population standard deviation | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](/tidb-cloud-lake/sql/array-stddev-samp.md) | Sample standard deviation | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](/tidb-cloud-lake/sql/array-kurtosis.md) | Excess kurtosis | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](/tidb-cloud-lake/sql/array-skewness.md) | Skewness | `ARRAY_SKEWNESS([1,2,3,10])` |
| [ARRAY_APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/array-approx-count-distinct.md) | Approximate distinct count | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` |
| [ARRAY_SORT](/tidb-cloud-lake/sql/array-sort.md) | Sorts values; variants control order/nulls | `ARRAY_SORT([3,1,2])` |
| [ARRAY_TO_STRING](/tidb-cloud-lake/sql/array-to-string.md) | Joins array elements | `ARRAY_TO_STRING(['a','b'], ',')` |
| [ARRAY_COMPACT](/tidb-cloud-lake/sql/array-compact.md) | Removes null values from an array | `ARRAY_COMPACT([1, NULL, 2, NULL, 3])` |
| [ARRAY_FLATTEN](/tidb-cloud-lake/sql/array-flatten.md) | Flattens nested arrays into a single array | `ARRAY_FLATTEN([[1,2], [3,4]])` |
| [ARRAY_REVERSE](/tidb-cloud-lake/sql/array-reverse.md) | Reverses the order of array elements | `ARRAY_REVERSE([1,2,3])` |
| [ARRAY_INDEXOF](/tidb-cloud-lake/sql/array-indexof.md) | Returns the index of first occurrence of an element | `ARRAY_INDEXOF([1,2,3,2], 2)` |
| [UNNEST](/tidb-cloud-lake/sql/unnest.md) | Expands an array into individual rows | `UNNEST([1,2,3])` |

## Object Functions

| Function | Description | Example |
|----------|-------------|--------|
| [OBJECT_CONSTRUCT](/tidb-cloud-lake/sql/object-construct.md) | Creates a JSON object from key-value pairs | `OBJECT_CONSTRUCT('name', 'John', 'age', 30)` |
| [OBJECT_CONSTRUCT_KEEP_NULL](/tidb-cloud-lake/sql/object-construct-keep-null.md) | Creates a JSON object keeping null values | `OBJECT_CONSTRUCT_KEEP_NULL('a', 1, 'b', NULL)` |
| [OBJECT_KEYS](/tidb-cloud-lake/sql/object-keys.md) | Returns all keys from a JSON object as an array | `OBJECT_KEYS(PARSE_JSON('{"a":1,"b":2}'))` |
| [OBJECT_INSERT](/tidb-cloud-lake/sql/object-insert.md) | Inserts or updates a key-value pair in a JSON object | `OBJECT_INSERT(json_obj, 'new_key', 'value')` |
| [OBJECT_DELETE](/tidb-cloud-lake/sql/object-delete.md) | Removes a key-value pair from a JSON object | `OBJECT_DELETE(json_obj, 'key_to_remove')` |
| [OBJECT_PICK](/tidb-cloud-lake/sql/object-pick.md) | Creates a new object with only specified keys | `OBJECT_PICK(json_obj, 'name', 'age')` |

## Map Functions

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_CAT](/tidb-cloud-lake/sql/map-cat.md) | Combines multiple maps into a single map | `MAP_CAT({'a':1}, {'b':2})` |
| [MAP_KEYS](/tidb-cloud-lake/sql/map-keys.md) | Returns all keys from a map as an array | `MAP_KEYS({'a':1, 'b':2})` |
| [MAP_VALUES](/tidb-cloud-lake/sql/map-values.md) | Returns all values from a map as an array | `MAP_VALUES({'a':1, 'b':2})` |
| [MAP_SIZE](/tidb-cloud-lake/sql/map-size.md) | Returns the number of key-value pairs in a map | `MAP_SIZE({'a':1, 'b':2})` |
| [MAP_CONTAINS_KEY](/tidb-cloud-lake/sql/map-contains-key.md) | Checks if a map contains a specific key | `MAP_CONTAINS_KEY({'a':1}, 'a')` |
| [MAP_INSERT](/tidb-cloud-lake/sql/map-insert.md) | Inserts a key-value pair into a map | `MAP_INSERT({'a':1}, 'b', 2)` |
| [MAP_DELETE](/tidb-cloud-lake/sql/map-delete.md) | Removes a key-value pair from a map | `MAP_DELETE({'a':1, 'b':2}, 'b')` |
| [MAP_TRANSFORM_KEYS](/tidb-cloud-lake/sql/map-transform-keys.md) | Applies a function to each key in a map | `MAP_TRANSFORM_KEYS(map, k -> UPPER(k))` |
| [MAP_TRANSFORM_VALUES](/tidb-cloud-lake/sql/map-transform-values.md) | Applies a function to each value in a map | `MAP_TRANSFORM_VALUES(map, v -> v * 2)` |
| [MAP_FILTER](/tidb-cloud-lake/sql/map-filter.md) | Filters key-value pairs based on a predicate | `MAP_FILTER(map, (k, v) -> v > 10)` |
| [MAP_PICK](/tidb-cloud-lake/sql/map-pick.md) | Creates a new map with only specified keys | `MAP_PICK({'a':1, 'b':2, 'c':3}, 'a', 'c')` |

## Type Conversion Functions

| Function | Description | Example |
|----------|-------------|---------|
| [AS_BOOLEAN](/tidb-cloud-lake/sql/as-boolean.md) | Converts a VARIANT value to BOOLEAN | `AS_BOOLEAN(PARSE_JSON('true'))` |
| [AS_INTEGER](/tidb-cloud-lake/sql/as-integer.md) | Converts a VARIANT value to BIGINT | `AS_INTEGER(PARSE_JSON('42'))` |
| [AS_FLOAT](/tidb-cloud-lake/sql/as-float.md) | Converts a VARIANT value to DOUBLE | `AS_FLOAT(PARSE_JSON('3.14'))` |
| [AS_DECIMAL](/tidb-cloud-lake/sql/as-decimal.md) | Converts a VARIANT value to DECIMAL | `AS_DECIMAL(PARSE_JSON('12.34'))` |
| [AS_STRING](/tidb-cloud-lake/sql/as-string.md) | Converts a VARIANT value to STRING | `AS_STRING(PARSE_JSON('"hello"'))` |
| [AS_BINARY](/tidb-cloud-lake/sql/as-binary.md) | Converts a VARIANT value to BINARY | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` |
| [AS_DATE](/tidb-cloud-lake/sql/as-date.md) | Converts a VARIANT value to DATE | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` |
| [AS_ARRAY](/tidb-cloud-lake/sql/as-array.md) | Converts a VARIANT value to ARRAY | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [AS_OBJECT](/tidb-cloud-lake/sql/as-object.md) | Converts a VARIANT value to OBJECT | `AS_OBJECT(PARSE_JSON('{"a":1}'))` |

## Type Predicate Functions

| Function | Description | Example |
|----------|-------------|--------|
| [IS_ARRAY](/tidb-cloud-lake/sql/is-array.md) | Checks if a JSON value is an array | `IS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [IS_OBJECT](/tidb-cloud-lake/sql/is-object.md) | Checks if a JSON value is an object | `IS_OBJECT(PARSE_JSON('{"a":1}'))` |
| [IS_STRING](/tidb-cloud-lake/sql/is-string.md) | Checks if a JSON value is a string | `IS_STRING(PARSE_JSON('"hello"'))` |
| [IS_INTEGER](/tidb-cloud-lake/sql/is-integer.md) | Checks if a JSON value is an integer | `IS_INTEGER(PARSE_JSON('42'))` |
| [IS_FLOAT](/tidb-cloud-lake/sql/is-float.md) | Checks if a JSON value is a floating-point number | `IS_FLOAT(PARSE_JSON('3.14'))` |
| [IS_BOOLEAN](/tidb-cloud-lake/sql/is-boolean.md) | Checks if a JSON value is a boolean | `IS_BOOLEAN(PARSE_JSON('true'))` |
| [IS_NULL_VALUE](/tidb-cloud-lake/sql/is-null-value.md) | Checks if a JSON value is null | `IS_NULL_VALUE(PARSE_JSON('null'))` |
