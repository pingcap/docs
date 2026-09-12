---
title: 类型谓词函数
summary: 本节提供 {{{ .lake }}} 中类型谓词函数的参考信息。这些函数支持对 JSON 值进行类型检查、验证和转换。
---

# 类型谓词函数

本节提供 {{{ .lake }}} 中类型谓词函数的参考信息。这些函数支持对 JSON 值进行类型检查、验证和转换。

## 类型检查 {#type-checking}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [IS_ARRAY](/tidb-cloud-lake/sql/is-array.md) | 检查 JSON 值是否为数组 | `IS_ARRAY('[1,2,3]')` → `true` |
| [IS_OBJECT](/tidb-cloud-lake/sql/is-object.md) | 检查 JSON 值是否为对象 | `IS_OBJECT('{"key":"value"}')` → `true` |
| [IS_STRING](/tidb-cloud-lake/sql/is-string.md) | 检查 JSON 值是否为字符串 | `IS_STRING('"hello"')` → `true` |
| [IS_INTEGER](/tidb-cloud-lake/sql/is-integer.md) | 检查 JSON 值是否为整数型 | `IS_INTEGER('42')` → `true` |
| [IS_FLOAT](/tidb-cloud-lake/sql/is-float.md) | 检查 JSON 值是否为浮点数 | `IS_FLOAT('3.14')` → `true` |
| [IS_BOOLEAN](/tidb-cloud-lake/sql/is-boolean.md) | 检查 JSON 值是否为布尔值 | `IS_BOOLEAN('true')` → `true` |
| [IS_NULL_VALUE](/tidb-cloud-lake/sql/is-null-value.md) | 检查 JSON 值是否为空值 | `IS_NULL_VALUE('null')` → `true` |