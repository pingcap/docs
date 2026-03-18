---
title: Type Conversion Functions
summary: This section provides reference information for type conversion functions in Databend. These functions enable strict casting of VARIANT values to other SQL data types.
---
This section provides reference information for type conversion functions in Databend. These functions enable strict casting of VARIANT values to other SQL data types.

## Type Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [AS_BOOLEAN](/tidb-cloud-lake/sql/as-boolean.md) | Converts a VARIANT value to BOOLEAN | `AS_BOOLEAN(PARSE_JSON('true'))` → `true` |
| [AS_INTEGER](/tidb-cloud-lake/sql/as-integer.md) | Converts a VARIANT value to BIGINT | `AS_INTEGER(PARSE_JSON('42'))` → `42` |
| [AS_FLOAT](/tidb-cloud-lake/sql/as-float.md) | Converts a VARIANT value to DOUBLE | `AS_FLOAT(PARSE_JSON('3.14'))` → `3.14` |
| [AS_DECIMAL](/tidb-cloud-lake/sql/as-decimal.md) | Converts a VARIANT value to DECIMAL | `AS_DECIMAL(PARSE_JSON('12.34'))` → `12.34` |
| [AS_STRING](/tidb-cloud-lake/sql/as-string.md) | Converts a VARIANT value to STRING | `AS_STRING(PARSE_JSON('"hello"'))` → `'hello'` |
| [AS_BINARY](/tidb-cloud-lake/sql/as-binary.md) | Converts a VARIANT value to BINARY | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` → `61626364` |
| [AS_DATE](/tidb-cloud-lake/sql/as-date.md) | Converts a VARIANT value to DATE | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` → `2025-10-11` |
| [AS_ARRAY](/tidb-cloud-lake/sql/as-array.md) | Converts a VARIANT value to ARRAY | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` → `[1,2,3]` |
| [AS_OBJECT](/tidb-cloud-lake/sql/as-object.md) | Converts a VARIANT value to OBJECT | `AS_OBJECT(PARSE_JSON('{"a":1}'))` → `{"a":1}` |

## Important Notes

- These functions perform **strict casting** of VARIANT values
- If the input data type is not VARIANT, the output is NULL
- If the type of value in the VARIANT does not match the expected output type, the output is NULL
- All AS_* functions ensure type safety by returning NULL for incompatible conversions
