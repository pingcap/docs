---
title: Changefeed Log Filters
summary: TiCDC のテーブル フィルターとイベント フィルターの使用方法を学習します。
---

# 変更フィードログフィルター {#changefeed-log-filters}

TiCDCは、テーブルとイベントによるデータのフィルタリングをサポートしています。このドキュメントでは、2種類のフィルターの使い方を紹介します。

## テーブルフィルター {#table-filter}

テーブル フィルターは、次の構成を指定して、特定のデータベースとテーブルを保持または除外できる機能です。

```toml
[filter]
# Filter rules
rules = ['*.*', '!test.*']
```

一般的なフィルタールール:

-   `rules = ['*.*']`
    -   すべてのテーブルを複製します（システムテーブルは含みません）
-   `rules = ['test1.*']`
    -   Replicate all tables in the `test1` database
-   `rules = ['*.*', '!scm1.tbl2']`
    -   `scm1.tbl2`テーブルを除くすべてのテーブルを複製します
-   `rules = ['scm1.tbl2', 'scm1.tbl3']`
    -   テーブル`scm1.tbl2`と`scm1.tbl3`のみを複製する
-   `rules = ['scm1.tidb_*']`
    -   `scm1`データベース内の、名前が`tidb_`で始まるすべてのテーブルを複製します。

詳細については[テーブルフィルタ構文](/table-filter.md#syntax)参照してください。

## イベントフィルタールール {#event-filter-rules}

TiCDC v6.2.0以降、イベントフィルターがサポートされます。イベントフィルタールールを設定することで、指定した条件を満たすDMLイベントとDDLイベントを除外できます。

以下はイベント フィルタ ルールの例です。

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

構成パラメータの説明:

-   `matcher` : このイベントフィルタルールが適用されるデータベースとテーブル。構文は[table filter](/table-filter.md)と同じです。

-   `ignore-event` : 無視するイベントの種類。このパラメータは文字列の配列を受け入れます。複数のイベントの種類を設定できます。現在、以下のイベントの種類がサポートされています。

    | イベント                             | タイプ | エイリアス       | 説明                                                                                                   |
    | -------------------------------- | --- | ----------- | ---------------------------------------------------------------------------------------------------- |
    | すべてのDML                          |     |             | Matches all DML events                                                                               |
    | すべてのDDL                          |     |             | すべてのDDLイベントに一致します                                                                                    |
    | 入れる                              | DML |             | Matches `insert` DML event                                                                           |
    | アップデート                           | DML |             | `update` DML イベントに一致                                                                                 |
    | 消去                               | DML |             | `delete` DML イベントに一致                                                                                 |
    | スキーマを作成する                        | DDL | データベースを作成する | `create database`イベントに一致                                                                             |
    | ドロップスキーマ                         | DDL | データベースを削除   | `drop database`イベントに一致                                                                               |
    | テーブルを作成する                        | DDL |             | `create table`イベントに一致                                                                                |
    | ドロップテーブル                         | DDL |             | `drop table`イベントに一致                                                                                  |
    | テーブルの名前を変更する                     | DDL |             | `rename table`イベントに一致                                                                                |
    | truncate table                   | DDL |             | `truncate table`イベントに一致                                                                              |
    | テーブルを変更する                        | DDL |             | Matches `alter table` event, including all clauses of `alter table`, `create index` and `drop index` |
    | テーブルパーティションを追加する                 | DDL |             | `add table partition`イベントに一致                                                                         |
    | テーブルパーティションの削除                   | DDL |             | Matches `drop table partition` event                                                                 |
    | テーブルパーティションを切り捨てる                | DDL |             | Matches `truncate table partition` event                                                             |
    | ビューを作成                           | DDL |             | `create view`イベントに一致                                                                                 |
    | ドロップビュー                          | DDL |             | Matches `drop view` event                                                                            |
    | スキーマの文字セットを変更して照合する              | DDL |             | `modify schema charset and collate`イベントに一致                                                           |
    | テーブルを回復する                        | DDL |             | `recover table`イベントに一致                                                                               |
    | 自動IDをリベースする                      | DDL |             | `rebase auto id`イベントに一致                                                                              |
    | modify table comment             | DDL |             | `modify table comment`イベントに一致                                                                        |
    | modify table charset and collate | DDL |             | `modify table charset and collate`イベントに一致                                                            |
    | 交換テーブルパーティション                    | DDL |             | `exchange table partition`イベントに一致                                                                    |
    | テーブルパーティションの再編成                  | DDL |             | `reorganize table partition`イベントに一致                                                                  |
    | テーブルパーティションの変更                   | DDL |             | `alter table partitioning`イベントに一致                                                                    |
    | テーブルパーティションを削除する                 | DDL |             | `remove table partitioning`イベントに一致                                                                   |
    | 列を追加                             | DDL |             | Matches `add column` event                                                                           |
    | ドロップ列                            | DDL |             | `drop column`イベントに一致                                                                                 |
    | 列を変更する                           | DDL |             | `modify column`イベントに一致                                                                               |
    | デフォルト値を設定する                      | DDL |             | `set default value`イベントに一致                                                                           |
    | 主キーを追加する                         | DDL |             | Matches `add primary key` event                                                                      |
    | 主キーを削除する                         | DDL |             | `drop primary key`イベントに一致                                                                            |
    | インデックスの名前を変更する                   | DDL |             | `rename index`イベントに一致                                                                                |
    | alter index visibility           | DDL |             | `alter index visibility`イベントに一致                                                                      |
    | TTL情報を変更する                       | DDL |             | `alter ttl info`イベントに一致                                                                              |
    | TTLの変更と削除                        | DDL |             | テーブルのすべてのTTL属性を削除するDDLイベントに一致します                                                                     |
    | 複数のスキーマの変更                       | DDL |             | 同じDDL文内でテーブルの複数の属性を変更するDDLイベントに一致します。                                                                |

    > **注記：**
    >
    > TiDB's DDL statements support changing multiple attributes of a single table at the same time, such as `ALTER TABLE t MODIFY COLUMN a INT, ADD COLUMN b INT, DROP COLUMN c;`. This operation is defined as MultiSchemaChange. If you want to filter out this type of DDL, you need to configure `"multi schema change"` in `ignore-event`.

-   `ignore-sql` : フィルタリングするDDL文の正規表現。このパラメータは文字列の配列を受け付け、複数の正規表現を設定できます。この設定はDDLイベントにのみ適用されます。

-   `ignore-delete-value-expr` : このパラメータは、指定された値を持つ`DELETE`種類の DML イベントをフィルタリングするために使用される、デフォルトの SQL モードに従う SQL 式を受け入れます。

-   `ignore-insert-value-expr` : このパラメータは、指定された値を持つ`INSERT`種類の DML イベントをフィルタリングするために使用される、デフォルトの SQL モードに従う SQL 式を受け入れます。

-   `ignore-update-old-value-expr` : このパラメータは、指定された古い値を持つ`UPDATE`種類の DML イベントを除外するために使用される、デフォルトの SQL モードに従う SQL 式を受け入れます。

-   `ignore-update-new-value-expr` : このパラメータは、デフォルトの SQL モードに従う SQL 式を受け入れ、指定された新しい値を持つ`UPDATE` DML イベントを除外するために使用されます。

> **注記：**
>
> -   TiDB がクラスター化インデックスの列の値を更新すると、イベント`UPDATE`がイベント`DELETE`とイベント`INSERT`に分割されます。TiCDC はこれらのイベントをイベント`UPDATE`として識別しないため、正しくフィルタリングできません。
> -   When you configure a SQL expression, make sure all tables that matches `matcher` contain all the columns specified in the SQL expression. Otherwise, the replication task cannot be created. In addition, if the table schema changes during the replication, which results in a table no longer containing a required column, the replication task fails and cannot be resumed automatically. In such a situation, you must manually modify the configuration and resume the task.
