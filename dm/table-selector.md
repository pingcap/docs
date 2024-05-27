---
title: Table Selector of TiDB Data Migration
summary: データ移行のテーブル ルーティング、 binlogイベント フィルタリング、列マッピング ルールで使用されるテーブル セレクターについて学習します。
---

# TiDB データ移行のテーブルセレクター {#table-selector-of-tidb-data-migration}

テーブル セレクターは、スキーマ/テーブルに対して[ワイルドカード文字](https://en.wikipedia.org/wiki/Wildcard_character)に基づいた一致ルールを提供します。指定されたテーブルに一致させるには、 `schema-pattern` / `table-pattern`を設定します。

## ワイルドカード文字 {#wildcard-character}

テーブルセレクターは`schema-pattern` `table-pattern`次の 2 つのワイルドカード文字を使用します。

-   アスタリスク文字（ `*` 、「スター」とも呼ばれる）

    -   `*` 0 個以上の文字に一致します。たとえば、 `doc*` `doc`と`document`に一致しますが、 `dodo`は一致しません。
    -   `*`単語の末尾にのみ配置できます。たとえば、 `doc*`はサポートされていますが、 `do*c`はサポートされていません。

-   疑問符（ `?` ）

    `?` 、空文字を除く 1 つの文字に一致します。

## 試合ルール {#match-rules}

-   `schema-pattern`空にできません。
-   `table-pattern`空でも構いません。空として設定すると、 `schema-pattern`に従って`schema`のみが一致します。
-   `table-pattern`が空でない場合、 `schema` `schema-pattern`に従って一致し、 `table` `table-pattern`に従って一致します。 `schema`と`table`両方が正常に一致した場合にのみ、一致結果を取得できます。

## 使用例 {#usage-examples}

-   スキーマ名に`schema_`プレフィックスを持つすべてのスキーマとテーブルを一致させます。

    ```yaml
    schema-pattern: "schema_*"
    table-pattern: ""
    ```

-   スキーマ名に`schema_`プレフィックスが付いていて、テーブル名に`table_`プレフィックスが付いているすべてのテーブルを一致させます。

    ```yaml
    schema-pattern = "schema_*"
    table-pattern = "table_*"
    ```
