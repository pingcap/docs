---
title: Data Check for Tables with Different Schema or Table Names
summary: Learn the data check for different database names or table names.
---

# スキーマ名またはテーブル名が異なるテーブルのデータチェック {#data-check-for-tables-with-different-schema-or-table-names}

[TiDBデータ移行](/dm/dm-overview.md)などのレプリケーションツールを使用する場合は、 `route-rules`を設定して、ダウンストリームの指定されたテーブルにデータをレプリケートできます。 sync-diff-inspectorを使用すると、 `rules`を設定することにより、異なるスキーマ名またはテーブル名を持つテーブルを検証できます。

以下は簡単な設定例です。完全な構成については、 [Sync-diff-inspectorユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    route-rules = ["rule1"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "t_1"          # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test_2"       # The name of the schema in the target database
target-table = "t_2"           # The name of the target table
```

この構成を使用して、ダウンストリームで`test_2.t_2`インスタンスで`test_1.t_1`をチェックでき`mysql1` 。

スキーマ名またはテーブル名が異なる多数のテーブルをチェックするには、 `rules`を使用してマッピング関係を設定することにより、構成を簡略化できます。スキーマまたはテーブル、あるいはその両方のマッピング関係を構成できます。たとえば、アップストリーム`test_1`データベースのすべてのテーブルがダウンストリーム`test_2`データベースにレプリケートされます。これは、次の構成で確認できます。

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    route-rules = ["rule1"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "*"            # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test_2"       # The name of the schema in the target database
target-table = "t_2"           # The name of the target table
```

## ノート {#note}

`test_2`の場合。 `t_2`はアップストリームデータベースに存在し、ダウンストリームデータベースもこのテーブルを比較します。
