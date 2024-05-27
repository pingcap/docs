---
title: JSON Functions
summary: JSON関数について学びます。
---

# JSON関数 {#json-functions}

TiDB は、MySQL 8.0 で利用可能な[JSON関数](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html)のほとんどをサポートしています。

## JSON値を作成する関数 {#functions-that-create-json-values}

| 関数名                                                                                                                      | 説明                                                 |
| ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| [JSON_ARRAY([val[, val] ...])](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-array) | 値のリスト（空の場合もある）を評価し、それらの値を含むJSON配列を返します。            |
| [JSON_OBJECT(キー、値[、キー、値]...)](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-object) | キーと値のペアの（空の場合もある）リストを評価し、それらのペアを含むJSONオブジェクトを返します。 |
| [JSON_QUOTE(文字列)](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-quote)              | 引用符付きのJSON値として文字列を返します                             |

## JSON値を検索する関数 {#functions-that-search-json-values}

| 関数名                                                                                                                                                             | 説明                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [JSON_CONTAINS(ターゲット、候補[、パス])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)                                       | 指定された候補JSONドキュメントがターゲットJSONドキュメント内に含まれているかどうかを1または0を返すことで示します。                             |
| [JSON_CONTAINS_PATH(json_doc、one_or_all、パス[、パス]...)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains-path)            | JSONドキュメントに指定されたパスまたはパスにデータが含まれているかどうかを示す0または1を返します。                                       |
| [JSON_EXTRACT(json_doc, パス[, パス] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-extract)                                | `path`の引数に一致するドキュメントの部分から選択されたJSONドキュメントからデータを返します。                                        |
| [-&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)                                                           | 評価パスの後のJSON列から値を返します。1 `JSON_EXTRACT(doc, path_literal)`別名です。                              |
| [-&gt;&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path)                                                       | 評価パスの後のJSON列からの値と、その結果の引用符を外した値を返します。1の別名です`JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` |
| [JSON_KEYS(json_doc[, パス])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys)                                              | JSONオブジェクトの最上位レベルの値からキーをJSON配列として返します。パス引数が指定されている場合は、選択したパスから最上位レベルのキーを返します。              |
| [JSON_SEARCH(json_doc、one_or_all、search_str[、escape_char[、path] ...])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search) | JSONドキュメントで文字列の1つまたはすべてに一致するものを検索する                                                        |
| [値 MEMBER OF(json_array)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of)                                                | 渡された値が JSON 配列の要素である場合は 1 を返します。それ以外の場合は 0 を返します。                                          |
| [JSON_OVERLAPS(json_doc1、json_doc2) は、](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps)                              | 2 つの JSON ドキュメントに重複部分があるかどうかを示します。重複している場合は 1 を返します。重複していない場合は 0 を返します。                    |

## JSON値を変更する関数 {#functions-that-modify-json-values}

| 関数名                                                                                                                                                           | 説明                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| [JSON_APPEND(json_doc、パス、値)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append)                                   | `JSON_ARRAY_APPEND`の別名                |
| [JSON_ARRAY_APPEND(json_doc、パス、val[、パス、val]...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)         | JSONドキュメント内の指定された配列の末尾に値を追加し、結果を返します。 |
| [JSON_ARRAY_INSERT(json_doc、パス、val[、パス、val]...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-insert)         | JSONドキュメントの指定された場所に値を挿入し、結果を返します。     |
| [JSON_INSERT(json_doc、パス、val[、パス、val]...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-insert)                     | JSONドキュメントにデータを挿入し、結果を返します            |
| [JSON_MERGE_PATCH(json_doc、json_doc[、json_doc]...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-patch)       | JSONドキュメントをマージする                      |
| [JSON_MERGE_PRESERVE(json_doc、json_doc[、json_doc]...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-preserve) | 2つ以上のJSONドキュメントを結合し、結合された結果を返します。     |
| [JSON_MERGE(json_doc、json_doc[、json_doc]...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge)                   | `JSON_MERGE_PRESERVE`の非推奨のエイリアス       |
| [JSON_REMOVE(json_doc, パス[, パス] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-remove)                          | JSONドキュメントからデータを削除し、結果を返します           |
| [JSON_REPLACE(json_doc, パス, val[, パス, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-replace)              | JSONドキュメント内の既存の値を置き換え、結果を返します         |
| [JSON_SET(json_doc、パス、val[、パス、val]...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-set)                           | JSONドキュメントにデータを挿入または更新し、結果を返します。      |
| [JSON_UNQUOTE(json_val)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-unquote)                                      | JSON値を引用符で囲まず、結果を文字列として返します。          |

## JSON値属性を返す関数 {#functions-that-return-json-value-attributes}

| 関数名                                                                                                                       | 説明                                                              |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [JSON_DEPTH(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-depth)         | JSONドキュメントの最大深度を返します                                            |
| [JSON_LENGTH(json_doc[, パス])](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-length) | JSONドキュメントの長さを返します。パス引数が指定されている場合は、パス内の値の長さを返します。               |
| [JSON_TYPE(json_val)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-type)           | JSON値の型を示す文字列を返します                                              |
| [JSON_VALID(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-valid)         | json_doc が有効な JSON であるかどうかを確認します。列を json 型に変換する前にチェックするのに役立ちます。 |

## ユーティリティ関数 {#utility-functions}

| 関数名                                                                                                                           | 説明                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| [JSON_PRETTY(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty)             | JSONドキュメントのきれいなフォーマット                                                                                                                      |
| [JSON_STORAGE_FREE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free) | JSON 値のバイナリ表現が更新された後に解放されたstorage容量を返します。TiDB は MySQL とは異なるstorageアーキテクチャを持っているため、この関数は有効な JSON 値に対して常に 0 を返し、MySQL 8.0 との互換性のために実装されています。 |
| [JSON_STORAGE_SIZE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-size) | json 値を格納するために必要なバイトのおおよそのサイズを返します。サイズは圧縮を使用する TiKV を考慮していないため、この関数の出力は MySQL と厳密には互換性がありません。                                              |

## 集計関数 {#aggregate-functions}

| 関数名                                                                                                              | 説明                  |
| ---------------------------------------------------------------------------------------------------------------- | ------------------- |
| [JSON_ARRAYAGG(キー)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-arrayagg)     | キーの集約を提供します。        |
| [JSON_OBJECTAGG(キー、値)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg) | 指定されたキーの値の集計を提供します。 |

## 参照 {#see-also}

-   [JSON 関数リファレンス](https://dev.mysql.com/doc/refman/8.0/en/json-function-reference.html)
-   [JSON データ型](/data-type-json.md)

## サポートされていない関数 {#unsupported-functions}

-   `JSON_SCHEMA_VALID()`
-   `JSON_SCHEMA_VALIDATION_REPORT()`
-   `JSON_TABLE()`
-   `JSON_VALUE()`

詳細については[＃14486](https://github.com/pingcap/tidb/issues/14486)参照してください。
