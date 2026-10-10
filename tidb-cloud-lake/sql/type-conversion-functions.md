---
title: 型変換関数
summary: このセクションでは、{{{ .lake }}} における型変換関数のリファレンス情報を提供します。これらの関数を使用すると、VARIANT 値を他の SQL データ型に厳密にキャストできます。
---

# 型変換関数

このセクションでは、{{{ .lake }}} における型変換関数のリファレンス情報を提供します。これらの関数を使用すると、VARIANT 値を他の SQL データ型に厳密にキャストできます。

## 型変換 {#type-conversion}

| Function | 説明 | 例 |
|----------|-------------|---------|
| [AS_BOOLEAN](/tidb-cloud-lake/sql/as-boolean.md) | VARIANT 値を BOOLEAN に変換します | `AS_BOOLEAN(PARSE_JSON('true'))` → `true` |
| [AS_INTEGER](/tidb-cloud-lake/sql/as-integer.md) | VARIANT 値を BIGINT に変換します | `AS_INTEGER(PARSE_JSON('42'))` → `42` |
| [AS_FLOAT](/tidb-cloud-lake/sql/as-float.md) | VARIANT 値を DOUBLE に変換します | `AS_FLOAT(PARSE_JSON('3.14'))` → `3.14` |
| [AS_DECIMAL](/tidb-cloud-lake/sql/as-decimal.md) | VARIANT 値を DECIMAL に変換します | `AS_DECIMAL(PARSE_JSON('12.34'))` → `12.34` |
| [AS_STRING](/tidb-cloud-lake/sql/as-string.md) | VARIANT 値を STRING に変換します | `AS_STRING(PARSE_JSON('"hello"'))` → `'hello'` |
| [AS_BINARY](/tidb-cloud-lake/sql/as-binary.md) | VARIANT 値を BINARY に変換します | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` → `61626364` |
| [AS_DATE](/tidb-cloud-lake/sql/as-date.md) | VARIANT 値を DATE に変換します | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` → `2025-10-11` |
| [AS_ARRAY](/tidb-cloud-lake/sql/as-array.md) | VARIANT 値を ARRAY に変換します | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` → `[1,2,3]` |
| [AS_OBJECT](/tidb-cloud-lake/sql/as-object.md) | VARIANT 値を OBJECT に変換します | `AS_OBJECT(PARSE_JSON('{"a":1}'))` → `{"a":1}` |

## 重要な注意事項 {#important-notes}

- これらの関数は、VARIANT 値に対して**厳密なキャスト**を実行します
- 入力データ型が VARIANT でない場合、出力は NULL になります
- VARIANT 内の値の型が期待される出力型と一致しない場合、出力は NULL になります
- すべての AS_* 関数は、互換性のない変換に対して NULL を返すことで型安全性を確保します