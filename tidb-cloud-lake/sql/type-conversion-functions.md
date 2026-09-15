---
title: 类型转换函数
summary: 本节提供 {{{ .lake }}} 中类型转换函数的参考信息。这些函数支持将 VARIANT 值严格转换为其他 SQL 数据类型。
---

# 类型转换函数

本节提供 {{{ .lake }}} 中类型转换函数的参考信息。这些函数支持将 VARIANT 值严格转换为其他 SQL 数据类型。

## 类型转换 {#type-conversion}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [AS_BOOLEAN](/tidb-cloud-lake/sql/as-boolean.md) | 将 VARIANT 值转换为 BOOLEAN | `AS_BOOLEAN(PARSE_JSON('true'))` → `true` |
| [AS_INTEGER](/tidb-cloud-lake/sql/as-integer.md) | 将 VARIANT 值转换为 BIGINT | `AS_INTEGER(PARSE_JSON('42'))` → `42` |
| [AS_FLOAT](/tidb-cloud-lake/sql/as-float.md) | 将 VARIANT 值转换为 DOUBLE | `AS_FLOAT(PARSE_JSON('3.14'))` → `3.14` |
| [AS_DECIMAL](/tidb-cloud-lake/sql/as-decimal.md) | 将 VARIANT 值转换为 DECIMAL | `AS_DECIMAL(PARSE_JSON('12.34'))` → `12.34` |
| [AS_STRING](/tidb-cloud-lake/sql/as-string.md) | 将 VARIANT 值转换为 STRING | `AS_STRING(PARSE_JSON('"hello"'))` → `'hello'` |
| [AS_BINARY](/tidb-cloud-lake/sql/as-binary.md) | 将 VARIANT 值转换为 BINARY | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` → `61626364` |
| [AS_DATE](/tidb-cloud-lake/sql/as-date.md) | 将 VARIANT 值转换为 DATE | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` → `2025-10-11` |
| [AS_ARRAY](/tidb-cloud-lake/sql/as-array.md) | 将 VARIANT 值转换为 ARRAY | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` → `[1,2,3]` |
| [AS_OBJECT](/tidb-cloud-lake/sql/as-object.md) | 将 VARIANT 值转换为 OBJECT | `AS_OBJECT(PARSE_JSON('{"a":1}'))` → `{"a":1}` |

## 重要说明 {#important-notes}

- 这些函数对 VARIANT 值执行**严格转换**
- 如果输入数据类型不是 VARIANT，则输出为 NULL
- 如果 VARIANT 中的值类型与预期的输出类型不匹配，则输出为 NULL
- 所有 AS_* 函数都会通过在不兼容转换时返回 NULL 来确保类型安全