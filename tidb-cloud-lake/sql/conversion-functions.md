---
title: Conversion Functions
summary: This page provides a comprehensive overview of Conversion functions in Databend, organized by functionality for easy reference.
---
This page provides a comprehensive overview of Conversion functions in Databend, organized by functionality for easy reference.

## Type Conversion Functions

| Function | Description | Example |
|----------|-------------|---------|
| [CAST](/tidb-cloud-lake/sql/cast.md) | Converts a value to a specified data type | `CAST('123' AS INT)` → `123` |
| [TRY_CAST](/tidb-cloud-lake/sql/try-cast.md) | Safely converts a value to a specified data type, returning NULL on failure | `TRY_CAST('abc' AS INT)` → `NULL` |
| [TO_BOOLEAN](/tidb-cloud-lake/sql/to-boolean.md) | Converts a value to BOOLEAN type | `TO_BOOLEAN('true')` → `true` |
| [TO_STRING](/tidb-cloud-lake/sql/to-string.md) | Converts a value to STRING type | `TO_STRING(123)` → `'123'` |
| [TO_VARCHAR](/tidb-cloud-lake/sql/to-varchar.md) | Converts a value to VARCHAR type | `TO_VARCHAR(123)` → `'123'` |
| [TO_TEXT](/tidb-cloud-lake/sql/to-text.md) | Converts a value to TEXT type | `TO_TEXT(123)` → `'123'` |

## Numeric Conversion Functions

| Function | Description | Example |
|----------|-------------|---------|
| [TO_INT8](/tidb-cloud-lake/sql/to-int8.md) | Converts a value to INT8 type | `TO_INT8('123')` → `123` |
| [TO_INT16](/tidb-cloud-lake/sql/to-int16.md) | Converts a value to INT16 type | `TO_INT16('123')` → `123` |
| [TO_INT32](/tidb-cloud-lake/sql/to-int32.md) | Converts a value to INT32 type | `TO_INT32('123')` → `123` |
| [TO_INT64](/tidb-cloud-lake/sql/to-int64.md) | Converts a value to INT64 type | `TO_INT64('123')` → `123` |
| [TO_UINT8](/tidb-cloud-lake/sql/to-uint8.md) | Converts a value to UINT8 type | `TO_UINT8('123')` → `123` |
| [TO_UINT16](/tidb-cloud-lake/sql/to-uint16.md) | Converts a value to UINT16 type | `TO_UINT16('123')` → `123` |
| [TO_UINT32](/tidb-cloud-lake/sql/to-uint32.md) | Converts a value to UINT32 type | `TO_UINT32('123')` → `123` |
| [TO_UINT64](/tidb-cloud-lake/sql/to-uint64.md) | Converts a value to UINT64 type | `TO_UINT64('123')` → `123` |
| [TO_FLOAT32](/tidb-cloud-lake/sql/to-float32.md) | Converts a value to FLOAT32 type | `TO_FLOAT32('123.45')` → `123.45` |
| [TO_FLOAT64](/tidb-cloud-lake/sql/to-float64.md) | Converts a value to FLOAT64 type | `TO_FLOAT64('123.45')` → `123.45` |

## Binary and Specialized Conversion Functions

| Function | Description | Example |
|----------|-------------|---------|
| [TO_BINARY](/tidb-cloud-lake/sql/to-binary.md) | Converts a value to BINARY type | `TO_BINARY('abc')` → `binary value` |
| [TRY_TO_BINARY](/tidb-cloud-lake/sql/try-to-binary.md) | Safely converts a value to BINARY type, returning NULL on failure | `TRY_TO_BINARY('abc')` → `binary value` |
| [TO_HEX](/tidb-cloud-lake/sql/to-hex.md) | Converts a value to hexadecimal string | `TO_HEX(255)` → `'FF'` |
| [TO_VARIANT](/tidb-cloud-lake/sql/to-variant.md) | Converts a value to VARIANT type | `TO_VARIANT('{"a": 1}')` → `{"a": 1}` |
| [BUILD_BITMAP](/tidb-cloud-lake/sql/build-bitmap.md) | Builds a bitmap from an array of integers | `BUILD_BITMAP([1,2,3])` → `bitmap value` |
| [TO_BITMAP](/tidb-cloud-lake/sql/to-bitmap.md) | Converts a value to BITMAP type | `TO_BITMAP([1,2,3])` → `bitmap value` |

Please note the following when converting a value from one type to another:

- When converting from floating-point, decimal numbers, or strings to integers or decimal numbers with fractional parts, Databend rounds the values to the nearest integer. This is determined by the setting `numeric_cast_option` (defaults to 'rounding') which controls the behavior of numeric casting operations. When `numeric_cast_option` is explicitly set to 'truncating', Databend will truncate the decimal part, discarding any fractional values.

    ```sql title='Example:'
    SELECT CAST('0.6' AS DECIMAL(10, 0)), CAST(0.6 AS DECIMAL(10, 0)), CAST(1.5 AS INT);

    ┌──────────────────────────────────────────────────────────────────────────────────┐
    │ cast('0.6' as decimal(10, 0)) │ cast(0.6 as decimal(10, 0)) │ cast(1.5 as int32) │
    ├───────────────────────────────┼─────────────────────────────┼────────────────────┤
    │                             1 │                           1 │                  2 │
    └──────────────────────────────────────────────────────────────────────────────────┘

    SET numeric_cast_option = 'truncating';

    SELECT CAST('0.6' AS DECIMAL(10, 0)), CAST(0.6 AS DECIMAL(10, 0)), CAST(1.5 AS INT);

    ┌──────────────────────────────────────────────────────────────────────────────────┐
    │ cast('0.6' as decimal(10, 0)) │ cast(0.6 as decimal(10, 0)) │ cast(1.5 as int32) │
    ├───────────────────────────────┼─────────────────────────────┼────────────────────┤
    │                             0 │                           0 │                  1 │
    └──────────────────────────────────────────────────────────────────────────────────┘
    ```

    The table below presents a summary of numeric casting operations, highlighting the casting possibilities between different source and target numeric data types. Please note that, it specifies the requirement for String to Integer casting, where the source string must contain an integer value.

    | Source Type    | Target Type |
    |----------------|-------------|
    | String         | Decimal     |
    | Float          | Decimal     |
    | Decimal        | Decimal     |
    | Float          | Int         |
    | Decimal        | Int         |
    | String (Int)   | Int         |


- Databend also offers a variety of functions for converting expressions into different date and time formats. For more information, see [Date & Time Functions](/tidb-cloud-lake/sql/date-time-functions.md).