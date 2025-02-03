---
title: JSON Functions
summary: JSON関数について学びます。
---

# JSON関数 {#json-functions}

JSON関数を使用して[JSONデータ型](/data-type-json.md)のデータを操作できます。

## JSON値を作成する関数 {#functions-that-create-json-values}

| 関数名                                                                                           | 説明                                                 |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [JSON_ARRAY()](/functions-and-operators/json-functions/json-functions-create.md#json_array)   | 値のリスト（空の場合もある）を評価し、それらの値を含むJSON配列を返します。            |
| [JSON_OBJECT()](/functions-and-operators/json-functions/json-functions-create.md#json_object) | キーと値のペアの（空の場合もある）リストを評価し、それらのペアを含むJSONオブジェクトを返します。 |
| [JSON_QUOTE()](/functions-and-operators/json-functions/json-functions-create.md#json_quote)   | 引用符付きのJSON値として文字列を返します                             |

## JSON値を検索する関数 {#functions-that-search-json-values}

| 関数名                                                                                                         | 説明                                                                                        |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [JSON_CONTAINS()](/functions-and-operators/json-functions/json-functions-search.md#json_contains)           | 指定された候補JSONドキュメントがターゲットJSONドキュメント内に含まれているかどうかを1または0を返すことで示します。                            |
| [JSON_CONTAINS_PATH()](/functions-and-operators/json-functions/json-functions-search.md#json_contains_path) | JSONドキュメントに指定されたパスまたはパスにデータが含まれているかどうかを示す0または1を返します。                                      |
| [JSON_EXTRACT()](/functions-and-operators/json-functions/json-functions-search.md#json_extract)             | `path`の引数に一致するドキュメントの部分から選択されたJSONドキュメントからデータを返します。                                       |
| [-&gt;](/functions-and-operators/json-functions/json-functions-search.md#-)                                 | 評価パスの後のJSON列から値を返します。1の別名です`JSON_EXTRACT(doc, path_literal)`                              |
| [-&gt;&gt;](/functions-and-operators/json-functions/json-functions-search.md#--1)                           | 評価パスの後のJSON列からの値と、その結果の引用符を外した値を返します`JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`の別名です。 |
| [JSON_KEYS()](/functions-and-operators/json-functions/json-functions-search.md#json_keys)                   | JSONオブジェクトの最上位レベルの値からキーをJSON配列として返します。パス引数が指定されている場合は、選択したパスから最上位レベルのキーを返します。             |
| [JSON_検索()](/functions-and-operators/json-functions/json-functions-search.md#json_search)                   | JSONドキュメントで文字列の1つまたはすべてに一致するものを検索する                                                       |
| [メンバー()](/functions-and-operators/json-functions/json-functions-search.md#member-of)                        | 渡された値が JSON 配列の要素である場合は 1 を返します。それ以外の場合は 0 を返します。                                         |
| [JSON_OVERLAPS()](/functions-and-operators/json-functions/json-functions-search.md#json_overlaps)           | 2 つの JSON ドキュメントに重複部分があるかどうかを示します。重複している場合は 1 を返します。重複していない場合は 0 を返します。                   |

## JSON値を変更する関数 {#functions-that-modify-json-values}

| 関数名                                                                                                           | 説明                                     |
| ------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| [JSON_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_append)                 | `JSON_ARRAY_APPEND()`の別名               |
| [JSON_ARRAY_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_append)     | JSONドキュメント内の指定された配列の末尾に値を追加し、結果を返します。  |
| [JSON_ARRAY_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_insert)     | JSONドキュメントの指定された場所に値を挿入し、結果を返します。      |
| [JSON_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_insert)                 | JSONドキュメントにデータを挿入し、結果を返します             |
| [JSON_MERGE_PATCH()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_patch)       | 重複するキーの値を保持せずに、2つ以上のJSONドキュメントをマージします。 |
| [JSON_MERGE_PRESERVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_preserve) | すべての値を保持しながら2つ以上のJSONドキュメントをマージします     |
| [JSON_MERGE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge)                   | `JSON_MERGE_PRESERVE()`の非推奨のエイリアス      |
| [JSON_REMOVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_remove)                 | JSONドキュメントからデータを削除し、結果を返します            |
| [JSON_REPLACE()](/functions-and-operators/json-functions/json-functions-modify.md#json_replace)               | JSONドキュメント内の既存の値を置き換え、結果を返します          |
| [JSON_SET()](/functions-and-operators/json-functions/json-functions-modify.md#json_set)                       | JSONドキュメントにデータを挿入または更新し、結果を返します。       |
| [JSON_UNQUOTE()](/functions-and-operators/json-functions/json-functions-modify.md#json_unquote)               | JSON値を引用符で囲まず、結果を文字列として返します。           |

## JSON値属性を返す関数 {#functions-that-return-json-value-attributes}

| 関数名                                                                                           | 説明                                                |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [JSON_DEPTH()](/functions-and-operators/json-functions/json-functions-return.md#json_depth)   | JSONドキュメントの最大深度を返します                              |
| [JSON_LENGTH()](/functions-and-operators/json-functions/json-functions-return.md#json_length) | JSONドキュメントの長さを返します。パス引数が指定されている場合は、パス内の値の長さを返します。 |
| [JSON_TYPE()](/functions-and-operators/json-functions/json-functions-return.md#json_type)     | JSON値の型を示す文字列を返します                                |
| [JSON_VALID()](/functions-and-operators/json-functions/json-functions-return.md#json_valid)   | json_doc が有効な JSON であるかどうかを確認します。                 |

## ユーティリティ関数 {#utility-functions}

| 関数名                                                                                                        | 説明                                                                                            |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [JSON_PRETTY()](/functions-and-operators/json-functions/json-functions-utility.md#json_pretty)             | JSONドキュメントのきれいなフォーマット                                                                         |
| [JSON_STORAGE_FREE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_free) | JSON 値のバイナリ表現が更新された後に解放されたstorage容量を返します。                                                     |
| [JSON_STORAGE_SIZE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_size) | json 値を格納するために必要なバイトのおおよそのサイズを返します。サイズは圧縮を使用する TiKV を考慮していないため、この関数の出力は MySQL と厳密には互換性がありません。 |

## 集計関数 {#aggregate-functions}

| 関数名                                                                                                      | 説明                  |
| -------------------------------------------------------------------------------------------------------- | ------------------- |
| [JSON_ARRAYAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg)     | キーの集約を提供します。        |
| [JSON_OBJECTAG() は、](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg) | 指定されたキーの値の集計を提供します。 |

## JSONパス {#jsonpath}

多くの JSON関数は、JSON ドキュメントの一部を選択するために[JSONパス](https://www.rfc-editor.org/rfc/rfc9535.html)使用します。

| シンボル           | 説明        |
| -------------- | --------- |
| `$`            | ドキュメントルート |
| `.`            | メンバーの選択   |
| `[]`           | 配列の選択     |
| `*`            | ワイルドカード   |
| `**`           | パスワイルドカード |
| `[<n> to <n>]` | 配列範囲の選択   |

以降のコンテンツでは、次の JSON ドキュメントを例として、JSONPath の使用方法を説明します。

```json
{
    "database": {
        "name": "TiDB",
        "features": [
            "distributed",
            "scalable",
            "relational",
            "cloud native"
        ],
        "license": "Apache-2.0 license",
        "versions": [
            {
                "version": "v8.1.2",
                "type": "lts",
                "release_date": "2024-12-26" 
            },
            {
                "version": "v8.0.0",        
                "type": "dmr",
                "release_date": "2024-03-29"
            }
        ]
    },
    "migration_tool": {
        "name": "TiDB Data Migration",
        "features": [
            "MySQL compatible",            
            "Shard merging"
        ],
        "license": "Apache-2.0 license"
    }
}
```

| JSONパス                                | 説明                         | 例[`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract)   |
| ------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------- |
| `$`                                   | 文書のルート                     | 完全な文書を返します                                                                                           |
| `$.database`                          | `database`オブジェクト           | `"database"`から始まる完全な構造を返します。 `"migration_tool"`とそれ以下の構造は含まれません。                                      |
| `$.database.name`                     | データベースの名前。                 | `"TiDB"`                                                                                             |
| `$.database.features`                 | すべてのデータベース機能               | `["distributed", "scalable", "relational", "cloud native"]`                                          |
| `$.database.features[0]`              | 最初のデータベース機能。               | `"distributed"`                                                                                      |
| `$.database.features[2]`              | 3番目のデータベース機能。              | `"relational"`                                                                                       |
| `$.database.versions[0].type`         | 最初のデータベース バージョンのタイプ。       | `"lts"`                                                                                              |
| `$.database.versions[*].release_date` | すべてのバージョンのリリース日。           | `["2024-12-26","2024-03-29"]`                                                                        |
| `$.*.features`                        | 2つの機能配列                    | `[["distributed", "scalable", "relational", "cloud native"], ["MySQL compatible", "Shard merging"]]` |
| `$**.version`                         | パスワイルドカードを使用したすべてのバージョン    | `["v8.1.2","v8.0.0"]`                                                                                |
| `$.database.features[0 to 2]`         | 1 番目から 3 番目までのデータベース機能の範囲。 | `["scalable","relational"]`                                                                          |

詳細については[JSONPathのIETFドラフト](https://www.ietf.org/archive/id/draft-goessner-dispatch-jsonpath-00.html)参照してください。

## 参照 {#see-also}

-   [JSON データ型](/data-type-json.md)

## サポートされていない関数 {#unsupported-functions}

-   `JSON_SCHEMA_VALID()`
-   `JSON_SCHEMA_VALIDATION_REPORT()`
-   `JSON_TABLE()`
-   `JSON_VALUE()`

詳細については[＃14486](https://github.com/pingcap/tidb/issues/14486)参照してください。

## MySQL 互換性 {#mysql-compatibility}

-   TiDB は、MySQL 8.0 で利用可能な[JSON関数](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html)のほとんどをサポートしています。
