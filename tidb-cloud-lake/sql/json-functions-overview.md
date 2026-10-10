---
title: JSON 関数
summary: このセクションでは、{{{ .lake }}} の JSON 関数に関するリファレンス情報を提供します。JSON 関数を使用すると、JSON データ構造の解析、検証、クエリ、および操作を実行できます。
---

# JSON 関数

このセクションでは、{{{ .lake }}} の JSON 関数に関するリファレンス情報を提供します。JSON 関数を使用すると、JSON データ構造の解析、検証、クエリ、および操作を実行できます。

## JSON の解析と検証 {#json-parsing-validation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [PARSE_JSON](/tidb-cloud-lake/sql/parse-json.md) | JSON 文字列を variant 値に解析します | `PARSE_JSON('{"name":"John","age":30}')` → `{"name":"John","age":30}` |
| [CHECK_JSON](/tidb-cloud-lake/sql/check-json.md) | 文字列が有効な JSON かどうかを検証します | `CHECK_JSON('{"valid": true}')` → `true` |

## JSON の型情報 {#json-type-information}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [JSON_TYPEOF](/tidb-cloud-lake/sql/json-typeof.md) | JSON 値の型を返します | `JSON_TYPEOF('{"key": "value"}')` → `'OBJECT'` |

## JSON の変換 {#json-conversion}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [JSON_TO_STRING](/tidb-cloud-lake/sql/json-to-string.md) | JSON 値を文字列に変換します | `JSON_TO_STRING({"name":"John"})` → `'{"name":"John"}'` |

## JSON パス操作 {#json-path-operations}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [JSON_PATH_EXISTS](/tidb-cloud-lake/sql/json-path-exists.md) | JSON パスが存在するかどうかを確認します | `JSON_PATH_EXISTS('{"a":1}', '$.a')` → `true` |
| [JSON_PATH_MATCH](/tidb-cloud-lake/sql/json-path-match.md) | JSON 値をパスパターンに照合します | `JSON_PATH_MATCH('{"items":[1,2,3]}', '$.items[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY](/tidb-cloud-lake/sql/json-path-query.md) | JSONPath を使用して JSON データをクエリします | `JSON_PATH_QUERY('{"a":1,"b":2}', '$.a')` → `1` |
| [JSON_PATH_QUERY_ARRAY](/tidb-cloud-lake/sql/json-path-query-array.md) | JSON データをクエリし、結果を配列として返します | `JSON_PATH_QUERY_ARRAY('[1,2,3]', '$[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY_FIRST](/tidb-cloud-lake/sql/json-path-query-first.md) | JSON パスクエリの最初の結果を返します | `JSON_PATH_QUERY_FIRST('[1,2,3]', '$[*]')` → `1` |

## JSON データの抽出 {#json-data-extraction}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [GET](/tidb-cloud-lake/sql/get.md) | インデックスまたはフィールド名で JSON から値を抽出します | `GET('{"name":"John"}', 'name')` → `"John"` |
| [GET_IGNORE_CASE](/tidb-cloud-lake/sql/get-ignore-case.md) | 大文字と小文字を区別しないフィールド照合で値を抽出します | `GET_IGNORE_CASE('{"Name":"John"}', 'name')` → `"John"` |
| [GET_BY_KEYPATH](/tidb-cloud-lake/sql/get-by-keypath.md) | 波かっこ形式のキーパスを使用してネストされた値を抽出します | `GET_BY_KEYPATH('{"user":{"name":"Ada"}}', '{user,name}')` → `"Ada"` |
| [GET_PATH](/tidb-cloud-lake/sql/get-path.md) | パス表記を使用して値を抽出します | `GET_PATH('{"user":{"name":"John"}}', 'user.name')` → `"John"` |
| [JSON_EXTRACT_PATH_TEXT](/tidb-cloud-lake/sql/json-extract-path-text.md) | パスを使用して JSON からテキスト値を抽出します | `JSON_EXTRACT_PATH_TEXT('{"name":"John"}', 'name')` → `'John'` |
| [JSON_EACH](/tidb-cloud-lake/sql/json-each.md) | JSON オブジェクトをキーと値のペアに展開します | `JSON_EACH('{"a":1,"b":2}')` → `[("a",1),("b",2)]` |
| [JSON_ARRAY_ELEMENTS](/tidb-cloud-lake/sql/json-array-elements.md) | JSON 配列を個々の要素に展開します | `JSON_ARRAY_ELEMENTS('[1,2,3]')` → `1, 2, 3` |
| [JQ](/tidb-cloud-lake/sql/jq.md) | jq スタイルのクエリを使用して JSON を処理します | `JQ('{"name":"John"}', '.name')` → `"John"` |

## JSON の整形と処理 {#json-formatting-processing}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [JSON_PRETTY](/tidb-cloud-lake/sql/json-pretty.md) | 適切なインデントで JSON を整形します | `JSON_PRETTY('{"a":1}')` → 整形済み JSON 文字列 |
| [STRIP_NULL_VALUE](/tidb-cloud-lake/sql/strip-null-value.md) | JSON から null 値を削除します | `STRIP_NULL_VALUE('{"a":1,"b":null}')` → `{"a":1}` |
| [JSON_STRIP_NULLS](/tidb-cloud-lake/sql/json-strip-nulls.md) | JSON オブジェクトから null 値を削除します | `JSON_STRIP_NULLS(PARSE_JSON('{"a":1,"b":null}'))` → `{"a":1}` |

## JSON の包含と存在確認 {#json-containment-existence}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [JSON_CONTAINS_IN_LEFT](/tidb-cloud-lake/sql/contains.md) | 左側の JSON が右側の JSON を含むかどうかを判定します | `JSON_CONTAINS_IN_LEFT('{"a":1,"b":2}', '{"b":2}')` → `true` |
| [JSON_EXISTS_KEY](/tidb-cloud-lake/sql/json-exists-key.md) | 特定のキーが存在するかどうかを確認します | `JSON_EXISTS_KEY('{"a":1}', 'a')` → `true` |
| [JSON_EXISTS_ANY_KEYS](/tidb-cloud-lake/sql/json-exists-key.md) | リスト内のいずれかのキーが存在する場合に `true` を返します | `JSON_EXISTS_ANY_KEYS('{"a":1}', ['x','a'])` → `true` |
| [JSON_EXISTS_ALL_KEYS](/tidb-cloud-lake/sql/json-exists-key.md) | すべてのキーが存在する場合にのみ `true` を返します | `JSON_EXISTS_ALL_KEYS('{"a":1,"b":2}', ['a','b'])` → `true` |