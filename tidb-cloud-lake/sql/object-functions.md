---
title: Object Functions
---

This section provides reference information for object functions in Databend. Object functions enable creation, manipulation, and extraction of information from JSON object data structures.

## Object Construction

| Function | Description | Example |
|----------|-------------|---------|
| [OBJECT_CONSTRUCT](object/object-construct) | Creates a JSON object from key-value pairs | `OBJECT_CONSTRUCT('name', 'John', 'age', 30)` → `{"name":"John","age":30}` |
| [OBJECT_CONSTRUCT_KEEP_NULL](object/object-construct-keep-null) | Creates a JSON object keeping null values | `OBJECT_CONSTRUCT_KEEP_NULL('a', 1, 'b', null)` → `{"a":1,"b":null}` |

## Object Information

| Function | Description | Example |
|----------|-------------|---------|
| [OBJECT_KEYS](object/object-keys) | Returns all keys from a JSON object as an array | `OBJECT_KEYS({"name":"John","age":30})` → `["name","age"]` |

## Object Modification

| Function | Description | Example |
|----------|-------------|---------|
| [OBJECT_INSERT](object/object-insert) | Inserts or updates a key-value pair in a JSON object | `OBJECT_INSERT({"name":"John"}, "age", 30)` → `{"name":"John","age":30}` |
| [OBJECT_DELETE](object/object-delete) | Removes a key-value pair from a JSON object | `OBJECT_DELETE({"name":"John","age":30}, "age")` → `{"name":"John"}` |

## Object Selection

| Function | Description | Example |
|----------|-------------|---------|
| [OBJECT_PICK](object/object-pick) | Creates a new object with only specified keys | `OBJECT_PICK({"a":1,"b":2,"c":3}, ["a","c"])` → `{"a":1,"c":3}` |
