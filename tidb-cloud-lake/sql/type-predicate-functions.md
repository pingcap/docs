---
title: Type Predicate Functions
summary: This section provides reference information for type predicate functions in Databend. These functions enable type checking, validation, and conversion of JSON values.
---
This section provides reference information for type predicate functions in Databend. These functions enable type checking, validation, and conversion of JSON values.

## Type Checking

| Function | Description | Example |
|----------|-------------|---------|
| [IS_ARRAY](/tidb-cloud-lake/sql/is-array.md) | Checks if a JSON value is an array | `IS_ARRAY('[1,2,3]')` → `true` |
| [IS_OBJECT](/tidb-cloud-lake/sql/is-object.md) | Checks if a JSON value is an object | `IS_OBJECT('{"key":"value"}')` → `true` |
| [IS_STRING](/tidb-cloud-lake/sql/is-string.md) | Checks if a JSON value is a string | `IS_STRING('"hello"')` → `true` |
| [IS_INTEGER](/tidb-cloud-lake/sql/is-integer.md) | Checks if a JSON value is an integer | `IS_INTEGER('42')` → `true` |
| [IS_FLOAT](/tidb-cloud-lake/sql/is-float.md) | Checks if a JSON value is a floating-point number | `IS_FLOAT('3.14')` → `true` |
| [IS_BOOLEAN](/tidb-cloud-lake/sql/is-boolean.md) | Checks if a JSON value is a boolean | `IS_BOOLEAN('true')` → `true` |
| [IS_NULL_VALUE](/tidb-cloud-lake/sql/is-null-value.md) | Checks if a JSON value is null | `IS_NULL_VALUE('null')` → `true` |


