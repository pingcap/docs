---
title: Table Selector of TiDB Data Migration
summary: Learn about Table Selector used by the table routing, binlog event filtering, and column mapping rule of Data Migration.
---

# TiDB データ移行のテーブルセレクター {#table-selector-of-tidb-data-migration}

テーブル セレクターは、スキーマ/テーブルの[ワイルドカード文字](https://en.wikipedia.org/wiki/Wildcard_character)に基づく一致ルールを提供します。指定したテーブルに一致させるには、 `schema-pattern` / `table-pattern`を設定します。

## ワイルドカード文字 {#wildcard-character}

テーブル セレクターは、 `schema-pattern` / `table-pattern`で次の 2 つのワイルドカード文字を使用します。

-   アスタリスク文字 ( `*` 、「スター」とも呼ばれます)

    -   `*` 0 個以上の文字に一致します。たとえば、 `doc*` `doc`および`document`一致しますが、 `dodo`には一致しません。
    -   `*`単語の末尾にのみ置くことができます。たとえば、 `doc*`はサポートされますが、 `do*c`はサポートされません。

-   疑問符 ( `?` )

    `?`空の文字を除く 1 つの文字に正確に一致します。

## 試合ルール {#match-rules}

-   `schema-pattern`空にすることはできません。
-   `table-pattern`空でも構いません。空として構成すると、 `schema-pattern`に従って`schema`のみが一致します。
-   `table-pattern`が空でない場合、 `schema`は`schema-pattern`に従って照合され、 `table`は`table-pattern`に従って照合されます。 `schema`と`table`両方が正常にマッチングされた場合のみ、マッチング結果を取得できます。

## 使用例 {#usage-examples}

-   スキーマ名に接頭辞`schema_`を持つすべてのスキーマとテーブルを照合します。

    ```yaml
    schema-pattern: "schema_*"
    table-pattern: ""
    ```

-   スキーマ名に`schema_`プレフィックスがあり、テーブル名に`table_`プレフィックスを持つすべてのテーブルと一致します。

    ```yaml
    schema-pattern = "schema_*"
    table-pattern = "table_*"
    ```
