---
title: 型述語関数
summary: このセクションでは、{{{ .lake }}} の型述語関数に関するリファレンス情報を提供します。これらの関数により、JSON 値の型チェック、検証、および変換が可能になります。
---

# 型述語関数

このセクションでは、{{{ .lake }}} の型述語関数に関するリファレンス情報を提供します。これらの関数により、JSON 値の型チェック、検証、および変換が可能になります。

## 型チェック {#type-checking}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [IS_ARRAY](/tidb-cloud-lake/sql/is-array.md) | JSON 値が配列かどうかをチェックします | `IS_ARRAY('[1,2,3]')` → `true` |
| [IS_OBJECT](/tidb-cloud-lake/sql/is-object.md) | JSON 値がオブジェクトかどうかをチェックします | `IS_OBJECT('{"key":"value"}')` → `true` |
| [IS_STRING](/tidb-cloud-lake/sql/is-string.md) | JSON 値が文字列かどうかをチェックします | `IS_STRING('"hello"')` → `true` |
| [IS_INTEGER](/tidb-cloud-lake/sql/is-integer.md) | JSON 値が整数かどうかをチェックします | `IS_INTEGER('42')` → `true` |
| [IS_FLOAT](/tidb-cloud-lake/sql/is-float.md) | JSON 値が浮動小数点数かどうかをチェックします | `IS_FLOAT('3.14')` → `true` |
| [IS_BOOLEAN](/tidb-cloud-lake/sql/is-boolean.md) | JSON 値がブール値かどうかをチェックします | `IS_BOOLEAN('true')` → `true` |
| [IS_NULL_VALUE](/tidb-cloud-lake/sql/is-null-value.md) | JSON 値が null かどうかをチェックします | `IS_NULL_VALUE('null')` → `true` |