---
title: Type Conversion Functions
---

This section provides reference information for type conversion functions in Databend. These functions enable strict casting of VARIANT values to other SQL data types.

## Type Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [AS_BOOLEAN](conversion/as-boolean) | Converts a VARIANT value to BOOLEAN | `AS_BOOLEAN(PARSE_JSON('true'))` → `true` |
| [AS_INTEGER](conversion/as-integer) | Converts a VARIANT value to BIGINT | `AS_INTEGER(PARSE_JSON('42'))` → `42` |
| [AS_FLOAT](conversion/as-float) | Converts a VARIANT value to DOUBLE | `AS_FLOAT(PARSE_JSON('3.14'))` → `3.14` |
| [AS_DECIMAL](conversion/as-decimal) | Converts a VARIANT value to DECIMAL | `AS_DECIMAL(PARSE_JSON('12.34'))` → `12.34` |
| [AS_STRING](conversion/as-string) | Converts a VARIANT value to STRING | `AS_STRING(PARSE_JSON('"hello"'))` → `'hello'` |
| [AS_BINARY](conversion/as-binary) | Converts a VARIANT value to BINARY | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` → `61626364` |
| [AS_DATE](conversion/as-date) | Converts a VARIANT value to DATE | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` → `2025-10-11` |
| [AS_ARRAY](conversion/as-array) | Converts a VARIANT value to ARRAY | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` → `[1,2,3]` |
| [AS_OBJECT](conversion/as-object) | Converts a VARIANT value to OBJECT | `AS_OBJECT(PARSE_JSON('{"a":1}'))` → `{"a":1}` |

## Important Notes

- These functions perform **strict casting** of VARIANT values
- If the input data type is not VARIANT, the output is NULL
- If the type of value in the VARIANT does not match the expected output type, the output is NULL
- All AS_* functions ensure type safety by returning NULL for incompatible conversions
