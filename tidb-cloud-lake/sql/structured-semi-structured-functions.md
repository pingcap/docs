---
title: Structured & Semi-Structured Functions
summary: {{{ .lake }}} の構造化関数および半構造化関数を使用すると、配列、オブジェクト、マップ、JSON、その他の構造化データ形式を効率的に処理できます。これらの関数は、構造化データおよび半構造化データの作成、解析、クエリ、変換、操作のための包括的な機能を提供します。
---

# Structured & Semi-Structured Functions

{{{ .lake }}} の構造化関数および半構造化関数を使用すると、配列、オブジェクト、マップ、JSON、その他の構造化データ形式を効率的に処理できます。これらの関数は、構造化データおよび半構造化データの作成、解析、クエリ、変換、操作のための包括的な機能を提供します。

## JSON 関数 {#json-functions}

### 解析と検証 {#parsing-validation}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [PARSE_JSON](/tidb-cloud-lake/sql/parse-json.md) | JSON 文字列を variant 値に解析します | `PARSE_JSON('[1,2,3]')` |
| [CHECK_JSON](/tidb-cloud-lake/sql/check-json.md) | 文字列が有効な JSON かどうかを検証します | `CHECK_JSON('{"a":1}')` |
| [JSON_TYPEOF](/tidb-cloud-lake/sql/json-typeof.md) | JSON 値の型を返します | `JSON_TYPEOF(PARSE_JSON('[1,2,3]'))` |

### パスベースのクエリ {#path-based-querying}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [JSON_PATH_EXISTS](/tidb-cloud-lake/sql/json-path-exists.md) | JSON パスが存在するかどうかを確認します | `JSON_PATH_EXISTS(json_obj, '$.name')` |
| [JSON_PATH_QUERY](/tidb-cloud-lake/sql/json-path-query.md) | JSONPath を使用して JSON データをクエリします | `JSON_PATH_QUERY(json_obj, '$.items[*]')` |
| [JSON_PATH_QUERY_ARRAY](/tidb-cloud-lake/sql/json-path-query-array.md) | JSON データをクエリし、結果を配列として返します | `JSON_PATH_QUERY_ARRAY(json_obj, '$.items')` |
| [JSON_PATH_QUERY_FIRST](/tidb-cloud-lake/sql/json-path-query-first.md) | JSON パスクエリの最初の結果を返します | `JSON_PATH_QUERY_FIRST(json_obj, '$.items[*]')` |
| [JSON_PATH_MATCH](/tidb-cloud-lake/sql/json-path-match.md) | JSON 値をパスパターンに照合します | `JSON_PATH_MATCH(json_obj, '$.age')` |
| [JQ](/tidb-cloud-lake/sql/jq.md) | jq 構文を使用して高度な JSON 処理を行います | `JQ('.name', json_obj)` |

### 値の抽出 {#value-extraction}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [GET](/tidb-cloud-lake/sql/get.md) | JSON オブジェクトからキーで、または配列からインデックスで値を取得します | `GET(PARSE_JSON('[1,2,3]'), 0)` |
| [GET_PATH](/tidb-cloud-lake/sql/get-path.md) | パス式を使用して JSON オブジェクトから値を取得します | `GET_PATH(json_obj, 'user.name')` |
| [GET_IGNORE_CASE](/tidb-cloud-lake/sql/get-ignore-case.md) | 大文字と小文字を区別しないキー照合で値を取得します | `GET_IGNORE_CASE(json_obj, 'NAME')` |
| [JSON_EXTRACT_PATH_TEXT](/tidb-cloud-lake/sql/json-extract-path-text.md) | パスを使用して JSON からテキスト値を抽出します | `JSON_EXTRACT_PATH_TEXT(json_obj, 'name')` |

### 変換と出力 {#transformation-output}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [JSON_TO_STRING](/tidb-cloud-lake/sql/json-to-string.md) | JSON 値を文字列に変換します | `JSON_TO_STRING(PARSE_JSON('{"a":1}'))` |
| [JSON_PRETTY](/tidb-cloud-lake/sql/json-pretty.md) | JSON を適切なインデントで整形します | `JSON_PRETTY(PARSE_JSON('{"a":1}'))` |
| [STRIP_NULL_VALUE](/tidb-cloud-lake/sql/strip-null-value.md) | JSON の null 値を SQL の NULL 値に変換します | `STRIP_NULL_VALUE(parse_json('null'))` → `NULL` |
| [JSON_STRIP_NULLS](/tidb-cloud-lake/sql/json-strip-nulls.md) | JSON オブジェクトから null 値を削除します | `JSON_STRIP_NULLS(PARSE_JSON('{"a":1,"b":null}'))` → `{"a":1}` |

### 配列/オブジェクトの展開 {#array-object-expansion}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [JSON_EACH](/tidb-cloud-lake/sql/json-each.md) | JSON オブジェクトをキーと値のペアに展開します | `JSON_EACH(PARSE_JSON('{"a":1,"b":2}'))` |
| [JSON_ARRAY_ELEMENTS](/tidb-cloud-lake/sql/json-array-elements.md) | JSON 配列を個々の要素に展開します | `JSON_ARRAY_ELEMENTS(PARSE_JSON('[1,2,3]'))` |

## 配列関数 {#array-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [ARRAY](/tidb-cloud-lake/sql/array.md) | 式から配列を構築します | `ARRAY(1, 2, 3)` |
| [ARRAY_CONSTRUCT](/tidb-cloud-lake/sql/array-construct.md) | 個々の値から配列を作成します | `ARRAY_CONSTRUCT(1, 2, 3)` |
| [RANGE](/tidb-cloud-lake/sql/range.md) | 連続した数値の配列を生成します | `RANGE(1, 5)` |
| [ARRAY_GENERATE_RANGE](/tidb-cloud-lake/sql/array-generate-range.md) | オプションのステップ付きでシーケンスを生成します | `ARRAY_GENERATE_RANGE(0, 6, 2)` |
| [GET](/tidb-cloud-lake/sql/get.md) | インデックスで配列から要素を取得します | `GET([1,2,3], 0)` |
| [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md) | GET 関数のエイリアスです | `ARRAY_GET([1,2,3], 1)` |
| [CONTAINS](/tidb-cloud-lake/sql/contains.md) | 配列に特定の値が含まれているかどうかを確認します | `CONTAINS([1,2,3], 2)` |
| [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md) | 配列に特定の値が含まれているかどうかを確認します | `ARRAY_CONTAINS([1,2,3], 2)` |
| [ARRAY_SIZE](/tidb-cloud-lake/sql/array-size.md) | 配列の長さを返します（エイリアス: `ARRAY_LENGTH`） | `ARRAY_SIZE([1,2,3])` |
| [ARRAY_COUNT](/tidb-cloud-lake/sql/array-count.md) | `NULL` ではない要素の数を数えます | `ARRAY_COUNT([1,NULL,2])` |
| [ARRAY_ANY](/tidb-cloud-lake/sql/array-any.md) | 最初の非 `NULL` エントリを返します | `ARRAY_ANY([NULL,'a','b'])` |
| [ARRAY_APPEND](/tidb-cloud-lake/sql/array-append.md) | 配列の末尾に要素を追加します | `ARRAY_APPEND([1,2], 3)` |
| [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md) | 配列の先頭に要素を追加します | `ARRAY_PREPEND([2,3], 1)` |
| [ARRAY_INSERT](/tidb-cloud-lake/sql/array-insert.md) | 指定した位置に要素を挿入します | `ARRAY_INSERT([1,3], 1, 2)` |
| [ARRAY_REMOVE](/tidb-cloud-lake/sql/array-remove.md) | 指定した要素のすべての出現を削除します | `ARRAY_REMOVE([1,2,2,3], 2)` |
| [ARRAY_REMOVE_FIRST](/tidb-cloud-lake/sql/array-remove-first.md) | 配列の最初の要素を削除します | `ARRAY_REMOVE_FIRST([1,2,3])` |
| [ARRAY_REMOVE_LAST](/tidb-cloud-lake/sql/array-remove-last.md) | 配列の最後の要素を削除します | `ARRAY_REMOVE_LAST([1,2,3])` |
| [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md) | 複数の配列を連結します | `ARRAY_CONCAT([1,2], [3,4])` |
| [ARRAY_SLICE](/tidb-cloud-lake/sql/array-slice.md) | 配列の一部を抽出します | `ARRAY_SLICE([1,2,3,4], 1, 2)` |
| [SLICE](/tidb-cloud-lake/sql/slice.md) | ARRAY_SLICE 関数のエイリアスです | `SLICE([1,2,3,4], 1, 2)` |
| [ARRAYS_ZIP](/tidb-cloud-lake/sql/arrays-zip.md) | 複数の配列を要素ごとに結合します | `ARRAYS_ZIP([1,2], ['a','b'])` |
| [ARRAY_DISTINCT](/tidb-cloud-lake/sql/array-distinct.md) | 配列から一意な要素を返します | `ARRAY_DISTINCT([1,2,2,3])` |
| [ARRAY_UNIQUE](/tidb-cloud-lake/sql/array-unique.md) | ARRAY_DISTINCT 関数のエイリアスです | `ARRAY_UNIQUE([1,2,2,3])` |
| [ARRAY_INTERSECTION](/tidb-cloud-lake/sql/array-intersection.md) | 配列間の共通要素を返します | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` |
| [ARRAY_EXCEPT](/tidb-cloud-lake/sql/array-except.md) | 1 つ目の配列にあり 2 つ目の配列にない要素を返します | `ARRAY_EXCEPT([1,2,3], [2,3])` |
| [ARRAY_OVERLAP](/tidb-cloud-lake/sql/array-overlap.md) | 配列に共通要素があるかどうかを確認します | `ARRAY_OVERLAP([1,2], [2,3])` |
| [ARRAY_TRANSFORM](/tidb-cloud-lake/sql/json-array-transform.md) | 各配列要素に関数を適用します | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` |
| [ARRAY_FILTER](/tidb-cloud-lake/sql/array-filter.md) | 条件に基づいて配列要素をフィルタリングします | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` |
| [ARRAY_REDUCE](/tidb-cloud-lake/sql/array-reduce.md) | 集計を使用して配列を単一の値に縮約します | `ARRAY_REDUCE([1,2,3], 0, (acc, x) -> acc + x)` |
| [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md) | 関数を使用して配列要素を集計します | `ARRAY_AGGREGATE([1,2,3], 'sum')` |
| [ARRAY_SUM](/tidb-cloud-lake/sql/array-sum.md) | 数値の合計を返します | `ARRAY_SUM([1,2,3])` |
| [ARRAY_AVG](/tidb-cloud-lake/sql/array-avg.md) | 数値の平均を返します | `ARRAY_AVG([1,2,3])` |
| [ARRAY_MEDIAN](/tidb-cloud-lake/sql/array-median.md) | 数値の中央値を返します | `ARRAY_MEDIAN([1,3,2])` |
| [ARRAY_MIN](/tidb-cloud-lake/sql/array-min.md) | 最小値を返します | `ARRAY_MIN([1,2,3])` |
| [ARRAY_MAX](/tidb-cloud-lake/sql/array-max.md) | 最大値を返します | `ARRAY_MAX([1,2,3])` |
| [ARRAY_STDDEV_POP](/tidb-cloud-lake/sql/array-stddev-pop.md) | 母標準偏差を返します | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](/tidb-cloud-lake/sql/array-stddev-samp.md) | 標本標準偏差を返します | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](/tidb-cloud-lake/sql/array-kurtosis.md) | 過剰尖度を返します | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](/tidb-cloud-lake/sql/array-skewness.md) | 歪度を返します | `ARRAY_SKEWNESS([1,2,3,10])` |
| [ARRAY_APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/array-approx-count-distinct.md) | 近似の distinct 件数を返します | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` |
| [ARRAY_SORT](/tidb-cloud-lake/sql/array-sort.md) | 値をソートします。バリアントにより順序や null の扱いを制御します | `ARRAY_SORT([3,1,2])` |
| [ARRAY_TO_STRING](/tidb-cloud-lake/sql/array-to-string.md) | 配列要素を連結します | `ARRAY_TO_STRING(['a','b'], ',')` |
| [ARRAY_COMPACT](/tidb-cloud-lake/sql/array-compact.md) | 配列から null 値を削除します | `ARRAY_COMPACT([1, NULL, 2, NULL, 3])` |
| [ARRAY_FLATTEN](/tidb-cloud-lake/sql/array-flatten.md) | ネストした配列を 1 つの配列に平坦化します | `ARRAY_FLATTEN([[1,2], [3,4]])` |
| [ARRAY_REVERSE](/tidb-cloud-lake/sql/array-reverse.md) | 配列要素の順序を反転します | `ARRAY_REVERSE([1,2,3])` |
| [ARRAY_INDEXOF](/tidb-cloud-lake/sql/array-indexof.md) | 要素が最初に出現するインデックスを返します | `ARRAY_INDEXOF([1,2,3,2], 2)` |
| [UNNEST](/tidb-cloud-lake/sql/unnest.md) | 配列を個々の行に展開します | `UNNEST([1,2,3])` |

## オブジェクト関数 {#object-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [OBJECT_CONSTRUCT](/tidb-cloud-lake/sql/object-construct.md) | キーと値のペアから JSON オブジェクトを作成します | `OBJECT_CONSTRUCT('name', 'John', 'age', 30)` |
| [OBJECT_CONSTRUCT_KEEP_NULL](/tidb-cloud-lake/sql/object-construct-keep-null.md) | null 値を保持したまま JSON オブジェクトを作成します | `OBJECT_CONSTRUCT_KEEP_NULL('a', 1, 'b', NULL)` |
| [OBJECT_KEYS](/tidb-cloud-lake/sql/object-keys.md) | JSON オブジェクトのすべてのキーを配列として返します | `OBJECT_KEYS(PARSE_JSON('{"a":1,"b":2}'))` |
| [OBJECT_INSERT](/tidb-cloud-lake/sql/object-insert.md) | JSON オブジェクトにキーと値のペアを挿入または更新します | `OBJECT_INSERT(json_obj, 'new_key', 'value')` |
| [OBJECT_DELETE](/tidb-cloud-lake/sql/object-delete.md) | JSON オブジェクトからキーと値のペアを削除します | `OBJECT_DELETE(json_obj, 'key_to_remove')` |
| [OBJECT_PICK](/tidb-cloud-lake/sql/object-pick.md) | 指定したキーのみを含む新しいオブジェクトを作成します | `OBJECT_PICK(json_obj, 'name', 'age')` |

## マップ関数 {#map-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [MAP_CAT](/tidb-cloud-lake/sql/map-cat.md) | 複数のマップを 1 つのマップに結合します | `MAP_CAT({'a':1}, {'b':2})` |
| [MAP_KEYS](/tidb-cloud-lake/sql/map-keys.md) | マップのすべてのキーを配列として返します | `MAP_KEYS({'a':1, 'b':2})` |
| [MAP_VALUES](/tidb-cloud-lake/sql/map-values.md) | マップのすべての値を配列として返します | `MAP_VALUES({'a':1, 'b':2})` |
| [MAP_SIZE](/tidb-cloud-lake/sql/map-size.md) | マップ内のキーと値のペア数を返します | `MAP_SIZE({'a':1, 'b':2})` |
| [MAP_CONTAINS_KEY](/tidb-cloud-lake/sql/map-contains-key.md) | マップに特定のキーが含まれているかどうかを確認します | `MAP_CONTAINS_KEY({'a':1}, 'a')` |
| [MAP_INSERT](/tidb-cloud-lake/sql/map-insert.md) | マップにキーと値のペアを挿入します | `MAP_INSERT({'a':1}, 'b', 2)` |
| [MAP_DELETE](/tidb-cloud-lake/sql/map-delete.md) | マップからキーと値のペアを削除します | `MAP_DELETE({'a':1, 'b':2}, 'b')` |
| [MAP_TRANSFORM_KEYS](/tidb-cloud-lake/sql/map-transform-keys.md) | マップ内の各キーに関数を適用します | `MAP_TRANSFORM_KEYS(map, k -> UPPER(k))` |
| [MAP_TRANSFORM_VALUES](/tidb-cloud-lake/sql/map-transform-values.md) | マップ内の各値に関数を適用します | `MAP_TRANSFORM_VALUES(map, v -> v * 2)` |
| [MAP_FILTER](/tidb-cloud-lake/sql/map-filter.md) | 述語に基づいてキーと値のペアをフィルタリングします | `MAP_FILTER(map, (k, v) -> v > 10)` |
| [MAP_PICK](/tidb-cloud-lake/sql/map-pick.md) | 指定したキーのみを含む新しいマップを作成します | `MAP_PICK({'a':1, 'b':2, 'c':3}, 'a', 'c')` |

## 型変換関数 {#type-conversion-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [AS_BOOLEAN](/tidb-cloud-lake/sql/as-boolean.md) | VARIANT 値を BOOLEAN に変換します | `AS_BOOLEAN(PARSE_JSON('true'))` |
| [AS_INTEGER](/tidb-cloud-lake/sql/as-integer.md) | VARIANT 値を BIGINT に変換します | `AS_INTEGER(PARSE_JSON('42'))` |
| [AS_FLOAT](/tidb-cloud-lake/sql/as-float.md) | VARIANT 値を DOUBLE に変換します | `AS_FLOAT(PARSE_JSON('3.14'))` |
| [AS_DECIMAL](/tidb-cloud-lake/sql/as-decimal.md) | VARIANT 値を DECIMAL に変換します | `AS_DECIMAL(PARSE_JSON('12.34'))` |
| [AS_STRING](/tidb-cloud-lake/sql/as-string.md) | VARIANT 値を STRING に変換します | `AS_STRING(PARSE_JSON('"hello"'))` |
| [AS_BINARY](/tidb-cloud-lake/sql/as-binary.md) | VARIANT 値を BINARY に変換します | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` |
| [AS_DATE](/tidb-cloud-lake/sql/as-date.md) | VARIANT 値を DATE に変換します | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` |
| [AS_ARRAY](/tidb-cloud-lake/sql/as-array.md) | VARIANT 値を ARRAY に変換します | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [AS_OBJECT](/tidb-cloud-lake/sql/as-object.md) | VARIANT 値を OBJECT に変換します | `AS_OBJECT(PARSE_JSON('{"a":1}'))` |

## 型判定関数 {#type-predicate-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [IS_ARRAY](/tidb-cloud-lake/sql/is-array.md) | JSON 値が配列かどうかを確認します | `IS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [IS_OBJECT](/tidb-cloud-lake/sql/is-object.md) | JSON 値がオブジェクトかどうかを確認します | `IS_OBJECT(PARSE_JSON('{"a":1}'))` |
| [IS_STRING](/tidb-cloud-lake/sql/is-string.md) | JSON 値が文字列かどうかを確認します | `IS_STRING(PARSE_JSON('"hello"'))` |
| [IS_INTEGER](/tidb-cloud-lake/sql/is-integer.md) | JSON 値が整数かどうかを確認します | `IS_INTEGER(PARSE_JSON('42'))` |
| [IS_FLOAT](/tidb-cloud-lake/sql/is-float.md) | JSON 値が浮動小数点数かどうかを確認します | `IS_FLOAT(PARSE_JSON('3.14'))` |
| [IS_BOOLEAN](/tidb-cloud-lake/sql/is-boolean.md) | JSON 値がブール値かどうかを確認します | `IS_BOOLEAN(PARSE_JSON('true'))` |
| [IS_NULL_VALUE](/tidb-cloud-lake/sql/is-null-value.md) | JSON 値が null かどうかを確認します | `IS_NULL_VALUE(PARSE_JSON('null'))` |