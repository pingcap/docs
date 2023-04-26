---
title: JSON Functions
summary: Learn about JSON functions.
---

# JSON 関数 {#json-functions}

TiDB は、 MySQL 5.7の GA リリースに同梱された JSON関数のほとんどをサポートしています。

## JSON 値を作成する関数 {#functions-that-create-json-values}

| 関数名                                                     | 説明                                                      |
| ------------------------------------------------------- | ------------------------------------------------------- |
| [JSON\_ARRAY(\[val\[, val\] ...\])][json_array]         | (空の可能性がある) 値のリストを評価し、それらの値を含む JSON 配列を返します。             |
| [JSON\_OBJECT(key, val\[, key, val\] ...)][json_object] | キーと値のペアの (場合によっては空の) リストを評価し、それらのペアを含む JSON オブジェクトを返します |
| [JSON\_QUOTE(string)][json_quote]                       | 文字列を引用符付きの JSON 値として返します                                |

## JSON 値を検索する関数 {#functions-that-search-json-values}

| 関数名                                                                                     | 説明                                                                                    |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [JSON\_CONTAINS(target, candidate\[, path\])][json_contains]                            | 指定された候補 JSON ドキュメントがターゲット JSON ドキュメント内に含まれているかどうかを 1 または 0 を返すことによって示します              |
| [JSON\_CONTAINS\_PATH(json\_doc, one\_or\_all, path\[, path\] ...)][json_contains_path] | JSON ドキュメントに特定のパスにデータが含まれているかどうかを示すために、0 または 1 を返します。                                 |
| [JSON\_EXTRACT(json\_doc, path\[, path\] ...)][json_extract]                            | `path`の引数に一致するドキュメントの部分から選択された JSON ドキュメントからデータを返します                                  |
| [->][json_short_extract]                                                                | 評価パスの後に JSON 列から値を返します。 `JSON_EXTRACT(doc, path_literal)`の別名                          |
| [->>][json_short_extract_unquote]                                                       | パスを評価し、結果の引用符を外した後、JSON 列から値を返します。 `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`の別名 |
| [JSON\_KEYS(json\_doc\[, path\])][json_keys]                                            | JSON オブジェクトの最上位の値からキーを JSON 配列として返すか、パス引数が指定されている場合は、選択したパスから最上位のキーを返します              |
| [JSON\_SEARCH(json\_doc, one\_or\_all, search\_string)][json_search]                    | 文字列の 1 つまたはすべての一致について JSON ドキュメントを検索します                                               |

## JSON 値を変更する関数 {#functions-that-modify-json-values}

| 関数名                                                                                   | 説明                                    |
| ------------------------------------------------------------------------------------- | ------------------------------------- |
| [JSON\_APPEND(json\_doc, path, value)][json_append]                                   | `JSON_ARRAY_APPEND`へのエイリアス            |
| [JSON\_ARRAY\_APPEND(json\_doc, path, value)][json_array_append]                      | 指定されたパスの JSON 配列の末尾に値を追加します           |
| [JSON\_ARRAY\_INSERT(json\_doc, path, val\[, path, val\] ...)][json_array_insert]     | json ドキュメントに配列を挿入し、変更されたドキュメントを返します   |
| [JSON\_INSERT(json\_doc, path, val\[, path, val\] ...)][json_insert]                  | データを JSON ドキュメントに挿入し、結果を返します          |
| [JSON\_MERGE(json\_doc, json\_doc\[, json\_doc\] ...)][json_merge]                    | `JSON_MERGE_PRESERVE`の非推奨のエイリアス       |
| [JSON\_MERGE\_PATCH(json\_doc, json\_doc\[, json\_doc\] ...)][json_merge_patch]       | JSON ドキュメントをマージする                     |
| [JSON\_MERGE\_PRESERVE(json\_doc, json\_doc\[, json\_doc\] ...)][json_merge_preserve] | 2 つ以上の JSON ドキュメントをマージし、マージ結果を返します    |
| [JSON\_REMOVE(json\_doc, path\[, path\] ...)][json_remove]                            | JSON ドキュメントからデータを削除し、結果を返します          |
| [JSON\_REPLACE(json\_doc, path, val\[, path, val\] ...)][json_replace]                | JSON ドキュメント内の既存の値を置き換え、結果を返します        |
| [JSON\_SET(json\_doc, path, val\[, path, val\] ...)][json_set]                        | JSON ドキュメントにデータを挿入または更新し、結果を返します      |
| [JSON\_UNQUOTE(json\_val)][json_unquote]                                              | JSON 値の引用符を外し、結果を文字列として返します           |
| [JSON\_ARRAY\_APPEND(json\_doc, path, val\[, path, val\] ...)][json_array_append]     | JSON ドキュメント内の指定された配列の末尾に値を追加し、結果を返します |
| [JSON\_ARRAY\_INSERT(json\_doc, path, val\[, path, val\] ...)][json_array_insert]     | JSON ドキュメントの指定された場所に値を挿入し、結果を返します     |

## JSON 値の属性を返す関数 {#functions-that-return-json-value-attributes}

| 関数名                                              | 説明                                                           |
| ------------------------------------------------ | ------------------------------------------------------------ |
| [JSON\_DEPTH(json\_doc)][json_depth]             | JSON ドキュメントの最大深度を返します                                        |
| [JSON\_LENGTH(json\_doc\[, path\])][json_length] | JSON ドキュメントの長さを返します。パス引数が指定されている場合は、パス内の値の長さを返します            |
| [JSON\_TYPE(json\_val)][json_type]               | JSON 値の型を示す文字列を返します                                          |
| [JSON\_VALID(json\_doc)][json_valid]             | json_doc が有効な JSON かどうかを確認します。 json 型に変換する前に列をチェックするのに役立ちます。 |

## ユーティリティ機能 {#utility-functions}

| 関数名                                                 | 説明                                                                                                                                              |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| [JSON\_PRETTY(json\_doc)][json_pretty]              | JSON ドキュメントの整形                                                                                                                                  |
| [JSON\_STORAGE\_FREE(json\_doc)][json_storage_free] | その場で更新された後、JSON 値のバイナリ表現で解放されたstorage容量を返します。 TiDB は MySQL とは異なるstorageアーキテクチャを持っているため、この関数は有効な JSON 値に対して常に 0 を返し、MySQL 8.0 との互換性のために実装されています。 |
| [JSON\_STORAGE\_SIZE(json\_doc)][json_storage_size] | json 値を格納するために必要な概算サイズのバイトを返します。サイズは圧縮を使用する TiKV を考慮していないため、この関数の出力は MySQL と厳密には互換性がありません。                                                      |

## 集計関数 {#aggregate-functions}

| 関数名                                           | 説明                |
| --------------------------------------------- | ----------------- |
| [JSON\_ARRAYAGG(key)][json_arrayagg]          | キーの集約を提供します。      |
| [JSON\_OBJECTAGG(key, value)][json_objectagg] | 特定のキーの値の集計を提供します。 |

## こちらもご覧ください {#see-also}

-   [JSON 関数リファレンス](https://dev.mysql.com/doc/refman/5.7/en/json-function-reference.html)
-   [JSON データ型](/data-type-json.md)

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract

[json_short_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path

[json_short_extract_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path

[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote

[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type

[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set

[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert

[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace

[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove

[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge

[json_merge_patch]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-patch

[json_merge_preserve]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve

[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object

[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array

[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys

[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length

[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid

[json_quote]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote

[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains

[json_contains_path]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path

[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-arrayagg

[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth

[json_search]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-search

[json_append]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-append

[json_array_append]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-append

[json_array_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-insert

[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-arrayagg

[json_objectagg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-objectagg

[json_pretty]: https://dev.mysql.com/doc/refman/5.7/en/json-utility-functions.html#function_json-pretty

[json_storage_free]: https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free

[json_storage_size]: https://dev.mysql.com/doc/refman/5.7/en/json-utility-functions.html#function_json-storage-size
