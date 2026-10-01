---
title: Changefeed Log Filters
summary: TiCDC のテーブルフィルターとイベントフィルターの使用方法を学習します。
---

# 変更フィードログフィルター {#changefeed-log-filters}

TiCDCは、テーブルとイベントによるデータのフィルタリングをサポートしています。このドキュメントでは、2種類のフィルターの使い方を紹介します。

## テーブルフィルター {#table-filter}

テーブルフィルターは、次の構成を指定して、特定のデータベースとテーブルを保持または除外できる機能です。

```toml
[filter]
# Filter rules
rules = ['*.*', '!test.*']
```

一般的なフィルタールール:

- `rules = ['*.*']`
    - すべてのテーブルを複製します（システムテーブルは含みません）
- `rules = ['test1.*']`
    - `test1`データベース内のすべてのテーブルを複製する
- `rules = ['*.*', '!scm1.tbl2']`
    - `scm1.tbl2`テーブルを除くすべてのテーブルを複製します
- `rules = ['scm1.tbl2', 'scm1.tbl3']`
    - テーブル`scm1.tbl2`と`scm1.tbl3`のみを複製する
- `rules = ['scm1.tidb_*']`
    - `scm1`データベース内の、名前が`tidb_`で始まるすべてのテーブルを複製します。

詳細については[テーブルフィルタ構文](/table-filter.md#syntax)を参照してください。

## イベントフィルタールール {#event-filter-rules}

TiCDC v6.2.0以降では、イベントフィルターがサポートされています。イベントフィルタールールを設定することで、指定した条件を満たすDMLイベントとDDLイベントを除外できます。

以下はイベントフィルタルールの例です。

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

- `matcher` : このイベントフィルタルールが適用されるデータベースとテーブル。構文は[テーブルフィルター](/table-filter.md)と同じです。

    > **Note:**
    >
    > `matcher`はデータベース名と一致するため、設定時には特に注意が必要です。例えば、 `event-filters`設定が以下の場合：
    >
    > ```toml
    > [filter]
    > [[filter.event-filters]]
    > matcher = ["test.t1"]
    > ignore-sql = ["^drop"]
    > ```
    >
    > `ignore-sql = ["^drop"]`は、`DROP TABLE test.t1`を除外するだけでなく`DROP DATABASE test`も除外します。これは、`matcher`にデータベース名`test`が含まれているためです。
    >
    > データベース全体ではなく、指定されたテーブルのみをフィルター処理する場合は、 `ignore-sql`値を`["drop table"]`に変更します。

- `ignore-event` : 無視するイベントの種類。このパラメータは文字列の配列を受け入れます。複数のイベントの種類を設定できます。現在、以下のイベントの種類がサポートされています。

    | イベント                | タイプ | エイリアス       | 説明                                                                      |
    | ------------------- | --- | ----------- | ----------------------------------------------------------------------- |
    | all dml |  |  | すべてのDMLイベントに一致します |
    | all ddl |  |  | すべてのDDLイベントに一致します |
    | insert | DML |  | `insert` DML イベントに一致 |
    | update | DML |  | `update` DML イベントに一致 |
    | delete | DML |  | `delete` DML イベントに一致 |
    | create schema | DDL | create database | `create database`イベントに一致 |
    | drop schema | DDL | drop database | `drop database`イベントに一致 |
    | create table | DDL |  | `create table`イベントに一致 |
    | drop table | DDL |  | `drop table`イベントに一致 |
    | rename table | DDL |  | `rename table`イベントに一致 |
    | truncate table | DDL |  | `truncate table`イベントに一致 |
    | alter table | DDL |  | `alter table`、`create index`、`drop index` のすべての句を含む `alter table` イベントに一致します |
    | add table partition | DDL |  | `add table partition`イベントに一致 |
    | drop table partition | DDL |  | `drop table partition`イベントに一致 |
    | truncate table partition | DDL |  | `truncate table partition`イベントに一致 |
    | create view | DDL |  | `create view`イベントに一致 |
    | drop view | DDL |  | `drop view`イベントに一致 |
    | modify schema charset and collate | DDL |  | `modify schema charset and collate`イベントに一致 |
    | recover table | DDL |  | `recover table`イベントに一致 |
    | rebase auto id | DDL |  | `rebase auto id`イベントに一致 |
    | modify table comment | DDL |  | `modify table comment`イベントに一致 |
    | modify table charset and collate | DDL |  | `modify table charset and collate`イベントに一致 |
    | exchange table partition | DDL |  | `exchange table partition`イベントに一致 |
    | reorganize table partition | DDL |  | `reorganize table partition`イベントに一致 |
    | alter table partitioning | DDL |  | `alter table partitioning`イベントに一致 |
    | remove table partitioning | DDL |  | `remove table partitioning`イベントに一致 |
    | add column | DDL |  | `add column`イベントに一致 |
    | drop column | DDL |  | `drop column`イベントに一致 |
    | modify column | DDL |  | `modify column`イベントに一致 |
    | set default value | DDL |  | `set default value`イベントに一致 |
    | add primary key | DDL |  | `add primary key`イベントに一致 |
    | drop primary key | DDL |  | `drop primary key`イベントに一致 |
    | rename index | DDL |  | `rename index`イベントに一致 |
    | alter index visibility | DDL |  | `alter index visibility`イベントに一致 |
    | alter ttl info | DDL |  | `alter ttl info`イベントに一致 |
    | alter ttl remove | DDL |  | テーブルのすべてのTTL属性を削除するDDLイベントに一致します |
    | multi schema change | DDL |  | 同じDDL文内でテーブルの複数の属性を変更するDDLイベントに一致します。 |

    > **Note:**
    >
    > TiDBのDDL文は、 `ALTER TABLE t MODIFY COLUMN a INT, ADD COLUMN b INT, DROP COLUMN c;`のように単一テーブルの複数の属性を同時に変更することをサポートしています。この操作はMultiSchemaChangeとして定義されています。このタイプのDDLを除外したい場合は、 `ignore-event`で`"multi schema change"`を設定する必要があります。

- `ignore-sql` : フィルタリングするDDL文の正規表現。このパラメータは文字列の配列を受け付け、複数の正規表現を設定できます。この設定はDDLイベントにのみ適用されます。

- `ignore-delete-value-expr` : このパラメータは、指定された値を持つ`DELETE`種類の DML イベントをフィルタリングするために使用される、デフォルトの SQL モードに従う SQL 式を受け入れます。

- `ignore-insert-value-expr` : このパラメータは、指定された値を持つ`INSERT`種類の DML イベントをフィルタリングするために使用される、デフォルトの SQL モードに従う SQL 式を受け入れます。

- `ignore-update-old-value-expr` : このパラメータは、デフォルトの SQL モードに従う SQL 式を受け入れ、指定された古い値を持つ`UPDATE`種類の DML イベントを除外するために使用されます。

- `ignore-update-new-value-expr` : このパラメータは、デフォルトの SQL モードに従う SQL 式を受け入れ、指定された新しい値を持つ`UPDATE` DML イベントを除外するために使用されます。

> **Note:**
>
> - TiDB がクラスター化インデックスの列の値を更新すると、イベント`UPDATE`がイベント`DELETE`とイベント`INSERT`に分割されます。TiCDC はこれらのイベントをイベント`UPDATE`として識別しないため、正しくフィルタリングできません。
> - SQL式を設定する際は、 `matcher`に一致するすべてのテーブルに、SQL式で指定されたすべての列が含まれていることを確認してください。そうでない場合、レプリケーションタスクを作成できません。また、レプリケーション中にテーブルスキーマが変更され、必要な列がテーブルに含まれなくなった場合、レプリケーションタスクは失敗し、自動的に再開できません。このような場合は、手動で設定を変更してタスクを再開する必要があります。
