---
title: Map Functions
summary: This section provides reference information for the map functions in Databend. Map functions allow you to create, manipulate, and extract information from map data structures (key-value pairs).
---
This section provides reference information for the map functions in Databend. Map functions allow you to create, manipulate, and extract information from map data structures (key-value pairs).

## Map Creation and Combination

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_CAT](/tidb-cloud-lake/sql/map-cat.md) | Combines multiple maps into a single map | `MAP_CAT({'a':1}, {'b':2})` → `{'a':1,'b':2}` |

## Map Access and Information

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_KEYS](/tidb-cloud-lake/sql/map-keys.md) | Returns all keys from a map as an array | `MAP_KEYS({'a':1,'b':2})` → `['a','b']` |
| [MAP_VALUES](/tidb-cloud-lake/sql/map-values.md) | Returns all values from a map as an array | `MAP_VALUES({'a':1,'b':2})` → `[1,2]` |
| [MAP_SIZE](/tidb-cloud-lake/sql/map-size.md) | Returns the number of key-value pairs in a map | `MAP_SIZE({'a':1,'b':2,'c':3})` → `3` |
| [MAP_CONTAINS_KEY](/tidb-cloud-lake/sql/map-contains-key.md) | Checks if a map contains a specific key | `MAP_CONTAINS_KEY({'a':1,'b':2}, 'a')` → `TRUE` |

## Map Modification

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_INSERT](/tidb-cloud-lake/sql/map-insert.md) | Inserts a key-value pair into a map | `MAP_INSERT({'a':1,'b':2}, 'c', 3)` → `{'a':1,'b':2,'c':3}` |
| [MAP_DELETE](/tidb-cloud-lake/sql/map-delete.md) | Removes a key-value pair from a map | `MAP_DELETE({'a':1,'b':2,'c':3}, 'b')` → `{'a':1,'c':3}` |

## Map Transformation

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_TRANSFORM_KEYS](/tidb-cloud-lake/sql/map-transform-keys.md) | Applies a function to each key in a map | `MAP_TRANSFORM_KEYS({'a':1,'b':2}, x -> UPPER(x))` → `{'A':1,'B':2}` |
| [MAP_TRANSFORM_VALUES](/tidb-cloud-lake/sql/map-transform-values.md) | Applies a function to each value in a map | `MAP_TRANSFORM_VALUES({'a':1,'b':2}, x -> x * 10)` → `{'a':10,'b':20}` |

## Map Filtering and Selection

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_FILTER](/tidb-cloud-lake/sql/map-filter.md) | Filters key-value pairs based on a predicate | `MAP_FILTER({'a':1,'b':2,'c':3}, (k,v) -> v > 1)` → `{'b':2,'c':3}` |
| [MAP_PICK](/tidb-cloud-lake/sql/map-pick.md) | Creates a new map with only specified keys | `MAP_PICK({'a':1,'b':2,'c':3}, ['a','c'])` → `{'a':1,'c':3}` |
