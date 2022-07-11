---
title: JSON Functions
summary: Learn about JSON functions.
---

# JSON関数 {#json-functions}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

TiDBは、 MySQL 5.7のGAリリースに付属しているほとんどのJSON関数をサポートしています。

## JSON値を作成する関数 {#functions-that-create-json-values}

| 関数名                                                     | 説明                                               |
| ------------------------------------------------------- | ------------------------------------------------ |
| [JSON\_ARRAY(\[val\[, val\] ...\])][json_array]         | （おそらく空の）値のリストを評価し、それらの値を含むJSON配列を返します            |
| [JSON\_OBJECT(key, val\[, key, val\] ...)][json_object] | キーと値のペアの（おそらく空の）リストを評価し、それらのペアを含むJSONオブジェクトを返します |
| [JSON\_QUOTE(string)][json_quote]                       | 文字列を引用符付きのJSON値として返します                           |

## JSON値を検索する関数 {#functions-that-search-json-values}

| 関数名                                                                                     | 説明                                                                                      |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [JSON\_CONTAINS(target, candidate\[, path\])][json_contains]                            | 特定の候補JSONドキュメントがターゲットJSONドキュメント内に含まれているかどうかを1または0で返すことによって示します                          |
| [JSON\_CONTAINS\_PATH(json\_doc, one\_or\_all, path\[, path\] ...)][json_contains_path] | 0または1を返し、JSONドキュメントに特定のパスにデータが含まれているかどうかを示します                                           |
| [JSON\_EXTRACT(json\_doc, path\[, path\] ...)][json_extract]                            | `path`の引数に一致するドキュメントの部分から選択されたJSONドキュメントからデータを返します                                      |
| [->][json_short_extract]                                                                | 評価パスの後のJSON列から値を返します。 `JSON_EXTRACT(doc, path_literal)`のエイリアス                           |
| [->>][json_short_extract_unquote]                                                       | パスを評価し、結果の引用符を外した後、JSON列から値を返します。 `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`のエイリアス |
| [JSON\_KEYS(json\_doc\[, path\])][json_keys]                                            | JSONオブジェクトのトップレベル値からのキーをJSON配列として返します。または、パス引数が指定されている場合は、選択したパスからのトップレベルキーを返します。       |
| [JSON\_SEARCH(json\_doc, one\_or\_all, search\_string)][json_search]                    | 文字列の1つまたはすべての一致をJSONドキュメントで検索します                                                        |

## JSON値を変更する関数 {#functions-that-modify-json-values}

| 関数名                                                                                   | 説明                                   |
| ------------------------------------------------------------------------------------- | ------------------------------------ |
| [JSON\_APPEND(json\_doc, path, value)][json_append]                                   | `JSON_ARRAY_APPEND`のエイリアス            |
| [JSON\_ARRAY\_APPEND(json\_doc, path, value)][json_array_append]                      | 指定されたパスのJSON配列の最後に値を追加します            |
| [JSON\_ARRAY\_INSERT(json\_doc, path, val\[, path, val\] ...)][json_array_insert]     | jsonドキュメントに配列を挿入し、変更されたドキュメントを返します   |
| [JSON\_INSERT(json\_doc, path, val\[, path, val\] ...)][json_insert]                  | JSONドキュメントにデータを挿入し、結果を返します           |
| [JSON\_MERGE(json\_doc, json\_doc\[, json\_doc\] ...)][json_merge]                    | `JSON_MERGE_PRESERVE`の非推奨のエイリアス      |
| [JSON\_MERGE\_PATCH(json\_doc, json\_doc\[, json\_doc\] ...)][json_merge_patch]       | JSONドキュメントをマージする                     |
| [JSON\_MERGE\_PRESERVE(json\_doc, json\_doc\[, json\_doc\] ...)][json_merge_preserve] | 2つ以上のJSONドキュメントをマージし、マージされた結果を返します   |
| [JSON\_REMOVE(json\_doc, path\[, path\] ...)][json_remove]                            | JSONドキュメントからデータを削除し、結果を返します          |
| [JSON\_REPLACE(json\_doc, path, val\[, path, val\] ...)][json_replace]                | JSONドキュメントの既存の値を置き換えて、結果を返します        |
| [JSON\_SET(json\_doc, path, val\[, path, val\] ...)][json_set]                        | JSONドキュメントにデータを挿入または更新し、結果を返します      |
| [JSON\_UNQUOTE(json\_val)][json_unquote]                                              | JSON値の引用符を解除し、結果を文字列として返します          |
| [JSON\_ARRAY\_APPEND(json\_doc, path, val\[, path, val\] ...)][json_array_append]     | JSONドキュメント内の指定された配列の最後に値を追加し、結果を返します |
| [JSON\_ARRAY\_INSERT(json\_doc, path, val\[, path, val\] ...)][json_array_insert]     | JSONドキュメントの指定された場所に値を挿入し、結果を返します     |

## JSON値属性を返す関数 {#functions-that-return-json-value-attributes}

| 関数名                                              | 説明                                                         |
| ------------------------------------------------ | ---------------------------------------------------------- |
| [JSON\_DEPTH(json\_doc)][json_depth]             | JSONドキュメントの最大深度を返します                                       |
| [JSON\_LENGTH(json\_doc\[, path\])][json_length] | JSONドキュメントの長さを返します。パス引数が指定されている場合は、パス内の値の長さを返します。          |
| [JSON\_TYPE(json\_val)][json_type]               | JSON値のタイプを示す文字列を返します                                       |
| [JSON\_VALID(json\_doc)][json_valid]             | json_docが有効なJSONであるかどうかを確認します。 json型に変換する前に列をチェックするのに便利です。 |

## ユーティリティ関数 {#utility-functions}

| 関数名                                                 | 説明                                                                                      |
| --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [JSON\_PRETTY(json\_doc)][json_pretty]              | JSONドキュメントのきれいなフォーマット                                                                   |
| [JSON\_STORAGE\_SIZE(json\_doc)][json_storage_size] | json値を格納するために必要なバイトのおおよそのサイズを返します。サイズは圧縮を使用するTiKVを考慮していないため、この関数の出力はMySQLと厳密に互換性がありません。 |

## 集計関数 {#aggregate-functions}

| 関数名                                           | 説明                |
| --------------------------------------------- | ----------------- |
| [JSON\_ARRAYAGG(key)][json_arrayagg]          | キーの集約を提供します。      |
| [JSON\_OBJECTAGG(key, value)][json_objectagg] | 特定のキーの値の集計を提供します。 |

## も参照してください {#see-also}

-   [JSON関数リファレンス](https://dev.mysql.com/doc/refman/5.7/en/json-function-reference.html)
-   [JSONデータ型](/data-type-json.md)

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

[json_storage_size]: https://dev.mysql.com/doc/refman/5.7/en/json-utility-functions.html#function_json-storage-size
