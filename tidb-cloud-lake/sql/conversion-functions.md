---
title: 转换函数
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的转换函数，便于参考。
---

# 转换函数

本页按功能分类，全面概述了 {{{ .lake }}} 中的转换函数，便于参考。

## 类型转换函数 {#type-conversion-functions}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [CAST](/tidb-cloud-lake/sql/cast.md) | 将值转换为指定的数据类型 | `CAST('123' AS INT)` → `123` |
| [TRY_CAST](/tidb-cloud-lake/sql/try-cast.md) | 安全地将值转换为指定的数据类型，失败时返回 NULL | `TRY_CAST('abc' AS INT)` → `NULL` |
| [TO_BOOLEAN](/tidb-cloud-lake/sql/to-boolean.md) | 将值转换为 BOOLEAN 类型 | `TO_BOOLEAN('true')` → `true` |
| [TO_STRING](/tidb-cloud-lake/sql/to-string.md) | 将值转换为 STRING 类型 | `TO_STRING(123)` → `'123'` |
| [TO_VARCHAR](/tidb-cloud-lake/sql/to-varchar.md) | 将值转换为 VARCHAR 类型 | `TO_VARCHAR(123)` → `'123'` |
| [TO_TEXT](/tidb-cloud-lake/sql/to-text.md) | 将值转换为 TEXT 类型 | `TO_TEXT(123)` → `'123'` |

## 数值转换函数 {#numeric-conversion-functions}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [TO_INT8](/tidb-cloud-lake/sql/to-int8.md) | 将值转换为 INT8 类型 | `TO_INT8('123')` → `123` |
| [TO_INT16](/tidb-cloud-lake/sql/to-int16.md) | 将值转换为 INT16 类型 | `TO_INT16('123')` → `123` |
| [TO_INT32](/tidb-cloud-lake/sql/to-int32.md) | 将值转换为 INT32 类型 | `TO_INT32('123')` → `123` |
| [TO_INT64](/tidb-cloud-lake/sql/to-int64.md) | 将值转换为 INT64 类型 | `TO_INT64('123')` → `123` |
| [TO_UINT8](/tidb-cloud-lake/sql/to-uint8.md) | 将值转换为 UINT8 类型 | `TO_UINT8('123')` → `123` |
| [TO_UINT16](/tidb-cloud-lake/sql/to-uint16.md) | 将值转换为 UINT16 类型 | `TO_UINT16('123')` → `123` |
| [TO_UINT32](/tidb-cloud-lake/sql/to-uint32.md) | 将值转换为 UINT32 类型 | `TO_UINT32('123')` → `123` |
| [TO_UINT64](/tidb-cloud-lake/sql/to-uint64.md) | 将值转换为 UINT64 类型 | `TO_UINT64('123')` → `123` |
| [TO_FLOAT32](/tidb-cloud-lake/sql/to-float32.md) | 将值转换为 FLOAT32 类型 | `TO_FLOAT32('123.45')` → `123.45` |
| [TO_FLOAT64](/tidb-cloud-lake/sql/to-float64.md) | 将值转换为 FLOAT64 类型 | `TO_FLOAT64('123.45')` → `123.45` |

## 二进制和专用转换函数 {#binary-and-specialized-conversion-functions}

| Function | 描述 | 示例 |
|----------|-------------|---------|
| [TO_BINARY](/tidb-cloud-lake/sql/to-binary.md) | 将值转换为 BINARY 类型 | `TO_BINARY('abc')` → `binary value` |
| [TRY_TO_BINARY](/tidb-cloud-lake/sql/try-to-binary.md) | 安全地将值转换为 BINARY 类型，失败时返回 NULL | `TRY_TO_BINARY('abc')` → `binary value` |
| [TO_HEX](/tidb-cloud-lake/sql/to-hex.md) | 将值转换为十六进制字符串 | `TO_HEX(255)` → `'FF'` |
| [TO_VARIANT](/tidb-cloud-lake/sql/to-variant.md) | 将值转换为 VARIANT 类型 | `TO_VARIANT('{"a": 1}')` → `{"a": 1}` |
| [BUILD_BITMAP](/tidb-cloud-lake/sql/build-bitmap.md) | 从整数数组构建位图 | `BUILD_BITMAP([1,2,3])` → `bitmap value` |
| [TO_BITMAP](/tidb-cloud-lake/sql/to-bitmap.md) | 将值转换为 BITMAP 类型 | `TO_BITMAP([1,2,3])` → `bitmap value` |

将值从一种类型转换为另一种类型时，请注意以下事项：

- 当从浮点数、小数或字符串转换为整数，或转换为带小数部分的小数时，{{{ .lake }}} 会将值四舍五入到最接近的整数。这由设置 `numeric_cast_option` 决定（默认值为 `'rounding'`），该设置控制数值类型转换操作的行为。当 `numeric_cast_option` 显式设置为 `'truncating'` 时，{{{ .lake }}} 会截断小数部分，丢弃所有小数值。

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

    下表汇总了数值类型转换操作，展示了不同源数值数据类型与目标数值数据类型之间的转换可能性。请注意，其中还说明了从 String 转换为 Integer 的要求，即源字符串必须包含一个整数值。

    | 源类型 | 目标类型 |
    |----------------|-------------|
    | 字符串         | Decimal     |
    | float          | Decimal     |
    | Decimal        | Decimal     |
    | float          | Int         |
    | Decimal        | Int         |
    | 字符串 (整数型)   | Int         |

- {{{ .lake }}} 还提供了多种函数，用于将表达式转换为不同的日期和时间格式。更多信息，请参见 [日期与时间函数](/tidb-cloud-lake/sql/date-time-functions.md)。