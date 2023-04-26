---
title: Table Selector of TiDB Data Migration
summary: Learn about Table Selector used by the table routing, binlog event filtering, and column mapping rule of Data Migration.
---

# TiDB データ移行のテーブル セレクター {#table-selector-of-tidb-data-migration}

テーブル セレクターは、スキーマ/テーブルの[ワイルドカード文字](https://en.wikipedia.org/wiki/Wildcard_character)に基づく一致ルールを提供します。指定したテーブルに一致させるには、 `schema-pattern` / `table-pattern`を構成します。

## ワイルドカード文字 {#wildcard-character}

テーブル セレクターは、次の 2 つのワイルドカード文字を`schema-pattern` / `table-pattern`で使用します。

-   アスタリスク文字 ( `*` 、「スター」とも呼ばれます)

    -   `*` 0 個以上の文字に一致します。たとえば、 `doc*` `doc`と`document`一致しますが、 `dodo`には一致しません。
    -   `*`単語の末尾にのみ配置できます。たとえば、 `doc*`はサポートされていますが、 `do*c`はサポートされていません。

-   クエスチョンマーク ( `?` )

    `?`空の文字を除く 1 文字に一致します。

## マッチルール {#match-rules}

-   `schema-pattern`空にすることはできません。
-   `table-pattern`空にすることができます。空として構成すると、 `schema-pattern`に従って`schema`のみが一致します。
-   `table-pattern`が空でない場合、 `schema`は`schema-pattern`に従って一致し、 `table`は`table-pattern`に従って一致します。 `schema`と`table`両方が一致した場合にのみ、一致結果を取得できます。

## 使用例 {#usage-examples}

-   スキーマ名に`schema_`プレフィックスを持つすべてのスキーマとテーブルを一致させる:

    ```yaml
    schema-pattern: "schema_*"
    table-pattern: ""
    ```

-   スキーマ名に`schema_`プレフィックスがあり、テーブル名に`table_`プレフィックスがあるすべてのテーブルを照合します。

    ```yaml
    schema-pattern = "schema_*"
    table-pattern = "table_*"
    ```
