---
title: Changefeed Log Filters
summary: Learn how to use the table filter and event filter of TiCDC.
---

# Changefeed ログ フィルタ {#changefeed-log-filters}

TiCDC は、テーブルとイベントによるデータのフィルタリングをサポートしています。このドキュメントでは、2 種類のフィルターの使用方法を紹介します。

## テーブル フィルター {#table-filter}

テーブル フィルターは、次の構成を指定することで、特定のデータベースとテーブルを保持または除外できる機能です。

```toml
[filter]
# Filter rules
rules = ['*.*', '!test.*']
```

一般的なフィルター規則:

-   `rules = ['*.*']`
    -   すべてのテーブルをレプリケート (システム テーブルを除く)
-   `rules = ['test1.*']`
    -   `test1`データベース内のすべてのテーブルをレプリケートする
-   `rules = ['*.*', '!scm1.tbl2']`
    -   `scm1.tbl2`のテーブルを除くすべてのテーブルをレプリケートする
-   `rules = ['scm1.tbl2', 'scm1.tbl3']`
    -   テーブル`scm1.tbl2`と`scm1.tbl3`のみをレプリケートする
-   `rules = ['scm1.tidb_*']`
    -   名前が`tidb_`で始まる`scm1`データベース内のすべてのテーブルをレプリケートします。

詳細については、 [テーブル フィルタの構文](/table-filter.md#syntax)を参照してください。

## イベント フィルター規則 {#event-filter-rules}

v6.2.0 以降、TiCDC はイベント フィルターをサポートします。指定した条件を満たす DML および DDL イベントを除外するイベント フィルター ルールを構成できます。

以下は、イベント フィルター ルールの例です。

```toml
[filter]
# The event filter rules must be under the `[filter]` configuration. You can configure multiple event filters at the same time.

[[filter.event-filters]]
matcher = ["test.worker"] # matcher is an allow list, which means this rule only applies to the worker table in the test database.
ignore-event = ["insert"] # Ignore insert events.
ignore-sql = ["^drop", "add column"] # Ignore DDLs that start with "drop" or contain "add column".
ignore-delete-value-expr = "name = 'john'" # Ignore delete DMLs that contain the condition "name = 'john'".
ignore-insert-value-expr = "id >= 100" # Ignore insert DMLs that contain the condition "id >= 100".
ignore-update-old-value-expr = "age < 18 or name = 'lili'" # Ignore update DMLs whose old value contains "age < 18" or "name = 'lili'".
ignore-update-new-value-expr = "gender = 'male' and age > 18" # Ignore update DMLs whose new value contains "gender = 'male'" and "age > 18".
```

設定パラメータの説明:

-   `matcher` : このイベント フィルター規則が適用されるデータベースとテーブル。構文は[テーブル フィルター](/table-filter.md)と同じです。
-   `ignore-event` : 無視するイベント タイプ。このパラメーターは、文字列の配列を受け入れます。複数のイベント タイプを設定できます。現在、次のイベント タイプがサポートされています。

| イベント              | タイプ | エイリアス       | 説明                                                                              |
| ----------------- | --- | ----------- | ------------------------------------------------------------------------------- |
| すべてのdml           |     |             | すべての DML イベントに一致                                                                |
| すべての ddl          |     |             | すべての DDL イベントに一致                                                                |
| 入れる               | DML |             | `insert` DML イベントに一致                                                            |
| アップデート            | DML |             | `update` DML イベントに一致                                                            |
| 消去                | DML |             | `delete` DML イベントに一致                                                            |
| スキーマを作成する         | DDL | データベースを作成する | `create database`イベントに一致                                                        |
| スキーマを削除           | DDL | データベースをドロップ | `drop database`イベントに一致                                                          |
| テーブルを作成           | DDL |             | `create table`イベントに一致                                                           |
| ドロップテーブル          | DDL |             | `drop table`イベントに一致                                                             |
| テーブルの名前を変更        | DDL |             | `rename table`イベントに一致                                                           |
| テーブルを切り捨てる        | DDL |             | `truncate table`イベントに一致                                                         |
| 他の机               | DDL |             | `alter table` 、 `create index` 、および`drop index`のすべての節を含む`alter table`イベントに一致します |
| テーブルパーティションを追加    | DDL |             | `add table partition`イベントに一致                                                    |
| テーブル パーティションの削除   | DDL |             | `drop table partition`イベントに一致                                                   |
| テーブル パーティションの切り捨て | DDL |             | `truncate table partition`イベントに一致                                               |
| ビューを作成            | DDL |             | `create view`イベントに一致                                                            |
| ビューをドロップ          | DDL |             | `drop view`イベントに一致                                                              |

-   `ignore-sql` : 無視される DDL ステートメント。このパラメーターは、複数の正規表現を構成できる文字列の配列を受け入れます。このルールは、DDL イベントにのみ適用されます。
-   `ignore-delete-value-expr` : このパラメーターは SQL 式を受け入れます。このルールは、指定された値を持つ DML イベントの削除にのみ適用されます。
-   `ignore-insert-value-expr` : このパラメーターは SQL 式を受け入れます。このルールは、指定された値を持つ挿入 DML イベントにのみ適用されます。
-   `ignore-update-old-value-expr` : このパラメーターは SQL 式を受け入れます。このルールは、古い値に指定された値が含まれる更新 DML イベントにのみ適用されます。
-   `ignore-update-new-value-expr` : このパラメーターは SQL 式を受け入れます。このルールは、新しい値に指定された値が含まれる更新 DML イベントにのみ適用されます。

> **ノート：**
>
> -   TiDB がクラスター化インデックスの列の値を更新すると、TiDB は`UPDATE`イベントを`DELETE`イベントと`INSERT`イベントに分割します。 TiCDC はそのようなイベントを`UPDATE`イベントとして識別しないため、そのようなイベントを正しく除外できません。
> -   SQL 式を構成するときは、 `matcher`に一致するすべてのテーブルに、SQL 式で指定されたすべての列が含まれていることを確認してください。そうしないと、レプリケーション タスクを作成できません。さらに、レプリケーション中にテーブル スキーマが変更され、テーブルに必要な列が含まれなくなった場合、レプリケーション タスクは失敗し、自動的に再開できません。このような状況では、構成を手動で変更し、タスクを再開する必要があります。
