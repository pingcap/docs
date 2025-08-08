---
title: Table Selector of TiDB Data Migration
summary: データ移行のテーブル ルーティング、 binlogイベント フィルタリング、列マッピング ルールで使用されるテーブル セレクターについて学習します。
---

# TiDBデータ移行のテーブルセレクター {#table-selector-of-tidb-data-migration}

テーブルセレクターは、スキーマ/テーブルに対して[ワイルドカード文字](https://en.wikipedia.org/wiki/Wildcard_character)に基づく一致ルールを提供します。特定のテーブルに一致させるには、 `schema-pattern` / `table-pattern`を設定してください。

## ワイルドカード文字 {#wildcard-character}

テーブルセレクターは`schema-pattern`で次の 2 つのワイルドカード文字`table-pattern`使用します。

-   アスタリスク文字（ `*` 、「スター」とも呼ばれる）

    -   `*` 0文字以上の文字に一致します。例えば、 `doc*` `doc`と`document`に一致しますが、 `dodo`は一致しません。
    -   `*`単語の末尾にのみ配置できます。例えば、 `doc*`サポートされていますが、 `do*c`サポートされていません。

-   疑問符（ `?` ）

    `?` 、空文字を除く 1 つの文字と一致します。

## 試合ルール {#match-rules}

-   `schema-pattern`を空にすることはできません。
-   `table-pattern`空でも構いません。空に設定すると、 `schema-pattern`に従って`schema`のみが一致します。
-   `table-pattern`が空でない場合、 `schema` `schema-pattern`に従ってマッチングされ、 `table` `table-pattern`に従ってマッチングされます。 `schema`と`table`両方が正常にマッチングされた場合にのみ、マッチング結果を取得できます。

## 使用例 {#usage-examples}

-   スキーマ名に`schema_`プレフィックスを持つすべてのスキーマとテーブルを一致させます。

    ```yaml
    schema-pattern: "schema_*"
    table-pattern: ""
    ```

-   スキーマ名に`schema_`プレフィックスが付き、テーブル名に`table_`プレフィックスが付いたすべてのテーブルを一致させます。

    ```yaml
    schema-pattern = "schema_*"
    table-pattern = "table_*"
    ```
