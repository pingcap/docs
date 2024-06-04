---
title: JSON Functions that search JSON values
summary: Learn about JSON functions that search JSON values.
---

## [JSON_CONTAINS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)

Indicates by returning 1 or 0 whether a given candidate JSON document is contained within a target JSON document.

## [JSON_CONTAINS_PATH()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains-path)

Returns 0 or 1 to indicate whether a JSON document contains data at a given path or paths.

## [JSON_EXTRACT()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-extract)

Returns data from a JSON document, selected from the parts of the document matched by the `path` arguments.

## [->](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)

Returns the value from a JSON column after the evaluating path; an alias for `JSON_EXTRACT(doc, path_literal)`.

## [->>](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path)

Returns the value from a JSON column after the evaluating path and unquoting the result; an alias for `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`.

## [JSON_KEYS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys)

Returns the keys from the top-level value of a JSON object as a JSON array, or, if a path argument is given, the top-level keys from the selected path.

## [JSON_SEARCH()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search)

Search a JSON document for one or all matches of a string.

## [MEMBER OF()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of)

If the passed value is an element of the JSON array, returns 1. Otherwise, returns 0.

## [JSON_OVERLAPS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps)

Indicates whether two JSON documents have overlapping part. If yes, returns 1. If not, returns 0.

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)