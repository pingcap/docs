---
title: JSON Functions
summary: Learn about JSON functions.
---

# JSON関数 {#json-functions}

TiDB は、 MySQL 5.7の GA リリースに同梱されている JSON関数のほとんどをサポートしています。

## JSON値を作成する関数 {#functions-that-create-json-values}

| 関数名                                                                                                                              | 説明                                                      |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [JSON_ARRAY([val[, val] ...])](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-array)         | (空の可能性がある) 値のリストを評価し、それらの値を含む JSON 配列を返します。             |
| [JSON_OBJECT(キー, val[, キー, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-object) | キーと値のペアの (空の可能性がある) リストを評価し、それらのペアを含む JSON オブジェクトを返します。 |
| [JSON_QUOTE(文字列)](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-quote)                      | 文字列を引用符付きの JSON 値として返します                                |

## JSON値を検索する関数 {#functions-that-search-json-values}

| 関数名                                                                                                                                                               | 説明                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [JSON_CONTAINS(ターゲット, 候補[, パス])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)                                       | 1 または 0 を返すことで、指定された候補 JSON ドキュメントがターゲット JSON ドキュメント内に含まれるかどうかを示します。                      |
| [JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains-path)      | 0 または 1 を返し、JSON ドキュメントに指定されたパスのデータが含まれているかどうかを示します。                                      |
| [JSON_EXTRACT(json_doc, パス[, パス] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-extract)                                  | `path`の引数に一致するドキュメントの部分から選択された JSON ドキュメントからデータを返します。                                     |
| [-&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)                                                             | 評価パスの後の JSON 列から値を返します。 `JSON_EXTRACT(doc, path_literal)`のエイリアス                           |
| [-&gt;&gt;](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path)                                                         | パスを評価し、結果の引用符を外した後の JSON 列から値を返します。 `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`のエイリアス |
| [JSON_KEYS(json_doc[, パス])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys)                                                | JSON オブジェクトのトップレベルの値からキーを JSON 配列として返します。パス引数が指定されている場合は、選択したパスからのトップレベルのキーを返します。         |
| [JSON_SEARCH(json_doc, one_or_all, search_str[,scape_char[, path] ...])](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search) | JSON ドキュメント内で文字列の 1 つまたはすべての一致を検索します。                                                     |
| [値のメンバー(json_array)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of)                                                       | 渡された値が JSON 配列の要素である場合は 1 を返します。それ以外の場合は 0 を返します。                                         |
| [JSON_OVERLAPS(json_doc1, json_doc2)](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps)                                  | 2 つの JSON ドキュメントに重複部分があるかどうかを示します。はいの場合は 1 を返します。そうでない場合は 0 を返します。                        |

## JSON値を変更する関数 {#functions-that-modify-json-values}

| 関数名                                                                                                                                                              | 説明                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| [JSON_APPEND(json_doc, パス, 値)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append)                                    | `JSON_ARRAY_APPEND`のエイリアス              |
| [JSON_ARRAY_APPEND(json_doc, パス, 値)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)                        | 指定されたパスにある JSON 配列の末尾に値を追加します          |
| [JSON_ARRAY_INSERT(json_doc, パス, val[, パス, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-insert)       | json ドキュメントに配列を挿入し、変更されたドキュメントを返します。   |
| [JSON_INSERT(json_doc, パス, val[, パス, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-insert)                   | JSON ドキュメントにデータを挿入し、結果を返します。           |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge)                   | `JSON_MERGE_PRESERVE`の非推奨のエイリアス        |
| [JSON_MERGE_PATCH(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-patch)       | JSONドキュメントを結合する                        |
| [JSON_MERGE_PRESERVE(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-preserve) | 2 つ以上の JSON ドキュメントをマージし、マージされた結果を返します。 |
| [JSON_REMOVE(json_doc, パス[, パス] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-remove)                             | JSON ドキュメントからデータを削除し、結果を返します。          |
| [JSON_REPLACE(json_doc, パス, val[, パス, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-replace)                 | JSON ドキュメント内の既存の値を置き換えて結果を返します         |
| [JSON_SET(json_doc, パス, val[, パス, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-set)                         | JSON ドキュメントにデータを挿入または更新し、結果を返します。      |
| [JSON_UNQUOTE(json_val)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-unquote)                                         | JSON 値の引用符を外し、結果を文字列として返します。           |
| [JSON_ARRAY_APPEND(json_doc, パス, val[, パス, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)       | JSON ドキュメント内の指定された配列の末尾に値を追加し、結果を返します。 |
| [JSON_ARRAY_INSERT(json_doc, パス, val[, パス, val] ...)](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-insert)       | JSON ドキュメントの指定された場所に値を挿入し、結果を返します。     |

## JSON 値属性を返す関数 {#functions-that-return-json-value-attributes}

| 関数名                                                                                                                       | 説明                                                              |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [JSON_DEPTH(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-depth)         | JSONドキュメントの最大の深さを返します。                                          |
| [JSON_LENGTH(json_doc[, パス])](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-length) | JSON ドキュメントの長さを返します。パス引数が指定されている場合は、パス内の値の長さを返します。              |
| [JSON_TYPE(json_val)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-type)           | JSON値のタイプを示す文字列を返します。                                           |
| [JSON_VALID(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-valid)         | json_doc が有効な JSON であるかどうかを確認します。 json 型に変換する前に列をチェックするのに役立ちます。 |

## ユーティリティ関数 {#utility-functions}

| 関数名                                                                                                                           | 説明                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [JSON_PRETTY(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty)             | JSON ドキュメントの整形                                                                                                                                             |
| [JSON_STORAGE_FREE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free) | JSON 値が適切に更新された後に、JSON 値のバイナリ表現で解放されたstorageスペースの量を返します。 TiDB は MySQL とは異なるstorageアーキテクチャを持っているため、この関数は有効な JSON 値に対して常に 0 を返し、MySQL 8.0 との互換性のために実装されています。 |
| [JSON_STORAGE_SIZE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-size) | json 値を保存するために必要なバイトのおおよそのサイズを返します。サイズには圧縮を使用する TiKV が考慮されていないため、この関数の出力は MySQL と厳密には互換性がありません。                                                            |

## 集計関数 {#aggregate-functions}

| 関数名                                                                                                               | 説明                  |
| ----------------------------------------------------------------------------------------------------------------- | ------------------- |
| [JSON_ARRAYAGG(キー)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-arrayagg)      | キーの集合を提供します。        |
| [JSON_OBJECTAGG(キー, 値)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg) | 指定されたキーの値の集計を提供します。 |

## こちらも参照 {#see-also}

-   [JSON関数リファレンス](https://dev.mysql.com/doc/refman/8.0/en/json-function-reference.html)
-   [JSON データ型](/data-type-json.md)
