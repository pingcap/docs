---
title: Type Predicate Functions
---

This section provides reference information for type predicate functions in Databend. These functions enable type checking, validation, and conversion of JSON values.

## Type Checking

| Function | Description | Example |
|----------|-------------|---------|
| [IS_ARRAY](type-predicate/is-array) | Checks if a JSON value is an array | `IS_ARRAY('[1,2,3]')` → `true` |
| [IS_OBJECT](type-predicate/is-object) | Checks if a JSON value is an object | `IS_OBJECT('{"key":"value"}')` → `true` |
| [IS_STRING](type-predicate/is-string) | Checks if a JSON value is a string | `IS_STRING('"hello"')` → `true` |
| [IS_INTEGER](type-predicate/is-integer) | Checks if a JSON value is an integer | `IS_INTEGER('42')` → `true` |
| [IS_FLOAT](type-predicate/is-float) | Checks if a JSON value is a floating-point number | `IS_FLOAT('3.14')` → `true` |
| [IS_BOOLEAN](type-predicate/is-boolean) | Checks if a JSON value is a boolean | `IS_BOOLEAN('true')` → `true` |
| [IS_NULL_VALUE](type-predicate/is-null-value) | Checks if a JSON value is null | `IS_NULL_VALUE('null')` → `true` |


