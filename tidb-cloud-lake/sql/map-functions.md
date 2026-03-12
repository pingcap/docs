---
title: Map Functions
---

This section provides reference information for the map functions in Databend. Map functions allow you to create, manipulate, and extract information from map data structures (key-value pairs).

## Map Creation and Combination

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_CAT](map/map-cat) | Combines multiple maps into a single map | `MAP_CAT({'a':1}, {'b':2})` → `{'a':1,'b':2}` |

## Map Access and Information

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_KEYS](map/map-keys) | Returns all keys from a map as an array | `MAP_KEYS({'a':1,'b':2})` → `['a','b']` |
| [MAP_VALUES](map/map-values) | Returns all values from a map as an array | `MAP_VALUES({'a':1,'b':2})` → `[1,2]` |
| [MAP_SIZE](map/map-size) | Returns the number of key-value pairs in a map | `MAP_SIZE({'a':1,'b':2,'c':3})` → `3` |
| [MAP_CONTAINS_KEY](map/map-contains-key) | Checks if a map contains a specific key | `MAP_CONTAINS_KEY({'a':1,'b':2}, 'a')` → `TRUE` |

## Map Modification

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_INSERT](map/map-insert) | Inserts a key-value pair into a map | `MAP_INSERT({'a':1,'b':2}, 'c', 3)` → `{'a':1,'b':2,'c':3}` |
| [MAP_DELETE](map/map-delete) | Removes a key-value pair from a map | `MAP_DELETE({'a':1,'b':2,'c':3}, 'b')` → `{'a':1,'c':3}` |

## Map Transformation

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_TRANSFORM_KEYS](map/map-transform-keys) | Applies a function to each key in a map | `MAP_TRANSFORM_KEYS({'a':1,'b':2}, x -> UPPER(x))` → `{'A':1,'B':2}` |
| [MAP_TRANSFORM_VALUES](map/map-transform-values) | Applies a function to each value in a map | `MAP_TRANSFORM_VALUES({'a':1,'b':2}, x -> x * 10)` → `{'a':10,'b':20}` |

## Map Filtering and Selection

| Function | Description | Example |
|----------|-------------|--------|
| [MAP_FILTER](map/map-filter) | Filters key-value pairs based on a predicate | `MAP_FILTER({'a':1,'b':2,'c':3}, (k,v) -> v > 1)` → `{'b':2,'c':3}` |
| [MAP_PICK](map/map-pick) | Creates a new map with only specified keys | `MAP_PICK({'a':1,'b':2,'c':3}, ['a','c'])` → `{'a':1,'c':3}` |
