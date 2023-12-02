---
title: Data Check for Tables with Different Schema or Table Names
summary: Learn the data check for different database names or table names.
---

# 異なるスキーマまたはテーブル名を持つテーブルのデータ チェック {#data-check-for-tables-with-different-schema-or-table-names}

[TiDB データ移行](/dm/dm-overview.md)などのレプリケーション ツールを使用する場合、 `route-rules`を設定すると、ダウンストリームの指定されたテーブルにデータをレプリケートできます。 sync-diff-inspector を使用すると、 `rules`を設定することで、異なるスキーマ名またはテーブル名を持つテーブルを検証できます。

以下に簡単な構成例を示します。完全な構成については、 [Sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。

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

この構成を使用して、ダウンストリームで`test_2.t_2`をチェックし、 `mysql1`インスタンスで`test_1.t_1`チェックできます。

スキーマ名やテーブル名が異なる多数のテーブルをチェックするには、 `rules`を使用してマッピング関係を設定することで構成を簡素化できます。スキーマまたはテーブルのいずれか、または両方のマッピング関係を構成できます。たとえば、アップストリーム`test_1`データベース内のすべてのテーブルはダウンストリーム`test_2`データベースにレプリケートされ、次の構成で確認できます。

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

## 注記 {#note}

`test_2`の場合。 `t_2`が上流データベースに存在する場合、下流データベースもこのテーブルを比較します。
