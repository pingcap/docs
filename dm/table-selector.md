---
title: Table Selector
summary: Learn about Table Selector used by the table routing, binlog event filtering, and column mapping rule of Data Migration.
---

# テーブルセレクター {#table-selector}

テーブルセレクターは、スキーマ/テーブルの[ワイルドカード文字](https://en.wikipedia.org/wiki/Wildcard_character)に基づく一致ルールを提供します。指定されたテーブルに一致させるには、 `schema-pattern` / `table-pattern`を構成します。

## ワイルドカード文字 {#wildcard-character}

テーブルセレクターは、 `schema-pattern` / `table-pattern`で次の2つのワイルドカード文字を使用します。

-   アスタリスク文字（ `*` 、「スター」とも呼ばれます）

    -   `*`は0個以上の文字に一致します。たとえば、 `doc*`は`doc`と`document`に一致しますが、 `dodo`には一致しません。
    -   `*`は単語の最後にのみ配置できます。たとえば、 `doc*`はサポートされていますが、 `do*c`はサポートされていません。

-   疑問符（ `?` ）

    `?`は、空の文字を除いて1文字に正確に一致します。

## 一致ルール {#match-rules}

-   `schema-pattern`を空にすることはできません。
-   `table-pattern`は空にすることができます。空として設定すると、 `schema-pattern`に従って`schema`だけが一致します。
-   `table-pattern`が空でない場合、 `schema`は`schema-pattern`に従って一致し、 `table`は`table-pattern`に従って一致します。 `schema`と`table`の両方が正常に一致した場合にのみ、一致結果を取得できます。

## 使用例 {#usage-examples}

-   スキーマ名に`schema_`のプレフィックスが含まれるすべてのスキーマとテーブルを照合します。

    ```yaml
    schema-pattern: "schema_*"
    table-pattern: ""
    ```

-   スキーマ名に`schema_`つのプレフィックスがあり、テーブル名に`table_`のプレフィックスがあるすべてのテーブルを照合します。

    ```yaml
    schema-pattern = "schema_*"
    table-pattern = "table_*"
    ```
