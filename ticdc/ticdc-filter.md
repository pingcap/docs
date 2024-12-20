---
title: Changefeed Log Filters
summary: TiCDC のテーブル フィルターとイベント フィルターの使用方法を学習します。
---

# チェンジフィードログフィルター {#changefeed-log-filters}

TiCDC は、テーブルとイベントによるデータのフィルタリングをサポートしています。このドキュメントでは、2 種類のフィルターの使用方法を紹介します。

## テーブルフィルター {#table-filter}

テーブル フィルターは、次の構成を指定して、特定のデータベースとテーブルを保持または除外できる機能です。

```toml
[filter]
# Filter rules
rules = ['*.*', '!test.*']
```

一般的なフィルタールール:

-   `rules = ['*.*']`
    -   すべてのテーブルを複製する（システムテーブルは含まない）
-   `rules = ['test1.*']`
    -   `test1`データベース内のすべてのテーブルを複製する
-   `rules = ['*.*', '!scm1.tbl2']`
    -   `scm1.tbl2`のテーブルを除くすべてのテーブルを複製する
-   `rules = ['scm1.tbl2', 'scm1.tbl3']`
    -   テーブル`scm1.tbl2`と`scm1.tbl3`のみを複製する
-   `rules = ['scm1.tidb_*']`
    -   `scm1`データベース内の、名前が`tidb_`で始まるすべてのテーブルを複製します。

詳細については[テーブルフィルタ構文](/table-filter.md#syntax)参照してください。

## イベントフィルタールール {#event-filter-rules}

v6.2.0 以降、TiCDC はイベント フィルターをサポートします。イベント フィルター ルールを構成して、指定した条件を満たす DML イベントと DDL イベントをフィルター処理できます。

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

構成パラメータの説明:

-   `matcher` : このイベント フィルター ルールが適用されるデータベースとテーブル。構文は[テーブルフィルター](/table-filter.md)と同じです。

-   `ignore-event` : 無視するイベント タイプ。このパラメータは文字列の配列を受け入れます。複数のイベント タイプを設定できます。現在、次のイベント タイプがサポートされています。

    | イベント               | タイプ    | エイリアス       | 説明                                                                    |
    | ------------------ | ------ | ----------- | --------------------------------------------------------------------- |
    | すべてのDML            |        |             | すべてのDMLイベントに一致します                                                     |
    | すべてのDDL            |        |             | すべてのDDLイベントに一致                                                        |
    | 入れる                | DMML の |             | `insert` DMLイベントに一致                                                   |
    | アップデート             | DMML の |             | `update` DMLイベントに一致                                                   |
    | 消去                 | DMML の |             | `delete` DMLイベントに一致                                                   |
    | スキーマを作成する          | DDL    | データベースを作成する | `create database`イベントに一致                                              |
    | スキーマを削除する          | DDL    | データベースを削除   | `drop database`イベントに一致                                                |
    | テーブルを作成する          | DDL    |             | `create table`イベントに一致                                                 |
    | ドロップテーブル           | DDL    |             | `drop table`イベントに一致                                                   |
    | テーブル名の変更           | DDL    |             | `rename table`イベントに一致                                                 |
    | テーブルを切り捨てる         | DDL    |             | `truncate table`イベントに一致                                               |
    | テーブルを変更する          | DDL    |             | `alter table`のすべての条項を含む`alter table` `create index` `drop index`一致します |
    | テーブルパーティションを追加     | DDL    |             | `add table partition`イベントに一致                                          |
    | テーブルパーティションを削除する   | DDL    |             | `drop table partition`イベントに一致                                         |
    | テーブルパーティションを切り捨てる  | DDL    |             | `truncate table partition`イベントに一致                                     |
    | ビューを作成             | DDL    |             | `create view`イベントに一致                                                  |
    | ドロップビュー            | DDL    |             | `drop view`イベントに一致                                                    |
    | スキーマの文字セットと照合を変更する | DDL    |             | `modify schema charset and collate`イベントに一致                            |
    | テーブルを回復する          | DDL    |             | `recover table`イベントに一致                                                |
    | 自動 ID をリベースする      | DDL    |             | `rebase auto id`イベントに一致                                               |
    | テーブルコメントの変更        | DDL    |             | `modify table comment`イベントに一致                                         |
    | テーブルの文字セットと照合を変更する | DDL    |             | `modify table charset and collate`イベントに一致                             |
    | 交換テーブルパーティション      | DDL    |             | `exchange table partition`イベントに一致                                     |
    | テーブルパーティションを再編成する  | DDL    |             | `reorganize table partition`イベントに一致                                   |
    | テーブルパーティションの変更     | DDL    |             | `alter table partitioning`イベントに一致                                     |
    | テーブルパーティションを削除する   | DDL    |             | `remove table partitioning`イベントに一致                                    |
    | 列を追加               | DDL    |             | `add column`イベントに一致                                                   |
    | ドロップ列              | DDL    |             | `drop column`イベントに一致                                                  |
    | 列を変更する             | DDL    |             | `modify column`イベントに一致                                                |
    | デフォルト値を設定する        | DDL    |             | `set default value`イベントに一致                                            |
    | 主キーを追加する           | DDL    |             | `add primary key`イベントに一致                                              |
    | 主キーを削除する           | DDL    |             | `drop primary key`イベントに一致                                             |
    | インデックス名の変更         | DDL    |             | `rename index`イベントに一致                                                 |
    | インデックスの可視性を変更する    | DDL    |             | `alter index visibility`イベントに一致                                       |
    | TTL情報を変更する         | DDL    |             | `alter ttl info`イベントに一致                                               |
    | TTLの変更削除           | DDL    |             | テーブルのすべてのTTL属性を削除するDDLイベントに一致します                                      |
    | 複数のスキーマの変更         | DDL    |             | 同じDDL文内でテーブルの複数の属性を変更するDDLイベントに一致します。                                 |

    > **注記：**
    >
    > TiDB の DDL ステートメントは、 `ALTER TABLE t MODIFY COLUMN a INT, ADD COLUMN b INT, DROP COLUMN c;`のように、単一テーブルの複数の属性を同時に変更することをサポートしています。この操作は MultiSchemaChange として定義されています。このタイプの DDL を除外する場合は、 `ignore-event`で`"multi schema change"`を構成する必要があります。

-   `ignore-sql` : フィルター処理する DDL ステートメントの正規表現。このパラメータは文字列の配列を受け入れ、複数の正規表現を構成できます。この構成は DDL イベントにのみ適用されます。

-   `ignore-delete-value-expr` : このパラメータは、デフォルトの SQL モードに従う SQL 式を受け入れ、指定された値を持つ`DELETE`種類の DML イベントをフィルタリングするために使用されます。

-   `ignore-insert-value-expr` : このパラメータは、デフォルトの SQL モードに従う SQL 式を受け入れ、指定された値を持つ`INSERT`種類の DML イベントをフィルタリングするために使用されます。

-   `ignore-update-old-value-expr` : このパラメータは、デフォルトの SQL モードに従う SQL 式を受け入れ、指定された古い値を持つ`UPDATE`種類の DML イベントを除外するために使用されます。

-   `ignore-update-new-value-expr` : このパラメータは、デフォルトの SQL モードに従う SQL 式を受け入れ、指定された新しい値を持つ`UPDATE` DML イベントを除外するために使用されます。

> **注記：**
>
> -   TiDB がクラスター化インデックスの列の値を更新すると、TiDB は`UPDATE`イベントを`DELETE`イベントと`INSERT`イベントに分割します。TiCDC はこのようなイベントを`UPDATE`イベントとして識別しないため、このようなイベントを正しくフィルター処理できません。
> -   SQL 式を構成するときは、 `matcher`に一致するすべてのテーブルに、SQL 式で指定されたすべての列が含まれていることを確認してください。そうでない場合、レプリケーション タスクを作成できません。また、レプリケーション中にテーブル スキーマが変更され、テーブルに必要な列が含まれなくなると、レプリケーション タスクは失敗し、自動的に再開できなくなります。このような状況では、手動で構成を変更してタスクを再開する必要があります。
