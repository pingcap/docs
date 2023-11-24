---
title: Changefeed Log Filters
summary: Learn how to use the table filter and event filter of TiCDC.
---

# 変更フィードログフィルター {#changefeed-log-filters}

TiCDC は、テーブルとイベントによるデータのフィルタリングをサポートしています。このドキュメントでは、2 種類のフィルターの使用方法を紹介します。

## テーブルフィルター {#table-filter}

テーブル フィルターは、次の構成を指定することで、特定のデータベースとテーブルを保持またはフィルターで除外できる機能です。

```toml
[filter]
# Filter rules
rules = ['*.*', '!test.*']
```

一般的なフィルター ルール:

-   `rules = ['*.*']`
    -   すべてのテーブルをレプリケートします (システム テーブルは含まれません)。
-   `rules = ['test1.*']`
    -   `test1`データベース内のすべてのテーブルをレプリケートする
-   `rules = ['*.*', '!scm1.tbl2']`
    -   `scm1.tbl2`のテーブルを除くすべてのテーブルをレプリケートする
-   `rules = ['scm1.tbl2', 'scm1.tbl3']`
    -   テーブル`scm1.tbl2`と`scm1.tbl3`のみを複製する
-   `rules = ['scm1.tidb_*']`
    -   `scm1`データベース内の名前が`tidb_`で始まるすべてのテーブルをレプリケートします。

詳細については、 [テーブルフィルターの構文](/table-filter.md#syntax)を参照してください。

## イベントフィルタールール {#event-filter-rules}

v6.2.0 以降、TiCDC はイベント フィルターをサポートします。イベント フィルター ルールを構成して、指定した条件を満たす DML イベントおよび DDL イベントをフィルターで除外できます。

以下はイベント フィルター ルールの例です。

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

-   `matcher` : このイベント フィルター ルールが適用されるデータベースとテーブル。構文は[テーブルフィルター](/table-filter.md)と同じです。
-   `ignore-event` : 無視するイベントの種類。このパラメータは文字列の配列を受け入れます。複数のイベント タイプを設定できます。現在、次のイベント タイプがサポートされています。

| イベント              | タイプ | エイリアス       | 説明                                                                            |
| ----------------- | --- | ----------- | ----------------------------------------------------------------------------- |
| すべてのDML           |     |             | すべての DML イベントに一致します                                                           |
| すべての ddl          |     |             | すべての DDL イベントに一致します                                                           |
| 入れる               | DML |             | `insert` DML イベントに一致します                                                       |
| アップデート            | DML |             | `update` DML イベントに一致します                                                       |
| 消去                | DML |             | `delete` DML イベントに一致します                                                       |
| スキーマを作成する         | DDL | データベースを作成する | `create database`件のイベントに一致                                                    |
| スキーマを削除する         | DDL | データベースを削除する | `drop database`件のイベントに一致                                                      |
| テーブルを作成する         | DDL |             | `create table`件のイベントに一致                                                       |
| ドロップテーブル          | DDL |             | `drop table`件のイベントに一致                                                         |
| テーブルの名前を変更する      | DDL |             | `rename table`件のイベントに一致                                                       |
| テーブルを切り捨てる        | DDL |             | `truncate table`件のイベントに一致                                                     |
| 他の机               | DDL |             | `alter table` 、 `create index` 、 `drop index`のすべての句を含む`alter table`イベントに一致します |
| テーブルパーティションを追加する  | DDL |             | `add table partition`件のイベントに一致                                                |
| テーブルパーティションを削除する  | DDL |             | `drop table partition`件のイベントに一致                                               |
| テーブルパーティションを切り詰める | DDL |             | `truncate table partition`件のイベントに一致                                           |
| ビューの作成            | DDL |             | `create view`件のイベントに一致                                                        |
| ドロップビュー           | DDL |             | `drop view`件のイベントに一致                                                          |

-   `ignore-sql` : DDL ステートメントは無視されます。このパラメーターは文字列の配列を受け入れ、複数の正規表現を構成できます。このルールは DDL イベントにのみ適用されます。
-   `ignore-delete-value-expr` : このパラメータは SQL 式を受け入れます。このルールは、指定された値を持つ DML イベントの削除にのみ適用されます。
-   `ignore-insert-value-expr` : このパラメータは SQL 式を受け入れます。このルールは、指定された値を持つ DML イベントの挿入にのみ適用されます。
-   `ignore-update-old-value-expr` : このパラメータは SQL 式を受け入れます。このルールは、古い値に指定された値が含まれる更新 DML イベントにのみ適用されます。
-   `ignore-update-new-value-expr` : このパラメータは SQL 式を受け入れます。このルールは、新しい値に指定された値が含まれる更新 DML イベントにのみ適用されます。

> **注記：**
>
> -   TiDB がクラスター化インデックスの列の値を更新すると、TiDB は`UPDATE`イベントを`DELETE`イベントと`INSERT`イベントに分割します。 TiCDC はそのようなイベントを`UPDATE`イベントとして識別しないため、そのようなイベントを正しく除外できません。
> -   SQL 式を構成するときは、 `matcher`に一致するすべてのテーブルに、SQL 式で指定されたすべての列が含まれていることを確認してください。そうしないと、レプリケーション タスクを作成できません。さらに、レプリケーション中にテーブル スキーマが変更され、テーブルに必要な列が含まれなくなると、レプリケーション タスクは失敗し、自動的に再開できなくなります。このような状況では、構成を手動で変更し、タスクを再開する必要があります。
